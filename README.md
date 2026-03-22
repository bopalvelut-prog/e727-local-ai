[![CI](https://github.com/bopalvelut-prog/e727-local-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/bopalvelut-prog/e727-local-ai/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/bopalvelut-prog/e727-local-ai?style=social)](https://github.com/bopalvelut-prog/e727-local-ai/stargazers)

# Primaclaw — Distributed AI from E-Waste

**Turn your old laptops, Raspberry Pis, and dusty desktops into an OpenAI-compatible AI cluster.**

Named after a 2009 eMachines E727 (Pentium T4500) that's still running.

```
  ____  ____  ___ __  __   _    ____ _        _ __        __
 |  _ \|  _ \|_ _|  \/  | / \  / ___| |      / \\ \      / /
 | |_) | |_) || || |\/| |/ _ \| |   | |     / _ \\ \ /\ / /
 |  __/|  _ < | || |  | / ___ \ |___| |___ / ___ \\ V  V /
 |_|   |_| \_\___|_|  |_/_/   \_\____|_____/_/   \_\\_/\_/
```

## How it works

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Old Laptop  │     │ Raspberry Pi │     │  eMachines   │
│  (Worker)    │     │  (Worker)    │     │  (Worker)    │
│  Qwen 1.5B   │     │  Qwen 0.5B   │     │  Qwen 0.5B   │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │ UDP discovery
                     ┌──────┴───────┐
                     │ Coordinator  │
                     │  (FastAPI)   │
                     │  OpenAI API  │
                     └──────────────┘
                            │
                     Any OpenAI client
                  (OpenWebUI, SillyTavern, etc.)
```

1. **Coordinator** — FastAPI gateway, OpenAI-compatible API on port 10000
2. **Workers** — Old machines running quantized models via llama.cpp
3. **Swarm** — Workers discover coordinator via UDP broadcast

## Quick start

```bash
# On your "brain" machine:
git clone https://github.com/bopalvelut-prog/e727-local-ai.git
cd e727-local-ai
pip install -e .
python -m src.coordinator

# On each old machine:
python -m src.worker
```

Or with Docker:
```bash
docker compose up -d
```

### Dashboard

Open `http://localhost:8888` for real-time swarm monitoring.

### Benchmark your swarm

```bash
python -m src.efficiency.cli -p "Explain quantum computing in 2 sentences"
python -m src.efficiency.cli -p "Hello" --format html -o report.html
```

## Features

| Feature | Description |
|---------|-------------|
| **OpenAI-compatible API** | Drop-in replacement for OpenAI endpoints |
| **UDP auto-discovery** | Workers find coordinator automatically |
| **Model efficiency** | Benchmark speed, quality, security per node |
| **Dashboard** | Browser-based swarm monitoring |
| **Docker support** | `docker compose up` to run everything |
| **Alpine/iSH** | Runs on Alpine Linux and iPhone (via iSH) |

## Tested hardware

| Machine | Year | CPU | Model | Speed |
|---------|------|-----|-------|-------|
| eMachines E727 | 2009 | Pentium T4500 | Qwen2.5 1.5B Q4 | 1.7 t/s |
| Acer Swift 3 | 2020 | Ryzen 5 4500U | Qwen2.5 3B Q4 | 0.5 t/s |
| iPhone 11 (iSH) | 2019 | A13 (emulated) | Qwen2.5 0.5B | ~0.3 t/s |

## Alpine Linux / iSH

See [ALPINE.md](ALPINE.md) for install instructions on Alpine Linux and iPhone.

## License

MIT. PRs welcome.
