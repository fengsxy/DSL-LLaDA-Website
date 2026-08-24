#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PYTHON=${DSL_DEMO_PYTHON:-python3}
HOST=${DSL_DEMO_HOST:-0.0.0.0}
PORT=${DSL_DEMO_PORT:-7860}

cd "$ROOT_DIR"
exec "$PYTHON" demo/replay_server.py \
  --host "$HOST" \
  --port "$PORT"
