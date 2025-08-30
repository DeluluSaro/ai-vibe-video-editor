#!/bin/bash

# 🎬 Vibe Video Editor - Comprehensive Installation Script
# This script will set up everything you need to run the application

echo "🎬 Welcome to Vibe Video Editor Installation!"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
    print_success "Python version is compatible (3.8+)"
else
    print_error "Python 3.8 or higher is required. Found Python $PYTHON_MAJOR.$PYTHON_MINOR"
    exit 1
fi

# Check if FFmpeg is installed
print_status "Checking FFmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version | head -n1 | cut -d' ' -f3)
    print_success "FFmpeg $FFMPEG_VERSION found"
else
    print_warning "FFmpeg is not installed. Some features may not work properly."
    echo ""
    echo "To install FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org/download.html"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
print_status "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Dependencies installed successfully"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Setup environment file
print_status "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.template" ]; then
        cp .env.template .env
        print_success "Environment file created from template"
    else
        print_error ".env.template not found!"
        exit 1
    fi
else
    print_warning "Environment file already exists"
fi

# Check for API keys
print_status "Checking API key configuration..."
if grep -q "your_groq_api_key_here" .env; then
    print_warning "Groq API key not configured"
    echo ""
    echo "📝 You need to add your API keys to the .env file:"
    echo "   1. Get Groq API key: https://console.groq.com/"
    echo "   2. Get Hugging Face key: https://huggingface.co/settings/tokens"
    echo "   3. Edit .env file and replace placeholder values"
    echo ""
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p temp
mkdir -p uploads
mkdir -p exports
print_success "Directories created"

# Test installation
print_status "Testing installation..."
python3 -c "
import streamlit
import moviepy
import whisper
import cv2
import langchain
print('✅ All core modules imported successfully')
" 2>/dev/null

if [ $? -eq 0 ]; then
    print_success "Installation test passed"
else
    print_error "Installation test failed - some modules may be missing"
fi

# Final instructions
echo ""
echo "🎉 Installation completed successfully!"
echo "=================================================="
echo ""
echo "🚀 To start the application:"
echo "   1. Make sure your API keys are set in .env file"
echo "   2. Run: streamlit run app.py"
echo "   3. Open your browser to http://localhost:8501"
echo ""
echo "📚 Need help?"
echo "   - Read PROJECT_STRUCTURE.md for detailed documentation"
echo "   - Check README.md for troubleshooting tips"
echo "   - Visit our GitHub repository for support"
echo ""
echo "Happy editing! 🎬✨"

# Deactivate virtual environment
deactivate
