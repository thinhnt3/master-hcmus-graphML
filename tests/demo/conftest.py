import numpy as np
import pytest
import torch
from PIL import Image
from torch_geometric.data import Batch

from src.data.schemas import Split
from src.demo.service import DemoConfig, RetrievalDemo
from src.embeddings.store import l2_normalize
from src.models.graph_data import image_graph_to_data
from src.models.graphsage import GraphImageEncoder, GraphSageConfig, ImageNodeFeature


class FakeEncoder:
    def __init__(self):
        self.seen = []

    def encode_texts(self, texts):
        self.seen.extend(texts)
        return np.array([[3, 0, 0] for _ in texts], dtype=np.float32)


@pytest.fixture
def demo(tmp_path):
    torch.manual_seed(7)
    vectors = torch.eye(3)
    cfg = GraphSageConfig(hidden_dim=8, num_layers=2, directed=True, image_node=ImageNodeFeature.LEARNED)
    model = GraphImageEncoder(cfg, vectors, vectors).eval()
    graphs = {
        101: {"vg_image_id": 101, "concept_ids": [0, 1], "triplets": [[0, 0, 1]]},
        102: {"vg_image_id": 102, "concept_ids": [0, 2], "triplets": [[0, 1, 2]]},
        103: {"vg_image_id": 103, "concept_ids": [1, 2], "triplets": [[1, 2, 2]]},
    }
    with torch.no_grad():
        graph_vectors = model(
            Batch.from_data_list([image_graph_to_data(g, i) for i, g in enumerate(graphs.values())])
        ).numpy()
    for image_id in graphs:
        Image.new("RGB", (20, 20), "green").save(tmp_path / f"{image_id}.jpg")
    return RetrievalDemo(
        DemoConfig(tmp_path / "unused.yaml", tmp_path, 13, Split.TEST, 3, 1),
        {"alpha": 0.7, "candidate_k": 2, "gallery_images": 3, "selection": "validation"},
        l2_normalize(np.array([[1, 0, 0], [0.8, 0.6, 0], [0, 1, 0]], dtype=np.float32)),
        graph_vectors,
        [{"vg_image_id": image_id, "split": "test"} for image_id in graphs],
        [{"query_id": "known-1", "text": "A person riding a horse.", "split": "test", "relevant_ids": [102]}],
        tmp_path,
        FakeEncoder(),
        model,
        graphs,
        {101: 0, 102: 1, 103: 2},
        {0: "person", 1: "horse", 2: "field"},
        {0: "riding", 1: "in", 2: "near"},
    )
