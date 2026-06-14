"""engine.py - RegimeEngine with detection, switching, and theory."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from .graph import DirectedGraph, seed_demo_graph

from . import regime as reg  # local regime.py

@dataclass
class RegimeTransition:
    from_regime: str
    to_regime: str
    reason: str
    phi_before: float
    phi_after: float

@dataclass
class RegimeEngine:
    graph: DirectedGraph
    current_regime: str = "Hybrid"
    history: List[Dict] = field(default_factory=list)
    transitions: List[RegimeTransition] = field(default_factory=list)
    detector_window: List[Dict] = field(default_factory=list)
    window_size: int = 5
    z_threshold: float = 2.0
    hysteresis: float = 0.05

    REGIME_COEFFS = {
        "Simple":   {"alpha": 0.8, "beta": 0.9, "gamma": 0.2},
        "Advanced": {"alpha": 1.2, "beta": 0.5, "gamma": 0.3},
        "Hybrid":   {"alpha": 1.0, "beta": 0.6, "gamma": 0.4},
    }

    def compute_phi(self, regime: Optional[str] = None) -> float:
        coeffs = self.REGIME_COEFFS.get(regime or self.current_regime, self.REGIME_COEFFS["Hybrid"])
        return self.graph.multi_objective(coeffs)

    def best_regime(self) -> Tuple[str, float]:
        best_name = self.current_regime
        best_phi = -float("inf")
        for name in self.REGIME_COEFFS:
            phi = self.compute_phi(name)
            if phi > best_phi:
                best_phi = phi
                best_name = name
        return best_name, best_phi

    def evaluate_and_switch(self) -> Optional[RegimeTransition]:
        best_name, best_phi = self.best_regime()
        current_phi = self.compute_phi()
        if best_name != self.current_regime and (best_phi - current_phi) > self.hysteresis:
            trans = RegimeTransition(
                from_regime=self.current_regime,
                to_regime=best_name,
                reason="Higher Φ(G) by > hysteresis",
                phi_before=current_phi,
                phi_after=best_phi,
            )
            self.transitions.append(trans)
            self.current_regime = best_name
            return trans
        return None

    def feed_detector(self, snap: Optional[Dict] = None):
        """Segmented regression style deviation detection."""
        if snap is None:
            snap = self.graph.snapshot()
        self.detector_window.append(snap)
        if len(self.detector_window) > self.window_size:
            self.detector_window.pop(0)
        if len(self.detector_window) < 3:
            return None
        # Simple z-score on key metrics
        keys = ["q", "coupling", "mean_v"]
        deviations = []
        for k in keys:
            vals = [w[k] for w in self.detector_window[:-1]]
            mean = sum(vals) / len(vals)
            std = math.sqrt(sum((v - mean)**2 for v in vals) / max(1, len(vals)-1)) or 1.0
            z = abs(snap[k] - mean) / std
            if z > self.z_threshold:
                deviations.append((k, z, snap[k] > mean))
        if deviations:
            direction = "Improving" if any(d[2] for d in deviations if d[0] in ["q"]) else "Degrading"
            return {"direction": direction, "deviations": deviations}
        return None

    def detect_and_switch(self) -> Optional[RegimeTransition]:
        deviation = self.feed_detector()
        if deviation:
            # Re-evaluate on deviation
            return self.evaluate_and_switch()
        return None

    def theory_explain(self) -> str:
        snap = self.graph.snapshot()
        phi = self.compute_phi()
        best, best_phi = self.best_regime()
        return f"""Theory Mode - Live Graph Analysis

Current Regime: {self.current_regime}
Φ(G) = {phi:.4f}   (best possible: {best} @ {best_phi:.4f})

Q (modularity):     {snap['q']:.4f}
Č (coupling):      {snap['coupling']:.4f}
mean(V) cyclomatic: {snap['mean_v']:.2f}
Nodes/Edges:        {snap['n_nodes']} / {snap['n_edges']}

Regime Strategy: {self.REGIME_COEFFS[self.current_regime]}

Deviation Status: {len(self.detector_window)} samples in window.
"""

# Example usage
if __name__ == "__main__":
    g = seed_demo_graph()
    engine = RegimeEngine(g)
    print(engine.theory_explain())
    print("Best regime:", engine.best_regime())
    trans = engine.evaluate_and_switch()
    if trans:
        print("Switched:", trans)
