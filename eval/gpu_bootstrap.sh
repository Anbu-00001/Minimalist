#!/usr/bin/env bash
# One-shot bootstrap + model-selection benchmark for the AMD hackathon GPU
# instance. Run inside the extracted AMDA directory:
#
#   bash eval/gpu_bootstrap.sh
#
# Works with whichever inference stack the instance preset provides:
#   - llama-server on PATH  -> downloads Q4_K_M GGUFs and benchmarks those
#   - vllm on PATH          -> serves HF models (bf16) and benchmarks those
# Both expose an OpenAI-compatible API, which is all the agent needs.
#
# Outputs: eval/ENV_REPORT.txt, eval/results_<model>.json (judged),
#          eval/bench_<model>.log, eval/MATRIX_SUMMARY.txt
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
PORT="${PORT:-18080}"
NTASKS="${NTASKS:-}"          # e.g. NTASKS=60 for a quick pass; empty = all 228
PY=python3

mkdir -p models eval
echo "=== environment ===" | tee eval/ENV_REPORT.txt
{ date -u
  command -v rocm-smi >/dev/null && rocm-smi 2>/dev/null | head -12
  "$PY" -V
  command -v vllm && vllm --version 2>/dev/null
  command -v llama-server && llama-server --version 2>&1 | head -2
  free -h | head -2
  df -h . | tail -1
  nproc
} 2>&1 | tee -a eval/ENV_REPORT.txt

"$PY" -m pip install -q --user openai httpx json-repair >/dev/null 2>&1 || \
  "$PY" -m pip install -q openai httpx json-repair >/dev/null 2>&1
export PATH="$HOME/.local/bin:$PATH"

SERVER_PID=""
cleanup() { [ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null; }
trap cleanup EXIT

wait_health() { # url, seconds
  for _ in $(seq 1 "$2"); do
    curl -s -o /dev/null -w '%{http_code}' "$1" 2>/dev/null | grep -qE '^(200)$' && return 0
    [ -n "$SERVER_PID" ] && ! kill -0 "$SERVER_PID" 2>/dev/null && return 1
    sleep 2
  done
  return 1
}

bench() { # <short-name> <model-name-for-api>
  local name="$1" mname="$2"
  echo; echo "=== benchmarking $name ==="
  TOTAL_BUDGET_S=100000 LOCAL_BASE_URL="http://127.0.0.1:$PORT/v1" \
    LOCAL_MODEL_NAME="$mname" "$PY" eval/run_local.py $NTASKS 2>&1 | tee "eval/bench_$name.log" | tail -6
  "$PY" eval/judge.py 2>&1 | tee -a "eval/bench_$name.log" | head -16
  mv -f eval/results_dev.json "eval/results_$name.json"
}

if command -v llama-server >/dev/null 2>&1; then
  # ---- GGUF path (matches what we'd bake into the container) ----
  GGUFS="${GGUFS:-
https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF/resolve/main/Qwen3-4B-Instruct-2507-Q4_K_M.gguf
https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF/resolve/main/Qwen2.5-7B-Instruct-Q4_K_M.gguf
https://huggingface.co/unsloth/gemma-3-4b-it-GGUF/resolve/main/gemma-3-4b-it-Q4_K_M.gguf
https://huggingface.co/unsloth/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf
}"
  for url in $GGUFS; do
    f="models/$(basename "$url")"
    [ -s "$f" ] || curl -sL --fail --retry 5 -o "$f" "$url" || { echo "!! download failed: $url"; rm -f "$f"; continue; }
    [ "$(head -c 4 "$f")" = "GGUF" ] || { echo "!! not a GGUF (gated repo?): $f"; rm -f "$f"; continue; }
    name="$(basename "$f" .gguf)"
    llama-server -m "$f" -c 8192 -ngl 99 --port "$PORT" --jinja > "eval/server_$name.log" 2>&1 &
    SERVER_PID=$!
    if wait_health "http://127.0.0.1:$PORT/health" 90; then
      bench "$name" local
    else
      echo "!! $name: server failed, see eval/server_$name.log"
    fi
    kill "$SERVER_PID" 2>/dev/null; wait "$SERVER_PID" 2>/dev/null; SERVER_PID=""
  done

elif command -v vllm >/dev/null 2>&1; then
  # ---- vLLM path (bf16; fine for model *selection*) ----
  VLLM_MODELS="${VLLM_MODELS:-Qwen/Qwen3-4B-Instruct-2507 Qwen/Qwen2.5-7B-Instruct meta-llama/Llama-3.2-3B-Instruct}"
  for mid in $VLLM_MODELS; do
    name="$(echo "$mid" | tr '/' '_')"
    vllm serve "$mid" --port "$PORT" --max-model-len 8192 \
      --gpu-memory-utilization 0.85 > "eval/server_$name.log" 2>&1 &
    SERVER_PID=$!
    if wait_health "http://127.0.0.1:$PORT/health" 600; then   # first load downloads weights
      bench "$name" "$mid"
    else
      echo "!! $mid: vllm failed to start, see eval/server_$name.log"
    fi
    kill "$SERVER_PID" 2>/dev/null; wait "$SERVER_PID" 2>/dev/null; SERVER_PID=""
  done
else
  echo "!! neither llama-server nor vllm found — check the instance preset" >&2
  exit 1
fi

# ---- summary ----
{
  echo "=== MATRIX SUMMARY ($(date -u)) ==="
  for f in eval/results_*.json; do
    [ -e "$f" ] || continue
    "$PY" - "$f" <<'EOF'
import json, sys, os
r = json.load(open(sys.argv[1]))
n = len(r) or 1
p = sum(t.get("verdict") == "pass" for t in r)
u = sum(t.get("verdict") == "unsure" for t in r)
from collections import defaultdict, Counter
bc = defaultdict(Counter)
for t in r:
    bc[t["true_category"]][t.get("verdict")] += 1
worst = sorted(bc, key=lambda c: bc[c]["pass"] / max(sum(bc[c].values()), 1))[:3]
print(f"{os.path.basename(sys.argv[1])[8:-5]:<45} strict {p}/{n} = {p/n:.0%} (+{u} unsure)  weakest: {', '.join(worst)}")
EOF
  done
  grep -H "tasks in" eval/bench_*.log 2>/dev/null
} | tee eval/MATRIX_SUMMARY.txt
echo; echo "done — download eval/MATRIX_SUMMARY.txt and eval/results_*.json"
