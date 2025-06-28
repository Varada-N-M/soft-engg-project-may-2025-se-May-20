#!/bin/bash

# Graceful cleanup on Ctrl+C
cleanup() {
    echo "Shutting down servers..."
    kill "$BACKEND_PID" 2>/dev/null
    kill "$FRONTEND_PID" 2>/dev/null
    wait "$BACKEND_PID" 2>/dev/null
    wait "$FRONTEND_PID" 2>/dev/null
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT

# Backend setup
cd backend || exit

if [ ! -d "env" ]; then
    python3 -m venv env
fi

source env/bin/activate
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "# Add your environment variables here" > .env
fi

# Start backend server in background
flask --app main --debug run &
BACKEND_PID=$!

cd ../frontend || exit
npm install

# Start frontend server in background
npm run dev &
FRONTEND_PID=$!

# Wait for either process to exit
while true; do
    sleep 1
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo "Backend server exited."
        cleanup
    fi
    if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo "Frontend server exited."
        cleanup
    fi
done
