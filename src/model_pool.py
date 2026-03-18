#!/usr/bin/env python3
"""
Primaclaw Model Pool
Automatically selects model based on performance:
- Speed < 1 tok/s: Use smaller model
- Speed > 10 tok/s: Try larger model
"""

import requests
import time
import subprocess
import os

MODELS = {
    "tiny": {"port": None, "model": None, "path": None, "size_gb": 0, "min_speed": 0},
    "small": {"port": None, "model": None, "path": None, "size_gb": 0, "min_speed": 1},
    "medium": {"port": None, "model": None, "path": None, "size_gb": 0, "min_speed": 5},
    "large": {"port": None, "model": None, "size_gb": 0, "min_speed": 10},
}

AUTO_START = {
    "tiny": {"path": "/home/ma/prima.cpp/models/Qwen2.5-1.5B-Instruct-Q4_K_M.gguf", "port": 8085},
    "small": {"path": "/home/ma/prima.cpp/models/qwen2.5-coder-3b-instruct-q4_0.gguf", "port": 8083},
    "deepseek": {"path": "/home/ma/Lataukset/deepseek-coder-1.3b-q2_k.gguf", "port": 8089},
}


def find_available_models():
    """Scan for running model servers."""
    found = {}
    ports = [8085, 8083, 8088, 8089]
    
    for port in ports:
        try:
            resp = requests.get(f"http://localhost:{port}/v1/models", timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                model_id = data["data"][0]["id"]
                path = model_id
                name = os.path.basename(path).lower()
                
                if "1.5b" in name or "q2_k" in name:
                    tier = "tiny"
                elif "3b" in name or "1.3b" in name:
                    tier = "small"
                elif "7b" in name:
                    tier = "medium"
                elif "14b" in name:
                    tier = "large"
                else:
                    tier = "small"
                
                found[tier] = {"port": port, "path": path}
        except:
            pass
    
    return found


def start_model(tier, port):
    """Start a model server."""
    if tier not in AUTO_START:
        return False
    
    info = AUTO_START[tier]
    if not os.path.exists(info["path"]):
        print(f"Model not found: {info['path']}")
        return False
    
    # Kill existing on port
    subprocess.run(f"pkill -f 'llama-server.*{info['port']}'", shell=True)
    time.sleep(1)
    
    # Start new
    subprocess.Popen(
        ["/home/ma/prima.cpp/llama-server", "-m", info["path"], "--port", str(info["port"])],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Wait for ready
    for _ in range(60):
        time.sleep(1)
        try:
            resp = requests.get(f"http://localhost:{info['port']}/v1/models", timeout=2)
            if resp.status_code == 200:
                print(f"Started {tier} model on port {info['port']}")
                return True
        except:
            pass
    
    return False


def measure_speed(port, prompt="Hello", max_tokens=20):
    """Measure tokens per second."""
    try:
        start = time.time()
        resp = requests.post(
            f"http://localhost:{port}/v1/chat/completions",
            json={"messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens},
            timeout=120
        )
        elapsed = time.time() - start
        
        if resp.status_code == 200:
            data = resp.json()
            tokens = data.get("usage", {}).get("completion_tokens", max_tokens)
            return tokens / elapsed if elapsed > 0 else 0
    except:
        pass
    return 0


def auto_select_model():
    """Automatically select best model based on speed."""
    available = find_available_models()
    
    if not available:
        print("No models running. Starting tiny model...")
        start_model("tiny", 8085)
        return
    
    # Measure speeds
    speeds = {}
    for tier, info in available.items():
        speed = measure_speed(info["port"])
        speeds[tier] = speed
        print(f"  {tier}: {speed:.2f} tok/s")
    
    # Determine action
    avg_speed = sum(speeds.values()) / len(speeds) if speeds else 0
    print(f"\nAverage speed: {avg_speed:.2f} tok/s")
    
    if avg_speed < 1:
        # Switch to smaller model
        print("Speed too slow! Switching to smaller model...")
        if "small" in available and "tiny" not in available:
            start_model("tiny", 8085)
        elif "medium" in available:
            start_model("small", 8083)
    elif avg_speed > 10:
        # Try larger model
        print("Speed good! Trying larger model...")
        if "tiny" in available:
            start_model("small", 8083)
        elif "small" in available:
            start_model("medium", 8087)
    
    return speeds


def send_to_pool(prompt, max_tokens=100):
    """Send prompt to best available model."""
    available = find_available_models()
    
    if not available:
        print("No models available!")
        return None
    
    # Try tiers in order: small > tiny > medium > large
    for tier in ["small", "tiny", "medium", "deepseek", "large"]:
        if tier in available:
            try:
                resp = requests.post(
                    f"http://localhost:{available[tier]['port']}/v1/chat/completions",
                    json={"messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens},
                    timeout=120
                )
                if resp.status_code == 200:
                    return resp.json()
            except:
                pass
    
    return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Primaclaw Model Pool")
    parser.add_argument("--list", action="store_true", help="List available models")
    parser.add_argument("--speed", action="store_true", help="Measure speed of all models")
    parser.add_argument("--auto", action="store_true", help="Auto-select model based on speed")
    parser.add_argument("--test", help="Send test prompt")
    args = parser.parse_args()
    
    if args.list:
        available = find_available_models()
        print("\nAvailable Models:")
        for tier, info in available.items():
            speed = measure_speed(info["port"])
            print(f"  [{tier}] Port {info['port']} - {speed:.2f} tok/s")
        return
    
    if args.speed:
        auto_select_model()
        return
    
    if args.auto:
        auto_select_model()
        return
    
    if args.test:
        result = send_to_pool(args.test)
        if result:
            print(result["choices"][0]["message"]["content"])
        return
    
    print("Primaclaw Model Pool\n")
    print("Usage:")
    print("  --list   List available models")
    print("  --speed  Measure speed of all models")
    print("  --auto   Auto-select model based on speed")
    print("  --test 'prompt'  Send test prompt")


if __name__ == "__main__":
    main()
