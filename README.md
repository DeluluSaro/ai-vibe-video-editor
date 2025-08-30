# 🎬 Vibe Video Editor

AI-Powered Video Editing with Mood Detection & Smart Styling using LangChain, Streamlit, Groq & Hugging Face

![Vibe Video Editor](https://img.shields.io/badge/AI-Powered-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-121212?logo=chainlink&logoColor=white) ![Groq](https://img.shields.io/badge/Groq-FF6B35) ![Hugging Face](https://img.shields.io/badge/🤗-Hugging%20Face-yellow)

## ✨ Features

🤖 **AI-Powered Vibe Detection** - Automatically analyzes video content to detect mood and atmosphere
🎨 **Smart Styling** - Applies appropriate visual effects, transitions, and color grading based on detected vibe
📝 **Intelligent Transcript Editing** - Edit videos by editing text transcripts with AI assistance
⚡ **Real-time Processing** - Powered by Groq's lightning-fast inference
🎵 **Music & Audio Suggestions** - AI recommends appropriate background music and audio effects
🌊 **Multiple Vibe Types** - Supports Energetic, Calm, Professional, Fun, Dramatic, and Minimalist vibes
🎬 **Export Options** - Multiple resolution and format options for final video export

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system
- Groq API key (get it from [console.groq.com](https://console.groq.com/))
- Hugging Face API key (get it from [huggingface.co](https://huggingface.co/settings/tokens))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/vibe-video-editor.git
cd vibe-video-editor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables**
```bash
cp .env.template .env
# Edit .env file and add your API keys:
# GROQ_API_KEY=your_groq_api_key_here
# HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

4. **Install FFmpeg** (if not already installed)

**On Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add to PATH environment variable

**On macOS:**
```bash
brew install ffmpeg
```

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Upload Video
- Navigate to the **Upload** tab
- Choose your video file (MP4, MOV, AVI, MKV)
- Click "Start AI Analysis" to process the video

### 2. Vibe Analysis
- View the AI-detected vibe and confidence score
- Choose a different vibe if desired
- Review AI suggestions for music and effects

### 3. Edit Transcript
- Review the generated transcript
- Edit text directly to modify video content
- Use AI tools to remove filler words and fix punctuation
- Delete unwanted segments

### 4. Apply Styling
- Configure visual effects based on selected vibe
- Adjust audio settings and background music
- Set export quality and format
- Generate the final styled video

## 🛠️ Technology Stack

- **Frontend**: Streamlit for web interface
- **AI Orchestration**: LangChain for agent workflows
- **LLM Inference**: Groq for fast AI processing
- **ML Models**: Hugging Face Transformers
- **Speech Recognition**: OpenAI Whisper
- **Video Processing**: MoviePy, OpenCV
- **Audio Processing**: FFmpeg, PyAudio

## 🎯 Vibe Types & Effects

### ⚡ Energetic
- **Visual**: Quick cuts, zoom transitions, high contrast, vibrant colors
- **Audio**: Upbeat electronic, rock anthems, high-energy music
- **Style**: Dynamic, fast-paced, exciting

### 🌊 Calm  
- **Visual**: Slow fades, gentle transitions, soft lighting, cool colors
- **Audio**: Ambient music, nature sounds, soft piano
- **Style**: Peaceful, relaxing, meditative

### 💼 Professional
- **Visual**: Clean cuts, corporate templates, neutral grading
- **Audio**: Corporate background music, minimal electronic
- **Style**: Business-focused, polished, formal

### 🎉 Fun
- **Visual**: Playful transitions, bright colors, animated elements
- **Audio**: Pop music, upbeat indie, comedy tracks
- **Style**: Entertainment-focused, colorful, playful

### 🎭 Dramatic
- **Visual**: Slow motion, dramatic lighting, high contrast
- **Audio**: Cinematic orchestral, emotional scores
- **Style**: Emotional, storytelling, intense

### ⚪ Minimalist
- **Visual**: Simple cuts, clean typography, negative space
- **Audio**: Minimal ambient, subtle soundscapes
- **Style**: Clean, simple, understated

## 📁 Project Structure

```
vibe-video-editor/
├── app.py                 # Main Streamlit application
├── pages/
│   └── video_editor.py    # Video editor page components
├── utils/
│   ├── ai_utils.py        # AI processing utilities
│   ├── video_utils.py     # Video processing utilities  
│   └── langchain_agents.py # LangChain agent implementations
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
├── .env.template         # Environment variables template
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

```env
# Required API Keys
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Optional Settings
STREAMLIT_SERVER_PORT=8501
MAX_VIDEO_SIZE_MB=500
WHISPER_MODEL=base
DEFAULT_VIBE=auto-detect
```

### Customizing Vibes

You can customize vibe detection and styling by modifying the `vibe_options` dictionary in `pages/video_editor.py`:

```python
self.vibe_options = {
    'your_custom_vibe': {
        'label': 'Your Custom Vibe 🎨',
        'color': '#custom_color',
        'description': 'Description of your vibe',
        'music_style': 'Preferred music style',
        'editing_style': 'Visual editing approach'
    }
}
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/vibe-video-editor.git

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 pre-commit

# Setup pre-commit hooks
pre-commit install
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for the Whisper speech recognition model
- Groq for lightning-fast LLM inference
- Hugging Face for the transformer models and ecosystem
- LangChain for the agent framework
- Streamlit for the amazing web app framework
- MoviePy for video processing capabilities

## 🐛 Troubleshooting

### Common Issues

**FFmpeg not found:**
```bash
# Ensure FFmpeg is installed and in PATH
ffmpeg -version
```

**API Key errors:**
- Verify your API keys are correct in the `.env` file
- Check that you have sufficient API credits/quota

**Memory issues with large videos:**
- Try using a smaller Whisper model (tiny or base)
- Reduce video resolution before processing
- Close other memory-intensive applications

**Slow processing:**
- Use Groq API for faster inference
- Consider upgrading your hardware (CPU/RAM)
- Process shorter video segments

### Getting Help

- 📧 Email: developer@example.com
- 💬 Discord: [Join our community](https://discord.gg/your-server)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/vibe-video-editor/issues)
- 📖 Docs: [Full Documentation](https://docs.your-domain.com)

## 🔮 Roadmap

- [ ] Real-time collaborative editing
- [ ] Advanced AI-powered scene detection  
- [ ] Custom model training for domain-specific vibes
- [ ] API for programmatic access
- [ ] Mobile app version
- [ ] Integration with popular video platforms
- [ ] Advanced audio analysis and enhancement
- [ ] Multi-language support for transcripts

---

**Made with ❤️ by the AI community**

*Transform your videos with the power of AI!*
