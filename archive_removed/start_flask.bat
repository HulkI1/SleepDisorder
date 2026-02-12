@echo off
REM Sleep Disorder Analysis Platform - Flask Startup Script (Windows)

echo ========================================================
echo  Sleep Disorder Analysis Platform - Flask Startup
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Flask not found, installing dependencies...
    pip install -r requirements.txt
)

echo Checking directories...
if not exist "data" mkdir data
if not exist "ml" mkdir ml
if not exist "templates" mkdir templates

echo Directories ready.
echo.

echo Starting Flask server on http://localhost:5000...
echo ========================================================
echo.
echo Press Ctrl+C to stop the server
echo.

python flask_app.py

pause
