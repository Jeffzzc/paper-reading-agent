@echo off
echo Starting Paper Reading Agent System...

cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    .\venv\Scripts\pip install -r requirements.txt
)

echo Activating virtual environment...
call .\venv\Scripts\activate

echo Starting backend server...
python -m app.main
pause
