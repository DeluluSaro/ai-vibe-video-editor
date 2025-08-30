import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import streamlit as st
import os
import tempfile
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Vibe Video Editor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }

    .vibe-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }


            
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }

    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 Vibe Video Editor</h1>
        <p>AI-Powered Video Editing with Mood Detection & Smart Styling</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("🎥 Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "🏠 Home", 
        "🎬 Video Editor", 
        "📊 Analytics",
        "⚙️ Settings"
    ])

    if page == "🏠 Home":
        show_home_page()
    elif page == "🎬 Video Editor":
        show_editor_page()
    elif page == "📊 Analytics":
        show_analytics_page()
    elif page == "⚙️ Settings":
        show_settings_page()

def show_home_page():
    st.markdown("## Welcome to Vibe Video Editor!")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI-Powered Analysis</h3>
            <p>Automatically detects the mood and vibe of your content using advanced AI models from Groq and Hugging Face.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>🎨 Smart Styling</h3>
            <p>Applies appropriate editing styles based on detected vibes: Energetic, Calm, Professional, Fun, Dramatic, or Minimalist.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 Transcript Editing</h3>
            <p>Edit your video by simply editing the transcript. Remove filler words, fix punctuation, and restructure content easily.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Real-time Processing</h3>
            <p>Powered by Groq's lightning-fast inference and LangChain's robust agent framework for seamless user experience.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚀 Get Started")
    st.markdown("1. Go to the **Video Editor** page")
    st.markdown("2. Upload your video file")
    st.markdown("3. Let AI analyze the vibe")
    st.markdown("4. Edit transcript and apply styles")
    st.markdown("5. Export your enhanced video!")

def show_editor_page():
    st.markdown("## 🎬 Video Editor")
    st.write("Upload and edit your videos with AI-powered vibe detection!")

    # Import editor components
    from pages.video_editor import VideoEditorApp

    editor_app = VideoEditorApp()
    editor_app.run()

def show_analytics_page():
    st.markdown("## 📊 Analytics Dashboard")
    st.info("Analytics dashboard coming soon! This will show statistics about your video projects, vibe distributions, and usage patterns.")

    # Placeholder analytics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Projects", "12", "+3")
    with col2:
        st.metric("Hours Processed", "45.2", "+12.1")
    with col3:
        st.metric("AI Accuracy", "94.2%", "+2.1%")

def show_settings_page():
    st.markdown("## ⚙️ Settings")

    st.subheader("API Configuration")

    # API Keys section
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Groq API")
        groq_api_key = st.text_input("Groq API Key", type="password", help="Get your API key from https://console.groq.com/")
        if groq_api_key:
            os.environ["GROQ_API_KEY"] = groq_api_key
            st.success("✅ Groq API Key saved!")

    with col2:
        st.markdown("### Hugging Face API")
        hf_api_key = st.text_input("Hugging Face API Key", type="password", help="Get your API key from https://huggingface.co/settings/tokens")
        if hf_api_key:
            os.environ["HUGGINGFACE_API_KEY"] = hf_api_key
            st.success("✅ Hugging Face API Key saved!")

    st.subheader("Processing Settings")

    col1, col2 = st.columns(2)
    with col1:
        st.slider("Video Quality", 480, 1080, 720, step=240, help="Output video resolution")
        st.slider("Audio Quality", 128, 320, 192, step=64, help="Audio bitrate in kbps")

    with col2:
        st.selectbox("Default Vibe", ["Auto-detect", "Energetic", "Calm", "Professional", "Fun", "Dramatic", "Minimalist"])
        st.checkbox("Auto-remove filler words", value=True)

    st.subheader("Export Settings")
    st.selectbox("Export Format", ["MP4", "MOV", "AVI", "WebM"])
    st.slider("Export Quality", 1, 10, 8, help="1 = Fastest, 10 = Best Quality")

    if st.button("Save Settings"):
        st.success("✅ Settings saved successfully!")

if __name__ == "__main__":
    main()
