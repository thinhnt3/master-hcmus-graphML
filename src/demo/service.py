"""Free-text retrieval using the same frozen artifacts, reranker and explanations as evaluation."""

from __future__ import annotations

import threading
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from importlib.metadata import version
from pathlib import Path
from typing import Any, Protocol

import numpy as np
import torch
from huggingface_hub import try_to_load_from_cache
from packaging.version import Version

from src.core.config_parsing import read_mapping, require_field
from src.core.exceptions import ConfigError, DataError
from src.data.config import DataConfig
from src.data.json_io import read_json
from src.data.schemas import Split
from src.data.sources import sha256_of
from src.embeddings.clip_encoder import ClipEncoder
from src.embeddings.store import l2_normalize, load_table, verify_inputs_unchanged
from src.evaluation.metrics import ranks_of_relevant
from src.models.ablations import ablate_graph
from src.models.checkpoint import BEST_FILE, GRAPH_VECTORS, RunDirectory
from src.models.explain import explain_graph_score
from src.models.graphsage import GraphImageEncoder
from src.models.run_validation import validate_artifact_inputs, validate_run
from src.retrieval.config import RetrievalConfig
from src.retrieval.rerank import rerank_scores

CODE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = CODE_ROOT / "configs/demo/vg_coco.yaml"
MAX_RESULTS = 10
MAX_RELATIONS = 10
MAX_QUERY_CHARS = 2000
_GRAPH_SCORE_TOLERANCE = 1e-4


class TextEncoder(Protocol):
    """Minimal interface shared by the real frozen CLIP encoder and test doubles."""

    def encode_texts(self, texts: Sequence[str]) -> np.ndarray:
        """Return one raw vector per text."""
        ...


