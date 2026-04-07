#!/bin/bash

# JDM Configurator - Stop All Services
# This script stops all running Docker containers

set -e

echo "============================================"
echo " JDM Configurator - Stop Services"
echo "============================================"
echo ""

# Use docker-compose or docker compose depending on what's available
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

echo "🛑 Stopping services..."
$COMPOSE_CMD down

echo ""
echo "✅ All services stopped."
