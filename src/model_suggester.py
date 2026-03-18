#!/usr/bin/env python3
"""
Primaclaw Model Suggester & Downloader
Suggests better quantized models based on speed and downloads from Hugging Face.
"""

import requests
import argparse
import subprocess
import os

MODELS_DB = {
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
            "Q8_0": {"suffix": "qwen2.5-7b-instruct-q8_0.gguf", "size_gb": 7.5, "quality": 1.0},
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
    "phi-3-mini": {
        "repo": "bartowski/Phi-3-mini-4k-instruct-GGUF",
        "quants": {
            "Q4_K_M": {"suffix": "Phi-3-mini-4k-instruct-Q4_K_M.gguf", "size_gb": 2.0, "quality": 0.9},
        }
    },
    "deepseek-r1-1.5b": {
        "repo": "lmstudio-community/DeepSeek-R1-Distill-Qwen-1.5B-GGUF",
        "quants": {
            "Q2_K": {"suffix": "DeepSeek-R1-Distill-Qwen-1.5B-Q3_K_L.gguf", "size_gb": 0.6, "quality": 0.7},
            "Q4_K_M": {"suffix": "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf", "size_gb": 0.9, "quality": 0.9},
        }
    },
}

DOWNLOAD_DIR = os.path.expanduser("~/Lataukset")


def list_models():
    print("\n Available Models & Quantizations:\n")
    print(f"{'Model':<25} {'Quant':<10} {'Size':<10} {'Quality':<10}")
    print("-" * 55)
    for model_key, info in MODELS_DB.items():
        first = True
        for quant, qinfo in info["quants"].items():
            prefix = model_key if first else ""
            print(f"{prefix:<25} {quant:<10} {qinfo['size_gb']:.1f} GB    {qinfo['quality']:.0%}")
            first = False


def suggest_model(target_size_gb=None, target_quality=0.9):
    print(f"\n Suggestions (target: {'any size' if not target_size_gb else f'<{target_size_gb}GB'}, quality >={target_quality:.0%}):\n")
    matches = []
    for model_key, info in MODELS_DB.items():
        for quant, qinfo in info["quants"].items():
            if qinfo["quality"] >= target_quality:
                if target_size_gb is None or qinfo["size_gb"] <= target_size_gb:
                    matches.append({
                        "model": model_key, "quant": quant, "size_gb": qinfo["size_gb"],
                        "quality": qinfo["quality"], "repo": info["repo"], "filename": qinfo["suffix"]
                    })
    matches.sort(key=lambda x: (x["size_gb"], -x["quality"]))
    print(f"{'#':<3} {'Model':<20} {'Quant':<10} {'Size':<10} {'Quality'}")
    print("-" * 55)
    for i, m in enumerate(matches[:10], 1):
        print(f"{i:<3} {m['model']:<20} {m['quant']:<10} {m['size_gb']:.1f} GB    {m['quality']:.0%}")
    return matches[:10]


def download_model(repo, filename, download_dir=DOWNLOAD_DIR):
    url = f"https://huggingface.co/{repo}/resolve/main/{filename}"
    output_path = os.path.join(download_dir, filename)
    if os.path.exists(output_path):
        print(f" Model already exists: {output_path}")
        return output_path
    print(f"\n Downloading {filename}...")
    print(f" From: {url}")
    try:
        result = subprocess.run(["wget", "-O", output_path, url], capture_output=True, text=True)
        if result.returncode == 0:
            print(f" Downloaded: {output_path}")
            return output_path
        else:
            print(f" Download failed: {result.stderr}")
            return None
    except Exception as e:
        print(f" Download failed: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Primaclaw Model Suggester & Downloader")
    parser.add_argument("--list", action="store_true", help="List all available models")
    parser.add_argument("--suggest", action="store_true", help="Suggest models based on criteria")
    parser.add_argument("--size", type=float, help="Max size in GB")
    parser.add_argument("--quality", type=float, default=0.9, help="Min quality (0-1)")
    parser.add_argument("--download", type=int, help="Download model # from suggestions")
    parser.add_argument("--model", help="Specific model to download")
    parser.add_argument("--quant", help="Quantization type")
    parser.add_argument("--dir", help="Download directory")
    args = parser.parse_args()
    
    if args.dir:
        global DOWNLOAD_DIR
        DOWNLOAD_DIR = args.dir
    
    if args.list:
        list_models()
        return
    
    if args.suggest:
        matches = suggest_model(target_size_gb=args.size, target_quality=args.quality)
        print(f"\n Run with --download N to download model #N")
        return
    
    if args.download:
        matches = suggest_model(target_size_gb=args.size, target_quality=args.quality)
        if 1 <= args.download <= len(matches):
            m = matches[args.download - 1]
            download_model(m["repo"], m["filename"])
        return
    
    if args.model and args.quant:
        model_key = args.model.lower()
        quant = args.quant.upper()
        if model_key in MODELS_DB and quant in MODELS_DB[model_key]["quants"]:
            info = MODELS_DB[model_key]["quants"][quant]
            download_model(MODELS_DB[model_key]["repo"], info["suffix"])
        else:
            print(f"Unknown model/quant: {model_key} {quant}")
        return
    
    print("Primaclaw Model Suggester & Downloader\n")
    print("Usage:")
    print("  --list                    List all available models")
    print("  --suggest                 Suggest models based on criteria")
    print("  --suggest --size 2        Suggest models smaller than 2GB")
    print("  --download N              Download suggestion #N")
    print("  --model qwen2.5-1.5b --quant Q4_K_M   Download specific")


if __name__ == "__main__":
    main()
