@echo off
REM Cloud System Failure Prediction - Windows Setup Script
REM Automatically sets up the project environment

echo.
echo ====================================================================
echo   Cloud System Failure Prediction - Automated Setup (Windows)
echo ====================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version

REM Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo [OK] pip is available

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment created

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment activated

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo Please check requirements.txt and try again
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully

REM Verify setup
echo.
echo Verifying setup...
python verify_setup.py

if errorlevel 1 (
    echo [WARNING] Some checks failed, but you can try running the project
    echo.
else
    echo [OK] All checks passed!
    echo.
)

REM Display next steps
echo ====================================================================
echo   Setup Complete!
echo ====================================================================
echo.
echo To run the project:
echo   1. Make sure venv is activated: venv\Scripts\activate.bat
echo   2. Run: python run.py
echo   3. Check results in: experiments\
echo.
echo To use Jupyter Notebook:
echo   1. Make sure venv is activated
echo   2. Run: jupyter notebook notebooks\experiments.ipynb
echo.
echo For more information, see README.md or QUICKSTART.md
echo.
pause
