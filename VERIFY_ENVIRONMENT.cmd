@echo off
cd /d "%~dp0backend"
if not exist .venv\Scripts\python.exe (
  echo Backend environment not found. Run START_BACKEND.cmd once first.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
python verify_environment.py
pause
