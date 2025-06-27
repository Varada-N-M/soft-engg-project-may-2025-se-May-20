#!/bin/bash
# This script sets up and runs both backend and frontend servers

# Backend setup
cd backend

# Create virtual environment if not exists
if [ ! -d "env" ]; then
    python -m venv env
fi

# Activate virtual environment
source env/Scripts/activate

# Install Flask
env/Scripts/python.exe -m pip install flask


# Install Python dependencies
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo "# Add your environment variables here" > .env
fi

# Start backend server in background
flask --app main --debug run &
BACKEND_PID=$!

cd ../frontend

# Install Node dependencies
npm install

# Start frontend server
npm run dev

# When frontend server stops, kill backend
kill $BACKEND_PID
