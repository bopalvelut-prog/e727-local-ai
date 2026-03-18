#!/usr/bin/env python3
"""
Primaclaw Model Suggester & Downloader
"""

import requests
import argparse
import subprocess
import os

MODELS_DB = {
    "qwen2.5-0.5b": {
        "repo": "Qwen/Qwen2.5-0.5B-Instruct-GGUF",
        "quants": {
            "Q2_K": {"suffix": "qwen2.5-0.5b-instruct-q2_k.gguf", "size_gb": 0.4, "quality": 0.7},
            "Q3_K_M": {"suffix": "qwen2.5-0.5b-instruct-q3_k_m.gguf", "size_gb": 0.5, "quality": 0.8},
            "Q4_K_M": {"suffix": "qwen2.5-0.5b-instruct-q4_k_m.gguf", "size_gb": 0.5, "quality": 0.9},
            "Q8_0": {"suffix": "qwen2.5-0.5b-instruct-q8_0.gguf", "size_gb": 0.6, "quality": 1.0},
        }
    },
    "qwen2.5-coder-0.5b": {
        "repo": "Qwen/Qwen2.5-Coder-0.5B-Instruct-GGUF",
        "quants": {
            "Q2_K": {"suffix": "qwen2.5-coder-0.5b-instruct-q2_k.gguf", "size_gb": 0.4, "quality": 0.7},
            "Q4_K_M": {"suffix": "qwen2.5-coder-0.5b-instruct-q4_k_m.gguf", "size_gb": 0.5, "quality": 0.9},
            "Q8_0": {"suffix": "qwen2.5-coder-0.5b-instruct-q8_0.gguf", "size_gb": 0.6, "quality": 1.0},
        }
    },
    "qwen2.5-1.5b": {
        "repo": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
        "quants": {
            "Q2_K": {"suffix": "qwen2.5-1.5b-instruct-q2_k.gguf", "size_gb": 0.7, "quality": 0.7},
            "Q3_K_M": {"suffix": "qwen2.5-1.5b-instruct-q3_k_m.gguf", "size_gb": 0.9, "quality": 0.8},
            "Q4_0": {"suffix": "qwen2.5-1.5b-instruct-q4_0.gguf", "size_gb": 1.0, "quality": 0.85},
            "Q4_K_M": {"suffix": "qwen2.5-1.5b-instruct-q4_k_m.gguf", "size_gb": 1.0, "quality": 0.9},
            "Q5_K_M": {"suffix": "qwen2.5-1.5b-instruct-q5_k_m.gguf", "size_gb": 1.2, "quality": 0.95},
            "Q8_0": {"suffix": "qwen2.5-1.5b-instruct-q8_0.gguf", "size_gb": 1.6, "quality": 1.0},
        }
    },
    "qwen2.5-3b": {
        "repo": "Qwen/Qwen2.5-3B-Instruct-GGUF",
        "quants": {
            "Q2_K": {"suffix": "qwen2.5-3b-instruct-q2_k.gguf", "size_gb": 1.4, "quality": 0.7},
            "Q3_K_M": {"suffix": "qwen2.5-3b-instruct-q3_k_m.gguf", "size_gb": 1.6, "quality": 0.8},
            "Q4_0": {"suffix": "qwen2.5-3b-instruct-q4_0.gguf", "size_gb": 1.9, "quality": 0.85},
            "Q4_K_M": {"suffix": "qwen2.5-3b-instruct-q4_k_m.gguf", "size_gb": 2.0, "quality": 0.9},
            "Q5_K_M": {"suffix": "qwen2.5-3b-instruct-q5_k_m.gguf", "size_gb": 2.3, "quality": 0.95},
            "Q8_0": {"suffix": "qwen2.5-3b-instruct-q8_0.gguf", "size_gb": 3.0, "quality": 1.0},
        }
    },
    "qwen2.5-7b": {
        "repo": "Qwen/Qwen2.5-7B-Instruct-GGUF",
        "quants": {
            "Q2_K": {"suffix": "qwen2.5-7b-instruct-q2_k.gguf", "size_gb": 3.0, "quality": 0.7},
            "Q3_K_M": {"suffix": "qwen2.5-7b-instruct-q3_k_m.gguf", "size_gb": 3.5, "quality": 0.8},
            "Q4_0": {"suffix": "qwen2.5-7b-instruct-q4_0.gguf", "size_gb": 4.2, "quality": 0.85},
            "Q4_K_M": {"suffix": "qwen2.5-7b-instruct-q4_k_m.gguf", "size_gb": 4.6, "quality": 0.9},
            "Q5_K_M": {"suffix": "qwen2.5-7b-instruct-q5_k_m.gguf", "size_gb": 5.3, "quality": 0.95},
            "Q6_K": {"suffix": "qwen2.5-7b-instruct-q6_k.gguf", "size_gb": 6.0, "quality": 0.98},
        }
    },
    "qwen2.5-coder-3b": {
        "repo": "Qwen/Qwen2.5-3B-Coder-Instruct-GGUF",
        "quants": {
            "Q4_0": {"suffix": "qwen2.5-coder-3b-instruct-q4_0.gguf", "size_gb": 1.9, "quality": 0.85},
            "Q8_0": {"suffix": "qwen2.5-coder-3b-instruct-q8_0.gguf", "size_gb": 3.4, "quality": 1.0},
        }
    },
    "llama-3.2-3b": {
        "repo": "meta-llama/Llama-3.2-3B-Instruct-GGUF",
        "quants": {
            "Q2_K": {"suffix": "Llama-3.2-3B-Instruct-Q2_K.gguf", "size_gb": 1.4, "quality": 0.7},
            "Q4_K_M": {"suffix": "Llama-3.2-3B-Instruct-Q4_K_M.gguf", "size_gb": 2.0, "quality": 0.9},
            "Q5_K_M": {"suffix": "Llama-3.2-3B-Instruct-Q5_K_M.gguf", "size_gb": 2.3, "quality": 0.95},
        }
    },
    "deepseek-coder-1.3b": {
        "repo": "TheBloke/deepseek-coder-1.3b-instruct-GGUF",
        "quants": {
            "Q2_K": {"suffix": "deepseek-coder-1.3b-instruct.Q2_K.gguf", "size_gb": 0.6, "quality": 0.75},
            "Q3_K_M": {"suffix": "deepseek-coder-1.3b-instruct.Q3_K_M.gguf", "size_gb": 0.7, "quality": 0.8},
            "Q4_0": {"suffix": "deepseek-coder-1.3b-instruct.Q4_0.gguf", "size_gb": 0.8, "quality": 0.85},
            "Q4_K_M": {"suffix": "deepseek-coder-1.3b-instruct.Q4_K_M.gguf", "size_gb": 0.8, "quality": 0.9},
        }
    },
}

