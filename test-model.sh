#!/bin/bash
# Test a new GGUF model quickly

MODEL_PATH="${1:-}"
PORT="${2:-8888}"

if [ -z "$MODEL_PATH" ]; then
    echo "Usage: ./test-model.sh <path-to-model.gguf> [port]"
    echo ""
    echo "Example:"
    echo "  ./test-model.sh /path/to/model.q4_0.gguf"
    echo "  ./test-model.sh ~/Downloads/model.gguf 8888"
    exit 1
fi

if [ ! -f "$MODEL_PATH" ]; then
    echo "Error: Model file not found: $MODEL_PATH"
    exit 1
fi

MODEL_NAME=$(basename "$MODEL_PATH")
echo "Starting server with: $MODEL_NAME"
echo "   Port: $PORT"

# Kill any existing server on that port
pkill -f "llama-server.*--port $PORT" 2>/dev/null
sleep 1

# Start server
/home/ma/prima.cpp/llama-server -m "$MODEL_PATH" --port $PORT &
echo "Waiting for model to load..."
sleep 60

# Check if loaded
if curl -s "http://localhost:$PORT/v1/models" | jq -e '.data[0].id' >/dev/null 2>&1; then
    echo "Model loaded! Testing..."
    curl -s -X POST "http://localhost:$PORT/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d '{"messages":[{"role":"user","content":"Hello!"}],"max_tokens":20}'
else
    echo "Model failed to load"
fi
