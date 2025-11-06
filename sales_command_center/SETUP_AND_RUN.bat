@echo off
REM Sales Command Center - Complete Setup and Run Script
REM This script sets up the database and starts the application

echo.
echo ============================================================
echo   SALES COMMAND CENTER - Setup and Run
echo ============================================================
echo.

REM Check if PostgreSQL is installed
echo [1/5] Checking PostgreSQL installation...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: PostgreSQL is not installed or not in PATH
    echo Please install PostgreSQL 15+ from https://www.postgresql.org/download/
    pause
    exit /b 1
)
echo ✓ PostgreSQL found
echo.

REM Check if Python is installed
echo [2/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✓ Python found
echo.

REM Check if database exists, if not create it
echo [3/5] Setting up database...
psql -U postgres -lqt | findstr /C:"sales_command_center" >nul 2>&1
if %errorlevel% neq 0 (
    echo Creating database 'sales_command_center'...
    createdb -U postgres sales_command_center
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create database
        echo Please check PostgreSQL credentials
        pause
        exit /b 1
    )
    echo ✓ Database created
) else (
    echo ✓ Database already exists
)
echo.

REM Run schema if tables don't exist
echo [4/5] Creating database schema and loading test data...
cd sales_dashboard\database

REM Run schema creation
echo Running schema.sql...
psql -U postgres -d sales_command_center -f schema.sql
if %errorlevel% neq 0 (
    echo ERROR: Failed to create schema
    pause
    exit /b 1
)
echo ✓ Schema created

REM Load test data
echo Loading test data...
psql -U postgres -d sales_command_center -f seed_data.sql
if %errorlevel% neq 0 (
    echo ERROR: Failed to load test data
    pause
    exit /b 1
)
echo ✓ Test data loaded successfully
echo.

cd ..\..

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

echo [5/5] Starting Sales Command Center...
echo.
echo ============================================================
echo   Application is starting...
echo ============================================================
echo.
echo   Frontend Dashboard: file:///C:/Users/pbkap/Documents/euron/Projects/salescommandcenter/sales_command_center/frontend/sales_dashboard.html
echo   API Documentation: http://localhost:8000/docs
echo   API Base URL: http://localhost:8000
echo.
echo   Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

REM Open the frontend dashboard in browser
start "" "C:\Users\pbkap\Documents\euron\Projects\salescommandcenter\sales_command_center\frontend\sales_dashboard.html"

REM Note: API server would start here when implemented
echo.
echo SUCCESS! Sales Command Center is ready!
echo.
echo NEXT STEPS:
echo 1. The dashboard should have opened in your browser
echo 2. To implement the API server, complete the FastAPI endpoints
echo 3. Update frontend API_BASE to http://localhost:8000
echo.
pause
