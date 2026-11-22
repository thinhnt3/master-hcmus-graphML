"""The knowledge-graph retrieval config loads for both datasets that share it."""

from __future__ import annotations

import pytest

from src.core.exceptions import ConfigError
from src.retrieval.mkg_w_config import MkgwRetrievalConfig, SelectionQueries

MKG_W = "configs/retrieval/mkg_w.yaml"
VN_HERITAGE = "configs/retrieval/vn_heritage_core.yaml"


def test_mkg_w_config_has_every_experiment_section() -> None:
    config = MkgwRetrievalConfig.from_yaml(MKG_W)
    assert config.anchor_self_weight_grid
    assert config.relation_paths.max_hops >= 1
    assert config.path_training.seeds == config.training.seeds


def test_config_without_mkg_w_sections_still_loads() -> None:
    config = MkgwRetrievalConfig.from_yaml(VN_HERITAGE)
    assert config.selection_queries is SelectionQueries.ALL
    assert config.graphsage.structure_only_rate == 0.0


@pytest.mark.parametrize("name", ["anchor_self_weight_grid", "relation_paths", "path_training"])
def test_reading_an_absent_section_fails_loudly(name: str) -> None:
    config = MkgwRetrievalConfig.from_yaml(VN_HERITAGE)
    with pytest.raises(ConfigError, match="section"):
        getattr(config, name)
