#!/bin/bash
# ============================================
# Dynamic Workload Distribution System
# One-Click Setup Script for Linux/Mac
# ============================================

echo ""
echo "============================================"
echo "Dynamic Workload Distribution System"
echo "Setup Script"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.7 or higher:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  macOS:         brew install python3"
    echo "  Or download from: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo "[1/3] Checking Python version..."
python3 --version
echo ""

echo "[2/3] Upgrading pip..."
python3 -m pip install --upgrade pip --user
echo ""

echo "[3/3] Installing required packages..."
python3 -m pip install -r requirements.txt --user
echo ""

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to install some packages!"
    echo "Please check the error messages above."
    echo ""
    exit 1
fi

echo ""
echo "============================================"
echo "Setup completed successfully!"
echo "============================================"
echo ""
echo "You can now run the simulation with:"
echo "  python3 main.py"
echo ""
echo "Or test the installation with:"
echo "  python3 SIMPLE_TEST.py"
echo ""

