#!/bin/bash

echo "🚗 Setting up Vehicle Detection System for macOS..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://python.org or using Homebrew:"
    echo "  brew install python3"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ ERROR: pip3 is not available"
    echo "Please install pip3 or reinstall Python 3"
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo
echo "🎉 Setup complete!"
echo
echo "To run the system:"
echo "  1. Activate environment: source .venv/bin/activate"
echo "  2. Run detection: python vehicle_detection_main_yolo.py imshow"
echo
echo "💡 Tip: You can also use the run.sh script for quick execution"
echo
