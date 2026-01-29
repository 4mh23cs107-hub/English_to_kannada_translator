@echo off
REM English to Kannada Translator - Windows Startup Script

echo.
echo ========================================
echo English to Kannada Translator
echo Full-Stack Web Application
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Run the Flask app
echo.
echo ========================================
echo Starting server at http://localhost:5000
echo Press Ctrl+C to stop the server
echo ========================================
echo.
python app.py

pause
