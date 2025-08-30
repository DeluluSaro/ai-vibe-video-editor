@echo off

echo 🎬 Starting Vibe Video Editor...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ FFmpeg is not installed. Some features may not work properly.
    echo Please install FFmpeg: https://ffmpeg.org/download.html
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo ⚙️ Creating environment file from template...
    copy .env.template .env
    echo 📝 Please edit .env file and add your API keys!
    echo    - GROQ_API_KEY: Get from https://console.groq.com/
    echo    - HUGGINGFACE_API_KEY: Get from https://huggingface.co/settings/tokens
)

REM Start Streamlit app
echo 🚀 Launching Vibe Video Editor...
streamlit run app.py

REM Deactivate virtual environment when done
deactivate

pause
