# NemoClaw 🤖🌊

**Distributed AI Swarm for Low-Resource Home Clusters.**

*NemoClaw on kevyt, hajautettu tekoälyparvi (swarm), joka on suunniteltu toimimaan vanhemmalla laitteistolla ja kotiolosuhteissa hyödyntäen prima.cpp- ja OpenClaw-ekosysteemejä.*

---

## 🚀 Overview

NemoClaw is a project following the principles of **github.com/bopalvelut-prog** (Business Oulu / City services) to provide a standardized, robust, and containerized way to manage a swarm of small LLM instances.

It takes the core logic of `prima-coordinator` and `prima-worker` and wraps it into a modern, production-ready repository structure with:
- **API-First Design** (FastAPI-based coordinator)
- **Containerization** (Docker & Docker Compose)
- **Standardized Structure** (`src/`, `tests/`, `docs/`)
- **Automated CI/CD** (GitHub Actions)

## 🏗️ Architecture

NemoClaw follows a **Coordinator-Worker** pattern:
- **Coordinator**: Manages the swarm state, tracks active workers, and provides a central discovery API.
- **Workers**: Individual nodes (e.g., eMachines E727, Raspberry Pis, old laptops) running `prima.cpp` or `llama-server`.
- **Discovery**: Automatic UDP-based discovery for dynamic joining/leaving of the swarm.

## 🛠️ Quick Start

### 1. Requirements
- Python 3.10+
- Docker & Docker Compose
- [prima.cpp](https://github.com/Lizonghang/prima.cpp) (installed in `~/prima.cpp`)

### 2. Installation
```bash
git clone https://github.com/bopalvelut-prog/nemoclaw
cd nemoclaw
cp .env.example .env
# Edit .env with your local settings
```

### 3. Running with Docker
```bash
docker-compose up -d
```

### 4. Running Locally (Python)
```bash
pip install -r requirements.txt
python -m src.coordinator  # On the head node
python -m src.worker       # On worker nodes
```

## 📋 Standardized Structure

Following **bopalvelut-prog** principles:
- `src/`: Core logic (Coordinator, Worker, Discovery)
- `tests/`: Automated test suite
- `docs/`: Architecture and API documentation
- `scripts/`: Utility scripts for setup and maintenance
- `.github/workflows/`: CI/CD pipelines

## 🤝 Contributing

We follow the **GitHub Flow**. Please submit pull requests for any changes.
1. Create a feature branch (`feat/your-feature`)
2. Commit your changes using **Conventional Commits**
3. Open a Pull Request for review

## 📄 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---
*Developed for the bopalvelut-prog ecosystem.*
