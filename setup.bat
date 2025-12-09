@echo off
REM ============================================
REM Dynamic Workload Distribution System
REM One-Click Setup Script for Windows
REM ============================================

echo.
echo ============================================
echo Dynamic Workload Distribution System
echo Setup Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Python version...
python --version
echo.

echo [2/3] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [3/3] Installing required packages...
python -m pip install -r requirements.txt
echo.

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install some packages!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Setup completed successfully!
echo ============================================
echo.
echo You can now run the simulation with:
echo   python main.py
echo.
echo Or test the installation with:
echo   python SIMPLE_TEST.py
echo.
pause

