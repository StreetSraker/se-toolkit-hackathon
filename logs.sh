#!/bin/bash

# JDM Configurator - View Logs
# This script shows logs from all services

set -e

# Use docker-compose or docker compose depending on what's available
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

SERVICE=${1:-all}

case $SERVICE in
  bot)
    echo "🤖 Telegram Bot Logs:"
    $COMPOSE_CMD logs -f bot
    ;;
  client)
    echo "🚗 Client Website Logs:"
    $COMPOSE_CMD logs -f client
    ;;
  admin)
    echo "🔧 Admin Panel Logs:"
    $COMPOSE_CMD logs -f admin
    ;;
  all)
    echo "📋 All Services Logs:"
    $COMPOSE_CMD logs -f
    ;;
  *)
    echo "Usage: $0 {bot|client|admin|all}"
    exit 1
    ;;
esac
