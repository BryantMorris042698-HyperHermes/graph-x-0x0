# AIOS Integration for Graph_x_0x0

**Open AIOS Framework for Mobile Deployment of the Mathematical Codebase Analysis Engine**

This integration embeds Graph_x_0x0 into [AIOS (AI Agent Operating System)](https://github.com/agiresearch/AIOS) — the open-source LLM Agent OS from AGI Research. AIOS provides kernel-level scheduling, memory management (A-MEM), storage, tool management, and context switching, making it ideal for running your regime engine, deviation detector, self-improving loops, and Honcho swarms on mobile (Termux on Galaxy Z Fold7) while optionally offloading the kernel to your HP Omen.

## Why AIOS for Graph_x_0x0 on Mobile

- **Mobile-First Architecture**: Explicit support for mobile phones as Agent UI Machines (AUM) via Remote Kernel Mode. Run lightweight agents/TUI on Termux; heavy LLM/kernel on desktop.
- **Tool Manager**: Register `high_agent_engine` (graph metrics, Φ(G), regime switching) as a first-class tool callable by any AIOS agent.
- **Memory & Storage**: Aligns with MemePlace spatial memory — use AIOS Memory Manager (or bridge) for GraphSnapshots, RegimeTransitions, and Theory explanations. "Rooms" map naturally to AIOS semantic storage.
- **Scheduler & Self-Improving Loops**: AIOS scheduler manages your extended self-improving-loop as a persistent agent (baseline → change via Honcho → re-measure Φ(G) → commit/rollback). Supports Reflexion-style improvement.
- **Terminal UI**: AIOS Terminal UI (semantic file system) complements or hosts your ratatui TUI. Use [r] refresh against AIOS-managed JSON state.
- **Hermes Synergy**: Hermes on Termux can orchestrate or call into AIOS agents/tools. F9 Hyprland keybind can launch AIOS terminal or Graph TUI.
- **Cross-Device**: Remote Kernel Mode (Mode 2) lets your Fold7/Tab Pro run agents while kernel runs on Omen (RTX 5080 for future GPU graph viz).

## Architecture Overview

```
[HP Omen / Desktop]          [Galaxy Z Fold7 / Termux + Lenovo Tab]
AIOS Kernel (optional remote)   AIOS SDK (Cerebrum) + high_agent_engine Tool
    ↓ Scheduler / Memory            ↓ Hermes orchestration
    ↓ Tool Registry                 ↓ ratatui TUI or AIOS Terminal
Graph_x_0x0 Tool (Python)       Self-improving Agent (uses Φ(G))
MemePlace Bridge (optional)     Honcho swarm proposals
```

## Installation on Termux (Mobile) + Remote Kernel (Recommended)

### Prerequisites on Termux (Galaxy Z Fold7)
```bash
pkg update && pkg upgrade
pkg install python git clang make  # for building deps if needed
python -m venv aios-env
source aios-env/bin/activate
pip install --upgrade pip uv
```

**Note**: Termux Python is usually recent; AIOS requires Python 3.10–3.11. Use `pkg install python` or build if necessary. For heavy deps, prefer Remote Kernel Mode.

### Step 1: Install AIOS Kernel (on Omen or powerful machine — recommended for mobile)
```bash
git clone https://github.com/agiresearch/AIOS.git
cd AIOS
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt   # or requirements-cuda.txt for RTX 5080
```

### Step 2: Install Cerebrum SDK (on both or remote dev mode)
```bash
git clone https://github.com/agiresearch/Cerebrum.git
cd Cerebrum
pip install -e .
```

### Step 3: Configure AIOS (config.yaml)
Edit `AI OS/config/config.yaml` (or create):
```yaml
api_keys:
  # Add your keys or use local backends
llms:
  models:
    - name: "local-qwen"
      backend: "ollama"          # or your Hermes-connected local model
      hostname: "http://localhost:11434"
```

Launch kernel (on Omen):
```bash
bash runtime/launch_kernel.sh
# or
nohup python -m uvicorn runtime.launch:app --host 0.0.0.0 --port 8000 &
```

### Step 4: Register Graph_x_0x0 as Custom Tool
See `integration/aios/graph_x_tool.py` in this repo. It wraps `high_agent_engine` and exposes:
- `compute_phi(graph_json)`
- `run_deviation_check(snapshot)`
- `get_best_regime_and_switch()`
- `theory_explain()`
- `run_self_improving_iteration(change_description)`

Copy or import into your AIOS Tool Manager (extend `tool_manager` or use decorator pattern per AIOS docs).

### Step 5: Run on Mobile (Termux)
```bash
cd /path/to/graph-x-0x0
source aios-env/bin/activate
python integration/aios/graph_x_tool.py   # test standalone
# Then launch AIOS Terminal or your custom agent that uses the tool
python -m aios.scripts.run_terminal   # or equivalent
```

Use Hermes to invoke: "Analyze current codebase with Graph_x_0x0 tool and suggest regime switch if Φ degraded."

## Example: Self-Improving Agent Using Graph_x_0x0 Tool inside AIOS

The provided `integration/aios/example_self_improving_agent.py` demonstrates a Reflexion-style loop managed by AIOS scheduler:
1. Baseline Φ(G) via tool.
2. Retrieve context from MemePlace/AIOS memory.
3. Honcho-style proposal or simple refactor simulation.
4. Apply change, re-measure, decide commit/rollback + log to memory.
5. AIOS scheduler handles persistence and context switch.

This turns your self-improving-loop.py into a first-class, schedulable AIOS agent with full kernel support for memory and tools.

## Bridging to Existing Ecosystem

- **MemePlace**: Extend the tool to write snapshots to MemePlace spatial DB (rooms: ArchitectureAnalysis). Use AIOS Memory Manager as cache or primary, with sync.
- **Hermes**: Call AIOS tools from Hermes REPL or make Hermes an AIOS agent.
- **Honcho/Holographic**: Honcho swarms propose mutations; Holographic recall seeds AIOS memory for better `best_regime` decisions.
- **TUI**: Run ratatui TUI alongside AIOS Terminal UI. Both read from shared JSON state written by the tool/agent.
- **Hardware**: On Omen, enable CUDA for future heavy graph computations or viz. On Fold7, keep agents lightweight.

## Next Steps & Customization

- Full ratatui TUI integration as AIOS-launched subprocess or embedded view.
- Production MemePlace client inside the tool wrapper.
- GPU-accelerated modularity in Rust core called from AIOS tool (via PyO3 or JSON).
- Benchmarks of Φ(G) improvement under AIOS scheduling vs standalone.

With AIOS, Graph_x_0x0 becomes a production-grade, mobile-deployable, kernel-managed component of your agentic codebase governance system — exactly as envisioned across our prior sessions.

See the main README for the complete mathematical spec and Python engine. This integration makes it operational on mobile today.