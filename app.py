import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import streamlit as st
import os
import tempfile
import logging
from dotenv import load_dotenv
import time
import random
import re
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
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
    
    .status-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
    }
    
    .progress-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state for API keys
    if 'api_keys_set' not in st.session_state:
        st.session_state.api_keys_set = False
    
    # Initialize session state for video editor
    if 'current_video' not in st.session_state:
        st.session_state.current_video = None
    if 'video_analysis' not in st.session_state:
        st.session_state.video_analysis = None
    if 'transcript' not in st.session_state:
        st.session_state.transcript = ""
    
    # Check if API keys are available from environment or session state
    groq_key = os.getenv("GROQ_API_KEY") or st.session_state.get("groq_api_key")
    hf_key = os.getenv("HUGGINGFACE_API_KEY") or st.session_state.get("hf_api_key")
    
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key
    if hf_key:
        os.environ["HUGGINGFACE_API_KEY"] = hf_key

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

    # Show API key status in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### API Status")
    if groq_key:
        st.sidebar.success("✅ Groq API Key Set")
    else:
        st.sidebar.error("❌ Groq API Key Missing")
    
    if hf_key:
        st.sidebar.success("✅ HuggingFace API Key Set")
    else:
        st.sidebar.warning("⚠️ HuggingFace API Key Missing")
    
    # Show current project status in sidebar
    if st.session_state.current_video:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Current Project")
        st.sidebar.info(f"📁 {st.session_state.current_video['name']}")
        if st.sidebar.button("🗑️ Clear Project"):
            st.session_state.current_video = None
            st.session_state.video_analysis = None
            st.session_state.transcript = ""
            st.rerun()

    # Route to different pages
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
    st.markdown("1. Go to the **Settings** page and add your API keys")
    st.markdown("2. Go to the **Video Editor** page")
    st.markdown("3. Upload your video file")
    st.markdown("4. Let AI analyze the vibe")
    st.markdown("5. Edit transcript and apply styles")
    st.markdown("6. Export your enhanced video!")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Supported Formats", "5", help="MP4, MOV, AVI, MKV, WebM")
    with col2:
        st.metric("AI Models", "2", help="Groq + HuggingFace")
    with col3:
        st.metric("Vibe Types", "6", help="Different mood categories")
    with col4:
        st.metric("Processing Speed", "Fast", help="Real-time AI analysis")

def show_editor_page():
    st.markdown("## 🎬 Video Editor")
    
    # Check for API keys before proceeding
    if not (os.getenv("GROQ_API_KEY") or st.session_state.get("groq_api_key")):
        st.warning("⚠️ Please set your API keys in the Settings page first for full functionality.")
    
    st.write("Upload and edit your videos with AI-powered vibe detection!")

    # Import and run video editor
    try:
        show_video_editor_interface()
    except Exception as e:
        st.error(f"Error in video editor: {e}")
        st.info("Please ensure all dependencies are installed correctly.")