def _under(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


@dataclass(frozen=True)
class DemoConfig:
    """A presentation config; alpha and candidate k are read from the benchmark, never fitted here."""

    retrieval_file: Path
    asset_root: Path
    seed: int
    split: Split
    results: int
    relations: int

    @classmethod
    def from_yaml(cls, path: str | Path = DEFAULT_CONFIG, *, asset_root: Path | None = None) -> DemoConfig:
        raw = read_mapping(path)
        split = require_field(raw, "gallery_split", str)
        if split not in {Split.VAL.value, Split.TEST.value}:
            raise ConfigError("demo.gallery_split must be val or test")
        results = require_field(raw, "results", int)
        relations = require_field(raw, "relations", int)
        if not 1 <= results <= MAX_RESULTS or not 0 <= relations <= MAX_RELATIONS:
            raise ConfigError("demo.results must be 1..10 and demo.relations 0..10")
        return cls(
            retrieval_file=_under(CODE_ROOT, Path(require_field(raw, "retrieval_config", str))),
            asset_root=(asset_root or CODE_ROOT).expanduser().resolve(),
            seed=require_field(raw, "seed", int),
            split=Split(split),
            results=results,
            relations=relations,
        )

    def retrieval(self) -> RetrievalConfig:
        config = RetrievalConfig.from_yaml(self.retrieval_file)
        return replace(
            config,
            data_config=_under(self.asset_root, config.data_config),
            embeddings_dir=_under(self.asset_root, config.embeddings_dir),
            runs_dir=_under(self.asset_root, config.runs_dir),
        )


def check_artifacts(options: DemoConfig) -> dict[str, Any]:
    """Check portable provenance and required inputs without loading CLIP or training anything."""
    environment = runtime_environment()
    config = options.retrieval()
    data = DataConfig.from_yaml(config.data_config)
    processed = _under(options.asset_root, data.paths.processed_dir)
    run_name = config.graphsage.run_name()
    run_path = config.runs_dir / "graphsage" / run_name / f"seed{options.seed}"
    benchmark_path = config.runs_dir / "benchmark" / f"graphsage-{run_name}.json"
    required = [
        processed / "images.json",
        processed / "queries.json",
        processed / "graph/image_graphs.json",
        run_path / BEST_FILE,
        run_path / f"{GRAPH_VECTORS}.npy",
        run_path / f"{GRAPH_VECTORS}.ids.json",
        benchmark_path,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise DataError("Thiếu dữ liệu/model để chạy demo:\n" + "\n".join(missing))
    verify_inputs_unchanged(config.model_embeddings_dir(), input_root=options.asset_root)
    validate_run(run_path, config, options.seed, input_root=options.asset_root)
    benchmark = read_json(benchmark_path)
    validate_artifact_inputs(benchmark, str(benchmark_path), input_root=options.asset_root)
    if benchmark.get("run_name") != run_name or benchmark.get("clip_model") != config.clip.model_name:
        raise DataError("benchmark model/run does not match the demo config")
    try:
        setting = benchmark["seeds"][str(options.seed)]["selected_on_validation"]
        alpha, top_k = float(setting["alpha"]), int(setting["top_k"])
    except (KeyError, TypeError, ValueError) as exc:
        raise DataError("benchmark has no valid validation-selected setting for this seed") from exc
    images = read_json(processed / "images.json")
    gallery = [row for row in images if row["split"] == options.split.value]
    if not gallery or not 0 <= alpha <= 1 or not 1 <= top_k <= len(gallery):
        raise DataError("invalid gallery or validation-selected alpha/k")
    available_images = sum((processed / "images" / f"{int(row['vg_image_id'])}.jpg").is_file() for row in gallery)
    return {
        "dataset": "VG ∩ COCO",
        "model": config.clip.model_name,
        "run_name": run_name,
        "seed": options.seed,
        "gallery_split": options.split.value,
        "gallery_images": len(gallery),
        "available_images": available_images,
        "alpha": alpha,
        "candidate_k": top_k,
        "selection": "validation",
        "benchmark_sha256": sha256_of(benchmark_path),
        "checkpoint_sha256": sha256_of(run_path / BEST_FILE),
        "environment": environment,
        "clip_cached": clip_is_cached(config.clip.model_name),
    }


def runtime_environment() -> dict[str, str]:
    """Fail clearly when an interpreter ignores the repository's Transformers constraint."""
    packages = {name: version(name) for name in ("transformers", "torch", "torch-geometric", "numpy", "Pillow")}
    if not Version("4.40") <= Version(packages["transformers"]) < Version("5"):
        raise DataError(
            "Demo cần transformers>=4.40,<5 theo requirements.txt. "
            "Dùng Python của .venv sau khi cài requirements-notebook.txt."
        )
    return packages


def clip_is_cached(model_name: str) -> bool:
    """Check the standard CLIP files without contacting Hugging Face."""

    def cached(name: str) -> bool:
        value = try_to_load_from_cache(model_name, name)
        return isinstance(value, str) and Path(value).is_file()

    tokenizer = cached("tokenizer.json") or (cached("vocab.json") and cached("merges.txt"))
    weights = cached("model.safetensors") or cached("pytorch_model.bin")
    return cached("config.json") and cached("preprocessor_config.json") and tokenizer and weights


class RetrievalDemo:
    """One frozen encoder/model shared by notebook and HTTP requests; no fitting or test tuning."""

    def __init__(
        self,
        options: DemoConfig,
        protocol: dict[str, Any],
        image_vectors: np.ndarray,
        graph_vectors: np.ndarray,
        images: Sequence[Mapping[str, Any]],
        queries: Sequence[Mapping[str, Any]],
        image_dir: Path,
        encoder: TextEncoder,
        model: GraphImageEncoder,
        graphs: Mapping[int, Mapping[str, Any]],
        image_rows: Mapping[int, int],
        concepts: Mapping[int, str],
        predicates: Mapping[int, str],
    ) -> None:
        self.options, self.protocol = options, protocol
        if image_vectors.shape != graph_vectors.shape or image_vectors.shape[0] != len(images):
            raise DataError("image/graph vectors must have the same shape and one row per gallery image")
        self.image_vectors, self.graph_vectors = image_vectors, graph_vectors
        self.images = [dict(row) for row in images]
        self.image_ids = [int(row["vg_image_id"]) for row in self.images]
        self.column_of = {image_id: i for i, image_id in enumerate(self.image_ids)}
        self.queries = {str(row["query_id"]): dict(row) for row in queries if row["split"] == options.split.value}
        self.image_dir, self.encoder, self.model = image_dir, encoder, model
        self.graphs, self.image_rows = graphs, image_rows
        self.concepts, self.predicates = concepts, predicates
        self._lock = threading.Lock()

    @classmethod
    def load(cls, options: DemoConfig, *, encoder: TextEncoder | None = None) -> RetrievalDemo:
        """Load and validate once. An injected encoder is useful for offline, controlled tests."""
        protocol = check_artifacts(options)
        if protocol["available_images"] != protocol["gallery_images"]:
            raise DataError("Thiếu ảnh gallery. Chạy: python -m scripts.run_demo images --asset-root <thư mục dữ liệu>")
        if encoder is None and not protocol["clip_cached"]:
            raise DataError("Chưa cache CLIP. Chạy một lần có mạng: python -m scripts.run_demo prepare-model")
        config = options.retrieval()
        data = DataConfig.from_yaml(config.data_config)
        processed = _under(options.asset_root, data.paths.processed_dir)
        embeddings = config.model_embeddings_dir()
        image_table = load_table(embeddings, "images")
        run_path = config.runs_dir / "graphsage" / config.graphsage.run_name() / f"seed{options.seed}"
        graph_table = load_table(run_path, GRAPH_VECTORS)
        images = sorted(
            [row for row in read_json(processed / "images.json") if row["split"] == options.split.value],
            key=lambda row: int(row["vg_image_id"]),
        )
        ids = [int(row["vg_image_id"]) for row in images]
        concepts, predicates = load_table(embeddings, "concepts"), load_table(embeddings, "predicates")
        model = GraphImageEncoder(
            config.graphsage,
            torch.from_numpy(concepts.vectors),
            torch.from_numpy(predicates.vectors),
            torch.from_numpy(image_table.vectors),
        ).eval()
        model.load_state_dict(RunDirectory(run_path).load_best()["model"])
        graphs = {int(row["vg_image_id"]): row for row in read_json(processed / "graph/image_graphs.json")}
        missing_graphs = set(ids) - graphs.keys()
        if missing_graphs:
            raise DataError(f"gallery images lack graphs: {sorted(missing_graphs)[:5]}")
        return cls(
            options,
            protocol,
            image_table.select(ids),
            graph_table.select(ids),
            images,
            read_json(processed / "queries.json"),
            processed / "images",
            encoder or ClipEncoder(config.clip.model_name, config.clip.device, local_files_only=True),
            model,
            graphs,
            {int(k): v for k, v in image_table.row_of().items()},
            {int(row["concept_id"]): row["text"] for row in read_json(processed / "graph/concepts.json")},
            {int(row["predicate_id"]): row["text"] for row in read_json(processed / "graph/predicates.json")},
        )

    def examples(self, limit: int = 6) -> list[dict[str, str]]:
        """Deterministic examples, selected by query ID rather than model success."""
        rows = sorted(self.queries.values(), key=lambda row: row["query_id"])
        return [{"query_id": row["query_id"], "text": row["text"]} for row in rows[:limit]]

    def image_file(self, image_id: int) -> Path:
        """Only expose images belonging to this gallery, never arbitrary local paths."""
        if image_id not in self.column_of:
            raise DataError("image is outside the demo gallery")
        path = self.image_dir / f"{image_id}.jpg"
        if not path.is_file():
            raise DataError("image file is missing; restore gallery images before the demo")
        return path

    def search(
        self,
        query: str,
        *,
        results: int | None = None,
        relations: int | None = None,
        query_id: str | None = None,
    ) -> dict[str, Any]:
        """Encode any new sentence; query_id only supplies known ground truth for an exact example."""
        if not isinstance(query, str) or not query.strip() or len(query) > MAX_QUERY_CHARS:
            raise DataError("Nhập một câu truy vấn từ 1 đến 2000 ký tự.")
        query = query.strip()
        results = self.options.results if results is None else results
        relations = self.options.relations if relations is None else relations
        if type(results) is not int or not 1 <= results <= min(MAX_RESULTS, len(self.images)):
            raise DataError("results must be an integer between 1 and min(10, gallery size)")
        if type(relations) is not int or not 0 <= relations <= MAX_RELATIONS:
            raise DataError("relations must be an integer between 0 and 10")
        if query_id is not None and not isinstance(query_id, str):
            raise DataError("query_id must be a string")
        known = self.queries.get(query_id) if query_id is not None else None
        if query_id is not None and (known is None or known["text"].strip() != query):
            raise DataError("query_id must identify the exact unchanged example text")
        start = time.perf_counter()
        # Serialize access to the shared CLIP/MPS encoder and graph model.
        with self._lock:
            raw_vector = np.asarray(self.encoder.encode_texts([query]), dtype=np.float32)
            if raw_vector.shape != (1, self.image_vectors.shape[1]) or not np.isfinite(raw_vector).all():
                raise DataError("text encoder returned an invalid query vector")
            vector = l2_normalize(raw_vector)
            clip = vector @ self.image_vectors.T
            graph = vector @ self.graph_vectors.T
            alpha, candidate_k = self.protocol["alpha"], self.protocol["candidate_k"]
            final = rerank_scores(clip, graph, alpha, candidate_k)
            cutoff = np.partition(clip[0], len(self.images) - candidate_k)[len(self.images) - candidate_k]
            candidates = clip[0] >= cutoff  # Same inclusive tie rule as the official reranker.
            clip_order = np.argsort(-clip[0], kind="stable")
            final_order = np.argsort(-final[0], kind="stable")
            clip_ranks = ranks_of_relevant(np.repeat(clip, results, axis=0), final_order[:results])
            ranked = []
            for position, column in enumerate(final_order[:results], 1):
                image_id = self.image_ids[column]
                selected_relations = []
                if relations:
                    image_graph = ablate_graph(
                        self.graphs[image_id], self.model.config.ablation, self.model.config.ablation_seed
                    )
                    score, contributions = explain_graph_score(
                        self.model,
                        image_graph,
                        self.image_rows[image_id],
                        torch.from_numpy(vector[0]),
                        self.concepts,
                        self.predicates,
                    )
                    if abs(score - float(graph[0, column])) > _GRAPH_SCORE_TOLERANCE:
                        raise DataError("exported graph vectors do not match the checkpoint used for explanations")
                    selected_relations = [
                        {
                            **item.to_dict(),
                            "final_score_drop": (1 - alpha) * item.score_drop if candidates[column] else 0.0,
                        }
                        for item in contributions[:relations]
                    ]
                ranked.append(
                    {
                        "rank": position,
                        "image_id": image_id,
                        "image_url": f"/api/image/{image_id}",
                        "clip_rank": int(clip_ranks[position - 1]),
                        "clip_score": float(clip[0, column]),
                        "graph_score": float(graph[0, column]),
                        "final_score": float(final[0, column]),
                        "rerank_candidate": bool(candidates[column]),
                        "relations": selected_relations,
                    }
                )
        ground_truth = None
        if known is not None:
            target = int(known["relevant_ids"][0])
            column = self.column_of[target]
            ground_truth = {
                "image_id": target,
                "image_url": f"/api/image/{target}",
                "clip_rank": int(ranks_of_relevant(clip, [column])[0]),
                "reranked_rank": int(ranks_of_relevant(final, [column])[0]),
            }
        return {
            "query": query,
            "query_id": query_id,
            "protocol": self.protocol,
            "elapsed_seconds": round(time.perf_counter() - start, 3),
            "clip_results": [
                {"rank": i, "image_id": self.image_ids[column], "image_url": f"/api/image/{self.image_ids[column]}"}
                for i, column in enumerate(clip_order[:results], 1)
            ],
            "results": ranked,
            "ground_truth": ground_truth,
        }
