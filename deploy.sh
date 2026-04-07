#!/bin/bash

# JDM Configurator - Deploy All Services
# This script deploys the Telegram bot and both websites using Docker

set -e

echo "============================================"
echo " JDM Configurator - Full Deployment"
echo "============================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Ubuntu: sudo apt install docker.io"
    echo "   Then: sudo usermod -aG docker \$USER"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed."
    echo "   Ubuntu: sudo apt install docker-compose"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and set your BOT_TOKEN before continuing."
    echo "   Get token from @BotFather on Telegram"
    exit 1
fi

# Check if BOT_TOKEN is set
if grep -q "your_bot_token_here" .env; then
    echo "⚠️  BOT_TOKEN not configured in .env"
    echo "   Please edit .env and set your actual bot token from @BotFather"
    exit 1
fi

echo "📦 Building and starting services..."
echo ""

# Use docker-compose or docker compose depending on what's available
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Stop existing containers if running
$COMPOSE_CMD down 2>/dev/null || true

# Build and start services
$COMPOSE_CMD up -d --build

echo ""
echo "============================================"
echo " ✅ Deployment Complete!"
echo "============================================"
echo ""
echo "Services:"
echo "  🤖 Telegram Bot:    Running (polling)"
echo "  🚗 Client Website:  http://localhost:5000"
echo "  🔧 Admin Panel:     http://localhost:5001"
echo ""
echo "Access from other devices:"
echo "  Client:  http://YOUR_SERVER_IP:5000"
echo "  Admin:   http://YOUR_SERVER_IP:5001"
echo ""
echo "Admin Password: service2024"
echo ""
echo "View logs:"
echo "  All services:  $COMPOSE_CMD logs -f"
echo "  Bot only:      $COMPOSE_CMD logs -f bot"
echo "  Client only:   $COMPOSE_CMD logs -f client"
echo "  Admin only:    $COMPOSE_CMD logs -f admin"
echo ""
echo "Stop services:"
echo "  $COMPOSE_CMD down"
echo ""
