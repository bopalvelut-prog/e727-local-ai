#!/usr/bin/env python3
"""
Krav Maga Self-Defense Tutor -- CLI interface.
Uses prima.cpp (llama-server) as default backend.

Usage:
  python -m src.tutor.cli                          # Interactive mode
  python -m src.tutor.cli -q "How do I escape a choke?"  # Single question
  python -m src.tutor.cli --level yellow           # Show training plan
  python -m src.tutor.cli --plan                   # Full training program
  python -m src.tutor.cli --backend primaclaw      # Via Primaclaw coordinator
"""

import sys
import os
import io

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import argparse

from src.tutor import SYSTEM_PROMPT, get_training_plan, TRAINING_LEVELS


def chat_primacpp(prompt, host="localhost", port=8080, n_predict=256):
    """Send prompt to prima.cpp (llama-server) directly."""
    import httpx
    try:
        full_prompt = f"<|system|>\n{SYSTEM_PROMPT}\n<|user|>\n{prompt}\n<|assistant|>"
        url = f"http://{host}:{port}/completion"
        resp = httpx.post(url, json={
            "prompt": full_prompt,
            "n_predict": n_predict,
            "temperature": 0.7,
            "stop": ["<|user|>", "<|system|>"],
        }, timeout=300)
        resp.raise_for_status()
        return resp.json().get("content", "").strip()
    except Exception as e:
        return f"Error: {e}\nMake sure prima.cpp is running:\n  llama-server.exe -m <model.gguf> --host 0.0.0.0 --port {port}"


def chat_primaclaw(prompt, coordinator_host="localhost", coordinator_port=10000):
    """Send prompt to Primaclaw coordinator (OpenAI-compatible proxy)."""
    import httpx
    try:
        url = f"http://{coordinator_host}:{coordinator_port}/v1/chat/completions"
        resp = httpx.post(url, json={
            "model": "primaclaw-swarm",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "temperature": 0.7,
        }, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}\nMake sure Primaclaw coordinator is running: python -m src.coordinator"


def interactive_mode(backend, host, port, n_predict):
    """Interactive chat loop."""
    print("\n=== Krav Maga Self-Defense Tutor ===")
    if backend == "primacpp":
        print(f"Backend: prima.cpp (llama-server at {host}:{port})")
    elif backend == "primaclaw":
        print(f"Backend: Primaclaw coordinator ({host}:{port})")
    print("Commands: 'quit' to exit, 'plan' for training plan, 'level <name>' for level")
    print("Examples: 'How do I escape a front choke?' / 'What are pre-attack indicators?'")
    print()

    if backend == "primacpp":
        chat_fn = lambda p: chat_primacpp(p, host, port, n_predict)
    elif backend == "primaclaw":
        chat_fn = lambda p: chat_primaclaw(p, host, port)
    else:
        chat_fn = lambda p: chat_primacpp(p, host, port, n_predict)

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nStay safe. De-escalate first.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Stay safe. De-escalate first.")
            break
        if user_input.lower() == "plan":
            print_training_plan()
            continue
        if user_input.lower().startswith("level "):
            level_name = user_input.lower().split(" ", 1)[1]
            print_level_detail(level_name)
            continue

        print("\nInstructor:", end=" ")
        response = chat_fn(user_input)
        print(response)
        print()


def print_training_plan():
    """Print full training program overview."""
    print("\n" + "=" * 60)
    print("KRAV MAGA TRAINING PROGRAM")
    print("=" * 60)
    for key, level in TRAINING_LEVELS.items():
        print(f"\n[{key.upper()}] {level['name']}")
        print(f"  Focus: {level['focus']}")
        print(f"  Exercises:")
        for ex in level['exercises']:
            print(f"    - {ex}")
    print()


def print_level_detail(level_name):
    """Print detailed info for a training level."""
    level = get_training_plan(level_name)
    print(f"\n{'=' * 60}")
    print(f"  {level['name']}")
    print(f"{'=' * 60}")
    print(f"  Focus: {level['focus']}")
    print(f"\n  Training Exercises:")
    for i, ex in enumerate(level['exercises'], 1):
        print(f"    {i}. {ex}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Krav Maga Self-Defense Tutor")
    parser.add_argument("-q", "--question", help="Ask a single question")
    parser.add_argument("--backend", choices=["primacpp", "primaclaw"], default="primacpp",
                        help="Inference backend: primacpp (llama-server) or primaclaw (coordinator)")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=8080,
                        help="Server port (8080 for prima.cpp, 10000 for coordinator)")
    parser.add_argument("--n-predict", type=int, default=256,
                        help="Max tokens to generate (prima.cpp only)")
    parser.add_argument("--level", help="Show training plan for level (white/yellow/orange/green/blue)")
    parser.add_argument("--plan", action="store_true", help="Show full training program")
    args = parser.parse_args()

    if args.plan:
        print_training_plan()
        return

    if args.level:
        print_level_detail(args.level)
        return

    if args.question:
        if args.backend == "primaclaw":
            print(chat_primaclaw(args.question, args.host, args.port))
        else:
            print(chat_primacpp(args.question, args.host, args.port, args.n_predict))
        return

    interactive_mode(args.backend, args.host, args.port, args.n_predict)


if __name__ == "__main__":
    main()
