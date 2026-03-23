# Primaclaw on Alpine Linux / iSH (iPhone)

## Quick Install (Alpine Linux)

```bash
# Install dependencies
apk update
apk add python3 py3-pip git curl

# Clone and install
git clone https://github.com/bopalvelut-prog/e727-local-ai.git
cd e727-local-ai
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
```

## Install on iSH (iPhone)

iSH runs Alpine Linux on your iPhone via user-mode x86 emulation.

```bash
# In iSH terminal:
apk add python3 py3-pip git curl

# Clone (small clone, shallow)
git clone --depth 1 https://github.com/bopalvelut-prog/e727-local-ai.git
cd e727-local-ai

# Setup
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .

# Start as coordinator (phone becomes the head node)
python -m src.coordinator
```

## Running prima.cpp on Alpine

```bash
# Build prima.cpp (or llama.cpp)
git clone https://github.com/bopalvelut-prog/prima.cpp
cd prima.cpp && make -j$(nproc)

# Download a GGUF model (e.g., Qwen2.5 0.5B)
# Place your .gguf file in models/

# Start the server
./llama-server -m models/qwen2.5-0.5b.gguf --port 8080 --host 0.0.0.0
```

## Running as Worker Node

```bash
# Set coordinator address
export WORKER_UDP_BROADCAST_IP=192.168.1.255
export WORKER_RANK=0

# Start worker
python -m src.worker
```

## Benchmark Your Node

```bash
python -m src.efficiency.cli -p "Hello, how are you?"
python -m src.efficiency.cli -p "Hello" --format html -o report.html
```

## Memory Tips for Old Hardware

- Use quantized models: `qwen2.5:0.5b` (350MB) or `tinyllama:1.1b` (600MB)
- Close unused services: `rc-service <service> stop`
- Monitor: `htop` or `free -h`
- iSH is limited to ~512MB RAM — stick to 0.5B models
