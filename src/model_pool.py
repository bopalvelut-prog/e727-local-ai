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

LLAMA_SERVER = "/home/ma/prima.cpp/llama-server"

MODELS = {
    "qwen-1.5b": {
        "path": "/home/ma/prima.cpp/models/Qwen2.5-1.5B-Instruct-Q4_K_M.gguf",
        "port": 8085,
        "speed_expected": 1.7,
        "type": "chat"
    },
    "qwen-coder-3b": {
        "path": "/home/ma/prima.cpp/models/qwen2.5-coder-3b-instruct-q4_0.gguf",
        "port": 8083,
        "speed_expected": 0.5,
        "type": "code"
    },
    "deepseek-coder-1.3b": {
        "path": "/home/ma/Lataukset/deepseek-coder-1.3b-q2_k.gguf",
        "port": 8089,
        "speed_expected": 0.8,
        "type": "code"
    },
}


def find_available_models():
    """Scan for running model servers."""
    found = []
    for name, info in MODELS.items():
        try:
            resp = requests.get(f"http://localhost:{info['port']}/v1/models", timeout=2)
            if resp.status_code == 200:
                speed = measure_speed(info['port'])
                found.append({
                    "name": name,
                    "port": info['port'],
                    "path": info['path'],
                    "speed": speed,
                    "expected": info['speed_expected']
                })
        except:
            pass
    return found


def start_model(name):
    """Start a model server."""
    info = MODELS.get(name)
    if not info:
        return False
    
    if not os.path.exists(info["path"]):
        print(f"Model not found: {info['path']}")
        return False
    
    # Kill existing on port
    subprocess.run(f"pkill -f 'llama-server.*{info['port']}'", shell=True)
    time.sleep(1)
    
    # Start new
    subprocess.Popen(
        [LLAMA_SERVER, "-m", info["path"], "--port", str(info["port"])],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    print(f"Starting {name} on port {info['port']}...")
    
    # Wait for ready
    for _ in range(60):
        time.sleep(1)
        try:
            resp = requests.get(f"http://localhost:{info['port']}/v1/models", timeout=2)
            if resp.status_code == 200:
                print(f"Ready! {name} on port {info['port']}")
                return True
        except:
            pass
    
    print(f"Failed to start {name}")
    return False


def measure_speed(port, max_tokens=20):
    """Measure tokens per second."""
    try:
        start = time.time()
        resp = requests.post(
            f"http://localhost:{port}/v1/chat/completions",
            json={"messages": [{"role": "user", "content": "Hi"}], "max_tokens": max_tokens},
            timeout=60
        )
        elapsed = time.time() - start
        
        if resp.status_code == 200:
            data = resp.json()
            tokens = data.get("usage", {}).get("completion_tokens", max_tokens)
            return tokens / elapsed if elapsed > 0 else 0
    except:
        pass
    return 0


def auto_select():
    """Automatically select best model based on speed."""
    available = find_available_models()
    
    if not available:
        print("No models running. Starting Qwen 1.5B...")
        start_model("qwen-1.5b")
        return
    
    # Sort by expected speed
    available.sort(key=lambda x: x['expected'], reverse=True)
    
    print("\nAvailable Models:")
    for m in available:
        ratio = m['speed'] / m['expected'] if m['expected'] > 0 else 0
        status = "OK" if ratio > 0.5 else "SLOW" if ratio > 0.2 else "TOO SLOW"
        print(f"  {m['name']:<20} {m['speed']:.2f} tok/s (expected {m['expected']:.1f}) [{status}]")
    
    # Check if current models are fast enough
    fastest = available[0] if available else None
    
    if fastest and fastest['speed'] < 0.5:
        print(f"\nAll models too slow! Current fastest: {fastest['name']} at {fastest['speed']:.2f} tok/s")
        print("This device may need GPU acceleration for better performance.")
    
    return available


def send_prompt(prompt, max_tokens=100):
    """Send prompt to best available model."""
    available = find_available_models()
    
    if not available:
        print("No models available!")
        return None
    
    # Try by preference: qwen-1.5b first (fastest for chat), then others
    for pref in ["qwen-1.5b", "deepseek-coder-1.3b", "qwen-coder-3b"]:
        for m in available:
            if m['name'] == pref:
                try:
                    resp = requests.post(
                        f"http://localhost:{m['port']}/v1/chat/completions",
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
    parser.add_argument("--status", action="store_true", help="Check model status")
    parser.add_argument("--start", help="Start specific model (qwen-1.5b, qwen-coder-3b, deepseek-coder-1.3b)")
    parser.add_argument("--test", help="Send test prompt")
    args = parser.parse_args()
    
    if args.start:
        start_model(args.start)
        return
    
    if args.list:
        available = find_available_models()
        print("\nAvailable Models:")
        if not available:
            print("  No models running")
        for m in available:
            print(f"  [{m['name']}] Port {m['port']} - {m['speed']:.2f} tok/s")
        return
    
    if args.status:
        auto_select()
        return
    
    if args.test:
        result = send_prompt(args.test)
        if result:
            print(result["choices"][0]["message"]["content"])
        return
    
    print("Primaclaw Model Pool\n")
    print("Usage:")
    print("  --list                List available models")
    print("  --status              Check model status")
    print("  --start qwen-1.5b    Start specific model")
    print("  --test 'prompt'      Send test prompt")


if __name__ == "__main__":
    main()
