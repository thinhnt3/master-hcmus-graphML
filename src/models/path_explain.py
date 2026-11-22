"""Explain a relation path score: the walks that carry mass from the query's anchor to one entity.

The scorer's value for an entity is the sum of the masses of all walks of at most `max_hops`
edges that end on it. Listing those walks is therefore an exact decomposition of the score;
the heaviest ones form the explanation sub-graph of a (query, entity) pair.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import numpy as np
import torch
from torch import nn

from src.core.exceptions import DataError
from src.models.relation_paths import RelationPathScorer


@dataclass(frozen=True)
class PathStep:
    """One edge of a walk, in walking order."""

    source: int
    relation: int
    forward: bool  # True: walked head → tail of the triple; False: tail → head
    target: int
    triple: int  # row of the triple in the scorer's graph


@dataclass(frozen=True)
class WeightedPath:
    """A walk from the anchor to the explained entity and the share of score it carries."""

    steps: tuple[PathStep, ...]
    mass: float

    def triples(self) -> frozenset[int]:
        """Rows of the graph triples this walk uses."""
        return frozenset(step.triple for step in self.steps)


class PathExplainer:
    """Lists the walks behind the scores of one trained `RelationPathScorer`."""

    def __init__(self, model: RelationPathScorer) -> None:
        self.model = model
        self.max_hops = model.config.max_hops
        self.sources = model.sources.cpu().numpy()
        self.targets = model.targets.cpu().numpy()
        self.edge_types = model.edge_types.cpu().numpy()
        self.edge_scale = model.edge_scale.cpu().numpy().astype(float)
        self.n_triples = model.n_triples
        self.n_relations = model.step_weights.out_features // (2 * self.max_hops)
        # Edge ids leaving each entity. Every triple is two edges: row i forward, row i + n_triples backward.
        order = np.argsort(self.sources, kind="stable")
        bounds = np.searchsorted(self.sources[order], np.arange(model.n_entities + 1))
        self._edges_from = [order[bounds[i] : bounds[i + 1]] for i in range(model.n_entities)]

    def edges_of(self, entity: int) -> np.ndarray:
        """Rows of the graph triples that touch the entity."""
        triples: np.ndarray = np.unique(self._edges_from[entity] % self.n_triples)
        return triples

    @torch.no_grad()
    def step_weights(self, query_vector: torch.Tensor) -> np.ndarray:
        """(max_hops × edge types) weight the scorer gives each relation and direction for this query."""
        if query_vector.ndim != 1:
            raise DataError("query vector must be one-dimensional")
        self.model.eval()
        device = self.model.step_weights.weight.device
        raw = self.model.step_weights(query_vector.to(device).unsqueeze(0))
        weights: np.ndarray = nn.functional.softplus(raw).view(self.max_hops, -1).cpu().numpy().astype(float)
        return weights

    def _hops_to(self, target: int) -> np.ndarray:
        """Fewest edges from every entity to the target, capped at max_hops (unreached entities keep the cap)."""
        distance = np.full(len(self._edges_from), self.max_hops, dtype=np.int64)
        distance[target] = 0
        queue = deque([target])
        while queue:
            node = queue.popleft()
            if distance[node] + 1 >= self.max_hops:
                continue
            for neighbour in np.unique(self.targets[self._edges_from[node]]):
                if distance[neighbour] > distance[node] + 1:
                    distance[neighbour] = distance[node] + 1
                    queue.append(int(neighbour))
        return distance

    def paths(self, query_vector: torch.Tensor, anchor: int, target: int) -> list[WeightedPath]:
        """Every walk of at most max_hops edges from the anchor that ends on the target, heaviest first.

        Walks may revisit entities, as in the scorer; their masses sum to the scorer's
        (un-normalized) score of the target. Equal masses keep the order they were found in.
        """
        if anchor == target:
            raise DataError("the anchor is never scored, so it has no paths to explain")
        weights = self.step_weights(query_vector)
        hops_left = self._hops_to(target)
        found: list[WeightedPath] = []
        # Depth-first over partial walks; a branch is dropped once the target is out of reach.
        stack: list[tuple[int, float, tuple[PathStep, ...]]] = [(anchor, 1.0, ())]
        while stack:
            node, mass, steps = stack.pop()
            hop = len(steps)
            edges = self._edges_from[node]
            edges = edges[hops_left[self.targets[edges]] <= self.max_hops - hop - 1]
            for edge in edges.tolist():
                after = int(self.targets[edge])
                edge_type = int(self.edge_types[edge])
                step = PathStep(node, edge_type % self.n_relations, edge < self.n_triples, after, edge % self.n_triples)
                walked = (*steps, step)
                walked_mass = mass * weights[hop, edge_type] * self.edge_scale[edge]
                if after == target:
                    found.append(WeightedPath(walked, walked_mass))
                if hop + 1 < self.max_hops:
                    stack.append((after, walked_mass, walked))
        return sorted(found, key=lambda path: -path.mass)
