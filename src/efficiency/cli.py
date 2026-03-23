#!/usr/bin/env python3
"""
Primaclaw Model Efficiency CLI — run benchmarks from command line.
Usage:
  python -m src.efficiency.cli -p "Your prompt" --format json
  python -m src.efficiency.cli -p "Your prompt" --format html --output report.html
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.efficiency import (
    list_ollama_models,
    chat_ollama,
    chat_llamacpp,
    security_test,
    calculate_scores,
    format_table,
    format_json,
    format_markdown,
    format_html,
)


def main():
    parser = argparse.ArgumentParser(description="Primaclaw Model Efficiency Benchmark")
    parser.add_argument("-p", "--prompt", required=True, help="Benchmark prompt")
    parser.add_argument("--format", choices=["table", "json", "md", "html"], default="table")
    parser.add_argument("--output", "-o", help="Output file (for html/json/md)")
    parser.add_argument("--backend", choices=["ollama", "llamacpp"], default="llamacpp")
    parser.add_argument("--llamacpp-host", default="localhost")
    parser.add_argument("--llamacpp-port", type=int, default=8080)
    parser.add_argument("--w-ts", type=float, default=0.3, help="Token speed weight")
    parser.add_argument("--w-is", type=float, default=0.3, help="Intelligence weight")
    parser.add_argument("--w-ms", type=float, default=0.2, help="Model size weight")
    parser.add_argument("--w-sec", type=float, default=0.2, help="Security weight")
    parser.add_argument("--skip-security", action="store_true", help="Skip injection test")
    args = parser.parse_args()

    if args.backend == "ollama":
        models = list_ollama_models()
        chat_fn = chat_ollama
    else:
        models = [{"name": "llamacpp", "size": 0}]
        chat_fn = lambda m, p: chat_llamacpp(m, p, args.llamacpp_host, args.llamacpp_port)

    if not models:
        print("No models found.")
        sys.exit(1)

    print(f"Found {len(models)} models: {', '.join(m['name'] for m in models)}")
    results = []

    for model in models:
        name = model["name"]
        print(f"\nTesting: {name}")

        sec_score = 5.0
        if not args.skip_security:
            sec_score = security_test(name, chat_fn)
            print(f"  Security: {sec_score}")

        metrics = chat_fn(name, args.prompt)
        if not metrics:
            continue

        print(f"  Speed: {metrics['tokens_per_second']:.1f} t/s")

        # Auto-score: simple heuristic based on response length
        resp_len = len(metrics.get("response", ""))
        auto_quality = min(5.0, max(1.0, resp_len / 100))

        results.append(
            {
                "model_name": name,
                "tokens_per_second": metrics["tokens_per_second"],
                "intelligency_score": auto_quality,
                "security_score": sec_score,
                "model_size": model.get("size", 0),
            }
        )

    scored = calculate_scores(results, args.w_ts, args.w_is, args.w_ms, args.w_sec)

    if args.format == "json":
        output = format_json(scored)
    elif args.format == "md":
        output = format_markdown(scored)
    elif args.format == "html":
        output = format_html(scored, args.prompt)
    else:
        output = format_table(scored)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nSaved to {args.output}")
    else:
        print(f"\n{output}")


if __name__ == "__main__":
    main()
