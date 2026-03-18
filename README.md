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
