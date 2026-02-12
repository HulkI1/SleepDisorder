#!/bin/bash
# Sleep Disorder Analysis Platform - Flask Startup Script

echo "🚀 Starting Sleep Disorder Analysis Platform..."
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed"
    exit 1
fi

echo "✓ Python found: $(python --version)"

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask not found, installing dependencies..."
    pip install -r requirements.txt
fi

echo "✓ Dependencies installed"
echo ""

# Create data directory if needed
mkdir -p data ml templates

echo "📂 Directories checked"
echo ""

# Start the Flask application
echo "🌐 Starting Flask server on http://localhost:5000..."
echo "=================================================="
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python flask_app.py
