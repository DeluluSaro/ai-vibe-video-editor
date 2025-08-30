@echo off
setlocal EnableDelayedExpansion

REM 🎬 Vibe Video Editor - Windows Installation Script
REM This script will set up everything you need to run the application

echo 🎬 Welcome to Vibe Video Editor Installation!
echo ==================================================
echo.

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8 or higher.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python !PYTHON_VERSION! found

REM Check if FFmpeg is installed
echo [INFO] Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] FFmpeg is not installed. Some features may not work properly.
    echo.
    echo To install FFmpeg:
    echo   Windows: Download from https://ffmpeg.org/download.html
    echo   Or use chocolatey: choco install ffmpeg
    echo.
    set /p continue="Continue anyway? (y/N): "
    if /i not "!continue!"=="y" exit /b 1
)

REM Create virtual environment
echo [INFO] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [INFO] Installing Python dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo [SUCCESS] Dependencies installed successfully
) else (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

REM Setup environment file
echo [INFO] Setting up environment configuration...
if not exist ".env" (
    if exist ".env.template" (
        copy .env.template .env >nul
        echo [SUCCESS] Environment file created from template
    ) else (
        echo [ERROR] .env.template not found!
        pause
        exit /b 1
    )
) else (
    echo [WARNING] Environment file already exists
)

REM Check for API keys
echo [INFO] Checking API key configuration...
findstr "your_groq_api_key_here" .env >nul
if %errorlevel% equ 0 (
    echo [WARNING] Groq API key not configured
    echo.
    echo 📝 You need to add your API keys to the .env file:
    echo    1. Get Groq API key: https://console.groq.com/
    echo    2. Get Hugging Face key: https://huggingface.co/settings/tokens
    echo    3. Edit .env file and replace placeholder values
    echo.
)

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "temp" mkdir temp
if not exist "uploads" mkdir uploads
if not exist "exports" mkdir exports
echo [SUCCESS] Directories created

REM Test installation
echo [INFO] Testing installation...
python -c "import streamlit; import moviepy; import whisper; import cv2; import langchain; print('✅ All core modules imported successfully')" 2>nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Installation test passed
) else (
    echo [ERROR] Installation test failed - some modules may be missing
)

REM Final instructions
echo.
echo 🎉 Installation completed successfully!
echo ==================================================
echo.
echo 🚀 To start the application:
echo    1. Make sure your API keys are set in .env file
echo    2. Run: streamlit run app.py
echo    3. Open your browser to http://localhost:8501
echo.
echo 📚 Need help?
echo    - Read PROJECT_STRUCTURE.md for detailed documentation
echo    - Check README.md for troubleshooting tips
echo    - Visit our GitHub repository for support
echo.
echo Happy editing! 🎬✨

pause