DOWNLOAD_DIR = os.path.expanduser("~/Lataukset")


def list_models():
    print("\nAvailable Models:\n")
    print(f"{'Model':<25} {'Quant':<10} {'Size':<10} {'Quality':<10}")
    print("-" * 55)
    for model_key, info in MODELS_DB.items():
        first = True
        for quant, qinfo in info["quants"].items():
            prefix = model_key if first else ""
            print(f"{prefix:<25} {quant:<10} {qinfo['size_gb']:.1f} GB    {qinfo['quality']:.0%}")
            first = False


def suggest_model(target_size_gb=None, target_quality=0.9):
    matches = []
    for model_key, info in MODELS_DB.items():
        for quant, qinfo in info["quants"].items():
            if qinfo.get("quality", 0) >= target_quality:
                if target_size_gb is None or qinfo.get("size_gb", 999) <= target_size_gb:
                    matches.append({
                        "model": model_key, "quant": quant, "size_gb": qinfo.get("size_gb", 0),
                        "quality": qinfo.get("quality", 0), "repo": info["repo"], "filename": qinfo["suffix"]
                    })
    matches.sort(key=lambda x: (x["size_gb"], -x["quality"]))
    print(f"\nSuggestions (<{target_size_gb}GB, >={target_quality:.0%}):\n")
    print(f"{'#':<3} {'Model':<22} {'Quant':<10} {'Size':<10} {'Quality'}")
    print("-" * 60)
    for i, m in enumerate(matches[:10], 1):
        print(f"{i:<3} {m['model']:<22} {m['quant']:<10} {m['size_gb']:.1f} GB    {m['quality']:.0%}")
    return matches[:10]


def download_model(repo, filename, download_dir=DOWNLOAD_DIR):
    url = f"https://huggingface.co/{repo}/resolve/main/{filename}"
    output_path = os.path.join(download_dir, filename)
    if os.path.exists(output_path):
        print(f"Already exists: {output_path}")
        return output_path
    print(f"\nDownloading {filename}...")
    try:
        result = subprocess.run(["wget", "-O", output_path, url], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Downloaded: {output_path}")
            return output_path
    except:
        pass
    return None


def main():
    parser = argparse.ArgumentParser(description="Primaclaw Model Suggester")
    parser.add_argument("--list", action="store_true", help="List all models")
    parser.add_argument("--suggest", action="store_true", help="Suggest models")
    parser.add_argument("--size", type=float, help="Max size in GB")
    parser.add_argument("--quality", type=float, default=0.9, help="Min quality")
    parser.add_argument("--download", type=int, help="Download #")
    args = parser.parse_args()
    
    if args.list:
        list_models()
        return
    
    if args.suggest:
        matches = suggest_model(target_size_gb=args.size, target_quality=args.quality)
        print(f"\nDownload with: --download N")
        return
    
    if args.download:
        matches = suggest_model(target_size_gb=args.size, target_quality=args.quality)
        if 1 <= args.download <= len(matches):
            m = matches[args.download - 1]
            download_model(m["repo"], m["filename"])
        return
    
    print("Usage: --list, --suggest, --suggest --size 1, --download N")


if __name__ == "__main__":
    main()
