# Cross-Device AIOS Agent Chat + TUI Setup (Phone / Tablet / Laptop)

**Complete unified setup for Bryant Issiah Morris Jr.**

This document + `run.py` provides the single entry point for your entire agentic ecosystem across all your devices.

## Features
- Auto device detection (phone via Termux, tablet, laptop)
- Identity verification exclusive to Bryant Issiah Morris Jr.
- Strict Truth mode (Graph_x_0x0 math + MemePlace grounding)
- Chat interface (natural language) and Dashboard TUI
- AIOS integration ready
- Optimized per device (light on phone, full features on laptop)
- Persistent state via JSON + MemePlace sync

## One-Time Setup (All Devices)

### 1. Common Steps
```bash
git clone https://github.com/BryantMorris042698-HyperHermes/graph-x-0x0.git
cd graph-x-0x0
python -m venv .venv
source .venv/bin/activate
pip install rich prompt_toolkit requests
```

### 2. Phone (Galaxy Z Fold7 - Termux)
Follow the detailed steps in `mobile/termux/README.md` or run:
```bash
bash mobile/termux/termux_bootstrap.sh
```

### 3. Tablet (Lenovo Tab Pro) & Laptop (HP Omen / Arch)
Use the same venv and run:
```bash
python run.py
```
The launcher will auto-detect and choose the best interface.

## Daily Usage

```bash
source .venv/bin/activate
python run.py                 # Smart auto mode
python run.py --chat          # Natural language chat
python run.py --dashboard     # Visual TUI
python run.py --aios          # AIOS kernel mode
```

## Device-Specific Optimizations
- **Phone (Termux)**: Lightweight chat first, minimal dependencies, uses existing Hermes SLM.
- **Tablet**: Balanced dashboard with touch-friendly output.
- **Laptop**: Full ratatui TUI + GPU acceleration possible for heavy graph analysis.

## Missing Pieces Now Addressed
- Unified launcher with device detection
- Cross-device state sharing (JSON files in `state/`)
- Hermes integration hooks
- MemePlace sync points in tools
- Identity + Truth enforcement everywhere
- Single `run.py` entry point

Run `python run.py` on any device after initial setup to start your personal AI Agent OS.
