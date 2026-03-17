from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Coordinator settings
    COORDINATOR_HOST: str = "0.0.0.0"
    COORDINATOR_PORT: int = 10000
    COORDINATOR_UDP_PORT: int = 10001
    
    # Worker settings
    WORKER_RANK: int = 0
    WORKER_MODEL_PATH: str = "/home/m/Lataukset/qwen2.5-1.5b-instruct-q4_k_m.gguf"
    WORKER_UDP_BROADCAST_IP: str = "255.255.255.255"
    
    # OpenAI API compatibility
    OPENAI_COMPAT_PORT: int = 8080
    
    # Files
    WORLD_SIZE_FILE: str = "/tmp/prima-world-size"
    WORKERS_FILE: str = "/tmp/prima-workers"

    class Config:
        env_file = ".env"

settings = Settings()
