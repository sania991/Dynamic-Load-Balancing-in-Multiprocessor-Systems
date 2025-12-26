#!/bin/bash

echo "========================================"
echo "Simplified Load Balancer - Setup"
echo "========================================"
echo ""

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

python3 --version

echo ""
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install dependencies"
    echo "Try running: python3 -m pip install --user -r requirements.txt"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To run the program, type:"
echo "  python3 main.py"
echo ""

