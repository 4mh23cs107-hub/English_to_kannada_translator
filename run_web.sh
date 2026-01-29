#!/bin/bash
# English to Kannada Translator - Linux/macOS Startup Script

echo ""
echo "========================================"
echo "English to Kannada Translator"
echo "Full-Stack Web Application"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the Flask app
echo ""
echo "========================================"
echo "Starting server at http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""
python app.py
