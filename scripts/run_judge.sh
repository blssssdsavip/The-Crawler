#!/usr/bin/env bash
# Start the judge and expose it to the bots.
uvicorn judge:app --host 0.0.0.0 --port 8080 &
cloudflared tunnel --url http://localhost:8080
