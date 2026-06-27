@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo PPT Generator Engine Test Script
echo ==========================================
echo.

:: Check if API key is already set
if "%GEMINI_API_KEY%"=="" (
    set /p "GEMINI_API_KEY=Enter your Gemini API Key: "
    if "!GEMINI_API_KEY!"=="" (
        echo Error: API Key is required to run the LLM.
        pause
        exit /b 1
    )
)

echo.
echo Installing dependencies (if not already installed)...
cd engine
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install requirements.
    pause
    exit /b %errorlevel%
)

echo.
echo Running the PPT Generator Engine...
python design2ppt.py --design ../test_design.md --input ../test_input.txt --out ../output.pptx --raw

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo Success! output.pptx has been generated.
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo Failed to generate PPT. Please check the errors above.
    echo ==========================================
)

pause
