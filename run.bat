@echo off
echo ========================================
echo    SAAS Change Detection Engine
echo ========================================

echo Checking Python...

where py >nul 2>nul
if %errorlevel% == 0 (
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo Using %PYTHON_CMD% ...

:: Create venv if not exists
if not exist venv (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv
) else (
    echo Virtual environment already exists.
)

call venv\Scripts\activate

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt

:: Create .env if missing
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please edit .env with your PostgreSQL details now!
    pause
)

echo.
echo ✅ Ready!
echo 🚀 Starting server on http://localhost:8000
echo Press Ctrl + C to stop.
echo.

uvicorn app.main:app --reload --port 8000