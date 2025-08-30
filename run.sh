#!/bin/bash

# Vibe Video Editor - Startup Script

echo "🎬 Starting Vibe Video Editor..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if FFmpeg is installed  
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️ FFmpeg is not installed. Some features may not work properly."
    echo "Please install FFmpeg: https://ffmpeg.org/download.html"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚙️ Creating environment file from template..."
    cp .env.template .env
    echo "📝 Please edit .env file and add your API keys!"
    echo "   - GROQ_API_KEY: Get from https://console.groq.com/"
    echo "   - HUGGINGFACE_API_KEY: Get from https://huggingface.co/settings/tokens"
fi

# Start Streamlit app
echo "🚀 Launching Vibe Video Editor..."
streamlit run app.py

# Deactivate virtual environment when done
deactivate
