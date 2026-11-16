@echo off
cd /d "%~dp0backend"
if not exist .venv\Scripts\python.exe (
  echo Creating Python 3.11 virtual environment...
  py -3.11 -m venv .venv
  if errorlevel 1 python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
pause
