#!/bin/bash

# Financial Chart Generator - Production Server Startup Script

echo "Starting Financial Chart Generator..."

# Check if gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo "Installing gunicorn..."
    python3 -m pip install gunicorn
fi

# Start the server with gunicorn
echo "Server running at http://127.0.0.1:5001"
echo "Press Ctrl+C to stop"

gunicorn -w 4 -b 127.0.0.1:5001 app:app --access-logfile - --error-logfile -
