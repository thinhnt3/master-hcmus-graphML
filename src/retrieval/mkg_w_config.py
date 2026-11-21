"""Typed, validated view of `configs/retrieval/mkg_w.yaml`."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from pathlib import Path
from typing import Any

from src.core.config_parsing import read_mapping, require_field, require_section
from src.core.exceptions import ConfigError
from src.embeddings.device import Device
from src.models.kg_adamf_mat import KgAdamfMatConfig
from src.models.kg_adamf_train import KgAdamfTrainingConfig
from src.models.kg_graphsage import KgSageConfig
from src.models.relation_paths import RelationPathConfig
from src.models.train import TrainingConfig
from src.retrieval.config import ClipConfig, _training_config
from src.retrieval.kg_adamf_config import load_adamf_configs


class SelectionQueries(StrEnum):
    """Which validation queries pick the best epoch of a graph model."""

    ALL = "all"
    INDIRECT = "indirect"


@dataclass(frozen=True)
class MkgwRetrievalConfig:
    """Root config for retrieval experiments on a knowledge graph (MKG-W, VN heritage).

    The `anchor_linking` and `relation_paths` sections belong to the MKG-W experiments only.
    A config without them still loads; reading the matching property then raises ConfigError.
    """

    data_config: Path
    clip: ClipConfig
    embeddings_dir: Path
    recall_ks: tuple[int, ...]
    candidate_ks: tuple[int, ...]
    alpha_grid: tuple[float, ...]
    top_k_grid: tuple[int, ...]
    path_decay_grid: tuple[float, ...]
    path_shuffle_seed: int
    anchor_linking_section: tuple[float, ...] | None
    graphsage: KgSageConfig
    selection_queries: SelectionQueries
    relation_paths_section: RelationPathConfig | None
    training: TrainingConfig
    path_training_section: TrainingConfig | None
    adamf_mat: KgAdamfMatConfig
    adamf_training: KgAdamfTrainingConfig
    runs_dir: Path

    @property
    def anchor_self_weight_grid(self) -> tuple[float, ...]:
        """Self-weight grid of anchor linking; needs the `anchor_linking` section."""
        if self.anchor_linking_section is None:
            raise ConfigError("this experiment needs the 'anchor_linking' section of the retrieval config")
        return self.anchor_linking_section

    @property
    def relation_paths(self) -> RelationPathConfig:
        """Relation-path model settings; needs the `relation_paths` section."""
        if self.relation_paths_section is None:
            raise ConfigError("this experiment needs the 'relation_paths' section of the retrieval config")
        return self.relation_paths_section

    @property
    def path_training(self) -> TrainingConfig:
        """Training settings of the relation-path model; needs the `relation_paths` section."""
        if self.path_training_section is None:
            raise ConfigError("this experiment needs the 'relation_paths' section of the retrieval config")
        return self.path_training_section

    @classmethod
    def from_yaml(cls, path: str | Path) -> MkgwRetrievalConfig:
        """Load and validate the YAML file; raise ConfigError on any problem."""
        return cls.from_dict(read_mapping(path))

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> MkgwRetrievalConfig:
        """Build from an already-parsed mapping (used by tests)."""
        clip_raw = require_section(raw, "clip")
        device = require_field(clip_raw, "device", str)
        if device not in {d.value for d in Device}:
            raise ConfigError(f"clip.device must be one of {[d.value for d in Device]}, got {device!r}")
        clip = ClipConfig(
            model_name=require_field(clip_raw, "model_name", str),
            device=Device(device),
            image_batch_size=require_field(clip_raw, "image_batch_size", int),
            text_batch_size=require_field(clip_raw, "text_batch_size", int),
        )
        if not clip.model_name or clip.image_batch_size < 1 or clip.text_batch_size < 1:
            raise ConfigError("clip.model_name must be set and batch sizes must be >= 1")
        benchmark_raw = require_section(raw, "benchmark")
        alpha_step = float(require_field(benchmark_raw, "alpha_step", (int, float)))
        steps = round(1.0 / alpha_step) if alpha_step > 0 else 0
        if not 0.0 < alpha_step <= 1.0 or abs(steps * alpha_step - 1.0) > 1e-9:
            raise ConfigError(f"benchmark.alpha_step must divide 1 evenly and lie in (0, 1], got {alpha_step}")
        path_raw = require_section(raw, "path_score")
        decays = path_raw.get("decay_grid")
        if (
            not isinstance(decays, list)
            or not decays
            or not all(isinstance(d, (int, float)) and not isinstance(d, bool) and 0 < d <= 1 for d in decays)
        ):
            raise ConfigError("path_score.decay_grid must be a non-empty list of numbers in (0, 1]")
        self_weights: list[Any] | None = None
        if "anchor_linking" in raw:
            self_weights = require_section(raw, "anchor_linking").get("self_weight_grid")
            if (
                not isinstance(self_weights, list)
                or not self_weights
                or not all(isinstance(w, (int, float)) and not isinstance(w, bool) and w >= 0 for w in self_weights)
            ):
                raise ConfigError("anchor_linking.self_weight_grid must be a non-empty list of numbers >= 0")
        sage_raw = require_section(raw, "kg_graphsage")
        # Absent keys keep what configs written before them did: select on all queries, no structure-only rows.
        selection = sage_raw.get("selection_queries", SelectionQueries.ALL.value)
        if selection not in {s.value for s in SelectionQueries}:
            raise ConfigError(f"kg_graphsage.selection_queries must be one of {[s.value for s in SelectionQueries]}")
        structure_only_rate = sage_raw.get("structure_only_rate", 0.0)
        if not isinstance(structure_only_rate, (int, float)) or isinstance(structure_only_rate, bool):
            raise ConfigError(f"kg_graphsage.structure_only_rate must be a number, got {structure_only_rate!r}")
        training = _training_config(raw)
        relation_paths: RelationPathConfig | None = None
        path_training: TrainingConfig | None = None
        if "relation_paths" in raw:
            paths_raw = require_section(raw, "relation_paths")
            relation_paths = RelationPathConfig(max_hops=require_field(paths_raw, "max_hops", int))
            # Same seeds, patience and stopping rule; only the optimizer step differs.
            path_training = replace(
                training,
                batch_size=require_field(paths_raw, "batch_size", int),
                learning_rate=float(require_field(paths_raw, "learning_rate", (int, float))),
            )
        adamf_mat, adamf_training = load_adamf_configs(raw)
        return cls(
            data_config=Path(require_field(raw, "data_config", str)),
            clip=clip,
            embeddings_dir=Path(require_field(raw, "embeddings_dir", str)),
            recall_ks=_positive_ints(benchmark_raw, "recall_ks"),
            candidate_ks=_positive_ints(benchmark_raw, "candidate_ks"),
            alpha_grid=tuple(round(i / steps, 6) for i in range(steps + 1)),
            top_k_grid=_positive_ints(benchmark_raw, "top_k_grid"),
            path_decay_grid=tuple(float(d) for d in decays),
            path_shuffle_seed=require_field(path_raw, "shuffle_seed", int),
            anchor_linking_section=tuple(float(w) for w in self_weights) if self_weights is not None else None,
            graphsage=KgSageConfig(
                hidden_dim=require_field(sage_raw, "hidden_dim", int),
                num_layers=require_field(sage_raw, "num_layers", int),
                structure_only_rate=float(structure_only_rate),
            ),
            selection_queries=SelectionQueries(selection),
            relation_paths_section=relation_paths,
            training=training,
            path_training_section=path_training,
            adamf_mat=adamf_mat,
            adamf_training=adamf_training,
            runs_dir=Path(require_field(raw, "runs_dir", str)),
        )

    def model_embeddings_dir(self) -> Path:
        """Directory holding the embedding tables of the configured CLIP model."""
        return self.embeddings_dir / self.clip.model_name.replace("/", "--")


def _positive_ints(raw: dict[str, Any], key: str) -> tuple[int, ...]:
    values = raw.get(key)
    if (
        not isinstance(values, list)
        or not values
        or not all(isinstance(v, int) and not isinstance(v, bool) and v >= 1 for v in values)
    ):
        raise ConfigError(f"benchmark.{key} must be a non-empty list of integers >= 1")
    return tuple(values)
