import pytest
import torch

from src.core.exceptions import DataError
from src.models.path_explain import PathExplainer
from src.models.relation_paths import RelationPathConfig, RelationPathScorer

# Two routes from 0 to 3: 0 -r0-> 1 -r1-> 3 and 0 -r0-> 2 -r1-> 3, a shortcut 0 -r2-> 3, and a spur 3 -r0-> 4.
TRIPLES = torch.tensor([[0, 0, 1], [1, 1, 3], [0, 0, 2], [2, 1, 3], [0, 2, 3], [3, 0, 4]])
DIM = 4


def _scorer(hops=3, trained=True):
    torch.manual_seed(0)
    scorer = RelationPathScorer(RelationPathConfig(max_hops=hops), TRIPLES, 5, 3, DIM)
    if trained:
        # Query-dependent step weights, as after training.
        torch.nn.init.normal_(scorer.step_weights.weight, std=0.5)
    return scorer


@pytest.mark.parametrize("hops", [1, 2, 3])
@pytest.mark.parametrize("target", [1, 3, 4])
def test_path_masses_add_up_to_the_score(hops, target):
    scorer, query = _scorer(hops), torch.randn(DIM)
    paths = PathExplainer(scorer).paths(query, 0, target)
    score = scorer(query.unsqueeze(0), torch.tensor([0]))[0, target].item()
    assert sum(p.mass for p in paths) == pytest.approx(score, rel=1e-5, abs=1e-9)
    assert all(p.steps[0].source == 0 and p.steps[-1].target == target and len(p.steps) <= hops for p in paths)
    assert [p.mass for p in paths] == sorted((p.mass for p in paths), reverse=True)


def test_steps_name_the_triple_relation_and_direction():
    paths = PathExplainer(_scorer(hops=2)).paths(torch.randn(DIM), 0, 3)
    routes = {tuple((s.source, s.relation, s.forward, s.target, s.triple) for s in p.steps) for p in paths}
    assert routes == {
        ((0, 2, True, 3, 4),),
        ((0, 0, True, 1, 0), (1, 1, True, 3, 1)),
        ((0, 0, True, 2, 2), (2, 1, True, 3, 3)),
    }
    assert paths[0].triples() <= {0, 1, 2, 3, 4}


def test_backward_steps_are_marked():
    paths = PathExplainer(_scorer(hops=1)).paths(torch.randn(DIM), 3, 1)
    assert [(s.source, s.relation, s.forward, s.target) for p in paths for s in p.steps] == [(3, 1, False, 1)]


def test_unreachable_entity_has_no_paths_and_anchor_is_rejected():
    explainer = PathExplainer(_scorer(hops=1))
    assert explainer.paths(torch.randn(DIM), 0, 4) == []
    with pytest.raises(DataError):
        explainer.paths(torch.randn(DIM), 0, 0)


def test_edges_of_lists_incident_triples():
    assert PathExplainer(_scorer()).edges_of(3).tolist() == [1, 3, 4, 5]
