@echo off
title Gemma Data Assistant
echo ========================================
echo   Gemma Data Assistant - Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >NUL 2>NUL
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python found.
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        echo.
        pause
        exit /b 1
    )
    echo Installing dependencies...
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies.
        echo.
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed successfully!
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo Starting Gemma Data Assistant...
echo Open http://localhost:8501 in your browser
echo.
echo Press Ctrl+C to stop the server.
echo.
streamlit run app.py

echo.
echo Application stopped.
pause
