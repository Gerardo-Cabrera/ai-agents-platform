#!/bin/bash

# Stop Ollama service if active
if systemctl is-active --quiet ollama; then
  echo "Stopping Ollama service..."
  sudo systemctl stop ollama
fi

# Kill any remaining Ollama process
echo "Killing any remaining Ollama processes..."
sudo pkill -f 'ollama serve' || true

# Wait for the port to be released
sleep 2

# Start Ollama listening on all interfaces
export OLLAMA_HOST=0.0.0.0
nohup ollama serve > ~/ollama_host.log 2>&1 &
echo "Ollama started on 0.0.0.0:11434 (see ~/ollama_host.log for logs)"
