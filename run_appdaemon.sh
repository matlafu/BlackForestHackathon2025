#!/bin/bash

echo "Starting AppDaemon using .env file..."

if command -v dotenv >/dev/null 2>&1; then
  echo "Using 'dotenv' to load environment variables"
  dotenv -f balkonsolar/.env run -- python3.11 -m appdaemon -c balkonsolar/appdaemon "$@"
else
  echo "Falling back to manual .env loading"
  set -a
  # This reads all lines that look like KEY=VALUE and exports them
  grep -v '^\s*#' balkonsolar/.env | grep -E '^\s*[A-Za-z_][A-Za-z0-9_]*=' > /tmp/.env.filtered
  . /tmp/.env.filtered
  set +a
  python3.11 -m appdaemon -c balkonsolar/appdaemon "$@"
fi
