#!/bin/bash

# Cloud System Failure Prediction - Linux/Mac Setup Script
# Automatically sets up the project environment

echo ""
echo "===================================================================="
echo "   Cloud System Failure Prediction - Automated Setup (Unix/Linux)"
echo "===================================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "[OK] Python is installed"
python3 --version

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "[ERROR] pip3 is not available"
    echo "Please ensure pip is installed with Python"
    exit 1
fi

echo "[OK] pip3 is available"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment"
    exit 1
fi

echo "[OK] Virtual environment created"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi

echo "[OK] Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip setuptools wheel

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    echo "Please check requirements.txt and try again"
    exit 1
fi

echo "[OK] Dependencies installed successfully"

# Verify setup
echo ""
echo "Verifying setup..."
python verify_setup.py

if [ $? -ne 0 ]; then
    echo "[WARNING] Some checks failed, but you can try running the project"
    echo ""
else
    echo "[OK] All checks passed!"
    echo ""
fi

# Display next steps
echo "===================================================================="
echo "   Setup Complete!"
echo "===================================================================="
echo ""
echo "To run the project:"
echo "   1. Activate environment: source venv/bin/activate"
echo "   2. Run: python run.py"
echo "   3. Check results in: experiments/"
echo ""
echo "To use Jupyter Notebook:"
echo "   1. Activate environment: source venv/bin/activate"
echo "   2. Run: jupyter notebook notebooks/experiments.ipynb"
echo ""
echo "For more information, see README.md or QUICKSTART.md"
echo ""
