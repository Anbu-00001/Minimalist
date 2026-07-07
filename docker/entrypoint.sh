#!/bin/sh
# Container entrypoint: boot the local llama.cpp server (zero-token inference),
# then run the agent. If no weights are baked in or the server fails to come
# up, the agent degrades gracefully and routes everything to Fireworks.
set -u

MODEL="$(ls /models/*.gguf 2>/dev/null | head -1)"
if [ -n "${MODEL:-}" ]; then
    LD_LIBRARY_PATH=/opt/llama /opt/llama/llama-server \
        -m "$MODEL" -c 4096 -t "$(nproc)" --port 8080 --jinja \
        > /tmp/llama-server.log 2>&1 &
    LLAMA_PID=$!

    # wait for model load, but never block the run: the 10-minute budget is
    # ours to spend, and a dead local server just means remote-only routing
    i=0
    while [ "$i" -lt 40 ]; do
        if ! kill -0 "$LLAMA_PID" 2>/dev/null; then
            echo "entrypoint: llama-server died, remote-only mode" >&2
            tail -3 /tmp/llama-server.log >&2 2>/dev/null
            break
        fi
        if python -c "import httpx,sys; sys.exit(0 if httpx.get('http://127.0.0.1:8080/health', timeout=1).status_code==200 else 1)" 2>/dev/null; then
            echo "entrypoint: local model ready after ${i}s" >&2
            break
        fi
        i=$((i+1)); sleep 1
    done
fi

exec python -m agent.main
