"""Execute Python code on a remote Jupyter server via the kernel websocket.

Usage: .venv/bin/python eval/jupyter_exec.py "<python code>" [timeout_s]
Env:   JUPYTER_BASE  e.g. https://host/instances/xyz   (no trailing slash)
       JUPYTER_TOKEN

Reuses one kernel across calls (id cached next to this file) so remote state
persists. Shell out with subprocess from the code you pass in.
"""
import json
import os
import sys
import uuid

import httpx
import websocket

BASE = os.environ["JUPYTER_BASE"].rstrip("/")
TOKEN = os.environ["JUPYTER_TOKEN"]
H = {"Authorization": f"token {TOKEN}"}
KERNEL_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".remote_kernel_id")


def get_kernel() -> str:
    if os.path.exists(KERNEL_CACHE):
        kid = open(KERNEL_CACHE).read().strip()
        if kid and httpx.get(f"{BASE}/api/kernels/{kid}", headers=H, timeout=15).status_code == 200:
            return kid
    r = httpx.post(f"{BASE}/api/kernels", headers=H, json={"name": "python3"}, timeout=30)
    r.raise_for_status()
    kid = r.json()["id"]
    open(KERNEL_CACHE, "w").write(kid)
    return kid


def execute(code: str, timeout: float = 120.0) -> int:
    kid = get_kernel()
    ws_url = BASE.replace("https://", "wss://").replace("http://", "ws://")
    ws = websocket.create_connection(f"{ws_url}/api/kernels/{kid}/channels?token={TOKEN}", timeout=timeout)
    msg_id = uuid.uuid4().hex
    session = uuid.uuid4().hex
    ws.send(json.dumps({
        "header": {"msg_id": msg_id, "username": "cc", "session": session,
                   "msg_type": "execute_request", "version": "5.3"},
        "parent_header": {}, "metadata": {}, "channel": "shell",
        "content": {"code": code, "silent": False, "store_history": False,
                    "user_expressions": {}, "allow_stdin": False},
    }))
    status = 0
    try:
        while True:
            msg = json.loads(ws.recv())
            if msg.get("parent_header", {}).get("msg_id") != msg_id:
                continue
            t = msg["msg_type"]
            c = msg.get("content", {})
            if t == "stream":
                print(c["text"], end="", flush=True)
            elif t == "execute_result":
                print(c["data"].get("text/plain", ""))
            elif t == "error":
                print("\n".join(c.get("traceback", [])), file=sys.stderr)
                status = 1
            elif t == "execute_reply":
                if c.get("status") == "error":
                    status = 1
                break
    finally:
        ws.close()
    return status


if __name__ == "__main__":
    code = sys.argv[1]
    tmo = float(sys.argv[2]) if len(sys.argv) > 2 else 120.0
    sys.exit(execute(code, tmo))
