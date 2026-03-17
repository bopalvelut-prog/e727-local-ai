import socket
import os
import subprocess
import logging
import time
from src.config import settings

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("worker")

def send_discovery():
    """Broadcasts discovery message to coordinator."""
    try:
        # Get local IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        message = f"{local_ip}:RANK_{settings.WORKER_RANK}"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Broadcast to local subnet or specific IP
        logger.info(f"🛰️ Sending discovery to {settings.WORKER_UDP_BROADCAST_IP}:{settings.COORDINATOR_PORT}")
        sock.sendto(message.encode("utf-8"), (settings.WORKER_UDP_BROADCAST_IP, settings.COORDINATOR_PORT))
        sock.close()
    except Exception as e:
        logger.error(f"❌ Discovery failed: {e}")

def run_llama_server():
    """Starts the prima.cpp llama-server."""
    # Assuming llama-server is in ~/prima.cpp/llama-server
    # Or in the PATH
    llama_path = os.path.expanduser("~/prima.cpp/llama-server")
    if not os.path.exists(llama_path):
        llama_path = "llama-server" # Try from path
        
    world_size = 1 # Default
    try:
        if os.path.exists(settings.WORLD_SIZE_FILE):
            with open(settings.WORLD_SIZE_FILE, "r") as f:
                world_size = int(f.read().strip())
    except: pass
    
    port = 8080 + settings.WORKER_RANK
    
    cmd = [
        llama_path,
        "-m", settings.WORKER_MODEL_PATH,
        "--world", str(world_size),
        "--rank", str(settings.WORKER_RANK),
        "--host", "0.0.0.0",
        "--port", str(port),
        "-c", "2048",
        "-ngl", "0",
        "--log-disable"
    ]
    
    logger.info(f"🤖 Starting llama-server: {' '.join(cmd)}")
    try:
        process = subprocess.Popen(cmd)
        process.wait()
    except Exception as e:
        logger.error(f"❌ Failed to start llama-server: {e}")

if __name__ == "__main__":
    # Wait for coordinator
    send_discovery()
    time.sleep(2) # Give coordinator time to update world size
    run_llama_server()
