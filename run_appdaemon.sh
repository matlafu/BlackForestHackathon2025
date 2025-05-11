#!/bin/bash

# Try to use python-dotenv if available, otherwise fallback to shell export
if command -v dotenv >/dev/null 2>&1; then
  dotenv -f balkonsolar/.env run -- python3.11 -m appdaemon -c balkonsolar/appdaemon "$@"
else
  set -a
  [ -f balkonsolar/.env ] && . balkonsolar/.env
  set +a
  python3.11 -m appdaemon -c balkonsolar/appdaemon "$@"
fi
