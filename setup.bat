@echo off
REM Interview Automation Engine - Setup Script for Windows

echo ==========================================
echo Interview Automation Engine - Setup
echo ==========================================
echo.

REM Check Python version
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo Dependencies installed
echo.

REM Create reports directory
echo Creating reports directory...
if not exist "backend\reports\output" (
    mkdir backend\reports\output
    echo Reports directory created
) else (
    echo Reports directory already exists
)
echo.

REM Summary
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Start the backend server:
echo    cd backend
echo    python app.py
echo.
echo 2. In another terminal, start a local server for frontend:
echo    cd frontend
echo    python -m http.server 8000
echo.
echo 3. Open browser and navigate to:
echo    http://localhost:8000
echo.
echo ==========================================
pause
