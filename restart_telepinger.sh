#!/bin/bash
# Restart telepinger

docker compose down && git pull && docker compose up -d && docker compose logs -f