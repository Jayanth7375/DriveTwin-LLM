@echo off
echo Starting Drive-Twin Diagnostics System...

echo Starting FastAPI Backend...
start "Drive-Twin Backend" cmd /k "cd backend && python -m uvicorn app.main:app --port 8000"

echo Starting Vite Frontend...
start "Drive-Twin Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting up in separate windows.
echo - Frontend UI will be available at: http://localhost:3000
echo - Backend API will be available at: http://localhost:8000
echo.
pause

