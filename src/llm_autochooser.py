#!/usr/bin/env python3
"""
Primaclaw LLM Autochooser
Automatically selects the best model based on task type and complexity.
"""

import requests
import json
import sys
from typing import Optional, Dict, List

SERVERS = {
    "fast": {"port": 8085, "model": "Qwen2.5-1.5B-Instruct", "size": "0.9GB", "speed": "1.7 tok/s"},
    "medium": {"port": 8083, "model": "qwen2.5-coder-3B", "size": "1.9GB", "speed": "~0.5 tok/s"},
}

TASK_MODELS = {
    "quick": "fast",           # Simple greetings, short answers
    "chat": "fast",            # General conversation
    "code": "medium",          # Code generation
    "complex": "medium",       # Complex reasoning
    "creative": "fast",        # Creative writing
    "analysis": "medium",      # Analysis tasks
}

def check_server(port: int) -> bool:
    """Check if a server is running."""
    try:
        resp = requests.get(f"http://localhost:{port}/v1/models", timeout=2)
        return resp.status_code == 200
    except:
        return False

def choose_model(task: str = None, speed_priority: bool = True, quality_priority: bool = False) -> Dict:
    """
    Choose the best model based on task and priorities.
    
    Args:
        task: Task type (quick, chat, code, complex, creative, analysis)
        speed_priority: Prefer faster models
        quality_priority: Prefer better quality models
    
    Returns:
        Dict with server info
    """
    if task and task in TASK_MODELS:
        choice = TASK_MODELS[task]
    elif speed_priority:
        choice = "fast"
    else:
        choice = "medium"
    
    return SERVERS[choice]

def list_available_models() -> List[Dict]:
    """List all available models."""
    available = []
    for name, info in SERVERS.items():
        if check_server(info["port"]):
            available.append({**info, "name": name})
    return available

def send_request(messages: List, model_key: str = None, task: str = None, **kwargs):
    """Send a chat completion request to the chosen model."""
    if model_key:
        server = SERVERS.get(model_key, SERVERS["fast"])
    else:
        server = choose_model(task)
    
    port = server["port"]
    url = f"http://localhost:{port}/v1/chat/completions"
    
    payload = {
        "messages": messages,
        **kwargs
    }
    
    resp = requests.post(url, json=payload, timeout=300)
    resp.raise_for_status()
    return resp.json()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Primaclaw LLM Autochooser")
    parser.add_argument("--task", choices=list(TASK_MODELS.keys()), help="Task type")
    parser.add_argument("--fast", action="store_true", help="Prefer fast model")
    parser.add_argument("--quality", action="store_true", help="Prefer quality")
    parser.add_argument("--list", action="store_true", help="List available models")
    parser.add_argument("--model", choices=list(SERVERS.keys()), help="Force specific model")
    parser.add_argument("--prompt", help="Single prompt to send")
    parser.add_argument("--messages", help="JSON array of messages")
    args = parser.parse_args()
    
    if args.list:
        print("Available models:")
        for m in list_available_models():
            print(f"  [{m['name']}] {m['model']} - {m['size']} - {m['speed']} (port {m['port']})")
        return
    
    if args.prompt:
        messages = [{"role": "user", "content": args.prompt}]
    elif args.messages:
        messages = json.loads(args.messages)
    else:
        print("Error: --prompt or --messages required")
        return
    
    try:
        result = send_request(
            messages, 
            model_key=args.model,
            task=args.task,
            max_tokens=kwargs.get("max_tokens", 200)
        )
        print(result["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
