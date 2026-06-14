# Termux / Galaxy Z Fold7 On-Device Deployment

**Fully phone-native execution of Graph_x_0x0 + AIOS integration for Bryant Issiah Morris Jr.**

This enables running the complete mathematical codebase analysis engine, regime optimizer, self-improving agent, and TUI **directly on the Galaxy Z Fold7** via Termux, using a local SLM/LLM. The TUI and agent are personalized exclusively for Bryant Issiah Morris Jr. and operate in strict "Truth mode" — all responses and decisions are grounded in deterministic computation (Φ(G), regimes) or verifiable retrieval from MemePlace. No speculation.

## Hardware & Environment Notes for Fold7
- Samsung Galaxy Z Fold7 (SM-F966) with Termux.
- Sufficient RAM for quantized SLM (recommend 4-bit GGUF models ≤ 3B parameters for responsive interaction; larger if using NPU acceleration).
- Existing Hermes agent setup provides the local LLM interface.
- Fingerprint auth and secure workflow already in use.

## Recommended SLM/LLM Stack for Fold7
- **Primary**: llama.cpp server (easiest in Termux) exposing OpenAI-compatible API on localhost:8080.
  - Models: Qwen2.5-1.5B-Instruct or 3B (4-bit), Phi-3.5-mini-4k (quantized), or your current Hermes model.
  - Command example: `./llama-server -m model.gguf -c 4096 --port 8080`
- **Alternative**: Ollama (community Termux builds) or direct integration with existing Hermes LLM backend.
- The deterministic Graph_x_0x0 core (metrics, Φ(G), deviation detection) requires **no LLM** — it runs pure Python. The SLM is used only for:
  - Natural language Theory Mode explanations (grounded by MemePlace retrieval).
  - Interpreting user commands in the TUI.
  - Generating Honcho-style improvement proposals (then validated by Φ(G) math).

## TUI Personalization & Truth Mode (Exclusive to Bryant Issiah Morris Jr.)
- All sessions begin with identity confirmation: "This interface is authorized exclusively for Bryant Issiah Morris Jr."
- Every prompt to the SLM is prefixed with: "You are operating exclusively for Bryant Issiah Morris Jr. Respond only with information that is either (1) the direct mathematical result from Graph_x_0x0 or (2) retrieved verbatim or summarized from MemePlace entries for this user. If uncertain, state 'Insufficient verified information' and do not speculate. Truth only."
- The TUI/REPL will not proceed without successful identity acknowledgment.
- MemePlace is the source of truth for user-specific knowledge (projects, preferences, architecture history).

## Quick Start on Termux

1. Ensure Termux has Python, git, clang, make, and storage access.
2. Clone or pull this repository into Termux.
3. Run the bootstrap script (see below).
4. Configure your local SLM server endpoint (default localhost:8080).
5. Launch the personalized dashboard/REPL.

The bootstrap sets up a dedicated venv, installs the Python engine + rich (for visual dashboard), and starts the identity-guarded interface.

## Files in This Directory
- `termux_bootstrap.sh` — One-command setup and launcher for Bryant Issiah Morris Jr.
- `mobile_dashboard.py` — Enhanced Python TUI/REPL with rich visuals, GraphXTool integration, identity guard, truth-mode prompts, and commands for Φ(G), regimes, theory, and self-improvement.

This setup allows you to start your personal agentic OS layer directly on the phone, with Graph_x_0x0 as the measurable architecture core.