#!/usr/bin/env python3
"""Explain relation-path retrieval on MKG-W with sub-graphs and measure the explanations.

Run from the repository root after `train_mkg_w_relation_paths --variant real`:
    python -m scripts.evaluate_mkg_w_path_explanations

For each sampled query the explained entity is the one ranked first by CLIP + path score,
right or wrong. Its explanation is the triples on the heaviest walks from the query's anchor.
Three things are measured per query and averaged per seed:
  fidelity  remove the explanation's triples, re-score every entity, compare the entity's
            path score and rank with removing as many random triples from two pools:
            `support` (triples on any walk to the entity) and `endpoints` (triples touching
            the anchor or the entity);
  sparsity  1 − explanation triples / support triples, and the share of score mass kept;
  validity  whether the explanation walks over the relation the query asks about.
Per-query sub-graphs, in ids and in words, go to the output file with the summaries.
"""
from __future__ import annotations

import argparse
import logging
import random
import sys
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import numpy as np
import torch

from src.core.config_parsing import read_mapping, require_field
from src.core.exceptions import AppError, DataError
from src.data.json_io import read_json, write_json
from src.data.mkg_w_config import MkgwConfig
from src.data.schemas import Split
from src.data.sources import sha256_of
from src.embeddings.store import load_table, verify_inputs_unchanged
from src.evaluation.mkg_w_benchmark import build_entity_split, gallery_columns
from src.evaluation.path_explanation import (
    deletion_effects,
    explanation_triples,
    path_sparsity,
    relation_validity,
    sample_controls,
    scores_without,
    summarize_deletions,
)
from src.models.kg_experiment import Variant
from src.models.path_explain import PathExplainer, WeightedPath
from src.models.relation_paths import RelationPathScorer
from src.retrieval.mkg_w_config import MkgwRetrievalConfig
from src.retrieval.rerank import rerank_scores

log = logging.getLogger("evaluate_mkg_w_path_explanations")

DEFAULT_PROTOCOL = "configs/evaluation/path_explanation.yaml"
# Per-query numbers averaged in the summary; a query without a control group is left out of that mean.
_SUMMARY_KEYS = (
    "sparsity", "mass_share", "explanation_triples", "support_triples",
    "relation_on_top_path", "relation_in_explanation", "relation_and_direction_in_explanation",
    "selected_path_drop", "selected_rank_increase", "selected_top1_lost",
    "support.random_path_drop_mean", "support.random_rank_increase_mean", "support.random_top1_lost_rate",
    "endpoints.random_path_drop_mean", "endpoints.random_rank_increase_mean", "endpoints.random_top1_lost_rate",
)


def _path_text(path: WeightedPath, entities: Sequence[Mapping[str, Any]],
               relations: Sequence[Mapping[str, Any]]) -> str:
    """A walk in words, arrows in triple direction: `A —[director]→ B ←[cast member]— C`."""
    text = entities[path.steps[0].source]["name"]
    for step in path.steps:
        label = relations[step.relation]["label"]
        arrow = f" —[{label}]→ " if step.forward else f" ←[{label}]— "
        text += arrow + entities[step.target]["name"]
    return text


