#!/bin/bash

# JDM Config Web - Startup Script
# Launches both Client and Admin Flask applications

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Using defaults from .env.example"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📝 Created .env file with defaults"
    fi
fi

# Export environment variables
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

# Kill any existing instances
echo "🛑 Stopping any existing instances..."
pkill -f "python.*web/client_app.py" 2>/dev/null
pkill -f "python.*web/admin_app.py" 2>/dev/null
sleep 1

# Create logs directory
mkdir -p logs

# Start Client App
echo "🚗 Starting Client App on port ${PORT:-5000}..."
nohup python web/client_app.py > logs/client_$(date +%Y%m%d_%H%M%S).log 2>&1 &
CLIENT_PID=$!

# Start Admin App
echo "🔧 Starting Admin App on port ${ADMIN_PORT:-5001}..."
nohup python web/admin_app.py > logs/admin_$(date +%Y%m%d_%H%M%S).log 2>&1 &
ADMIN_PID=$!

echo ""
echo "✅ Applications started successfully!"
echo "🌐 Client: http://localhost:${PORT:-5000} (PID: $CLIENT_PID)"
echo "🔧 Admin:  http://localhost:${ADMIN_PORT:-5001} (PID: $ADMIN_PID)"
echo ""
echo "📝 Logs: logs/client_*.log, logs/admin_*.log"
echo "🛑 To stop: kill $CLIENT_PID $ADMIN_PID or run: pkill -f 'python.*web/(client|admin)_app.py'"
echo ""

# Save PIDs to file for easy management
echo "$CLIENT_PID" > logs/client.pid
echo "$ADMIN_PID" > logs/admin.pid

# Keep script running to show logs (optional - remove if you want it to background)
echo "📊 Applications are running in background. Press Ctrl+C to exit this script."
echo ""

# Wait for both processes
wait $CLIENT_PID $ADMIN_PID