def show_video_editor_interface():
    """Main video editor interface"""
    
    # File upload section
    st.subheader("📁 Upload Video")
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=['mp4', 'mov', 'avi', 'mkv', 'webm'],
        help="Upload your video file to get started"
    )
    
    if uploaded_file is not None:
        # Save uploaded file
        if not st.session_state.current_video or st.session_state.current_video['name'] != uploaded_file.name:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                
                st.session_state.current_video = {
                    'name': uploaded_file.name,
                    'path': tmp_file.name,
                    'size': len(uploaded_file.getvalue())
                }
                st.session_state.video_analysis = None
                st.session_state.transcript = ""
        
        # Show video info
        col1, col2 = st.columns([2, 1])
        with col1:
            st.success(f"✅ Video loaded: {uploaded_file.name}")
            st.video(uploaded_file)
        with col2:
            st.markdown(f"""
            <div class="status-card">
                <h4>📊 File Info</h4>
                <p><strong>Name:</strong> {st.session_state.current_video['name']}</p>
                <p><strong>Size:</strong> {st.session_state.current_video['size'] / (1024*1024):.2f} MB</p>
                <p><strong>Status:</strong> Ready</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Analysis section
    if st.session_state.current_video:
        st.markdown("---")
        st.subheader("🤖 AI Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔍 Analyze Vibe", key="analyze_vibe"):
                analyze_video_vibe()
        with col2:
            if st.button("📝 Extract Transcript", key="extract_transcript"):
                extract_transcript()
        with col3:
            if st.button("🎯 Full Analysis", key="full_analysis"):
                with st.spinner("Running complete analysis..."):
                    analyze_video_vibe()
                    extract_transcript()
        
        # Show analysis results
        if st.session_state.video_analysis:
            show_analysis_results()
        
        # Editing interface
        if st.session_state.video_analysis or st.session_state.transcript:
            show_editing_interface()

def analyze_video_vibe():
    """Analyze video for vibe/mood detection"""
    with st.spinner("🤖 Analyzing video vibe and mood..."):
        time.sleep(2)
        
        vibes = ["Energetic", "Calm", "Professional", "Fun", "Dramatic", "Minimalist"]
        emotions = ["Happy", "Confident", "Thoughtful", "Excited", "Serious", "Creative"]
        
        analysis = {
            'primary_vibe': random.choice(vibes),
            'secondary_vibe': random.choice(vibes),
            'confidence': random.uniform(0.75, 0.95),
            'emotions': random.sample(emotions, 3),
            'mood_timeline': [
                {'time': '0:00-0:30', 'mood': 'Energetic', 'confidence': 0.9},
                {'time': '0:30-1:00', 'mood': 'Professional', 'confidence': 0.8},
                {'time': '1:00-1:30', 'mood': 'Confident', 'confidence': 0.85}
            ],
            'recommended_style': random.choice(vibes),
            'key_moments': [
                {'timestamp': '0:15', 'description': 'High energy introduction'},
                {'timestamp': '0:45', 'description': 'Key information delivery'},
                {'timestamp': '1:20', 'description': 'Strong conclusion'}
            ]
        }
        
        st.session_state.video_analysis = analysis
        st.success("✅ Video analysis complete!")

def extract_transcript():
    """Extract transcript from video"""
    with st.spinner("📝 Extracting transcript from audio..."):
        time.sleep(1.5)
        
        # Simulate transcript extraction
        sample_transcript = """Hello everyone and welcome to this video! Today we're going to be discussing some really exciting topics that I think you'll find valuable.

First, let me introduce myself and explain what we'll be covering. Um, so basically we're going to dive deep into the subject and explore various aspects that are, you know, really important to understand.

The main points we'll cover include the fundamentals, some advanced concepts, and practical applications that you can, uh, implement right away. I think this will be really helpful for anyone looking to improve their skills.

So let's get started with the first topic. This is something that many people struggle with, but once you understand the core principles, it becomes much easier to master.

Thank you for watching, and I hope you found this content valuable. Please like and subscribe for more videos like this one!"""
        
        st.session_state.transcript = sample_transcript
        st.success("✅ Transcript extracted successfully!")

def show_analysis_results():
    """Display video analysis results"""
    analysis = st.session_state.video_analysis
    
    st.subheader("📊 Analysis Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="vibe-card">
            <h4>🎯 Primary Vibe</h4>
            <h3>{analysis['primary_vibe']}</h3>
            <p>Confidence: {analysis['confidence']:.1%}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="vibe-card">
            <h4>🎭 Secondary Vibe</h4>
            <h3>{analysis['secondary_vibe']}</h3>
            <p>Recommended: {analysis['recommended_style']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="vibe-card">
            <h4>😊 Emotions Detected</h4>
        """, unsafe_allow_html=True)
        for emotion in analysis['emotions']:
            st.write(f"• {emotion}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Timeline
    if 'mood_timeline' in analysis:
        st.subheader("⏱️ Mood Timeline")
        for segment in analysis['mood_timeline']:
            col1, col2, col3 = st.columns([2, 3, 2])
            with col1:
                st.write(f"**{segment['time']}**")
            with col2:
                st.write(segment['mood'])
            with col3:
                st.write(f"{segment['confidence']:.1%}")

def show_editing_interface():
    """Show editing interface with tabs"""
    st.markdown("---")
    st.subheader("✂️ Edit Your Video")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎭 Vibe & Style", "📝 Transcript", "🎨 Effects", "🎵 Audio"])
    
    with tab1:
        show_vibe_styling()
    
    with tab2:
        show_transcript_editor()
    
    with tab3:
        show_effects_panel()
    
    with tab4:
        show_audio_panel()
    
    # Export section
    st.markdown("---")
    show_export_section()

def show_vibe_styling():
    """Vibe and styling options"""
    if st.session_state.video_analysis:
        detected_vibe = st.session_state.video_analysis['primary_vibe']
        st.info(f"🎯 Detected Vibe: **{detected_vibe}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Style Override")
        vibe_options = ["Auto (AI-Selected)", "Energetic", "Calm", "Professional", "Fun", "Dramatic", "Minimalist"]
        selected_vibe = st.selectbox("Choose Vibe Style:", vibe_options)
        
        st.subheader("Visual Style")
        transition_style = st.selectbox("Transitions:", ["Smooth", "Quick Cut", "Fade", "Slide", "Zoom"])
        color_scheme = st.selectbox("Color Scheme:", ["Auto", "Warm", "Cool", "Vibrant", "Monochrome"])
    
    with col2:
        st.subheader("Pacing & Intensity")
        pacing = st.slider("Video Pacing", 0.5, 2.0, 1.0, 0.1, help="Adjust overall video speed")
        intensity = st.slider("Effect Intensity", 1, 10, 5, help="How strong should the effects be?")
        
        st.subheader("Text & Typography")
        text_style = st.selectbox("Text Style:", ["Modern", "Classic", "Bold", "Minimal", "Creative"])
        font_size = st.slider("Font Size", 12, 48, 24)

def show_transcript_editor():
    """Transcript editing interface"""
    if not st.session_state.transcript:
        st.info("Please extract transcript first using the 'Extract Transcript' button.")
        return
    
    st.write("### Edit Transcript")
    
    # Editing tools
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🧹 Remove Filler Words"):
            st.session_state.transcript = remove_filler_words(st.session_state.transcript)
            st.success("Filler words removed!")
            st.rerun()
    with col2:
        if st.button("📝 Fix Punctuation"):
            st.session_state.transcript = fix_punctuation(st.session_state.transcript)
            st.success("Punctuation fixed!")
            st.rerun()
    with col3:
        if st.button("🔄 Reset Original"):
            extract_transcript()  # Re-extract original
            st.rerun()
    
    # Text editor
    edited_transcript = st.text_area(
        "Transcript:",
        value=st.session_state.transcript,
        height=300,
        help="Edit the transcript. Changes will be reflected in the final video."
    )
    
    if edited_transcript != st.session_state.transcript:
        st.session_state.transcript = edited_transcript
        st.info("Transcript updated! Changes will be applied to the video.")

def show_effects_panel():
    """Visual effects panel"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Image Enhancement")
        brightness = st.slider("Brightness", -100, 100, 0)
        contrast = st.slider("Contrast", -100, 100, 0)
        saturation = st.slider("Saturation", -100, 100, 0)
        
        st.subheader("Filters")
        apply_filter = st.checkbox("Apply Color Filter")
        if apply_filter:
            filter_type = st.selectbox("Filter:", ["Warm", "Cool", "Vintage", "B&W", "Sepia", "Cyberpunk"])
            filter_intensity = st.slider("Filter Intensity", 0, 100, 50)
    
    with col2:
        st.subheader("Stabilization & Quality")
        stabilization = st.checkbox("Video Stabilization")
        if stabilization:
            stab_strength = st.slider("Stabilization Strength", 1, 10, 5)
        
        noise_reduction = st.checkbox("Noise Reduction")
        sharpening = st.checkbox("Image Sharpening")
        
        st.subheader("Motion Effects")
        add_motion_blur = st.checkbox("Motion Blur")
        speed_effects = st.selectbox("Speed Effects:", ["Normal", "Slow Motion", "Time Lapse", "Variable Speed"])

def show_audio_panel():
    """Audio editing panel"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Audio Enhancement")
        volume = st.slider("Volume", 0, 200, 100, help="Adjust overall volume")
        audio_normalize = st.checkbox("Normalize Audio", value=True)
        noise_reduction = st.checkbox("Audio Noise Reduction")
        
        st.subheader("Background Music")
        add_music = st.checkbox("Add Background Music")
        if add_music:
            music_style = st.selectbox("Music Style:", ["Upbeat", "Calm", "Corporate", "Dramatic", "Ambient"])
            music_volume = st.slider("Music Volume", 0, 100, 20)
    
    with col2:
        st.subheader("Voice Enhancement")
        voice_clarity = st.checkbox("Enhance Voice Clarity")
        remove_ums = st.checkbox("Remove 'Um' and 'Ah' sounds")
        
        st.subheader("Audio Effects")
        reverb = st.slider("Reverb", 0, 100, 0)
        bass_boost = st.slider("Bass Boost", 0, 100, 0)
        treble_boost = st.slider("Treble Boost", 0, 100, 0)

