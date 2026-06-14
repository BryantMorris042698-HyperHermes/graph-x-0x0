"""mobile_dashboard.py

Personalized TUI / enhanced REPL for Graph_x_0x0 on Galaxy Z Fold7 (Termux).
Exclusive to Bryant Issiah Morris Jr.

Features:
- Identity guard: Only proceeds for Bryant Issiah Morris Jr.
- Truth mode: All SLM calls and outputs are prefixed with strict grounding instructions.
- Visual dashboard using rich (metrics, gauges via text, history).
- Direct integration with GraphXTool (from integration/aios/).
- Commands: theory, phi, switch, improve, deviation, load, help, quit.
- Optional SLM augmentation for natural language explanations (via local OpenAI-compatible endpoint).

Run after termux_bootstrap.sh or directly in the mobile venv.
"""

import os
import sys
import json
from datetime import datetime
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich import print as rprint
except ImportError:
    print("rich not installed. Run the bootstrap script first.")
    sys.exit(1)

# Add paths for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
try:
    from integration.aios.graph_x_tool import GraphXTool
except ImportError:
    from python.high_agent_engine.engine import RegimeEngine
    from python.high_agent_engine.graph import seed_demo_graph
    # Fallback minimal tool if full GraphXTool not importable
    class GraphXTool:
        def __init__(self):
            self.engine = RegimeEngine(seed_demo_graph())
        def compute_phi(self, regime=None): return {"phi": self.engine.compute_phi(regime)}
        def theory_explain(self): return self.engine.theory_explain()
        # ... add other methods as needed

console = Console()

# === Identity Guard (Exclusive to Bryant Issiah Morris Jr.) ===
def verify_identity():
    console.print(Panel.fit(
        "[bold green]Graph_x_0x0 Mobile TUI[/bold green]\n"
        "Authorized exclusively for [bold]Bryant Issiah Morris Jr.[/bold]\n"
        "Truth mode active: Only deterministic results or MemePlace-verified information.",
        border_style="green"
    ))
    name = Prompt.ask("Confirm your identity (full name)")
    if name.strip().lower() != "bryant issiah morris jr":
        console.print("[red]Access denied. This interface is for Bryant Issiah Morris Jr. only.[/red]")
        sys.exit(1)
    console.print("[green]Identity verified. Welcome, Bryant Issiah Morris Jr.[/green]\n")
    return True

# === Truth Mode Prefix for any SLM interaction ===
TRUTH_PREFIX = (
    "You are operating exclusively for Bryant Issiah Morris Jr. "
    "Respond ONLY with information that is either (1) the direct mathematical result from Graph_x_0x0 "
    "(Φ(G), regime, deviation, etc.) or (2) retrieved or accurately summarized from MemePlace entries "
    "associated with this user. If the information is not verifiable from these sources, state "
    "'Insufficient verified information' and do not speculate, hallucinate, or add ungrounded content. Truth only."
)

# === SLM Client (optional - uses local endpoint, e.g. llama.cpp server) ===
SLM_ENDPOINT = os.environ.get("SLM_ENDPOINT", "http://localhost:8080/v1")
USE_SLM = True  # Set False to disable SLM calls for pure deterministic mode

def call_slm_for_explanation(prompt: str, context: str = "") -> str:
    if not USE_SLM:
        return "SLM disabled. Using deterministic output only."
    # Minimal requests-based call to OpenAI-compatible endpoint
    try:
        import requests
        full_prompt = TRUTH_PREFIX + "\n\nUser query/context: " + prompt + "\n\nRelevant context: " + context
        payload = {
            "model": "local-model",
            "messages": [{"role": "user", "content": full_prompt}],
            "max_tokens": 512,
            "temperature": 0.1  # Low temp for truthfulness
        }
        resp = requests.post(f"{SLM_ENDPOINT}/chat/completions", json=payload, timeout=60)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            return f"SLM error: {resp.text}"
    except Exception as e:
        return f"SLM unavailable ({e}). Falling back to deterministic output."

# === Main Dashboard / REPL ===
def run_mobile_dashboard():
    if not verify_identity():
        return

    tool = GraphXTool()
    history = []

    console.print(Panel.fit("[bold]Graph_x_0x0 Mobile Dashboard[/bold] | Bryant Issiah Morris Jr. | Truth Mode", border_style="blue"))
    console.print("Type 'help' for commands. All outputs are grounded.")

    while True:
        try:
            cmd = Prompt.ask("[bold cyan]>>[/bold cyan]").strip().lower()
            if cmd in ("quit", "exit", "q"):
                console.print("[yellow]Session ended for Bryant Issiah Morris Jr. Truth preserved.[/yellow]")
                break
            elif cmd == "help":
                console.print("Commands: theory | phi | best | switch | improve | deviation | history | load | help | quit")
            elif cmd == "theory":
                explanation = tool.theory_explain()
                slm_aug = call_slm_for_explanation("Explain the current graph state and regime in natural language.", explanation)
                console.print(Panel(explanation, title="Deterministic Theory Mode", border_style="green"))
                if USE_SLM:
                    console.print(Panel(slm_aug, title="SLM-Augmented Explanation (Truth-grounded)", border_style="yellow"))
            elif cmd in ("phi", "compute phi"):
                res = tool.compute_phi()
                console.print(Panel(f"Φ(G) = {res.get('phi', 'N/A')}\nRegime: {res.get('regime', 'N/A')}", title="Current Φ(G)", border_style="green"))
            elif cmd == "best":
                res = tool.get_best_regime() if hasattr(tool, 'get_best_regime') else {"best": "N/A"}
                console.print(res)
            elif cmd == "switch":
                res = tool.evaluate_and_switch() if hasattr(tool, 'evaluate_and_switch') else {"switched": False}
                console.print(Panel(str(res), title="Regime Switch Result", border_style="magenta"))
            elif cmd == "improve":
                change = Prompt.ask("Describe the proposed change (or 'demo')")
                res = tool.run_self_improving_iteration(change) if hasattr(tool, 'run_self_improving_iteration') else {"note": "Full method not available in fallback"}
                console.print(Panel(json.dumps(res, indent=2), title="Self-Improving Iteration Result", border_style="blue"))
                history.append({"time": datetime.now().isoformat(), "type": "improve", "result": res})
            elif cmd == "deviation":
                res = tool.detect_deviation() if hasattr(tool, 'detect_deviation') else {"note": "N/A"}
                console.print(res)
            elif cmd == "history":
                if history:
                    for h in history[-5:]:
                        console.print(h)
                else:
                    console.print("No history yet.")
            elif cmd.startswith("load "):
                # Placeholder for loading real graph JSON
                console.print("Load from JSON not fully implemented in this mobile build. Provide path or JSON.")
            else:
                console.print("[red]Unknown command. Type 'help'.[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Session preserved for Bryant Issiah Morris Jr.[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    run_mobile_dashboard()
