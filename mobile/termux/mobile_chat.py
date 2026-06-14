"""mobile_chat.py

Conversational chat interface...
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
    from llm_client import call_llm, get_llm_endpoint
    from integration.aios.graph_x_tool import GraphXTool
except ImportError:
    from python.high_agent_engine.engine import RegimeEngine
    from python.high_agent_engine.graph import seed_demo_graph
    def call_llm(prompt, system_prompt=None, max_tokens=600):
        return "LLM client not available."
    class GraphXTool:
        def __init__(self): self.engine = RegimeEngine(seed_demo_graph())
        def theory_explain(self): return self.engine.theory_explain()

console = Console()

TRUTH_PREFIX = "You are operating exclusively for Bryant Issiah Morris Jr. Respond ONLY with verifiable Graph_x_0x0 results or MemePlace content. Truth only."

def verify_identity():
    name = Prompt.ask("Confirm your identity (full name)")
    if name.strip().lower() != "bryant issiah morris jr":
        console.print("[red]Access denied.[/red]")
        sys.exit(1)
    return True

def run_chat():
    if not verify_identity():
        return

    tool = GraphXTool()
    console.print(Panel("Chat ready. Type naturally. 'quit' to exit.", border_style="blue"))

    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()
            if user_input.lower() in ("quit", "exit", "q"):
                break

            lower = user_input.lower()
            tool_response = None

            if any(k in lower for k in ["phi", "score"]):
                tool_response = tool.compute_phi()
            elif "theory" in lower or "explain" in lower:
                tool_response = tool.theory_explain()
            elif "switch" in lower or "regime" in lower:
                tool_response = tool.evaluate_and_switch()
            elif "improve" in lower:
                tool_response = tool.run_self_improving_iteration(user_input)

            if tool_response:
                context = json.dumps(tool_response, indent=2) if isinstance(tool_response, dict) else str(tool_response)
                console.print(Panel(context, title="Deterministic Result", border_style="green"))
                natural = call_llm(user_input, TRUTH_PREFIX + "\n\nContext: " + context)
                console.print(Panel(natural, title="Grounded Explanation", border_style="yellow"))
            else:
                current_state = tool.theory_explain()[:600]
                reply = call_llm(user_input, TRUTH_PREFIX + "\n\nCurrent state: " + current_state)
                console.print(Panel(reply, title="Response", border_style="cyan"))

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    run_chat()
