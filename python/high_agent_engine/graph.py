"""graph.py - Core G=(V,E) model and metrics computation."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import math

@dataclass
class Node:
    id: str
    module: str
    cyclomatic: float = 1.0
    quality: float = 0.8

@dataclass
class Edge:
    from_id: str
    to_id: str
    weight: float = 1.0

@dataclass
class DirectedGraph:
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def modularity(self) -> float:
        """Approximate Newman-Girvan style modularity based on modules."""
        if not self.nodes:
            return 0.0
        modules = {}
        for n in self.nodes.values():
            modules.setdefault(n.module, []).append(n.id)
        if len(modules) <= 1:
            return 0.0
        total_edges = len(self.edges) or 1
        q = 0.0
        for mod_nodes in modules.values():
            intra = sum(1 for e in self.edges if e.from_id in mod_nodes and e.to_id in mod_nodes)
            # Expected random term simplified
            deg_sum = len(mod_nodes)
            q += (intra / total_edges) - (deg_sum / (2 * total_edges)) ** 2
        return max(0.0, min(1.0, q))

    def mean_coupling(self) -> float:
        """Mean inter-module edge weight per node."""
        if not self.nodes or not self.edges:
            return 0.0
        inter = 0.0
        count = 0
        node_mod = {nid: n.module for nid, n in self.nodes.items()}
        for e in self.edges:
            if node_mod.get(e.from_id) != node_mod.get(e.to_id):
                inter += e.weight
                count += 1
        return inter / max(1, count)

    def mean_cyclomatic(self) -> float:
        if not self.nodes:
            return 0.0
        return sum(n.cyclomatic for n in self.nodes.values()) / len(self.nodes)

    def mean_quality(self) -> float:
        if not self.nodes:
            return 0.0
        return sum(n.quality for n in self.nodes.values()) / len(self.nodes)

    def snapshot(self):
        return {
            "n_nodes": len(self.nodes),
            "n_edges": len(self.edges),
            "q": self.modularity(),
            "coupling": self.mean_coupling(),
            "mean_v": self.mean_cyclomatic(),
            "mean_quality": self.mean_quality(),
        }

    def multi_objective(self, coeffs: Optional[Dict[str, float]] = None) -> float:
        """Compute Φ(G) = αQ - βČ - γ mean(V)."""
        if coeffs is None:
            coeffs = {"alpha": 1.0, "beta": 0.6, "gamma": 0.4}
        snap = self.snapshot()
        phi = (coeffs["alpha"] * snap["q"]
               - coeffs["beta"] * snap["coupling"]
               - coeffs["gamma"] * snap["mean_v"])
        return phi


def seed_demo_graph() -> DirectedGraph:
    """Seed a small 7-node demo graph matching the spec."""
    g = DirectedGraph()
    modules = ["core", "cli", "skills", "graph", "tui"]
    nodes_data = [
        ("main", "core", 2.0, 0.85),
        ("parse_args", "cli", 3.5, 0.75),
        ("run_engine", "core", 4.0, 0.8),
        ("modularity", "graph", 5.0, 0.9),
        ("draw_dashboard", "tui", 2.5, 0.7),
        ("orchestrator", "core", 3.0, 0.82),
        ("theory_explain", "core", 2.0, 0.88),
    ]
    for nid, mod, cyc, qual in nodes_data:
        g.add_node(Node(nid, mod, cyc, qual))
    edges_data = [
        ("main", "parse_args", 1.2),
        ("main", "run_engine", 2.0),
        ("run_engine", "modularity", 1.5),
        ("run_engine", "orchestrator", 1.0),
        ("orchestrator", "theory_explain", 0.8),
        ("parse_args", "draw_dashboard", 0.5),
        ("modularity", "theory_explain", 0.7),
        ("skills", "main", 0.3),  # cross module example
    ]
    for fr, to, w in edges_data:
        g.add_edge(Edge(fr, to, w))
    return g
