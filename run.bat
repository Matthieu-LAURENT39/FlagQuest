@echo off

REM Check if Python is installed
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installé. Installer le et réessayer.
    echo La version recommandé et testé est Python 3.10.10
    echo Lien: https://www.python.org/downloads/release/python-31010/
    pause
    exit /b 1
)

echo ==============================
echo Mise en place des requirements
echo ==============================

REM Create a new virtual environment
py -3 -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Install the required dependencies from requirements.txt
pip install -r requirements.txt

REM Set the FLASK_APP environment variable
set FLASK_APP=main.py

cls
echo =====================
echo Lancement du site web
echo =====================

REM Start the Flask app
REM flask run
waitress-serve --port=5000 --call main:create_app