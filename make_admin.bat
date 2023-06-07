@echo off

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Set the FLASK_APP environment variable
set FLASK_APP=main.py

REM on récupère le username
set /p "username=Nom d'utilisateur: "

flask make-admin %%username%%

pause
