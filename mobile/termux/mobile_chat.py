"""mobile_chat.py

Conversational chat interface for Graph_x_0x0 on Galaxy Z Fold7 (Termux).
Exclusive to Bryant Issiah Morris Jr.

This provides a natural language chat experience in addition to the command-based TUI.
It uses the same identity verification, Truth mode prefix, and GraphXTool backend.

Run with:
  source ~/graphx0x0-mobile-venv/bin/activate
  python mobile/termux/mobile_chat.py

You can ask things like:
  - "What is the current Φ(G) score?"
  - "Should I switch regimes?"
  - "Run a self-improvement cycle on the core module"
  - "Explain the deviation in natural language"

The system will call the mathematical engine when appropriate and always stay grounded.
"""

import os
import sys
import json
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
except ImportError:
    print("rich not installed. Please run the bootstrap script first.")
    sys.exit(1)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
try:
    from integration.aios.graph_x_tool import GraphXTool
except ImportError:
    from python.high_agent_engine.engine import RegimeEngine
    from python.high_agent_engine.graph import seed_demo_graph
    class GraphXTool:
        def __init__(self):
            self.engine = RegimeEngine(seed_demo_graph())
        def compute_phi(self, regime=None):
            return {"phi": self.engine.compute_phi(regime), "regime": self.engine.current_regime}
        def theory_explain(self):
            return self.engine.theory_explain()
        def evaluate_and_switch(self):
            return self.engine.evaluate_and_switch() or {"switched": False}
        def run_self_improving_iteration(self, change_description="user requested"):
            return self.engine.run_self_improving_iteration(change_description) if hasattr(self.engine, 'run_self_improving_iteration') else {"note": "Method not available"}

console = Console()

# === Identity Guard ===
def verify_identity():
    console.print(Panel.fit(
        "[bold green]Graph_x_0x0 Chat[/bold green]\n"
        "Authorized exclusively for [bold]Bryant Issiah Morris Jr.[/bold]\n"
        "Truth mode: Only deterministic results or MemePlace-verified information.",
        border_style="green"
    ))
    name = Prompt.ask("Confirm your identity (full name)")
    if name.strip().lower() != "bryant issiah morris jr":
        console.print("[red]Access denied. This chat is for Bryant Issiah Morris Jr. only.[/red]")
        sys.exit(1)
    console.print("[green]Identity verified. Welcome, Bryant Issiah Morris Jr. You may now chat.[/green]\n")
    return True

# === Truth Mode ===
TRUTH_PREFIX = (
    "You are operating exclusively for Bryant Issiah Morris Jr. "
    "Respond ONLY with information that is either (1) the direct mathematical result from Graph_x_0x0 "
    "(Φ(G), regime, deviation, etc.) or (2) retrieved or accurately summarized from MemePlace entries "
    "associated with this user. If the information is not verifiable from these sources, state "
    "'Insufficient verified information' and do not speculate. Truth only."
)

SLM_ENDPOINT = os.environ.get("SLM_ENDPOINT", "http://localhost:8080/v1")

try:
    import requests
except ImportError:
    requests = None


def call_grounded_slm(user_message: str, tool_context: str = "") -> str:
    if requests is None:
        return "SLM client not available. Please install requests."
    try:
        full_prompt = TRUTH_PREFIX + "\n\nUser: " + user_message + "\n\nCurrent Graph_x_0x0 context: " + tool_context
        payload = {
            "model": "local-model",
            "messages": [{"role": "user", "content": full_prompt}],
            "max_tokens": 600,
            "temperature": 0.1
        }
        resp = requests.post(f"{SLM_ENDPOINT}/chat/completions", json=payload, timeout=90)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        return f"SLM error ({resp.status_code})."
    except Exception as e:
        return f"SLM unavailable: {e}. Using deterministic fallback."


def run_chat():
    if not verify_identity():
        return

    tool = GraphXTool()
    console.print(Panel("[bold]Chat ready.[/bold] Type naturally. Use 'quit' to exit. Commands like 'theory', 'phi', 'improve' still work.", border_style="blue"))

    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                console.print("[yellow]Chat ended for Bryant Issiah Morris Jr. Truth preserved.[/yellow]")
                break

            # Simple intent detection for tool use
            lower = user_input.lower()
            tool_response = None

            if any(k in lower for k in ["phi", "score", "current value"]):
                tool_response = tool.compute_phi()
            elif "theory" in lower or "explain" in lower:
                tool_response = tool.theory_explain()
            elif "switch" in lower or "regime" in lower:
                tool_response = tool.evaluate_and_switch()
            elif "improve" in lower or "self improve" in lower or "iteration" in lower:
                tool_response = tool.run_self_improving_iteration(user_input)
            elif "deviation" in lower:
                tool_response = tool.detect_deviation() if hasattr(tool, "detect_deviation") else "Deviation detection available in dashboard."

            if tool_response:
                context = json.dumps(tool_response, indent=2) if isinstance(tool_response, dict) else str(tool_response)
                console.print(Panel(context, title="Deterministic Result", border_style="green"))
                # Also ask SLM for natural language version
                natural = call_grounded_slm(user_input, context)
                console.print(Panel(natural, title="Grounded Explanation", border_style="yellow"))
            else:
                # Pure chat - send to SLM with full context
                current_state = tool.theory_explain()[:800]
                reply = call_grounded_slm(user_input, current_state)
                console.print(Panel(reply, title="Bryant Issiah Morris Jr. - Truth Mode", border_style="cyan"))

        except KeyboardInterrupt:
            console.print("\n[yellow]Chat interrupted. Session ended for Bryant Issiah Morris Jr.[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    run_chat()
