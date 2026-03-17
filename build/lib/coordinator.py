import socket
import threading
import logging
from fastapi import FastAPI
from src.config import settings

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("coordinator")

app = FastAPI(title="NemoClaw Coordinator API")

# Swarm state
workers = set()

def udp_listener():
    """Listens for UDP broadcast from workers."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((settings.COORDINATOR_HOST, settings.COORDINATOR_PORT))
    logger.info(f"🚀 UDP Listener running on port {settings.COORDINATOR_PORT}")
    
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
                with open(settings.WORLD_SIZE_FILE, "w") as f:
                    f.write(str(len(workers)))
                with open(settings.WORKERS_FILE, "a") as f:
                    f.write(f"{worker_id}\n")

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

@app.on_event("startup")
def startup_event():
    # Start UDP listener in background
    thread = threading.Thread(target=udp_listener, daemon=True)
    thread.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.COORDINATOR_HOST, port=settings.COORDINATOR_PORT)
