@echo off
REM QAUTO Installation Script for Windows
REM This script sets up the QAUTO CLI tool

echo ==================================
echo QAUTO CLI Tool - Windows Setup
echo ==================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python is installed.
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install pyyaml openpyxl
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo [OK] Dependencies installed.
echo.

REM Create batch file wrapper
echo Creating 'qauto.bat' wrapper...
set SCRIPT_DIR=%~dp0
set WRAPPER=%SCRIPT_DIR%qauto.bat

echo @echo off > "%WRAPPER%"
echo python "%SCRIPT_DIR%qauto.py" %%* >> "%WRAPPER%"

echo [OK] Created %WRAPPER%
echo.

REM Instructions for adding to PATH
echo ==================================
echo Installation Complete!
echo ==================================
echo.
echo To run 'qauto' from anywhere, add this folder to your PATH environment variable:
echo.
echo %SCRIPT_DIR%
echo.
echo How to add to PATH:
echo 1. Search for "Edit the system environment variables" in Start menu
echo 2. Click "Environment Variables"
echo 3. Under "User variables", select "Path" and click "Edit"
echo 4. Click "New" and paste the path above
echo 5. Click OK on all windows
echo.
echo Quick Start:
echo 1. Open a new terminal
echo 2. Navigate to your screenshots folder
echo 3. Run: qauto prepare
echo.
pause
