# Primaclaw 🤖🐚🌊 (OpenAI)-compatible Swarm

```
  ____  ____  ___ __  __   _    ____ _        _ __        __
 |  _ \|  _ \|_ _|  \/  | / \  / ___| |      / \\ \      / /
 | |_) | |_) || || |\/| |/ _ \| |   | |     / _ \\ \ /\ / / 
 |  __/|  _ < | || |  | / ___ \ |___| |___ / ___ \\ V  V /  
 |_|   |_| \_\___|_|  |_/_/   \_\____|_____/_/   \_\\_/\_/   
                                    v1.0 (Swarm Edition)
```

**Turn your e-waste into an (OpenAI)-compatible distributed AI cluster.**  
Primaclaw connects your dusty laptops, Raspberry Pis, and old desktops into a single, unified AI entity using a local (OpenAI)-compatible API.

---

## 🏗️ How It Works

1.  **The Brain (Coordinator):** A lightweight **FastAPI** server that acts as the "Universal Gateway". It mimics the **OpenAI API**, so you can connect any tool (OpenWebUI, SillyTavern, OpenClaw) to it.
2.  **The Limbs (Workers):** Python scripts that wrap local inference engines. They broadcast their existence via UDP.
3.  **The Swarm:** When you send a prompt to the Coordinator, it intelligently routes the request to the active workers.

---

## 📊 Benchmarking & Efficiency

Primaclaw now includes a built-in benchmark tool to measure your swarm's performance and security.

### Features
- **Token Throughput:** Measures real-world tokens/second across the swarm.
- **Security Check:** Automatic prompt injection resistance testing.
- **Smart Recommendations:** Suggests optimal quantization levels based on performance.
- **Auto-Downloader:** Offers to pull better-performing model versions automatically.

### Usage
```bash
python -m src.benchmark -p "Your test prompt"
```

---

## ⚡ Quick Start

```bash
# Run the Brain (Coordinator)
python -m src.coordinator

# Run a Limb (Worker)
python -m src.worker

# Benchmark the Swarm
python -m src.benchmark
```

---

## 📊 Running Servers

| Port | Model | Size | Speed |
|------|-------|------|-------|
| 8085 | Qwen2.5-1.5B-Instruct-Q4_K_M | 0.9GB | Fast (1.7 tok/s) |
| 8083 | qwen2.5-coder-3B-Instruct | 1.9GB | Medium (~0.5 tok/s) |

Run with: `/home/ma/prima.cpp/llama-server -m <model-path> --port <port>`

---

## 🌍 Finnish / Suomeksi

**Primaclaw** muuttaa vanhat tietokoneet hajautetuksi tekoälyparveksi, joka on täysin **(OpenAI)-yhteensopiva**.

---

## 🤝 Join the Swarm

License: MIT. PRs welcome!