def _summary(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Means over evaluated queries: all, per hop distance, and per outcome of the explained prediction."""
    groups: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for record in records:
        if record["status"] != "evaluated":
            continue
        outcome = ("relevant" if record["predicted_is_relevant"]
                   else "known_answer" if record["predicted_is_known_answer"] else "wrong")
        for name in ("all", f"hops={record['hops']}", f"predicted={outcome}"):
            groups[name].append(record["metrics"])
    return {
        name: {"queries": len(rows),
               **{key: float(np.mean([r[key] for r in rows if key in r])) for key in _SUMMARY_KEYS
                  if any(key in r for r in rows)},
               "queries_with_support_control": sum("support.random_path_drop_mean" in r for r in rows)}
        for name, rows in sorted(groups.items())
    }


def run(protocol_path: str) -> None:
    """Explain the sampled queries with every trained seed and write records and summaries."""
    protocol = read_mapping(protocol_path)
    config_path = require_field(protocol, "retrieval_config", str)
    config = MkgwRetrievalConfig.from_yaml(config_path)
    split = Split(require_field(protocol, "split", str))
    if split is Split.TRAIN:
        raise DataError("explanations are evaluated on validation or test")
    sample = require_field(protocol, "sample_queries", int)
    max_paths = require_field(protocol, "max_paths", int)
    repeats = require_field(protocol, "random_repeats", int)
    sample_seed = require_field(protocol, "sample_seed", int)
    random_seed = require_field(protocol, "random_seed", int)
    if min(sample, max_paths, repeats) < 1:
        raise DataError("sample_queries, max_paths and random_repeats must be positive")

    processed = MkgwConfig.from_yaml(config.data_config).paths.processed_dir
    entities = read_json(processed / "entities.json")
    relations = read_json(processed / "relations.json")
    queries = read_json(processed / "queries.json")
    embeddings_dir = config.model_embeddings_dir()
    verify_inputs_unchanged(embeddings_dir)
    query_table = load_table(embeddings_dir, "queries")
    data = build_entity_split(split, entities, queries, load_table(embeddings_dir, "images"), query_table)
    column_of = gallery_columns(entities)
    gallery_ids = list(column_of)
    gallery = torch.tensor(gallery_ids)
    triples = torch.tensor([tuple(t) for t in read_json(processed / "triples.json")["train"]], dtype=torch.long)

    anchored = [row for row, q in enumerate(data.queries) if q["anchor_id"] is not None]
    if sample > len(anchored):
        raise DataError(f"sample_queries exceeds the {len(anchored)} anchored queries of the split")
    rows = sorted(random.Random(sample_seed).sample(anchored, sample))
    vectors = torch.from_numpy(query_table.select([data.queries[row]["query_id"] for row in rows]))

    run_dir = config.runs_dir / "relation_paths" / Variant.REAL.value
    benchmark_path = run_dir / "benchmark.json"
    benchmark = read_json(benchmark_path)
    inputs = [Path(protocol_path), Path(config_path), benchmark_path, embeddings_dir / "meta.json",
              processed / "triples.json", processed / "queries.json"]
    seeds: dict[str, Any] = {}
    for seed in config.path_training.seeds:
        model = RelationPathScorer(config.relation_paths, triples, len(entities), len(relations), vectors.shape[1])
        model.load_state_dict(torch.load(run_dir / f"seed-{seed}" / "model.pt", weights_only=True))
        explainer = PathExplainer(model)
        choice = benchmark["seeds"][str(seed)]["selected"]
        alpha, top_k = float(choice["alpha"]), int(choice["top_k"])
        records = []
        for done, (row, vector) in enumerate(zip(rows, vectors, strict=True), 1):
            query = data.queries[row]
            anchor = int(query["anchor_id"])
            clip_row = data.clip_scores[row]
            # The prediction to explain: first place under the full graph.
            baseline_row = scores_without(model, vector, anchor, gallery, [[]])
            fused_top = int(np.argmax(rerank_scores(clip_row[None, :], baseline_row, alpha, top_k)[0]))
            entity = gallery_ids[fused_top]
            record: dict[str, Any] = {
                "query_id": query["query_id"], "text": query["text"], "hops": query["hops"],
                "anchor": entities[anchor]["name"], "predicted": entities[entity]["name"],
                "predicted_is_relevant": fused_top in data.relevant[row],
                # A correct answer already stated in the train graph; the benchmark skips these when ranking.
                "predicted_is_known_answer": fused_top in data.known[row],
            }
            paths = explainer.paths(vector, anchor, entity) if entity != anchor else []
            if not paths:
                # CLIP alone put this entity first; the graph has nothing to explain.
                records.append({**record, "status": "skipped", "reason": "no_path_to_prediction"})
                continue
            chosen = explanation_triples(paths, max_paths)
            support = sorted({t for p in paths for t in p.triples()})
            endpoints = sorted({*explainer.edges_of(anchor).tolist(), *explainer.edges_of(entity).tolist()})
            rng = random.Random(random_seed + row)
            controls = {"support": sample_controls(support, len(chosen), repeats, rng),
                        "endpoints": sample_controls(endpoints, len(chosen), repeats, rng)}
            groups = [[], chosen, *controls["support"], *controls["endpoints"]]
            effects = deletion_effects(clip_row, scores_without(model, vector, anchor, gallery, groups),
                                       fused_top, alpha, top_k)
            baseline, selected = effects[0], effects[1]
            metrics: dict[str, Any] = {
                **path_sparsity(paths, max_paths),
                **relation_validity(paths, max_paths, int(query["relation_id"]), query["direction"] == "tail"),
            }
            start = 2
            for pool, pool_groups in controls.items():
                summary = summarize_deletions(baseline, selected, effects[start:start + len(pool_groups)])
                start += len(pool_groups)
                metrics.update({k: v for k, v in summary.items() if k.startswith("selected_")})
                metrics.update({f"{pool}.{k}": v for k, v in summary.items() if k.startswith("random_")})
            records.append({
                **record, "status": "evaluated", "metrics": metrics,
                "baseline": baseline, "without_explanation": selected,
                "explanation": [{"path": _path_text(p, entities, relations), "mass": p.mass,
                                 "triples": sorted(p.triples())} for p in paths[:max_paths]],
                "removed_triples": chosen, "control_triples": controls,
            })
            if done % 50 == 0:
                log.info("seed %s: %d/%d queries", seed, done, sample)
        seeds[str(seed)] = {"selected": choice, "summary": _summary(records), "queries": records}
        inputs.append(run_dir / f"seed-{seed}" / "model.pt")
        overall = seeds[str(seed)]["summary"].get("all", {})
        log.info("seed %s: evaluated %s/%d; %s", seed, overall.get("queries", 0), sample,
                 {k: round(v, 4) for k, v in overall.items() if k != "queries"})

    output = Path(require_field(protocol, "output", str))
    write_json(output, {
        "protocol": protocol,
        "target": "entity ranked first by CLIP + path score; all entities re-scored after each removal",
        "limitation": (
            "Explanation walks are chosen by the mass the scorer itself assigns; validity checks relation "
            "types only, not whether a walk is a sound argument; degrees are not recomputed after removal"
        ),
        "seeds": seeds,
        "inputs_sha256": {str(p): sha256_of(p) for p in inputs},
    })
    log.info("wrote %s", output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", default=DEFAULT_PROTOCOL)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    try:
        run(args.config)
    except AppError:
        log.exception("path explanation evaluation failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
