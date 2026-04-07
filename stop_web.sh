#!/bin/bash

# JDM Config Web - Stop Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🛑 Stopping JDM Web applications..."

# Stop using PID files if they exist
if [ -f "logs/client.pid" ]; then
    CLIENT_PID=$(cat logs/client.pid)
    if kill -0 $CLIENT_PID 2>/dev/null; then
        echo "🚗 Stopping Client App (PID: $CLIENT_PID)..."
        kill $CLIENT_PID
    fi
    rm -f logs/client.pid
fi

if [ -f "logs/admin.pid" ]; then
    ADMIN_PID=$(cat logs/admin.pid)
    if kill -0 $ADMIN_PID 2>/dev/null; then
        echo "🔧 Stopping Admin App (PID: $ADMIN_PID)..."
        kill $ADMIN_PID
    fi
    rm -f logs/admin.pid
fi

# Also kill by process name as fallback
pkill -f "python.*web/client_app.py" 2>/dev/null
pkill -f "python.*web/admin_app.py" 2>/dev/null

echo "✅ Applications stopped."
