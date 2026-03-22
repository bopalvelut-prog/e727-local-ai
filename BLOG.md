# Running AI on E-Waste: The Primaclaw Toolkit

*How to turn your dusty laptops and old desktops into a distributed AI cluster*

---

Most people think you need a $2000 GPU to run AI locally. You don't. With a
collection of old laptops, some open-source software, and a bit of patience, you
can build a functional AI cluster from hardware that would otherwise end up in a
landfill.

This post introduces the **Primaclaw Toolkit** — three open-source projects
that work together to bring AI to your old hardware.

## The Problem

Cloud AI APIs are expensive and send your data to third parties. Local AI
requires powerful GPUs most people don't have. There's a gap between "run
everything in the cloud" and "buy an H100."

## The Solution: Three Projects

### 1. [AutoResearch](https://github.com/bopalvelut-prog/autoresearch)

An autonomous AI researcher that optimizes hyperparameters while you sleep.
Forked from Karpathy's autoresearch and adapted for **any hardware** — CPU,
Apple Silicon, or NVIDIA GPU.

- Runs experiments on a fixed 5-minute budget
- Uses a local Ollama model (Qwen 2.5 0.5B) to suggest improvements
- Automatically commits and logs results
- Achieved **2.23 val_bpb** on CPU (from 2.29 baseline)

```bash
# Quick start
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/bopalvelut-prog/autoresearch.git
cd autoresearch && uv sync && uv run prepare.py
./run_agent.sh  # let it run overnight
```

### 2. [Primaclaw (e727-local-ai)](https://github.com/bopalvelut-prog/e727-local-ai)

A distributed AI swarm that connects old machines into a single
OpenAI-compatible API. Named after the eMachines E727 (2009 Pentium T4500)
that inspired it.

- **Coordinator**: FastAPI gateway that routes requests to workers
- **Workers**: Old machines running quantized models via llama.cpp
- **Dashboard**: Real-time monitoring via browser
- **Efficiency module**: Benchmark and compare models automatically
- Works on **Alpine Linux** and even **iSH on iPhone**

```bash
# On your "brain" node:
python -m src.coordinator

# On each old laptop:
python -m src.worker
```

### 3. [Model Efficiency Comparator](https://github.com/bopalvelut-prog/model-efficiency)

A tool to find the best model for your hardware. Measures tokens/second,
intelligence, security (prompt injection resistance), and model size.

```bash
python model_efficiency_comparator.py -p "Explain AI" --format html -o report.html
```

Also available as a module inside Primaclaw:
```bash
python -m src.efficiency.cli -p "Hello" --format json
```

## Real Results

| Hardware | Year | Model | Speed | Notes |
|----------|------|-------|-------|-------|
| eMachines E727 | 2009 | Qwen2.5 1.5B Q4 | 1.7 t/s | Pentium T4500 |
| Acer Swift 3 | 2020 | Qwen2.5 3B Q4 | 0.5 t/s | Ryzen 5 4500U |
| iPhone 11 (iSH) | 2019 | Qwen2.5 0.5B | ~0.3 t/s | Emulated x86 |

These are real, measured numbers. Not impressive by cloud standards, but they're
running on hardware worth less than a single month of GPT-4 API usage.

## Getting Started

1. Install [Ollama](https://ollama.com) on each machine
2. Pull a small model: `ollama pull qwen2.5:0.5b`
3. Clone the repos and run
4. Let AutoResearch optimize overnight

All three repos are MIT licensed. PRs welcome.

---

*Matti A. Pöysti — Tampere, Finland — March 2026*
