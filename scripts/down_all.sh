#!/bin/bash
# Down all services of the app and monitoring from any location

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

docker compose -f docker-compose.yml -f docker-compose-monitoring.yml down 