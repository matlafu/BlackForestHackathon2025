#!/bin/bash
set -a
source balkonsolar/.env
set +a
python3.11 -m appdaemon -c balkonsolar/appdaemon "$@"
