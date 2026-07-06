# Track 1 submission image. Judging harness mounts /input and /output and
# injects FIREWORKS_API_KEY / FIREWORKS_BASE_URL / ALLOWED_MODELS.
# Build:  docker buildx build --platform linux/amd64 -t ghcr.io/anbu-00001/amda-agent:latest .
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# TODO(model): bake in llama.cpp + GGUF weights once the judging VM specs are
# known. Placeholder runs remote-only (router degrades gracefully).
# COPY models/ /models/

COPY agent/ /app/agent/
ENTRYPOINT ["python", "-m", "agent.main"]
