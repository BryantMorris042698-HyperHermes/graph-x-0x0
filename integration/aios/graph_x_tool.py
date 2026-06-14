"""graph_x_tool.py

AIOS-compatible Tool wrapper for Graph_x_0x0 high_agent_engine.

Exposes the mathematical core (Φ(G), regime switching, deviation detection, theory)
as callable functions for AIOS Tool Manager and agents (Honcho swarms, self-improving loops, Hermes-orchestrated tasks).

Usage in AIOS:
- Import and register with Tool Manager (see AIOS docs for custom tools).
- Or run standalone / via Hermes for immediate mobile use.
- Designed for Termux + Remote Kernel Mode.
"""

import json
import math
from typing import Dict, Any, Optional, List
from dataclasses import asdict

# Import the existing Python mirror (adjust path as needed)
try:
    from high_agent_engine.graph import DirectedGraph, seed_demo_graph, Node, Edge
    from high_agent_engine.engine import RegimeEngine, RegimeTransition
except ImportError:
    # Fallback for standalone testing
    import sys
    sys.path.append(".")
    from python.high_agent_engine.graph import DirectedGraph, seed_demo_graph, Node, Edge
    from python.high_agent_engine.engine import RegimeEngine, RegimeTransition


class GraphXTool:
    """AIOS Tool exposing Graph_x_0x0 capabilities."""

    def __init__(self, initial_graph: Optional[DirectedGraph] = None):
        self.graph = initial_graph or seed_demo_graph()
        self.engine = RegimeEngine(self.graph)
        self.name = "graph_x_0x0"
        self.description = "Mathematical codebase analysis: compute Φ(G), detect deviations, switch regimes, explain theory, run self-improving iterations."

    def compute_phi(self, regime: Optional[str] = None) -> Dict[str, Any]:
        """Compute Φ(G) for current or specified regime."""
        phi = self.engine.compute_phi(regime)
        snap = self.engine.graph.snapshot()
        return {
            "phi": round(phi, 4),
            "regime": regime or self.engine.current_regime,
            "snapshot": snap,
            "status": "success"
        }

    def get_best_regime(self) -> Dict[str, Any]:
        """Evaluate all regimes and return the best one with Φ."""
        best_name, best_phi = self.engine.best_regime()
        return {
            "best_regime": best_name,
            "best_phi": round(best_phi, 4),
            "current_regime": self.engine.current_regime,
            "current_phi": round(self.engine.compute_phi(), 4)
        }

    def evaluate_and_switch(self) -> Dict[str, Any]:
        """Check if switching regime improves Φ beyond hysteresis; switch if so."""
        trans = self.engine.evaluate_and_switch()
        if trans:
            return {
                "switched": True,
                "from": trans.from_regime,
                "to": trans.to_regime,
                "reason": trans.reason,
                "phi_before": round(trans.phi_before, 4),
                "phi_after": round(trans.phi_after, 4)
            }
        return {"switched": False, "current_regime": self.engine.current_regime}

    def detect_deviation(self) -> Dict[str, Any]:
        """Run segmented regression deviation detection on latest snapshot."""
        deviation = self.engine.feed_detector()
        if deviation:
            return {
                "deviation_detected": True,
                "direction": deviation.get("direction"),
                "details": deviation.get("deviations", [])
            }
        return {"deviation_detected": False, "window_size": len(self.engine.detector_window)}

    def theory_explain(self) -> str:
        """Return formatted Theory Mode explanation with live values."""
        return self.engine.theory_explain()

    def run_self_improving_iteration(self, change_description: str = "simulated refactor") -> Dict[str, Any]:
        """Execute one cycle of the self-improving loop using this engine."""
        baseline = self.engine.compute_phi()
        snap_before = self.engine.graph.snapshot()

        # Simulate change impact (in real use: apply actual code change or Honcho proposal)
        # For demo: randomly improve quality or add coupling
        import random
        if random.random() > 0.4:
            for nid in list(self.engine.graph.nodes.keys())[:2]:
                self.engine.graph.nodes[nid].quality = min(1.0, self.engine.graph.nodes[nid].quality + 0.04)
            impact = "positive (quality improved)"
        else:
            # Add a cross-module edge (risky)
            mods = list(set(n.module for n in self.engine.graph.nodes.values()))
            if len(mods) > 1:
                self.engine.graph.add_edge(Edge(mods[0], mods[1], 1.5))
            impact = "negative (added coupling)"

        new_phi = self.engine.compute_phi()
        deviation = self.engine.feed_detector()
        trans = self.engine.evaluate_and_switch()

        improved = new_phi > baseline
        result = {
            "iteration_impact": impact,
            "baseline_phi": round(baseline, 4),
            "new_phi": round(new_phi, 4),
            "improved": improved,
            "deviation": deviation,
            "regime_switch": asdict(trans) if trans else None,
            "change_description": change_description,
            "snapshot_after": self.engine.graph.snapshot()
        }
        # In production: log to MemePlace / AIOS Memory Manager here
        return result

    def load_graph_from_json(self, json_str: str) -> Dict[str, Any]:
        """Load a real codebase graph (from Python crawler) into the engine."""
        data = json.loads(json_str)
        # Minimal reconstruction; extend for full Node/Edge hydration
        self.graph = DirectedGraph()
        for n in data.get("nodes", []):
            self.graph.add_node(Node(n["id"], n.get("module", "unknown"), n.get("cyclomatic", 1.0), n.get("quality", 0.8)))
        for e in data.get("edges", []):
            self.graph.add_edge(Edge(e["from"], e["to"], e.get("weight", 1.0)))
        self.engine = RegimeEngine(self.graph)
        return {"status": "graph loaded", "nodes": len(self.graph.nodes)}


# Standalone test / Hermes-callable entrypoint
if __name__ == "__main__":
    tool = GraphXTool()
    print("=== Graph_x_0x0 AIOS Tool Test ===")
    print(tool.theory_explain())
    print("\nBest regime:", tool.get_best_regime())
    print("\nDeviation check:", tool.detect_deviation())
    switch_res = tool.evaluate_and_switch()
    print("\nSwitch result:", switch_res)
    iter_res = tool.run_self_improving_iteration("demo refactor from Honcho proposal")
    print("\nSelf-improving iteration:", json.dumps(iter_res, indent=2))
