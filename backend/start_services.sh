#!/bin/bash

# Function to handle script termination
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $BACKEND_PID
    kill $STREAMLIT_PID
    exit
}

# Trap SIGINT (Ctrl+C) to run cleanup
trap cleanup INT

echo "Starting FastAPI Backend..."
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

echo "Starting Streamlit Dashboard..."
streamlit run streamlit_app.py &
STREAMLIT_PID=$!

echo "Services are running."
echo "Backend: http://localhost:8000"
echo "Dashboard: http://localhost:8501"
echo "Press Ctrl+C to stop."

wait