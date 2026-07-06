#!/usr/bin/env bash
# Benchmark a matrix of local GGUF models against the merged dev set.
#
# Built for the AMD hackathon GPU instance ("Unsloth + llama.cpp for Radeon"
# preset) but runs anywhere llama-server does — on CPU set NGL=0.
#
# Usage:
#   eval/bench_matrix.sh models/a.gguf models/b.gguf ...
#
# Env overrides:
#   LLAMA_SERVER  path to llama-server (default tools/llama-b9888/llama-server)
#   NGL           GPU layers to offload (default 99; 0 = pure CPU)
#   PORT          server port (default 8080)
#   NTASKS        subsample size (default: full dev set)
#
# Per model writes eval/results_<name>.json (judged) and prints the summary.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LLAMA_SERVER="${LLAMA_SERVER:-$ROOT/tools/llama-b9888/llama-server}"
NGL="${NGL:-99}"
PORT="${PORT:-8080}"
NTASKS="${NTASKS:-}"
PY="$ROOT/.venv/bin/python"; [ -x "$PY" ] || PY=python3

[ $# -ge 1 ] || { echo "usage: $0 model1.gguf [model2.gguf ...]"; exit 1; }

for MODEL in "$@"; do
  name="$(basename "$MODEL" .gguf)"
  echo "=== $name (ngl=$NGL) ==="

  LD_LIBRARY_PATH="$(dirname "$LLAMA_SERVER")" "$LLAMA_SERVER" \
    -m "$MODEL" -c 8192 -ngl "$NGL" --port "$PORT" --jinja \
    > "$ROOT/eval/server_$name.log" 2>&1 &
  SPID=$!

  up=""
  for _ in $(seq 1 180); do
    curl -s "http://127.0.0.1:$PORT/health" 2>/dev/null | grep -q ok && up=1 && break
    kill -0 "$SPID" 2>/dev/null || break   # server died during load
    sleep 1
  done
  if [ -z "$up" ]; then
    echo "!! $name: server failed to start, see eval/server_$name.log"
    kill "$SPID" 2>/dev/null
    continue
  fi

  # big budget: benchmarking must never trip the container's 540s deadline logic
  TOTAL_BUDGET_S=100000 LOCAL_BASE_URL="http://127.0.0.1:$PORT/v1" \
    "$PY" "$ROOT/eval/run_local.py" $NTASKS
  "$PY" "$ROOT/eval/judge.py"
  mv "$ROOT/eval/results_dev.json" "$ROOT/eval/results_$name.json"

  kill "$SPID" 2>/dev/null; wait "$SPID" 2>/dev/null
done

echo
echo "=== matrix summary ==="
for f in "$ROOT"/eval/results_*.json; do
  [ "$f" = "$ROOT/eval/results_dev.json" ] && continue
  "$PY" - "$f" <<'EOF'
import json, sys, os
r = json.load(open(sys.argv[1]))
n = len(r)
p = sum(t.get("verdict") == "pass" for t in r)
u = sum(t.get("verdict") == "unsure" for t in r)
print(f"{os.path.basename(sys.argv[1]):<55} strict {p}/{n} = {p/max(n,1):.0%}  (+{u} unsure)")
EOF
done
