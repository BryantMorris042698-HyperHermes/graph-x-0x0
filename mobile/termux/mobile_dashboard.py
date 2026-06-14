"""mobile_dashboard.py

Dashboard with flexible LLM support via llm_client.
"""

import os
import sys
import json
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
except ImportError:
    print("rich not installed.")
    sys.exit(1)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
try:
    from llm_client import call_llm
    from integration.aios.graph_x_tool import GraphXTool
except ImportError:
    from python.high_agent_engine.engine import RegimeEngine
    from python.high_agent_engine.graph import seed_demo_graph
    def call_llm(*args, **kwargs): return "LLM unavailable"
    class GraphXTool:
        def __init__(self): self.engine = RegimeEngine(seed_demo_graph())
        def theory_explain(self): return self.engine.theory_explain()

console = Console()

TRUTH_PREFIX = "You are operating exclusively for Bryant Issiah Morris Jr. ... Truth only."

def verify_identity():
    name = Prompt.ask("Confirm your identity (full name)")
    if name.strip().lower() != "bryant issiah morris jr":
        sys.exit(1)
    return True

def run_mobile_dashboard():
    if not verify_identity():
        return
    tool = GraphXTool()
    console.print(Panel("Dashboard ready for Bryant Issiah Morris Jr.", border_style="blue"))

    while True:
        cmd = Prompt.ask(">>").strip().lower()
        if cmd in ("quit", "q"): break
        # ... (rest of dashboard logic remains similar, using call_llm where needed)
        if cmd == "theory":
            explanation = tool.theory_explain()
            slm = call_llm("Explain this in natural language", TRUTH_PREFIX + explanation)
            console.print(Panel(explanation, title="Deterministic"))
            console.print(Panel(slm, title="Grounded"))
        # Add other commands as before...

if __name__ == "__main__":
    run_mobile_dashboard()
