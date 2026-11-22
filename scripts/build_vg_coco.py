#!/usr/bin/env python3
"""Build VG-COCO with the existing data modules, one restartable stage at a time.

Run from the repository root. Rebuilding versioned JSON requires --overwrite;
image restoration never changes the split. Raw downloads are checksum-pinned.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

import yaml

from src.core.exceptions import AppError, DataError
from src.data.coco_captions import load_karpathy_coco
from src.data.config import DataConfig
from src.data.download import ImageJob, download_images
from src.data.export import build_queries, split_of_image
from src.data.graph_build import build_graphs, graph_statistics
from src.data.json_io import read_json, write_json
from src.data.scene_graphs import normalize_scene_graphs
from src.data.schemas import JoinedImage, SceneGraph, Split
from src.data.sources import ensure_source, load_manifest, save_manifest
from src.data.splits import make_vg_coco_split, select_candidates
from src.data.vg_coco_join import join_vg_coco

log = logging.getLogger("build_vg_coco")
STAGES = ("sources", "join", "normalize", "split", "export", "images", "graph")


def _save(path: Path, payload: Any, overwrite: bool) -> None:
    """Refuse to replace an existing, different JSON without explicit intent."""
    payload = json.loads(json.dumps(payload))
    if path.exists() and not overwrite:
        if read_json(path) != payload:
            raise DataError(f"{path} already exists with different contents; use --overwrite or another config")
        return
    write_json(path, payload)


def run(config: DataConfig, stage: str, *, overwrite: bool = False, skip_images: bool = False) -> None:
    """Execute a stage or the whole build; preserve the configured split on image restore."""
    if stage not in (*STAGES, "all"):
        raise DataError(f"unknown stage: {stage}")
    if stage == "all":
        for step in STAGES:
            if step != "images" or not skip_images:
                run(config, step, overwrite=overwrite)
        return
    paths = config.paths
    joined_file = paths.interim_dir / "joined_images.json"
    normalized_file = paths.interim_dir / "scene_graphs.json"
    if stage == "sources":
        manifest = load_manifest(paths.manifest_file)
        for spec in config.sources:
            manifest[spec.name] = ensure_source(spec, paths.raw_dir, manifest)
            save_manifest(paths.manifest_file, manifest)
    elif stage == "join":
        images, funnel = join_vg_coco(
            read_json(config.raw_path("vg_image_data")),
            load_karpathy_coco(config.raw_path("karpathy_coco")),
            config.join.captions_per_image,
        )
        _save(joined_file, [image.to_dict() for image in images], overwrite)
        _save(paths.interim_dir / "join_report.json", funnel.to_dict(), overwrite)
    elif stage == "normalize":
        graphs, normalization_report = normalize_scene_graphs(
            read_json(config.raw_path("vg_scene_graphs")),
            {int(row["vg_image_id"]) for row in read_json(joined_file)},
            backfill_min_count=config.normalize.backfill_min_count,
            backfill_min_share=config.normalize.backfill_min_share,
        )
        _save(normalized_file, [graph.to_dict() for graph in graphs], overwrite)
        _save(paths.interim_dir / "normalization_report.json", normalization_report.to_dict(), overwrite)
    elif stage == "split":
        images = [JoinedImage.from_dict(row) for row in read_json(joined_file)]
        graphs = [SceneGraph.from_dict(row) for row in read_json(normalized_file)]
        candidates = select_candidates(
            {image.vg_image_id: image.karpathy_split for image in images},
            {graph.vg_image_id: len(graph.relations) for graph in graphs},
            min_relations=config.split.min_relations,
            exclude_ids=config.split.exclude_ids,
        )
        result = make_vg_coco_split(candidates, config.split.sizes, config.split.n_strata, config.split.seed)
        _save(paths.split_file, {"config": config.split.to_dict(), **result.to_dict()}, overwrite)
    elif stage == "images":
        download_report = download_images(
            [ImageJob(int(row["vg_image_id"]), row["url"]) for row in read_json(paths.processed_dir / "images.json")],
            paths.processed_dir / "images",
            workers=config.download.workers,
            retries=config.download.retries,
            timeout_s=config.download.timeout_s,
        )
        write_json(paths.interim_dir / "image_download_report.json", download_report.to_dict())
        if download_report.failed:
            raise DataError(f"{len(download_report.failed)} images failed; rerun --stage images with the same split")
    else:
        split = read_json(paths.split_file)
        assignment = split_of_image({s: split[s.value] for s in Split})
        if stage == "export":
            selected = [
                JoinedImage.from_dict(row) for row in read_json(joined_file) if row["vg_image_id"] in assignment
            ]
            if {image.vg_image_id for image in selected} != set(assignment):
                raise DataError("split names images absent from the join")
            _save(
                paths.processed_dir / "images.json",
                [{**image.to_dict(), "split": assignment[image.vg_image_id].value} for image in selected],
                overwrite,
            )
            _save(
                paths.processed_dir / "queries.json",
                [query.to_dict() for query in build_queries(selected, assignment)],
                overwrite,
            )
        elif stage == "graph":
            graphs = [
                SceneGraph.from_dict(row) for row in read_json(normalized_file) if row["vg_image_id"] in assignment
            ]
            build = build_graphs(
                graphs,
                assignment,
                min_train_images=config.graph.min_train_images,
                junk_names=config.graph.junk_names,
            )
            out = paths.processed_dir / "graph"
            _save(out / "concepts.json", [vars(c) for c in build.vocabulary.concepts], overwrite)
            _save(out / "predicates.json", [vars(p) for p in build.vocabulary.predicates], overwrite)
            _save(out / "image_graphs.json", [g.to_dict() for g in build.image_graphs], overwrite)
            card = json.loads(json.dumps(graph_statistics(build)))
            if (
                paths.graph_card_file.exists()
                and not overwrite
                and yaml.safe_load(paths.graph_card_file.read_text()) != card
            ):
                raise DataError(f"{paths.graph_card_file} differs; use --overwrite or another config")
            if overwrite or not paths.graph_card_file.exists():
                paths.graph_card_file.parent.mkdir(parents=True, exist_ok=True)
                paths.graph_card_file.write_text(yaml.safe_dump(card, sort_keys=False), encoding="utf-8")
    log.info("completed stage %s", stage)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/data/vg_coco.yaml")
    parser.add_argument("--stage", choices=(*STAGES, "all"), default="all")
    parser.add_argument("--overwrite", action="store_true", help="allow rebuilding existing processed metadata")
    parser.add_argument("--skip-images", action="store_true", help="build metadata only; no JPEG downloads")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        run(DataConfig.from_yaml(args.config), args.stage, overwrite=args.overwrite, skip_images=args.skip_images)
    except (AppError, OSError, ValueError):
        log.exception("dataset build failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
