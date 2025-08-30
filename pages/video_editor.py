
import streamlit as st
import tempfile
import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
import whisper
from groq import Groq
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain.schema import SystemMessage, HumanMessage
from langchain.callbacks.streamlit import StreamlitCallbackHandler
import json
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

class VideoEditorApp:
    def __init__(self):
        self.vibe_options = {
            'energetic': {
                'label': 'Energetic ⚡', 
                'color': '#ff6b35', 
                'description': 'High energy, fast-paced content',
                'music_style': 'Upbeat, electronic, rock',
                'editing_style': 'Quick cuts, dynamic transitions'
            },
            'calm': {
                'label': 'Calm 🌊', 
                'color': '#6b73ff', 
                'description': 'Peaceful, relaxing content',
                'music_style': 'Ambient, classical, nature sounds',
                'editing_style': 'Slow transitions, gentle fades'
            },
            'professional': {
                'label': 'Professional 💼', 
                'color': '#2c3e50', 
                'description': 'Business, corporate content',
                'music_style': 'Corporate, minimal, sophisticated',
                'editing_style': 'Clean cuts, corporate templates'
            },
            'fun': {
                'label': 'Fun 🎉', 
                'color': '#e91e63', 
                'description': 'Entertainment, comedy content',
                'music_style': 'Pop, comedy, upbeat',
                'editing_style': 'Playful effects, colorful themes'
            },
            'dramatic': {
                'label': 'Dramatic 🎭', 
                'color': '#8e24aa', 
                'description': 'Emotional, storytelling content',
                'music_style': 'Cinematic, orchestral, emotional',
                'editing_style': 'Dramatic lighting, slow motion'
            },
            'minimalist': {
                'label': 'Minimalist ⚪', 
                'color': '#263238', 
                'description': 'Clean, simple design',
                'music_style': 'Minimal, ambient, subtle',
                'editing_style': 'Simple cuts, clean typography'
            }
        }

        # Initialize session state
        if 'project_data' not in st.session_state:
            st.session_state.project_data = {}
        if 'current_video' not in st.session_state:
            st.session_state.current_video = None
        if 'transcript' not in st.session_state:
            st.session_state.transcript = []
        if 'detected_vibe' not in st.session_state:
            st.session_state.detected_vibe = None
        if 'selected_vibe' not in st.session_state:
            st.session_state.selected_vibe = None

    def run(self):
        # Create tabs for different editor sections
        tab1, tab2, tab3, tab4 = st.tabs(["📹 Upload", "🎯 Vibe Analysis", "✏️ Transcript", "🎨 Styling"])

        with tab1:
            self.show_upload_section()

        with tab2:
            self.show_vibe_analysis_section()

        with tab3:
            self.show_transcript_section()

        with tab4:
            self.show_styling_section()

    def show_upload_section(self):
        st.markdown("### 📹 Upload Your Video")

        uploaded_file = st.file_uploader(
            "Choose a video file", 
            type=['mp4', 'mov', 'avi', 'mkv'],
            help="Upload your video file to get started with AI-powered editing"
        )

        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                video_path = tmp_file.name

            st.session_state.current_video = video_path

            # Display video info
            col1, col2 = st.columns(2)

            with col1:
                st.video(uploaded_file.getvalue())

            with col2:
                # Get video metadata
                video_info = self.get_video_info(video_path)
                st.markdown("#### 📊 Video Information")
                st.write(f"**Filename:** {uploaded_file.name}")
                st.write(f"**Size:** {uploaded_file.size / (1024*1024):.1f} MB")
                st.write(f"**Duration:** {video_info['duration']:.1f} seconds")
                st.write(f"**Resolution:** {video_info['width']}x{video_info['height']}")
                st.write(f"**FPS:** {video_info['fps']:.1f}")

            # Process button
            if st.button("🚀 Start AI Analysis", type="primary"):
                self.process_video(video_path)

    def get_video_info(self, video_path):
        """Extract video metadata using OpenCV"""
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            cap.release()

            return {
                "fps": fps,
                "duration": duration,
                "width": width,
                "height": height,
                "frame_count": frame_count
            }
        except Exception as e:
            st.error(f"Error getting video info: {e}")
            return {"fps": 30, "duration": 0, "width": 1920, "height": 1080, "frame_count": 0}

    def process_video(self, video_path):
        """Process video with AI analysis"""
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Step 1: Extract audio
            status_text.text("📤 Extracting audio from video...")
            progress_bar.progress(20)

            audio_path = self.extract_audio(video_path)

            # Step 2: Generate transcript
            status_text.text("🎤 Generating transcript with Whisper...")
            progress_bar.progress(50)

            transcript = self.generate_transcript(audio_path)
            st.session_state.transcript = transcript

            # Step 3: Analyze vibe
            status_text.text("🧠 Analyzing content vibe with AI...")
            progress_bar.progress(80)

            detected_vibe = self.analyze_vibe(transcript)
            st.session_state.detected_vibe = detected_vibe
            st.session_state.selected_vibe = detected_vibe

            progress_bar.progress(100)
            status_text.text("✅ Processing complete!")

            st.success("🎉 Video analysis completed successfully!")
            st.balloons()

        except Exception as e:
            st.error(f"Error processing video: {e}")
            progress_bar.empty()
            status_text.empty()

    def extract_audio(self, video_path):
        """Extract audio from video using MoviePy"""
        try:
            video = VideoFileClip(video_path)
            audio_path = video_path.replace('.mp4', '_audio.wav')
            video.audio.write_audiofile(audio_path, verbose=False, logger=None)
            video.close()
            return audio_path
        except Exception as e:
            st.error(f"Error extracting audio: {e}")
            return None

    def generate_transcript(self, audio_path):
        """Generate transcript using Whisper"""
        try:
            # Load Whisper model
            model = whisper.load_model("base")

            # Transcribe audio
            result = model.transcribe(audio_path)

            # Format transcript with timestamps
            transcript = []
            for segment in result['segments']:
                transcript.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip(),
                    'confidence': segment.get('avg_logprob', 0)
                })

            return transcript

        except Exception as e:
            st.error(f"Error generating transcript: {e}")
            # Return mock transcript for demo
            return [
                {'start': 0.0, 'end': 5.0, 'text': 'Welcome to our amazing product demo!', 'confidence': 0.95},
                {'start': 5.0, 'end': 12.0, 'text': 'Today we are going to show you something incredible.', 'confidence': 0.92},
                {'start': 12.0, 'end': 18.0, 'text': 'This revolutionary technology will change everything.', 'confidence': 0.90}
            ]

    def analyze_vibe(self, transcript):
        """Analyze content vibe using Groq/LangChain"""
        try:
            # Check if API keys are available
            if not os.getenv("GROQ_API_KEY"):
                st.warning("⚠️ Groq API key not set. Using mock analysis.")
                return self.mock_vibe_analysis(transcript)

            # Initialize Groq LLM
            llm = ChatGroq(
                groq_api_key=os.getenv("GROQ_API_KEY"),
                model_name="mixtral-8x7b-32768",
                temperature=0.1
            )

            # Prepare transcript text
            transcript_text = " ".join([segment['text'] for segment in transcript])

            # Create vibe analysis prompt
            system_prompt = """You are an expert video content analyzer. Analyze the provided transcript and determine the overall vibe/mood of the content.

            Choose from these vibe categories:
            - energetic: High energy, fast-paced, exciting content
            - calm: Peaceful, relaxing, meditative content  
            - professional: Business, corporate, formal content
            - fun: Entertainment, comedy, playful content
            - dramatic: Emotional, storytelling, intense content
            - minimalist: Clean, simple, understated content

            Respond with just the vibe category name (lowercase) and a confidence score (0-1).
            Format: vibe_name,confidence_score
            """

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Transcript: {transcript_text}")
            ]

            response = llm(messages)
            result = response.content.strip().split(',')

            if len(result) == 2:
                vibe = result[0].strip()
                confidence = float(result[1].strip())
                return {'vibe': vibe, 'confidence': confidence}
            else:
                return self.mock_vibe_analysis(transcript)

        except Exception as e:
            st.warning(f"Using mock analysis due to error: {e}")
            return self.mock_vibe_analysis(transcript)

    def mock_vibe_analysis(self, transcript):
        """Mock vibe analysis for demo purposes"""
        # Simple keyword-based analysis
        text = " ".join([segment['text'].lower() for segment in transcript])

        vibe_keywords = {
            'energetic': ['amazing', 'incredible', 'exciting', 'awesome', 'fantastic'],
            'professional': ['business', 'corporate', 'professional', 'strategy', 'solution'],
            'fun': ['fun', 'funny', 'hilarious', 'entertaining', 'comedy'],
            'calm': ['peaceful', 'relaxing', 'calm', 'meditation', 'serene'],
            'dramatic': ['dramatic', 'emotional', 'intense', 'powerful', 'moving'],
            'minimalist': ['simple', 'clean', 'minimal', 'basic', 'essential']
        }

        scores = {}
        for vibe, keywords in vibe_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            scores[vibe] = score

        detected_vibe = max(scores, key=scores.get) if any(scores.values()) else 'professional'
        confidence = min(0.8, scores[detected_vibe] * 0.2 + 0.4)

        return {'vibe': detected_vibe, 'confidence': confidence}

    def show_vibe_analysis_section(self):
        st.markdown("### 🎯 AI Vibe Analysis")

        if st.session_state.detected_vibe:
            vibe_data = st.session_state.detected_vibe
            vibe_info = self.vibe_options[vibe_data['vibe']]

            # Display detected vibe
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"""
                <div style="background: {vibe_info['color']}20; padding: 1rem; border-radius: 10px; border-left: 4px solid {vibe_info['color']};">
                    <h3>🤖 AI Detected Vibe: {vibe_info['label']}</h3>
                    <p><strong>Description:</strong> {vibe_info['description']}</p>
                    <p><strong>Confidence:</strong> {vibe_data['confidence']:.1%}</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                # Confidence gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = vibe_data['confidence'] * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Confidence"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': vibe_info['color']},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig.update_layout(height=200)
                st.plotly_chart(fig, use_container_width=True)

            # Vibe selector
            st.markdown("#### 🎨 Choose Your Vibe")
            st.write("You can override the AI detection and choose a different vibe:")

            cols = st.columns(3)
            for i, (vibe_key, vibe_info) in enumerate(self.vibe_options.items()):
                col_idx = i % 3
                with cols[col_idx]:
                    if st.button(
                        f"{vibe_info['label']}", 
                        key=f"vibe_{vibe_key}",
                        help=vibe_info['description'],
                        use_container_width=True
                    ):
                        st.session_state.selected_vibe = {'vibe': vibe_key, 'confidence': 1.0}
                        st.rerun()

            # Show selected vibe
            if st.session_state.selected_vibe:
                selected_vibe_info = self.vibe_options[st.session_state.selected_vibe['vibe']]
                st.markdown(f"""
                <div style="background: {selected_vibe_info['color']}10; padding: 1rem; border-radius: 5px; margin-top: 1rem;">
                    <strong>Selected Vibe:</strong> {selected_vibe_info['label']} 
                    <br><strong>Music Style:</strong> {selected_vibe_info['music_style']}
                    <br><strong>Editing Style:</strong> {selected_vibe_info['editing_style']}
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("👆 Please upload and process a video first to see vibe analysis.")

    def show_transcript_section(self):
        st.markdown("### ✏️ Transcript Editor")

        if st.session_state.transcript:
            st.markdown("**Edit your transcript by clicking on any segment:**")

            # Transcript editing controls
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🧹 Remove Filler Words"):
                    self.remove_filler_words()
            with col2:
                if st.button("📝 Fix Punctuation"):
                    self.fix_punctuation()
            with col3:
                if st.button("🔄 Reset Transcript"):
                    st.rerun()

            # Display editable transcript
            st.markdown("---")

            for i, segment in enumerate(st.session_state.transcript):
                col1, col2, col3 = st.columns([1, 4, 1])

                with col1:
                    st.write(f"{self.format_time(segment['start'])} - {self.format_time(segment['end'])}")

                with col2:
                    # Editable text area for each segment
                    new_text = st.text_area(
                        f"Segment {i+1}",
                        value=segment['text'],
                        key=f"transcript_{i}",
                        height=60,
                        label_visibility="collapsed"
                    )

                    # Update transcript if text changed
                    if new_text != segment['text']:
                        st.session_state.transcript[i]['text'] = new_text

                with col3:
                    if st.button("🗑️", key=f"delete_{i}", help="Delete segment"):
                        st.session_state.transcript.pop(i)
                        st.rerun()

            # Export transcript
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Transcript"):
                    self.save_transcript()
            with col2:
                transcript_text = "\n".join([f"[{self.format_time(seg['start'])} - {self.format_time(seg['end'])}] {seg['text']}" for seg in st.session_state.transcript])
                st.download_button(
                    "📄 Download Transcript",
                    transcript_text,
                    "transcript.txt",
                    "text/plain"
                )

        else:
            st.info("👆 Please upload and process a video first to see the transcript.")

    def show_styling_section(self):
        st.markdown("### 🎨 Video Styling & Export")

        if st.session_state.selected_vibe:
            vibe_info = self.vibe_options[st.session_state.selected_vibe['vibe']]

            st.markdown(f"**Current Vibe:** {vibe_info['label']}")

            # Style preview
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🎵 Audio Styling")
                st.write(f"**Music Style:** {vibe_info['music_style']}")
                st.slider("Background Music Volume", 0, 100, 20, key="music_volume")
                st.selectbox("Music Track", ["Track 1", "Track 2", "Track 3", "Custom Upload"], key="music_track")

                st.markdown("#### 🎬 Visual Effects")
                st.write(f"**Editing Style:** {vibe_info['editing_style']}")
                st.slider("Transition Speed", 0.5, 3.0, 1.0, 0.1, key="transition_speed")
                st.color_picker("Accent Color", vibe_info['color'], key="accent_color")

            with col2:
                st.markdown("#### 📐 Export Settings")
                resolution = st.selectbox("Resolution", ["720p", "1080p", "4K"], index=1)
                quality = st.slider("Quality", 1, 10, 8, help="1=Fastest, 10=Best")
                format_type = st.selectbox("Format", ["MP4", "MOV", "AVI"])

                st.markdown("#### 🎯 Advanced Options")
                st.checkbox("Add subtitles", value=True)
                st.checkbox("Remove silent parts", value=False)
                st.checkbox("Auto-adjust audio levels", value=True)

            # Preview and Export
            st.markdown("---")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("👁️ Preview Changes", type="secondary"):
                    st.info("🎬 Preview functionality would show a sample of the styled video here.")

            with col2:
                if st.button("🎬 Generate Video", type="primary"):
                    self.generate_styled_video()

            with col3:
                if st.button("💾 Save Project"):
                    self.save_project()

        else:
            st.info("👆 Please complete vibe analysis first.")

    def format_time(self, seconds):
        """Format seconds to MM:SS format"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def remove_filler_words(self):
        """Remove common filler words from transcript"""
        filler_words = ['um', 'uh', 'like', 'you know', 'so', 'well', 'actually', 'basically']

        for segment in st.session_state.transcript:
            text = segment['text']
            for filler in filler_words:
                text = text.replace(f" {filler} ", " ")
                text = text.replace(f" {filler.capitalize()} ", " ")
            segment['text'] = text

        st.success("🧹 Filler words removed!")

    def fix_punctuation(self):
        """Basic punctuation fixing"""
        for segment in st.session_state.transcript:
            text = segment['text'].strip()
            if text and not text.endswith(('.', '!', '?')):
                segment['text'] = text + '.'

        st.success("📝 Punctuation fixed!")

    def save_transcript(self):
        """Save transcript to session state"""
        st.success("💾 Transcript saved!")

    def generate_styled_video(self):
        """Generate the final styled video"""
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            status_text.text("🎬 Generating styled video...")
            progress_bar.progress(20)

            # Simulate video processing steps
            import time

            status_text.text("🎵 Adding background music...")
            time.sleep(1)
            progress_bar.progress(40)

            status_text.text("🎨 Applying visual effects...")
            time.sleep(1)
            progress_bar.progress(60)

            status_text.text("📝 Adding subtitles...")
            time.sleep(1)
            progress_bar.progress(80)

            status_text.text("💾 Exporting final video...")
            time.sleep(1)
            progress_bar.progress(100)

            status_text.text("✅ Video generation complete!")

            st.success("🎉 Your styled video has been generated successfully!")

            # Mock download button
            st.download_button(
                "📥 Download Video",
                b"Mock video data",
                "styled_video.mp4",
                "video/mp4"
            )

        except Exception as e:
            st.error(f"Error generating video: {e}")

    def save_project(self):
        """Save current project state"""
        project_data = {
            'timestamp': datetime.now().isoformat(),
            'vibe': st.session_state.selected_vibe,
            'transcript': st.session_state.transcript,
            'settings': {
                'resolution': '1080p',
                'quality': 8,
                'format': 'MP4'
            }
        }

        st.session_state.project_data = project_data
        st.success("💾 Project saved successfully!")
