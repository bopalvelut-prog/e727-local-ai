import socket
import threading
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config import settings

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("coordinator")

# Swarm state
workers = set()

def udp_listener():
    """Listens for UDP broadcast from workers."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Use UDP port from config
    sock.bind((settings.COORDINATOR_HOST, settings.COORDINATOR_UDP_PORT))
    logger.info(f"🚀 UDP Listener running on port {settings.COORDINATOR_UDP_PORT}")
    
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode("utf-8")
        logger.info(f"✓ Received discovery from {addr}: {message}")
        
        # message format: IP:RANK_N
        if ":" in message:
            ip, rank_str = message.split(":")
            rank = rank_str.replace("RANK_", "")
            worker_id = f"{ip}:{rank}"
            
            if worker_id not in workers:
                workers.add(worker_id)
                logger.info(f"✓ Worker {worker_id} joined. Total: {len(workers)}")
                # Update files (for prima.cpp compatibility)
                try:
                    with open(settings.WORLD_SIZE_FILE, "w") as f:
                        f.write(str(len(workers)))
                    with open(settings.WORKERS_FILE, "a") as f:
                        f.write(f"{worker_id}\n")
                except Exception as e:
                    logger.error(f"⚠️ Could not update world files: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start UDP listener in background
    thread = threading.Thread(target=udp_listener, daemon=True)
    thread.start()
    yield
    # Shutdown logic can be added here if needed

app = FastAPI(title="NemoClaw Coordinator API", lifespan=lifespan)

@app.get("/")
async def get_status():
    """Returns the swarm status."""
    return {
        "status": "online",
        "swarm": {
            "size": len(workers),
            "workers": sorted(list(workers))
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.COORDINATOR_HOST, port=settings.COORDINATOR_PORT)
