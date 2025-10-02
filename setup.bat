@echo off
echo Setting up Vehicle Detection System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found. Creating virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .\.venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup complete! 
echo.
echo To run the system:
echo   1. Activate environment: .\.venv\Scripts\activate.bat
echo   2. Run detection: python vehicle_detection_main_yolo.py imshow
echo.
pause
