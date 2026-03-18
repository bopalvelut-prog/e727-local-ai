import argparse
import time
import httpx
import sys
from src.config import settings

def get_recommendation(tokens_per_sec):
    """Suggests higher or lower quantization based on speed threshold."""
    if tokens_per_sec < 5:
        return "Slow (<5t/s). Try lower quantization (e.g., q3_K or q2_K)"
    else:
        return "Fast (>=5t/s). Try higher quantization (e.g., q6_K or q8_0) for better quality"

def benchmark_swarm(prompt: str):
    """Benchmarks the current Primaclaw swarm via the Coordinator."""
    url = f"http://localhost:{settings.COORDINATOR_PORT}/v1/chat/completions"
    
    payload = {
        "model": "primaclaw-swarm",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    print(f"\n🚀 Benchmarking Primaclaw Swarm at {url}...")
    print(f"📝 Prompt: {prompt}")

    start_time = time.time()
    try:
        with httpx.Client(timeout=None) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception as e:
        print(f"❌ Error connecting to Coordinator: {e}")
        print("Make sure the Coordinator is running (python -m src.coordinator)")
        return

    end_time = time.time()
    total_duration = end_time - start_time
    
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    
    # Estimate tokens (approx 4 chars per token)
    token_count = len(content) / 4
    tokens_per_sec = token_count / total_duration if total_duration > 0 else 0

    print(f"\n--- Swarm Response ---\n{content}\n")
    print(f"⏱️  Total Duration: {total_duration:.2f}s")
    print(f"📊 Estimated Speed: {tokens_per_sec:.2f} tokens/sec")

    # Intelligency score (ported from model-efficiency)
    while True:
        try:
            score = input("\n⭐ Rate intelligency/quality (1-5, or skip with Enter): ")
            if not score:
                score = "N/A"
                break
            score = float(score)
            if 1 <= score <= 5:
                break
            print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    recommendation = get_recommendation(tokens_per_sec)

    print("\n--- Efficiency Report ---")
    print(f"{'Target':<20} {'Tokens/Sec':<12} {'Quality':<8} {'Status':<10}")
    print("-" * 50)
    print(f"{'Primaclaw Swarm':<20} {tokens_per_sec:<12.2f} {score:<8} {'PASS':<10}")
    print(f"\n💡 Recommendation: {recommendation}")
    print("\n✅ Benchmark complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Primaclaw Swarm Efficiency Benchmark")
    parser.add_argument("-p", "--prompt", default="Explain quantum computing in 2 sentences.", help="Prompt to test")
    args = parser.parse_args()
    
    benchmark_swarm(args.prompt)
