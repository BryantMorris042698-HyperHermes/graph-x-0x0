"""example_self_improving_agent.py

Example AIOS-managed agent that uses the GraphXTool for Φ(G)-driven self-improvement.

This demonstrates how Graph_x_0x0 becomes a schedulable, memory-aware agent inside AIOS.
Can be extended with Honcho swarm proposals, MemePlace retrieval, and Hermes orchestration.

Run inside AIOS environment (or standalone for testing).
"""

import json
from datetime import datetime
try:
    from graph_x_tool import GraphXTool
except ImportError:
    from integration.aios.graph_x_tool import GraphXTool


def run_aios_managed_self_improving_agent(max_cycles: int = 5):
    print("=== AIOS-Managed Graph_x_0x0 Self-Improving Agent ===")
    tool = GraphXTool()

    for cycle in range(max_cycles):
        print(f"\n--- Cycle {cycle + 1} ---")
        # 1. Baseline via tool
        baseline = tool.compute_phi()
        print(f"Baseline: {json.dumps(baseline, indent=2)}")

        # 2. (Optional) Retrieve context from AIOS Memory / MemePlace
        # memory_context = retrieve_from_memeplace("ArchitectureAnalysis", query=...)

        # 3. Simulate Honcho proposal or agent reasoning for change
        change_desc = f"Cycle {cycle+1} refactor proposal (e.g. extract module to reduce coupling)"

        # 4. Execute improvement iteration via tool
        result = tool.run_self_improving_iteration(change_desc)
        print(f"Result: improved={result['improved']}, new_phi={result['new_phi']}")

        # 5. Log transition / snapshot to AIOS Memory Manager or MemePlace
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "cycle": cycle,
            "result": result,
            "theory": tool.theory_explain()[:300] + "..."
        }
        print("Logged to AIOS memory / MemePlace:", json.dumps(log, indent=2)[:400])

        if result.get("regime_switch"):
            print("Regime switched by AIOS scheduler influence.")

    print("\nAgent run complete. Final theory:\n" + tool.theory_explain())


if __name__ == "__main__":
    run_aios_managed_self_improving_agent()
