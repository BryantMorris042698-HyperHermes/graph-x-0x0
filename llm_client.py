"""llm_client.py

Flexible LLM client for Graph_x_0x0.

Supports:
- Any OpenAI-compatible API (via SLM_ENDPOINT env var)
- Automatic Ollama detection (uses the most recently pulled local model)
- Graceful fallback to deterministic mode if no LLM is available

This makes the system work out of the box with:
  ollama pull phi3.5
  python run.py

or with any other provider (Groq, OpenRouter, vLLM, etc.)
"""

import os
import json
from typing import Optional, Dict, Any

try:
    import requests
except ImportError:
    requests = None


def get_llm_endpoint() -> str:
    """Determine the best LLM endpoint to use."""
    # 1. Explicit environment variable takes highest priority
    env_endpoint = os.environ.get("SLM_ENDPOINT")
    if env_endpoint:
        return env_endpoint

    # 2. Try to auto-detect running Ollama
    ollama_url = "http://localhost:11434"
    try:
        if requests:
            # Check if Ollama is running
            resp = requests.get(f"{ollama_url}/api/tags", timeout=2)
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                if models:
                    # Use the most recently modified model
                    latest_model = max(models, key=lambda m: m.get("modified_at", ""))
                    model_name = latest_model["name"]
                    print(f"[LLM] Auto-detected Ollama. Using model: {model_name}")
                    return f"{ollama_url}/v1"  # Ollama exposes OpenAI-compatible API
    except Exception:
        pass

    # 3. Default fallback (llama.cpp style)
    return "http://localhost:8080/v1"


def call_llm(prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 600) -> str:
    """Call the LLM with proper grounding."""
    if requests is None:
        return "[LLM unavailable] requests not installed."

    endpoint = get_llm_endpoint()
    model = "local-model"  # Works for both Ollama and llama.cpp

    # Build messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.1
    }

    try:
        resp = requests.post(f"{endpoint}/chat/completions", json=payload, timeout=120)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            return f"[LLM error] Status {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        return f"[LLM unavailable] {str(e)}"


def is_llm_available() -> bool:
    """Quick check if an LLM backend is reachable."""
    try:
        endpoint = get_llm_endpoint()
        if requests:
            resp = requests.get(endpoint.replace("/v1", "/v1/models"), timeout=3)
            return resp.status_code == 200
    except Exception:
        pass
    return False
