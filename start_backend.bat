@echo off
echo ================================================
echo    Aegis Mental Wellness Platform - Backend
echo ================================================
echo.

cd backend

echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist myenv\Scripts\activate.bat (
    call myenv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\activate
    echo Then run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Starting Flask backend server...
echo Backend will be available at: http://localhost:5000
echo.

python app.py

pause
