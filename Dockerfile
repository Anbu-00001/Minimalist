# Track 1 submission image. The judging harness mounts /input and /output and
# injects FIREWORKS_API_KEY / FIREWORKS_BASE_URL / ALLOWED_MODELS at runtime.
#
# Build:  docker buildx build --platform linux/amd64 -t ghcr.io/anbu-00001/amda-agent:latest .
# Run:    docker run --rm -v ./input:/input:ro -v ./output:/output \
#           -e FIREWORKS_API_KEY -e FIREWORKS_BASE_URL -e ALLOWED_MODELS \
#           ghcr.io/anbu-00001/amda-agent:latest
FROM python:3.12-slim

WORKDIR /app
# libgomp1: OpenMP runtime required by the prebuilt llama.cpp binaries
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# local inference stack: llama.cpp (CPU build, portable) + quantized weights.
# Local tokens score zero — every answer that never leaves the container is free.
COPY tools/llama-b9888/ /opt/llama/
COPY models/ /models/

COPY agent/ /app/agent/
COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Local-dominant routing is the submission's operating mode; the grader only
# injects the Fireworks variables, so this MUST be baked in (an unset
# LOCAL_ONLY silently reverts the agent to remote-first — the 8,282-token
# configuration). Still just an env default: overridable at docker run.
ENV LOCAL_ONLY=1

ENTRYPOINT ["/app/entrypoint.sh"]
