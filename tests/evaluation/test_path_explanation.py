import random

import numpy as np
import pytest
import torch

from src.core.exceptions import DataError
from src.evaluation.path_explanation import (
    deletion_effects,
    explanation_triples,
    path_sparsity,
    relation_validity,
    sample_controls,
    scores_without,
    summarize_deletions,
)
from src.models.path_explain import PathExplainer
from tests.models.test_path_explain import DIM, _scorer

GALLERY = torch.arange(5)


def _paths(hops=2):
    scorer, query = _scorer(hops), torch.ones(DIM)
    return scorer, query, PathExplainer(scorer).paths(query, 0, 3)


def test_sparsity_counts_triples_of_the_heaviest_paths():
    _, _, paths = _paths()
    one = path_sparsity(paths, 1)
    assert one["paths"] == 3 and one["support_triples"] == 5
    assert one["explanation_triples"] == len(paths[0].triples())
    assert one["sparsity"] == pytest.approx(1 - one["explanation_triples"] / 5)
    assert 0 < one["mass_share"] < 1
    everything = path_sparsity(paths, 10)
    assert everything["sparsity"] == 0 and everything["mass_share"] == pytest.approx(1.0)
    assert everything["explanation_paths"] == 3
    with pytest.raises(DataError):
        path_sparsity([], 1)


def test_removing_the_whole_support_zeroes_the_target_only_for_that_group():
    scorer, query, paths = _paths()
    support = explanation_triples(paths, 10)
    rows = scores_without(scorer, query, 0, GALLERY, [[], support, [5]])
    assert rows[0, 3] > 0 and rows[1, 3] == 0
    assert rows[2, 3] == pytest.approx(rows[0, 3])  # the spur 3 → 4 is on no walk of two edges to 3
    assert rows.max(axis=1)[0] == pytest.approx(1.0)


def test_deletion_effects_report_rank_changes_against_controls():
    scorer, query, paths = _paths()
    rows = scores_without(scorer, query, 0, GALLERY, [[], explanation_triples(paths, 10), [5]])
    baseline, selected, control = deletion_effects(np.zeros(5, dtype=np.float32), rows, 3, alpha=0.0, top_k=5)
    summary = summarize_deletions(baseline, selected, [control])
    assert summary["selected_path_drop"] == pytest.approx(baseline["path_score"])
    assert summary["selected_rank_increase"] > 0
    assert summary["random_path_drop_mean"] == pytest.approx(0.0, abs=1e-6)
    assert summary["random_rank_increase_mean"] == 0
    assert "random_path_drop_mean" not in summarize_deletions(baseline, selected, [])


def test_validity_checks_relation_and_direction():
    _, _, paths = _paths()
    shortcut = [p for p in paths if len(p.steps) == 1]
    assert relation_validity(shortcut, 1, relation_id=2, forward=True) == {
        "relation_on_top_path": True,
        "relation_in_explanation": True,
        "relation_and_direction_in_explanation": True,
    }
    against = relation_validity(shortcut, 1, relation_id=2, forward=False)
    assert against["relation_and_direction_in_explanation"] is False
    assert relation_validity(shortcut, 1, relation_id=1, forward=True)["relation_in_explanation"] is False
    # Relation 1 is on both two-edge walks, so widening the explanation finds it.
    assert relation_validity([*shortcut, *paths], 4, relation_id=1, forward=True)["relation_in_explanation"] is True


def test_controls_need_a_pool_larger_than_the_group():
    rng = random.Random(3)
    assert sample_controls([1, 2], 2, 5, rng) == []
    groups = sample_controls([1, 2, 3, 3, 4], 2, 5, rng)
    assert len(groups) == 5 and all(len(set(g)) == 2 and set(g) <= {1, 2, 3, 4} for g in groups)
