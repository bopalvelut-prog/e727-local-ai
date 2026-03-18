import socket
import threading
import logging
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from src.config import settings

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("coordinator")

# Swarm state
workers = set()

def udp_listener():
    """Listens for UDP broadcast from workers."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((settings.COORDINATOR_HOST, settings.COORDINATOR_UDP_PORT))
    logger.info(f"🚀 UDP Listener running on port {settings.COORDINATOR_UDP_PORT}")
    
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode("utf-8")
        
        if ":" in message:
            ip, rank_str = message.split(":")
            rank = rank_str.replace("RANK_", "")
            worker_id = f"{ip}:{rank}"
            
            if worker_id not in workers:
                workers.add(worker_id)
                logger.info(f"✓ Worker {worker_id} joined. Total: {len(workers)}")
                try:
                    with open(settings.WORLD_SIZE_FILE, "w") as f:
                        f.write(str(len(workers)))
                    with open(settings.WORKERS_FILE, "a") as f:
                        f.write(f"{worker_id}\n")
                except Exception as e:
                    logger.error(f"⚠️ Could not update world files: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=udp_listener, daemon=True)
    thread.start()
    yield

app = FastAPI(title="Primaclaw Coordinator & Gateway", lifespan=lifespan)

# --- OpenAI Proxy Gateway ---

@app.api_route("/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def openai_proxy(request: Request, path: str):
    """Proxies requests to the Rank 0 worker (Master)."""
    if not workers:
        return Response(content='{"error": "No workers available in the swarm"}', status_code=503)
    
    # Identify Master (Rank 0)
    master_ip = "127.0.0.1"
    for w in workers:
        if w.endswith(":0"):
            master_ip = w.split(":")[0]
            break
            
    worker_url = f"http://{master_ip}:8080/v1/{path}"
    
    async with httpx.AsyncClient(timeout=None) as client:
        method = request.method
        content = await request.body()
        headers = dict(request.headers)
        # Remove host header to avoid conflicts
        headers.pop("host", None)
        
        logger.info(f"🌐 Gateway: Proxying {method} /v1/{path} to {worker_url}")
        
        try:
            rp_resp = await client.request(
                method,
                worker_url,
                content=content,
                headers=headers,
                params=request.query_params,
            )
            return Response(
                content=rp_resp.content,
                status_code=rp_resp.status_code,
                headers=dict(rp_resp.headers),
            )
        except Exception as e:
            logger.error(f"❌ Gateway Error: {e}")
            return Response(content=f'{{"error": "{str(e)}"}}', status_code=502)

@app.get("/")
async def get_status():
    return {
        "status": "online",
        "gateway": "active",
        "swarm": {
            "size": len(workers),
            "workers": sorted(list(workers))
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.COORDINATOR_HOST, port=settings.COORDINATOR_PORT)