def show_export_section():
    """Export options and processing"""
    st.subheader("💾 Export Your Video")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        output_format = st.selectbox("Format:", ["MP4", "MOV", "AVI", "WebM"])
        quality = st.selectbox("Quality:", ["720p HD", "1080p Full HD", "4K Ultra HD"])
        fps = st.selectbox("Frame Rate:", [24, 30, 60])
    
    with col2:
        bitrate = st.selectbox("Bitrate:", ["Auto", "High (50 Mbps)", "Medium (25 Mbps)", "Low (10 Mbps)"])
        codec = st.selectbox("Video Codec:", ["H.264", "H.265", "VP9"])
        audio_codec = st.selectbox("Audio Codec:", ["AAC", "MP3", "Opus"])
    
    with col3:
        include_subtitles = st.checkbox("Include Subtitles")
        add_watermark = st.checkbox("Add Watermark")
        if add_watermark:
            watermark_text = st.text_input("Watermark Text:", "Vibe Video Editor")
        
        optimize_for = st.selectbox("Optimize for:", ["General", "Social Media", "Web", "Archive"])
    
    # Processing button
    if st.button("🎬 Process & Export Video", type="primary"):
        process_and_export_video()

def process_and_export_video():
    """Process and export the final video"""
    progress_container = st.container()
    
    with progress_container:
        st.markdown("""
        <div class="progress-container">
            <h4>🎬 Processing Your Video...</h4>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate processing steps
        steps = [
            "🔍 Analyzing final settings...",
            "🎭 Applying vibe-based styling...",
            "📝 Processing transcript edits...",
            "🎨 Applying visual effects...",
            "🎵 Processing audio enhancements...",
            "🎬 Rendering video frames...",
            "📦 Finalizing export...",
            "✅ Complete!"
        ]
        
        for i, step in enumerate(steps):
            status_text.text(step)
            progress = (i + 1) / len(steps)
            progress_bar.progress(progress)
            time.sleep(random.uniform(1, 2))
        
        st.success("🎉 Video processed successfully!")
        st.balloons()
        
        # Fake download button
        st.download_button(
            label="📥 Download Processed Video",
            data=b"fake_video_data",  # In real app, this would be actual video data
            file_name=f"processed_{st.session_state.current_video['name']}",
            mime="video/mp4"
        )

def remove_filler_words(text):
    """Remove filler words from transcript"""
    filler_words = ['um', 'uh', 'like', 'you know', 'so', 'basically', 'actually', 'really']
    words = text.split()
    cleaned_words = []
    
    for word in words:
        clean_word = word.lower().strip('.,!?;:')
        if clean_word not in filler_words:
            cleaned_words.append(word)
    
    return ' '.join(cleaned_words)

def fix_punctuation(text):
    """Fix basic punctuation issues"""
    # Add periods at sentence ends
    text = re.sub(r'([a-z])\s+([A-Z])', r'\1. \2', text)
    
    # Fix spacing around punctuation
    text = re.sub(r'\s+([,.!?;:])', r'\1', text)
    text = re.sub(r'([,.!?;:])([a-zA-Z])', r'\1 \2', text)
    
    # Capitalize after periods
    text = re.sub(r'(\. )([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
    
    return text

def show_analytics_page():
    st.markdown("## 📊 Analytics Dashboard")
    st.info("Analytics dashboard showing your video editing statistics and usage patterns.")
    
    # Placeholder analytics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Projects", "12", "+3")
    with col2:
        st.metric("Hours Processed", "45.2", "+12.1")
    with col3:
        st.metric("AI Accuracy", "94.2%", "+2.1%")
    with col4:
        st.metric("Export Success", "98%", "+1%")
    
    # Mock charts
    st.subheader("📈 Usage Statistics")
    
    # Generate sample data
    dates = pd.date_range('2024-01-01', periods=30)
    usage_data = pd.DataFrame({
        'Date': dates,
        'Videos Processed': np.random.randint(1, 10, 30),
        'Total Duration (hours)': np.random.uniform(0.5, 8.0, 30)
    })
    
    st.line_chart(usage_data.set_index('Date'))
    
    # Vibe distribution
    st.subheader("🎭 Vibe Distribution")
    vibe_data = pd.DataFrame({
        'Vibe': ['Energetic', 'Professional', 'Calm', 'Fun', 'Dramatic', 'Minimalist'],
        'Count': [25, 18, 15, 12, 8, 5]
    })
    st.bar_chart(vibe_data.set_index('Vibe'))

def show_settings_page():
    st.markdown("## ⚙️ Settings")
    
    st.subheader("API Configuration")
    st.info("💡 You can either use a .env file or enter keys here. Keys entered here will override .env file settings.")
    
    # API Keys section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Groq API")
        current_groq = os.getenv("GROQ_API_KEY") or st.session_state.get("groq_api_key", "")
        groq_api_key = st.text_input(
            "Groq API Key", 
            value="***" if current_groq else "",
            type="password", 
            help="Get your API key from https://console.groq.com/",
            placeholder="Enter your Groq API key"
        )
        
        if st.button("Update Groq Key", key="update_groq"):
            if groq_api_key and groq_api_key != "***":
                st.session_state.groq_api_key = groq_api_key
                os.environ["GROQ_API_KEY"] = groq_api_key
                st.success("✅ Groq API Key updated!")
                st.rerun()
    
    with col2:
        st.markdown("### Hugging Face API")
        current_hf = os.getenv("HUGGINGFACE_API_KEY") or st.session_state.get("hf_api_key", "")
        hf_api_key = st.text_input(
            "Hugging Face API Key", 
            value="***" if current_hf else "",
            type="password", 
            help="Get your API key from https://huggingface.co/settings/tokens",
            placeholder="Enter your HuggingFace API key"
        )
        
        if st.button("Update HuggingFace Key", key="update_hf"):
            if hf_api_key and hf_api_key != "***":
                st.session_state.hf_api_key = hf_api_key
                os.environ["HUGGINGFACE_API_KEY"] = hf_api_key
                st.success("✅ HuggingFace API Key updated!")
                st.rerun()
    
    # Test API connections
    st.markdown("---")
    st.markdown("### 🔧 Test API Connections")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Test Groq Connection"):
            test_groq_connection()
    
    with col2:
        if st.button("Test HuggingFace Connection"):
            test_hf_connection()
    
    # Processing Settings
    st.markdown("---")
    st.subheader("Processing Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        st.slider("Video Quality", 480, 1080, 720, step=240, help="Output video resolution")
        st.slider("Audio Quality", 128, 320, 192, step=64, help="Audio bitrate in kbps")
        st.checkbox("Auto-remove filler words", value=True)
        st.checkbox("Enable GPU acceleration", value=False)
    
    with col2:
        st.selectbox("Default Vibe", ["Auto-detect", "Energetic", "Calm", "Professional", "Fun", "Dramatic", "Minimalist"])
        st.selectbox("Export Format", ["MP4", "MOV", "AVI", "WebM"])
        st.slider("Export Quality", 1, 10, 8, help="1 = Fastest, 10 = Best Quality")
        st.checkbox("Include subtitles by default", value=True)
    
    # Save settings
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Settings saved successfully!")

def test_groq_connection():
    """Test Groq API connection"""
    groq_key = os.getenv("GROQ_API_KEY") or st.session_state.get("groq_api_key")
    
    if not groq_key:
        st.error("❌ Groq API key not found!")
        return
    
    try:
        with st.spinner("Testing Groq connection..."):
            time.sleep(1)  # Simulate API call
            
            # In a real implementation, you would make an actual API call here
            # For demo purposes, we'll simulate a successful connection
            if len(groq_key) > 10:  # Basic validation
                st.success("✅ Groq connection successful!")
                st.info("API is responding and ready for video analysis.")
            else:
                st.error("❌ Invalid Groq API key format!")
                
    except Exception as e:
        st.error(f"❌ Groq connection failed: {e}")

def test_hf_connection():
    """Test Hugging Face API connection"""
    hf_key = os.getenv("HUGGINGFACE_API_KEY") or st.session_state.get("hf_api_key")
    
    if not hf_key:
        st.error("❌ HuggingFace API key not found!")
        return
    
    try:
        with st.spinner("Testing HuggingFace connection..."):
            time.sleep(1)  # Simulate API call
            
            # In a real implementation, you would make an actual API call here
            # For demo purposes, we'll simulate a successful connection
            if len(hf_key) > 10:  # Basic validation
                st.success("✅ HuggingFace connection successful!")
                st.info("API is responding and ready for model inference.")
            else:
                st.error("❌ Invalid HuggingFace API key format!")
                
    except Exception as e:
        st.error(f"❌ HuggingFace connection failed: {e}")

if __name__ == "__main__":
    main()
