#!/usr/bin/env python3
"""Audit the versioned VG-COCO metadata without downloading models or images."""

from __future__ import annotations

import argparse
import logging
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from src.core.exceptions import AppError, DataError
from src.data.config import DataConfig
from src.data.export import split_of_image
from src.data.json_io import read_json, write_json
from src.data.schemas import Split
from src.data.sources import sha256_of

log = logging.getLogger("review_vg_coco")


def audit(config: DataConfig) -> dict[str, Any]:
    """Fail on inconsistent IDs, overlapping splits, query leakage or graph schema drift.

    This checks metadata contracts, not human semantic labels or byte identity of
    distinct photographs. Embedding/model consumers separately check cache hashes.
    """
    root = config.paths.processed_dir
    split = read_json(config.paths.split_file)
    assignment = split_of_image({s: split[s.value] for s in Split})
    images = read_json(root / "images.json")
    queries = read_json(root / "queries.json")
    graphs = read_json(root / "graph/image_graphs.json")
    for name, rows in (("images", images), ("graphs", graphs)):
        ids = [row["vg_image_id"] for row in rows]
        if len(ids) != len(set(ids)) or set(ids) != set(assignment):
            raise DataError(f"{name} IDs must cover the split exactly once")
        if any(row["split"] != assignment[row["vg_image_id"]].value for row in rows):
            raise DataError(f"{name} split labels disagree with the fixed split")
    for image in images:
        if (image["karpathy_split"] == "test") != (image["split"] == "test"):
            raise DataError("Karpathy test images must only appear in test, and all test images must come from it")
    query_ids: set[str] = set()
    caption_of = {
        f"coco-{caption['caption_id']}": (image["vg_image_id"], caption["text"])
        for image in images
        for caption in image["captions"]
    }
    if len(caption_of) != sum(len(image["captions"]) for image in images):
        raise DataError("duplicate caption IDs across images")
    for query in queries:
        key = query["query_id"]
        if key in query_ids or key not in caption_of:
            raise DataError("duplicate or unknown query ID")
        query_ids.add(key)
        image_id, text = caption_of[key]
        if query["relevant_ids"] != [image_id] or query["text"] != text:
            raise DataError("query text or ground truth differs from the original caption")
        if query["split"] != assignment[image_id].value:
            raise DataError("query and relevant image cross splits")
    if query_ids != set(caption_of):
        raise DataError("not all image captions have queries")
    concepts = read_json(root / "graph/concepts.json")
    predicates = read_json(root / "graph/predicates.json")
    for rows, key in ((concepts, "concept_id"), (predicates, "predicate_id")):
        if sorted(row[key] for row in rows) != list(range(len(rows))):
            raise DataError(f"{key} must be contiguous and unique")
        if any(row["train_images"] < config.graph.min_train_images for row in rows):
            raise DataError("vocabulary entries do not satisfy train-image frequency threshold")
    concept_ids = {row["concept_id"] for row in concepts}
    predicate_ids = {row["predicate_id"] for row in predicates}
    for graph in graphs:
        ids = graph["concept_ids"]
        if len(ids) != len(set(ids)) or not set(ids) <= concept_ids:
            raise DataError("graph contains duplicate or unknown concepts")
        if len(ids) != len(graph["concept_counts"]) or any(n < 1 for n in graph["concept_counts"]):
            raise DataError("graph concept counts are invalid")
        for subject, predicate, obj in graph["triplets"]:
            if subject not in ids or obj not in ids or predicate not in predicate_ids:
                raise DataError("graph relation refers to an unknown endpoint or predicate")
    files = [config.paths.split_file, root / "images.json", root / "queries.json"]
    files += [root / "graph" / f"{name}.json" for name in ("concepts", "predicates", "image_graphs")]
    return {
        "status": "passed",
        "images": dict(sorted(Counter(row["split"] for row in images).items())),
        "queries": dict(sorted(Counter(row["split"] for row in queries).items())),
        "concepts": len(concepts),
        "predicates": len(predicates),
        "sha256": {str(path): sha256_of(path) for path in files},
        "limits": ["No manual semantic audit", "No detection of identical photos with different IDs"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/data/vg_coco.yaml")
    parser.add_argument("--output", type=Path, default=Path("runs/data-review/vg-coco-audit.json"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        result = audit(DataConfig.from_yaml(args.config))
        write_json(args.output, result)
    except (AppError, OSError, ValueError, KeyError, TypeError):
        log.exception("dataset audit failed")
        return 1
    log.info("audit passed: %s; written to %s", result["images"], args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
