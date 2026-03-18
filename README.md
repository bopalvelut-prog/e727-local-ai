# Primaclaw 🤖🐚🌊

```
  ____  ____  ___ __  __   _    ____ _        _ __        __
 |  _ \|  _ \|_ _|  \/  | / \  / ___| |      / \\ \      / /
 | |_) | |_) || || |\/| |/ _ \| |   | |     / _ \\ \ /\ / / 
 |  __/|  _ < | || |  | / ___ \ |___| |___ / ___ \\ V  V /  
 |_|   |_| \_\___|_|  |_/_/   \_\____|_____/_/   \_\\_/\_/   
                                    v1.0 (Swarm Edition)
```

> **"Don't throw away your old laptop. Make it part of the Swarm."**

**Turn your e-waste into a distributed AI cluster.**  
Primaclaw connects your dusty laptops, Raspberry Pis, and old desktops into a single, unified AI entity capable of running modern LLMs like **Qwen2.5-1.5B** or even **70B models** (via `prima.cpp`).

---

## 🚀 The Mission

Most AI projects require $10,000 GPUs.  
**Primaclaw requires a 2009 Pentium and a dream.**

We built this to prove that decentralized, low-resource AI is possible. By using a **Coordinator-Worker** architecture, Primaclaw lets devices "discover" each other on your home network and share the workload.

- **♻️ Zero Waste:** Give new life to old hardware.
- **🔋 Low Power:** Optimized for efficiency (145MB RAM usage on idle).
- **🕸️ Self-Healing:** Workers auto-discover the coordinator via UDP.
- **🛡️ Private:** 100% local. No data leaves your home.

---

## ⚡ Quick Start (The "One-Liner")

Copy and paste this into your terminal (Ubuntu/Debian/MacOS):

```bash
curl -sL https://raw.githubusercontent.com/bopalvelut-prog/e727-local-ai/main/install.sh | bash
```

### Manual Install
1. **Clone & Setup:**
   ```bash
   git clone https://github.com/bopalvelut-prog/e727-local-ai.git primaclaw
   cd primaclaw
   python3 -m venv venv && source venv/bin/activate
   pip install .
   ```

2. **Run the Brain (Coordinator):**
   ```bash
   python -m src.coordinator
   # 🌐 Dashboard at http://localhost:10000
   ```

3. **Run a Limb (Worker):**
   *(Do this on as many devices as you have!)*
   ```bash
   python -m src.worker
   ```

---

## 🏗️ How It Works

1.  **The Brain (Coordinator):** A lightweight **FastAPI** server that acts as the "Universal Gateway". It mimics the OpenAI API, so you can connect any tool (OpenWebUI, SillyTavern, OpenClaw) to it.
2.  **The Limbs (Workers):** Python scripts that wrap `prima.cpp` or `llama-server`. They broadcast their existence via UDP.
3.  **The Swarm:** When you send a prompt to the Coordinator, it intelligently routes the request to the active workers.

**Tech Stack:**
- **Python 3.10+** (The glue)
- **FastAPI** (The API Gateway)
- **UDP Multicast** (The nervous system)
- **Prima.cpp** (The muscle - distributed inference)

---

## 🔧 Running Large Models with prima.cpp (Distributed Mode)

prima.cpp enables **distributed inference** across multiple devices - each device only loads the layers it needs via mmap (memory-mapped files). No single device loads the entire model!

### How It Works

1. **Lazy Loading**: Each device uses `mmap` to map the GGUF model file - only accessed pages are loaded into RAM
2. **Layer Distribution**: The scheduler assigns model layers to each device based on:
   - Compute power (CPU/GPU)
   - Disk read speed
   - Available RAM/VRAM
3. **Ring Pipeline**: Devices pass activations in a ring (Device A → B → C → A), overlapping disk I/O with compute
4. **Low Memory Pressure**: 70B models can run with <6% memory pressure on devices with just 2-4GB available RAM

### Benchmark (Token Latency)

| Model | llama.cpp | prima.cpp |
|-------|-----------|-----------|
| Qwen-2.5-7B | 14 ms | 14 ms |
| Qwen-2.5-14B | 23 ms | 23 ms |
| Qwen-2.5-32B | 224 ms | **89 ms** |
| Qwen-2.5-72B | 12227 ms | **867 ms** |
| DeepSeek-R1-Distill-Llama-70B | 10978 ms | **724 ms** |

*Note: For small models (3B-14B), prima.cpp falls back to single-device mode. Speed advantage shows on 32B+ models.*

### Setup (Multiple Devices)

Connect devices to the same Wi-Fi. Each device runs the **same model file path** (can be local or shared network drive):

```bash
# Device 0 (head device - also runs the API server):
./llama-server -m qwen2.5-72b-q4_k_m.gguf --world 4 --rank 0 \
  --master 192.168.1.2 --next 192.168.1.3 --prefetch \
  --host 127.0.0.1 --port 8080

# Device 1 (worker with 8GB VRAM):
./llama-cli -m qwen2.5-72b-q4_k_m.gguf --world 4 --rank 1 \
  --master 192.168.1.2 --next 192.168.1.4 --prefetch --gpu-mem 8

# Device 2 (worker with 11GB VRAM):
./llama-cli -m qwen2.5-72b-q4_k_m.gguf --world 4 --rank 2 \
  --master 192.168.1.2 --next 192.168.1.3 --prefetch --gpu-mem 11

# Device 3 (worker, CPU only):
./llama-cli -m qwen2.5-72b-q4_k_m.gguf --world 4 --rank 3 \
  --master 192.168.1.2 --next 192.168.1.2 --prefetch
```

**Key options:**
- `--world N` - Total number of devices in the cluster
- `--rank N` - This device's rank (0 = head)
- `--master IP` - IP address of rank 0 device
- `--next IP` - IP address of next device in ring
- `--prefetch` - Enable layer prefetching
- `--gpu-mem N` - GPU memory limit (GiB)
- `-c N` - Context size (default: 2048)

**API Usage:**
```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-72b",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 200
  }'
```

### Tips

- Use SSD for model files if possible
- Disable firewall or open ports 9000 (data) and 10000 (signal)
- For CPU-only devices, omit `--gpu-mem`
- prima.cpp automatically profiles devices and assigns optimal layer distribution

---

## 📊 Running Servers

| Port | Model | Size | Speed |
|------|-------|------|-------|
| 8085 | Qwen2.5-1.5B-Instruct-Q4_K_M | 0.9GB | Fast (1.7 tok/s) |
| 8083 | qwen2.5-coder-3B-Instruct | 1.9GB | Medium (~0.5 tok/s) |

Run with: `/home/ma/prima.cpp/llama-server -m <model-path> --port <port>`

---

## 🌍 Finnish / Suomeksi

**Primaclaw** on Business Oulun (bopalvelut-prog) periaatteita noudattava projekti, joka muuttaa vanhat tietokoneet hajautetuksi tekoälyparveksi.

- **Tavoite:** Vähentää elektroniikkajätettä ja demokratisoida tekoäly.
- **Teknologia:** Perustuu `prima.cpp`-kirjastoon, joka mahdollistaa LLM-mallien ajamisen kuluttajalaitteilla.
- **Asennus:** Katso yllä oleva "Quick Start".

---

## 🤝 Join the Swarm

This project follows the **bopalvelut-prog** open-source principles.
- **License:** MIT
- **Contributing:** PRs welcome! (See `CONTRIBUTING.md`)

**🌟 Star us on GitHub if you hate e-waste!**
