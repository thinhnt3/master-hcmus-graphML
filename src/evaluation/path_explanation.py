"""Fidelity, sparsity and relation validity of a path explanation sub-graph. No file I/O here.

The explanation of a (query, entity) pair is the set of graph triples on its heaviest walks.
Fidelity removes those triples for that query and re-scores every entity, so rivals move too;
controls remove the same number of triples drawn at random from a named pool.
"""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
import torch

from src.core.exceptions import DataError
from src.evaluation.fidelity import target_rank
from src.models.path_explain import WeightedPath
from src.models.relation_paths import RelationPathScorer
from src.retrieval.rerank import rerank_scores


def explanation_triples(paths: Sequence[WeightedPath], max_paths: int) -> list[int]:
    """Graph triples on the `max_paths` heaviest walks, sorted."""
    if max_paths < 1:
        raise DataError("max_paths must be >= 1")
    return sorted({triple for path in paths[:max_paths] for triple in path.triples()})


def path_sparsity(paths: Sequence[WeightedPath], max_paths: int) -> dict[str, int | float]:
    """How small the explanation is next to everything that feeds the score.

    `support_triples` are the triples on any walk to the entity; removing all of them sets its
    score to 0. `mass_share` is the part of the score the explanation's walks carry.
    """
    if not paths:
        raise DataError("an entity without paths has no explanation")
    explanation = explanation_triples(paths, max_paths)
    support = {triple for path in paths for triple in path.triples()}
    total = sum(path.mass for path in paths)
    return {
        "paths": len(paths),
        "explanation_paths": min(max_paths, len(paths)),
        "support_triples": len(support),
        "explanation_triples": len(explanation),
        "sparsity": 1 - len(explanation) / len(support),
        "mass_share": sum(path.mass for path in paths[:max_paths]) / total,
    }


def relation_validity(
    paths: Sequence[WeightedPath], max_paths: int, relation_id: int, forward: bool
) -> dict[str, bool]:
    """Whether the explanation walks over the relation the query asks about.

    `forward` is the direction the query reads the relation in: True when it names the head
    and asks for the tail. This checks relation types only; it does not judge whether the
    walk is a sound argument for the answer.
    """
    chosen = paths[:max_paths]
    return {
        "relation_on_top_path": any(step.relation == relation_id for step in chosen[0].steps),
        "relation_in_explanation": any(step.relation == relation_id for path in chosen for step in path.steps),
        "relation_and_direction_in_explanation": any(
            step.relation == relation_id and step.forward is forward for path in chosen for step in path.steps
        ),
    }


def sample_controls(pool: Sequence[int], size: int, repeats: int, rng: random.Random) -> list[list[int]]:
    """`repeats` random groups of `size` triples from the pool; empty when the pool is not larger than a group."""
    candidates = sorted(set(pool))
    if len(candidates) <= size:
        return []
    return [sorted(rng.sample(candidates, size)) for _ in range(repeats)]


@torch.no_grad()
def scores_without(
    model: RelationPathScorer,
    query_vector: torch.Tensor,
    anchor: int,
    gallery: torch.Tensor,
    removed_groups: Sequence[Sequence[int]],
) -> np.ndarray:
    """(groups × gallery) path scores with each group of triples removed; rows divided by their largest value.

    Same normalization as the benchmark, so a row can be fused with CLIP as usual. Degree
    normalization keeps the degrees of the full graph, as when the scorer hides a fact in training.
    """
    if not removed_groups:
        raise DataError("no groups of triples to remove")
    model.eval()
    n = len(removed_groups)
    hidden = torch.tensor(
        [(row, triple) for row, group in enumerate(removed_groups) for triple in group], dtype=torch.long
    ).reshape(-1, 2)
    scores = model(query_vector.unsqueeze(0).expand(n, -1), torch.full((n,), anchor), hidden)[:, gallery]
    normalized: np.ndarray = (scores / scores.amax(dim=1, keepdim=True).clamp(min=1e-30)).numpy().astype(np.float32)
    return normalized


def deletion_effects(
    clip_row: np.ndarray,
    path_rows: np.ndarray,
    target: int,
    alpha: float,
    top_k: int,
) -> list[dict[str, float | int]]:
    """Path score, fused score and rank of the target column in each row of `path_rows`."""
    fused = rerank_scores(np.repeat(clip_row[None, :], len(path_rows), axis=0), path_rows, alpha, top_k)
    return [
        {
            "path_score": float(path_rows[row, target]),
            "fused_score": float(fused[row, target]),
            "rank": target_rank(fused[row], target, float(fused[row, target])),
        }
        for row in range(len(path_rows))
    ]


def summarize_deletions(
    baseline: Mapping[str, Any], selected: Mapping[str, Any], controls: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Drop of the target after removing the explanation, next to the mean over random groups."""
    result: dict[str, Any] = {
        "selected_path_drop": baseline["path_score"] - selected["path_score"],
        "selected_rank_increase": selected["rank"] - baseline["rank"],
        "selected_top1_lost": baseline["rank"] == 1 and selected["rank"] > 1,
    }
    if controls:
        result.update(
            random_path_drop_mean=float(np.mean([baseline["path_score"] - c["path_score"] for c in controls])),
            random_rank_increase_mean=float(np.mean([c["rank"] - baseline["rank"] for c in controls])),
            random_top1_lost_rate=float(np.mean([baseline["rank"] == 1 and c["rank"] > 1 for c in controls])),
        )
    return result
