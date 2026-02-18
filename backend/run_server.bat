@echo off
echo ============================================================
echo Starting Lost & Found Platform API Server
echo ============================================================
echo.

cd /d "%~dp0"

echo Starting server...
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

py -c "import sys; sys.path.insert(0, r'D:\Lib\site-packages'); import uvicorn; uvicorn.run('main:app', host='127.0.0.1', port=8000, log_level='info')"

pause

