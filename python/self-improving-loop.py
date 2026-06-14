"""self-improving-loop.py - Extended with Graph_x_0x0 / RegimeEngine integration.

Cycle: baseline Φ → apply change (or agent proposal) → re-measure → commit/rollback + MemePlace log.

This version demonstrates the loop on the demo graph. In production, replace
'apply_change' with real refactor or Honcho swarm output, and persist to MemePlace.
"""

import json
import os
from datetime import datetime
from high_agent_engine.graph import seed_demo_graph
from high_agent_engine.engine import RegimeEngine

STATE_FILE = "state/self_improving_state.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"iterations": 0, "last_phi": None}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def apply_demo_change(g, iteration: int):
    """Simulate a refactor or feature addition that may improve or degrade metrics."""
    # Example: add a well-placed node/edge or increase quality
    if iteration % 2 == 0:
        # "Good" change: improve quality of core nodes
        for nid in ["main", "run_engine"]:
            if nid in g.nodes:
                g.nodes[nid].quality = min(1.0, g.nodes[nid].quality + 0.05)
        return "Improved core quality (refactor)"
    else:
        # "Risky" change: add cross-module spaghetti
        g.add_edge(Edge("skills", "tui", 2.5))  # bad coupling
        return "Added cross-module dependency (risky)"

def run_self_improving_loop(max_iter: int = 6):
    print("=== Self-Improving Loop with Graph_x_0x0 ===")
    g = seed_demo_graph()
    engine = RegimeEngine(g)
    state = load_state()

    for i in range(max_iter):
        print(f"\n--- Iteration {i+1} ---")
        baseline_phi = engine.compute_phi()
        snap = engine.graph.snapshot()
        print(f"Baseline Φ(G): {baseline_phi:.4f} | Q={snap['q']:.3f} Č={snap['coupling']:.3f}")

        # Simulate agent-proposed change (in real: from Honcho or MemePlace task)
        change_desc = apply_demo_change(engine.graph, i)
        print(f"Applied change: {change_desc}")

        new_phi = engine.compute_phi()
        deviation = engine.feed_detector()
        trans = engine.evaluate_and_switch()

        improved = new_phi > baseline_phi
        print(f"New Φ(G): {new_phi:.4f} | Improved: {improved}")
        if trans:
            print(f"Regime switched to {trans.to_regime}")

        # Log to MemePlace (stub - replace with actual client call)
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "iteration": i,
            "baseline_phi": baseline_phi,
            "new_phi": new_phi,
            "improved": improved,
            "change": change_desc,
            "regime": engine.current_regime,
            "deviation": deviation,
        }
        print("Logged to MemePlace (spatial entry in ArchitectureAnalysis room):", json.dumps(log_entry, indent=2)[:200] + "...")

        state["iterations"] = i + 1
        state["last_phi"] = new_phi
        save_state(state)

    print("\nLoop complete. Final regime:", engine.current_regime)
    print("Theory:\n" + engine.theory_explain())

if __name__ == "__main__":
    run_self_improving_loop()
