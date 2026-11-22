from dataclasses import replace

import numpy as np
import pytest
import torch
from torch_geometric.data import Batch

from src.core.exceptions import DataError
from src.demo.notebook import result_html
from src.demo.service import runtime_environment
from src.models.graph_data import image_graph_to_data
from src.retrieval.rerank import rerank_scores


def test_new_text_uses_encoder_official_reranker_and_has_no_invented_answer(demo):
    result = demo.search("A newly typed sentence.")
    assert demo.encoder.seen == ["A newly typed sentence."]
    assert result["ground_truth"] is None
    assert result["protocol"]["alpha"] == 0.7
    clip = demo.image_vectors[:, 0][None, :]
    graph = demo.graph_vectors[:, 0][None, :]
    expected = rerank_scores(clip, graph, 0.7, 2)
    order = np.argsort(-expected[0], kind="stable")
    assert [row["image_id"] for row in result["results"]] == [demo.image_ids[i] for i in order]
    assert [row["final_score"] for row in result["results"]] == pytest.approx(expected[0, order])


def test_relation_delta_predicts_actual_graph_score_change_and_non_candidate_is_not_fused(demo):
    result = demo.search("Anything")
    for row in result["results"]:
        image_id = row["image_id"]
        removed = {**demo.graphs[image_id], "triplets": []}
        with torch.no_grad():
            after = demo.model(Batch.from_data_list([image_graph_to_data(removed, demo.image_rows[image_id])]))[
                0, 0
            ].item()
        relation = row["relations"][0]
        assert relation["score_drop"] == pytest.approx(row["graph_score"] - after, abs=1e-6)
        if row["rerank_candidate"]:
            assert relation["final_score_drop"] == pytest.approx(0.3 * relation["score_drop"])
        else:
            assert relation["final_score_drop"] == 0
    assert result["results"][-1]["rerank_candidate"] is False


def test_ties_at_clip_cutoff_remain_candidates(demo):
    demo.image_vectors[1] = demo.image_vectors[0]
    demo.protocol = {**demo.protocol, "candidate_k": 1}
    result = demo.search("Tied candidates")
    assert sum(row["rerank_candidate"] for row in result["results"]) == 2


def test_known_answer_requires_the_unchanged_matching_query_id(demo):
    result = demo.search("A person riding a horse.", query_id="known-1")
    assert result["ground_truth"]["image_id"] == 102
    assert result["ground_truth"]["clip_rank"] == 2
    assert demo.search("A person riding a horse.")["ground_truth"] is None
    with pytest.raises(DataError, match="exact unchanged"):
        demo.search("A different sentence", query_id="known-1")


def test_wrong_exported_graph_vectors_cannot_explain_a_different_checkpoint(demo):
    demo.graph_vectors = np.roll(demo.graph_vectors, 1, axis=1)
    with pytest.raises(DataError, match="do not match the checkpoint"):
        demo.search("Anything")


@pytest.mark.parametrize(
    "query,kwargs",
    [
        ("", {}),
        (" ", {}),
        ("x" * 2001, {}),
        (None, {}),
        ("x", {"results": True}),
        ("x", {"results": 4}),
        ("x", {"relations": -1}),
        ("x", {"query_id": [1]}),
    ],
)
def test_invalid_requests_are_rejected(demo, query, kwargs):
    with pytest.raises(DataError):
        demo.search(query, **kwargs)


def test_notebook_renderer_escapes_query_and_contains_real_images(demo):
    result = demo.search('<img src=x onerror="alert(1)">', results=1)
    output = result_html(demo, result)
    assert "data:image/jpeg;base64," in output
    assert "<img src=x" not in output
    assert "&lt;img src=x" in output
    assert "chưa có nhãn đáp án" in output


def test_image_access_is_limited_to_gallery(demo):
    assert demo.image_file(101).is_file()
    with pytest.raises(DataError, match="outside"):
        demo.image_file(9999)


def test_example_order_does_not_depend_on_predictions(demo):
    assert demo.examples() == [{"query_id": "known-1", "text": "A person riding a horse."}]
    demo.options = replace(demo.options, seed=37)
    assert demo.examples()[0]["query_id"] == "known-1"


def test_wrong_transformers_major_version_gets_an_actionable_error(monkeypatch):
    monkeypatch.setattr("src.demo.service.version", lambda name: "5.0.0" if name == "transformers" else "1.0")
    with pytest.raises(DataError, match="transformers>=4.40,<5"):
        runtime_environment()
