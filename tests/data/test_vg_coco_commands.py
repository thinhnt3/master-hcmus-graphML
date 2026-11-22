"""Exercise the raw-to-graph command boundary and reject broken evaluation metadata."""

from dataclasses import replace

import pytest

from scripts.build_vg_coco import run
from scripts.review_vg_coco import audit
from src.core.exceptions import ChecksumMismatchError, DataError
from src.data.config import DataConfig, SourceSpec
from src.data.json_io import read_json, write_json
from src.data.schemas import Split


@pytest.fixture
def built_data(tmp_path):
    base = DataConfig.from_yaml("configs/data/vg_coco.yaml")
    images, coco, graphs = [], [], []
    for image_id in range(1, 13):
        images.append(
            {
                "image_id": image_id,
                "coco_id": image_id,
                "url": "file:///unused.jpg",
                "width": 10,
                "height": 10,
            }
        )
        coco.append(
            {
                "cocoid": image_id,
                "split": "test" if image_id > 8 else "train",
                "sentences": [{"sentid": image_id, "raw": "A man rides a horse."}],
            }
        )
        graphs.append(
            {
                "image_id": image_id,
                "objects": [
                    {"object_id": 1, "names": ["man"], "synsets": ["man.n.01"]},
                    {"object_id": 2, "names": ["horse"], "synsets": ["horse.n.01"]},
                ],
                "relationships": [{"subject_id": 1, "object_id": 2, "predicate": "riding"}],
            }
        )
    specs = []
    for name, payload in (("vg_image_data", images), ("vg_scene_graphs", graphs), ("karpathy_coco", {"images": coco})):
        source = tmp_path / "remote" / f"{name}.json"
        write_json(source, payload)
        specs.append(SourceSpec(name, source.as_uri(), f"{name}.json"))
    config = replace(
        base,
        paths=replace(
            base.paths,
            raw_dir=tmp_path / "raw",
            interim_dir=tmp_path / "interim",
            manifest_file=tmp_path / "raw/MANIFEST.json",
            split_file=tmp_path / "split.json",
            processed_dir=tmp_path / "processed",
            graph_card_file=tmp_path / "graph.yaml",
        ),
        sources=tuple(specs),
        join=replace(base.join, captions_per_image=1),
        split=replace(base.split, sizes={s: 2 for s in Split}, n_strata=1),
        graph=replace(base.graph, min_train_images=1),
    )
    run(config, "all", skip_images=True)
    return config


def test_build_is_restartable_and_preserves_raw_to_query_mapping(built_data):
    config = built_data
    # Existing metadata may use a different JSON formatting style. A no-op
    # rebuild must preserve bytes, because consumers pin the file hashes.
    queries_file = config.paths.processed_dir / "queries.json"
    write_json(queries_file, read_json(queries_file), indent=None)
    before = audit(config)
    assert before["images"] == {"train": 2, "val": 2, "test": 2}
    assert before["concepts"] == 2 and before["predicates"] == 1
    run(config, "all", skip_images=True)
    assert audit(config) == before
    for query in read_json(config.paths.processed_dir / "queries.json"):
        assert query["query_id"] == f"coco-{query['relevant_ids'][0]}"


def test_build_refuses_changed_raw_file(built_data):
    config = built_data
    write_json(config.raw_path("vg_image_data"), [])
    with pytest.raises(ChecksumMismatchError):
        run(config, "sources")


@pytest.mark.parametrize("defect", ["overlap", "cross_split", "wrong_answer", "unknown_predicate"])
def test_audit_rejects_corrupted_evaluation_metadata(built_data, defect):
    config = built_data
    root = config.paths.processed_dir
    if defect == "overlap":
        split = read_json(config.paths.split_file)
        split["test"].append(split["train"][0])
        write_json(config.paths.split_file, split)
    elif defect in {"cross_split", "wrong_answer"}:
        queries = read_json(root / "queries.json")
        if defect == "cross_split":
            queries[0]["split"] = "test" if queries[0]["split"] != "test" else "train"
        else:
            queries[0]["relevant_ids"] = [99999]
        write_json(root / "queries.json", queries)
    else:
        graphs = read_json(root / "graph/image_graphs.json")
        graphs[0]["triplets"][0][1] = 99999
        write_json(root / "graph/image_graphs.json", graphs)
    with pytest.raises(DataError):
        audit(config)


def test_rebuild_requires_explicit_overwrite_for_changed_outputs(built_data):
    config = built_data
    queries_file = config.paths.processed_dir / "queries.json"
    write_json(queries_file, [])
    with pytest.raises(DataError, match="already exists"):
        run(config, "export")
    run(config, "export", overwrite=True)
    assert audit(config)["status"] == "passed"
