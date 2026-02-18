@echo off
echo ============================================================
echo Lost & Found Platform - Backend Setup and Test
echo ============================================================
echo.

echo Step 1: Verifying setup...
python verify_setup.py
if %errorlevel% neq 0 (
    echo.
    echo Setup verification failed. Please fix the issues above.
    pause
    exit /b 1
)

echo.
echo Step 2: Starting FastAPI server...
echo Server will start at http://localhost:8000
echo API docs will be available at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
start "FastAPI Server" cmd /k "uvicorn main:app --reload"

timeout /t 3 /nobreak >nul

echo.
echo Step 3: Waiting for server to start...
timeout /t 5 /nobreak >nul

echo.
echo Step 4: Running API tests...
python test_api.py

echo.
echo ============================================================
echo Setup complete!
echo ============================================================
echo.
echo The server is running in a separate window.
echo You can:
echo   - View API docs: http://localhost:8000/docs
echo   - Test endpoints manually
echo   - Close the server window to stop it
echo.
pause

