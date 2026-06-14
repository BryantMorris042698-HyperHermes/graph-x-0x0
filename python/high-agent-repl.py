"""high-agent-repl.py - Interactive REPL / daemon stub for Graph_x_0x0.

Commands: theory, sweep, history, watch, switch, quit.
Use in Termux with Hermes or as background daemon writing JSON state.
"""

from high_agent_engine.engine import RegimeEngine
from high_agent_engine.graph import seed_demo_graph


def repl():
    g = seed_demo_graph()
    engine = RegimeEngine(g)
    print("Graph_x_0x0 REPL ready. Type 'help' for commands.")
    while True:
        try:
            cmd = input(">> ").strip().lower()
            if cmd in ("quit", "exit", "q"):
                break
            elif cmd == "help":
                print("Commands: theory | sweep | history | watch | switch <regime> | quit")
            elif cmd == "theory":
                print(engine.theory_explain())
            elif cmd == "sweep":
                best, phi = engine.best_regime()
                print(f"Best regime: {best} with Φ={phi:.4f}")
            elif cmd == "history":
                print("Transitions:", [t.to_regime for t in engine.transitions])
            elif cmd.startswith("switch "):
                _, r = cmd.split(None, 1)
                if r.title() in engine.REGIME_COEFFS:
                    engine.current_regime = r.title()
                    print("Switched to", r)
                else:
                    print("Unknown regime")
            elif cmd == "watch":
                print("Watching... (daemon mode stub - would poll for changes)")
            else:
                print("Unknown command. Type help.")
        except (EOFError, KeyboardInterrupt):
            break
    print("REPL exited.")

if __name__ == "__main__":
    repl()
