# Windows Setup Guide

Running Primaclaw with prima.cpp on Windows via WSL or Docker.

---

## Option 1: WSL (Recommended)

### Step 1: Enable WSL
```powershell
# Open PowerShell as Administrator
wsl --install -d Ubuntu
```

### Step 2: Setup Ubuntu
```bash
# Update and install dependencies
sudo apt update && sudo apt install -y build-essential cmake git

# Clone prima.cpp
git clone https://gitee.com/zonghang-li/prima.cpp
cd prima.cpp

# Build (this takes ~10 minutes)
make -j$(nproc)

# Test it works
./llama-cli -m /path/to/model.gguf -p "Hello" -n 10
```

### Step 3: Access from Windows
Your models are now accessible at:
- WSL path: `/home/ma/prima.cpp/models/`
- Windows path: `\\wsl$\Ubuntu\home\ma\prima.cpp\models\`

---

## Option 2: Docker

### Step 1: Install Docker
Download from: https://www.docker.com/products/docker-desktop

### Step 2: Run prima.cpp in Docker
```bash
# Build the image
docker build -t primaclaw .

# Run with your model
docker run -v /path/to/models:/models -p 8080:8080 primaclaw \
  ./llama-server -m /models/qwen2.5-7b.gguf --port 8080
```

---

## Quick Test (from Windows)

### In WSL terminal:
```bash
cd ~/e727-local-ai
./test-model.sh ~/Lataukset/Qwen2.5-1.5B-Instruct-Q4_K_M.gguf 8085
```

### From Windows PowerShell (after starting server):
```powershell
Invoke-RestMethod -Uri "http://localhost:8085/v1/chat/completions" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"messages":[{"role":"user","content":"Hello!"}],"max_tokens":20}'
```

---

## Troubleshooting

### WSL not found
```powershell
# Run PowerShell as Administrator
wsl --update
wsl --install
```

### Docker won't start
- Enable virtualization in BIOS
- Make sure Hyper-V is enabled in Windows Features

### Model path issues
- Use WSL paths: `/home/ma/...`
- Avoid spaces in folder names
- Use forward slashes: `/c/Users/...` or mount drives
