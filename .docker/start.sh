#!/bin/bash

# Copy .env
! test -s ./.env && cp ./.env.local.sample ./.env

# Start fastapi app must bin to host 0.0.0.0 for docker
uvicorn pyfolio.main:app --reload --host 0.0.0.0 --port 8000