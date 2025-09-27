#!/bin/bash
# Railway startup script for Jam Hot API

echo "🚀 Starting Jam Hot API..."

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Start the FastAPI application
echo "🌐 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port $PORT
