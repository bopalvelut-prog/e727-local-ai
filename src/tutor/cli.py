#!/usr/bin/env python3
"""
Krav Maga Self-Defense Tutor — CLI interface.
Uses Primaclaw swarm or local Ollama as backend.

Usage:
  python -m src.tutor.cli                          # Interactive mode
  python -m src.tutor.cli -q "How do I escape a choke?"  # Single question
  python -m src.tutor.cli --level yellow           # Show training plan
  python -m src.tutor.cli --plan                   # Full training program
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.tutor import SYSTEM_PROMPT, get_training_plan, TRAINING_LEVELS


def chat_primaclaw(prompt, coordinator_host="localhost", coordinator_port=10000):
    """Send prompt to Primaclaw swarm."""
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


def chat_ollama(prompt, model="qwen2.5:0.5b"):
    """Send prompt to local Ollama."""
    import httpx
    try:
        url = "http://localhost:11434/api/chat"
        resp = httpx.post(url, json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "temperature": 0.7,
        }, timeout=120)
        resp.raise_for_status()
        return resp.json()["message"]["content"]
    except Exception as e:
        return f"Error: {e}\nMake sure Ollama is running: ollama serve"


def interactive_mode(backend, host, port, model):
    """Interactive chat loop."""
    print("\n=== Krav Maga Self-Defense Tutor ===")
    print("Backend:", "Primaclaw" if backend == "primaclaw" else f"Ollama ({model})")
    print("Type 'quit' to exit, 'plan' for training plan, 'level <name>' for level details")
    print("Examples: 'How do I escape a front choke?' / 'What are pre-attack indicators?'")
    print()

    if backend == "primaclaw":
        chat_fn = lambda p: chat_primaclaw(p, host, port)
    else:
        chat_fn = lambda p: chat_ollama(p, model)

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
            print(f"    • {ex}")
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
    parser.add_argument("--backend", choices=["primaclaw", "ollama"], default="ollama",
                        help="Inference backend (default: ollama)")
    parser.add_argument("--host", default="localhost", help="Primaclaw coordinator host")
    parser.add_argument("--port", type=int, default=10000, help="Primaclaw coordinator port")
    parser.add_argument("--model", default="qwen2.5:0.5b", help="Ollama model name")
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
            print(chat_ollama(args.question, args.model))
        return

    interactive_mode(args.backend, args.host, args.port, args.model)


if __name__ == "__main__":
    main()
