@echo off
echo ================================================
echo    Aegis Mental Wellness Platform - Frontend
echo ================================================
echo.

cd frontend

echo Starting frontend server...
echo Frontend will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python -m http.server 8000

pause
