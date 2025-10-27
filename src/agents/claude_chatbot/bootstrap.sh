#!/bin/bash
set -e
echo "[BOOTSTRAP] Starting agent bootstrap..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi
echo "[BOOTSTRAP] Launching agent..."
exec uvicorn entrypoint:app --host 0.0.0.0 --port 8080
