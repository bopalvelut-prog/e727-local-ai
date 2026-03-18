#!/usr/bin/env python3
"""Primaclaw Model Pool"""

import requests
import time
import subprocess
import os

LLAMA_SERVER = "/home/ma/prima.cpp/llama-server"

MODELS = {
    "qwen-coder-0.5b-q8": {
        "path": "/home/ma/Lataukset/Qwen2.5-Coder-0.5B-Q8_0.gguf",
        "port": 8092,
        "speed_expected": 5.0,
        "type": "code"
    },
    "qwen-0.5b": {
        "path": "/home/ma/Lataukset/Qwen2.5-0.5B-Q2_K.gguf",
        "port": 8090,
        "speed_expected": 2.0,
        "type": "chat"
    },
    "qwen-coder-0.5b": {
        "path": "/home/ma/Lataukset/Qwen2.5-Coder-0.5B-Q2_K.gguf",
        "port": 8091,
        "speed_expected": 2.0,
        "type": "code"
    },
    "qwen-1.5b": {
        "path": "/home/ma/prima.cpp/models/Qwen2.5-1.5B-Instruct-Q4_K_M.gguf",
        "port": 8085,
        "speed_expected": 1.7,
        "type": "chat"
    },
    "deepseek-coder-1.3b": {
        "path": "/home/ma/Lataukset/deepseek-coder-1.3b-q2_k.gguf",
        "port": 8089,
        "speed_expected": 0.8,
        "type": "code"
    },
}


def find_available_models():
    found = []
    for name, info in MODELS.items():
        try:
            resp = requests.get(f"http://localhost:{info['port']}/v1/models", timeout=2)
            if resp.status_code == 200:
                speed = measure_speed(info['port'])
                found.append({"name": name, "port": info['port'], "speed": speed, "expected": info['speed_expected'], "type": info['type']})
        except:
            pass
    return found


def start_model(name):
    info = MODELS.get(name)
    if not info:
        print(f"Unknown: {name}")
        return False
    if not os.path.exists(info["path"]):
        print(f"Not found: {info['path']}")
        return False
    subprocess.run(f"pkill -f 'llama-server.*{info['port']}'", shell=True)
    time.sleep(1)
    subprocess.Popen([LLAMA_SERVER, "-m", info["path"], "--port", str(info["port"])], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Starting {name} on port {info['port']}...")
    for _ in range(60):
        time.sleep(1)
        try:
            resp = requests.get(f"http://localhost:{info['port']}/v1/models", timeout=2)
            if resp.status_code == 200:
                print(f"Ready! {name}")
                return True
        except:
            pass
    return False


def measure_speed(port, max_tokens=20):
    try:
        start = time.time()
        resp = requests.post(f"http://localhost:{port}/v1/chat/completions",
            json={"messages": [{"role": "user", "content": "Hi"}], "max_tokens": max_tokens}, timeout=60)
        elapsed = time.time() - start
        if resp.status_code == 200:
            return resp.json().get("usage", {}).get("completion_tokens", max_tokens) / elapsed if elapsed > 0 else 0
    except:
        pass
    return 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Primaclaw Model Pool")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--start", help="Model name")
    args = parser.parse_args()
    
    if args.start:
        start_model(args.start)
        return
    
    if args.list:
        available = find_available_models()
        print("\nAvailable Models:")
        if not available:
            print("  None")
        for m in sorted(available, key=lambda x: -x['speed']):
            print(f"  {m['name']:<25} {m['speed']:.2f} tok/s [{m['type']}]")
        return
    
    print("Primaclaw Model Pool")
    print("Models:", ", ".join(MODELS.keys()))
    print("\nUsage:")
    print("  --list             List available")
    print("  --start qwen-coder-0.5b-q8  Start model")


if __name__ == "__main__":
    main()
