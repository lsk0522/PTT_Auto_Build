@echo off
setlocal

echo ==========================================
echo PPT Generator UI Start Script
echo ==========================================
echo.

:: Check if Rust is installed
rustc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Rust is not installed or not in PATH.
    echo Please install Rust from https://rustup.rs/ before running the UI.
    pause
    exit /b 1
)

cd ui

echo Installing node modules...
call npm install
if %errorlevel% neq 0 (
    echo Error: Failed to install node modules.
    pause
    exit /b %errorlevel%
)

echo.
echo Starting Tauri Development Window...
call npm run tauri dev

pause
