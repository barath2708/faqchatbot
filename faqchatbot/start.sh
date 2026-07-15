#!/bin/bash
set -e
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting backend..."
cd "$ROOT_DIR/Backend"
uvicorn app.main:app --reload &
BACKEND_PID=$!

sleep 2

echo "Starting frontend..."
cd "$ROOT_DIR/Frontend"
npm run dev &
FRONTEND_PID=$!

trap "echo 'Stopping...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT INT TERM

wait
