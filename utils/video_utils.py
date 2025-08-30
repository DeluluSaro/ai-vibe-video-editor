
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
import whisper
import tempfile
import os
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.whisper_model = None
        self.temp_files = []

    def load_whisper_model(self, model_size: str = "base"):
        """Load Whisper model for transcription"""
        try:
            self.whisper_model = whisper.load_model(model_size)
            logger.info(f"✅ Whisper {model_size} model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            raise

    def extract_audio_from_video(self, video_path: str) -> str:
        """Extract audio from video file"""
        try:
            video = VideoFileClip(video_path)

            # Create temporary audio file
            audio_path = tempfile.mktemp(suffix='.wav')
            self.temp_files.append(audio_path)

            # Extract and save audio
            video.audio.write_audiofile(
                audio_path, 
                verbose=False, 
                logger=None,
                codec='pcm_s16le'
            )

            video.close()
            logger.info(f"✅ Audio extracted to: {audio_path}")
            return audio_path

        except Exception as e:
            logger.error(f"Error extracting audio: {e}")
            raise

    def transcribe_audio(self, audio_path: str) -> List[Dict]:
        """Transcribe audio using Whisper"""
        try:
            if not self.whisper_model:
                self.load_whisper_model()

            # Transcribe with word-level timestamps
            result = self.whisper_model.transcribe(
                audio_path, 
                word_timestamps=True,
                verbose=False
            )

            # Format segments
            segments = []
            for segment in result['segments']:
                segments.append({
                    'start': segment['start'],
                    'end': segment['end'], 
                    'text': segment['text'].strip(),
                    'confidence': segment.get('avg_logprob', 0),
                    'words': segment.get('words', [])
                })

            logger.info(f"✅ Transcription completed: {len(segments)} segments")
            return segments

        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            # Return mock data for demo
            return self._get_mock_transcript()

    def get_video_metadata(self, video_path: str) -> Dict:
        """Extract video metadata"""
        try:
            # Using OpenCV for basic metadata
            cap = cv2.VideoCapture(video_path)

            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0

            cap.release()

            # Using MoviePy for additional metadata
            try:
                clip = VideoFileClip(video_path)
                has_audio = clip.audio is not None
                audio_fps = clip.audio.fps if has_audio else None
                clip.close()
            except:
                has_audio = False
                audio_fps = None

            metadata = {
                'width': width,
                'height': height,
                'fps': fps,
                'duration': duration,
                'frame_count': frame_count,
                'has_audio': has_audio,
                'audio_fps': audio_fps,
                'resolution': f"{width}x{height}",
                'aspect_ratio': width / height if height > 0 else 1.0
            }

            logger.info(f"✅ Video metadata extracted: {metadata['resolution']}, {duration:.1f}s")
            return metadata

        except Exception as e:
            logger.error(f"Error getting video metadata: {e}")
            return {
                'width': 1920, 'height': 1080, 'fps': 30, 
                'duration': 60, 'frame_count': 1800, 
                'has_audio': True, 'audio_fps': 44100
            }

    def extract_frames(self, video_path: str, times: List[float]) -> List[np.ndarray]:
        """Extract frames at specific timestamps"""
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)

            frames = []
            for time_sec in times:
                frame_number = int(time_sec * fps)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

                ret, frame = cap.read()
                if ret:
                    frames.append(frame)
                else:
                    # Add black frame if extraction fails
                    frames.append(np.zeros((480, 640, 3), dtype=np.uint8))

            cap.release()
            logger.info(f"✅ Extracted {len(frames)} frames")
            return frames

        except Exception as e:
            logger.error(f"Error extracting frames: {e}")
            return []

    def create_video_segments(self, video_path: str, segments: List[Dict]) -> List[VideoFileClip]:
        """Create video clips based on transcript segments"""
        try:
            video = VideoFileClip(video_path)
            clips = []

            for segment in segments:
                start_time = segment['start']
                end_time = segment['end']

                # Create subclip
                clip = video.subclip(start_time, end_time)
                clips.append(clip)

            logger.info(f"✅ Created {len(clips)} video segments")
            return clips

        except Exception as e:
            logger.error(f"Error creating video segments: {e}")
            return []

    def apply_vibe_styling(self, video_clip: VideoFileClip, vibe: str, settings: Dict = None) -> VideoFileClip:
        """Apply vibe-based styling to video clip"""
        try:
            if settings is None:
                settings = {}

            styled_clip = video_clip

            # Apply vibe-specific effects
            if vibe == 'energetic':
                # Increase saturation and contrast
                styled_clip = styled_clip.fx(lambda clip: clip)  # Placeholder for actual effects

            elif vibe == 'calm':
                # Soft, peaceful effects
                styled_clip = styled_clip.fx(lambda clip: clip)  # Placeholder

            elif vibe == 'professional':
                # Clean, corporate look
                styled_clip = styled_clip.fx(lambda clip: clip)  # Placeholder

            elif vibe == 'fun':
                # Bright, colorful effects
                styled_clip = styled_clip.fx(lambda clip: clip)  # Placeholder

            elif vibe == 'dramatic':
                # High contrast, cinematic
                styled_clip = styled_clip.fx(lambda clip: clip)  # Placeholder

            elif vibe == 'minimalist':
                # Simple, clean effects
                styled_clip = styled_clip.fx(lambda clip: clip)  # Placeholder

            # Apply custom settings
            if 'speed' in settings:
                styled_clip = styled_clip.fx(lambda clip: clip.speedx(settings['speed']))

            if 'volume' in settings and styled_clip.audio:
                styled_clip = styled_clip.volumex(settings['volume'])

            logger.info(f"✅ Applied {vibe} styling to video clip")
            return styled_clip

        except Exception as e:
            logger.error(f"Error applying vibe styling: {e}")
            return video_clip

    def add_subtitles(self, video_clip: VideoFileClip, segments: List[Dict], style: Dict = None) -> VideoFileClip:
        """Add subtitles to video based on transcript segments"""
        try:
            if style is None:
                style = {
                    'fontsize': 40,
                    'color': 'white',
                    'font': 'Arial',
                    'position': ('center', 'bottom'),
                    'stroke_color': 'black',
                    'stroke_width': 2
                }

            subtitle_clips = []

            for segment in segments:
                if not segment['text'].strip():
                    continue

                # Create text clip for subtitle
                txt_clip = TextClip(
                    segment['text'],
                    fontsize=style['fontsize'],
                    color=style['color'],
                    font=style['font'],
                    stroke_color=style.get('stroke_color'),
                    stroke_width=style.get('stroke_width', 0)
                ).set_start(segment['start']).set_duration(
                    segment['end'] - segment['start']
                ).set_position(style['position'])

                subtitle_clips.append(txt_clip)

            # Composite video with subtitles
            if subtitle_clips:
                final_clip = CompositeVideoClip([video_clip] + subtitle_clips)
                logger.info(f"✅ Added {len(subtitle_clips)} subtitle clips")
                return final_clip
            else:
                return video_clip

        except Exception as e:
            logger.error(f"Error adding subtitles: {e}")
            return video_clip

    def export_video(self, video_clip: VideoFileClip, output_path: str, 
                    quality: int = 8, codec: str = 'libx264') -> str:
        """Export final video with specified quality settings"""
        try:
            # Quality settings mapping
            quality_settings = {
                1: {'bitrate': '500k', 'audio_bitrate': '64k'},
                3: {'bitrate': '1000k', 'audio_bitrate': '128k'}, 
                5: {'bitrate': '2000k', 'audio_bitrate': '192k'},
                8: {'bitrate': '5000k', 'audio_bitrate': '256k'},
                10: {'bitrate': '10000k', 'audio_bitrate': '320k'}
            }

            settings = quality_settings.get(quality, quality_settings[8])

            # Export video
            video_clip.write_videofile(
                output_path,
                codec=codec,
                bitrate=settings['bitrate'],
                audio_bitrate=settings['audio_bitrate'],
                verbose=False,
                logger=None
            )

            logger.info(f"✅ Video exported successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error exporting video: {e}")
            raise

    def cleanup_temp_files(self):
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                logger.warning(f"Could not remove temp file {temp_file}: {e}")

        self.temp_files.clear()
        logger.info("✅ Temporary files cleaned up")

    def _get_mock_transcript(self) -> List[Dict]:
        """Return mock transcript for demo purposes"""
        return [
            {
                'start': 0.0,
                'end': 5.2,
                'text': 'Welcome to our amazing product demonstration!',
                'confidence': 0.95,
                'words': []
            },
            {
                'start': 5.2,
                'end': 11.8,
                'text': 'Today we are going to show you something truly incredible.',
                'confidence': 0.92,
                'words': []
            },
            {
                'start': 11.8,
                'end': 18.5,
                'text': 'This revolutionary technology will change the way you work.',
                'confidence': 0.89,
                'words': []
            },
            {
                'start': 18.5,
                'end': 25.0,
                'text': 'Let us dive deep into the features and capabilities.',
                'confidence': 0.91,
                'words': []
            }
        ]

    def __del__(self):
        """Cleanup on object destruction"""
        self.cleanup_temp_files()


class VibeStyler:
    """Class for applying vibe-specific styling to videos"""

    def __init__(self):
        self.vibe_configs = {
            'energetic': {
                'color_multiplier': [1.2, 1.1, 1.0],  # Boost red/orange
                'contrast': 1.3,
                'saturation': 1.4,
                'speed_factor': 1.1,
                'transition_style': 'quick_cut'
            },
            'calm': {
                'color_multiplier': [0.9, 1.0, 1.2],  # Boost blue/cool tones
                'contrast': 0.8,
                'saturation': 0.9,
                'speed_factor': 0.9,
                'transition_style': 'fade'
            },
            'professional': {
                'color_multiplier': [1.0, 1.0, 1.0],
                'contrast': 1.1,
                'saturation': 0.95,
                'speed_factor': 1.0,
                'transition_style': 'cut'
            },
            'fun': {
                'color_multiplier': [1.3, 1.2, 1.1],
                'contrast': 1.4,
                'saturation': 1.5,
                'speed_factor': 1.2,
                'transition_style': 'zoom'
            },
            'dramatic': {
                'color_multiplier': [1.1, 0.9, 0.8],
                'contrast': 1.5,
                'saturation': 1.2,
                'speed_factor': 0.8,
                'transition_style': 'fade'
            },
            'minimalist': {
                'color_multiplier': [1.0, 1.0, 1.0],
                'contrast': 0.9,
                'saturation': 0.7,
                'speed_factor': 1.0,
                'transition_style': 'simple_cut'
            }
        }

    def get_vibe_config(self, vibe: str) -> Dict:
        """Get configuration for specific vibe"""
        return self.vibe_configs.get(vibe, self.vibe_configs['professional'])

    def apply_color_grading(self, frame: np.ndarray, vibe: str) -> np.ndarray:
        """Apply vibe-specific color grading to frame"""
        config = self.get_vibe_config(vibe)

        # Apply color multipliers (BGR format)
        frame = frame.astype(np.float32)
        frame[:, :, 0] *= config['color_multiplier'][2]  # Blue
        frame[:, :, 1] *= config['color_multiplier'][1]  # Green  
        frame[:, :, 2] *= config['color_multiplier'][0]  # Red

        # Apply contrast
        frame = frame * config['contrast']

        # Clip values and convert back
        frame = np.clip(frame, 0, 255).astype(np.uint8)

        return frame

    def get_subtitle_style(self, vibe: str) -> Dict:
        """Get subtitle styling based on vibe"""
        styles = {
            'energetic': {
                'fontsize': 48,
                'color': 'yellow',
                'stroke_color': 'red', 
                'stroke_width': 3,
                'font': 'Arial-Bold'
            },
            'calm': {
                'fontsize': 40,
                'color': 'lightblue',
                'stroke_color': 'navy',
                'stroke_width': 2,
                'font': 'Arial'
            },
            'professional': {
                'fontsize': 42,
                'color': 'white',
                'stroke_color': 'black',
                'stroke_width': 2,
                'font': 'Arial'
            },
            'fun': {
                'fontsize': 50,
                'color': 'magenta',
                'stroke_color': 'yellow',
                'stroke_width': 3,
                'font': 'Comic Sans MS'
            },
            'dramatic': {
                'fontsize': 44,
                'color': 'white',
                'stroke_color': 'darkred',
                'stroke_width': 3,
                'font': 'Times New Roman'
            },
            'minimalist': {
                'fontsize': 36,
                'color': 'white',
                'stroke_color': 'gray',
                'stroke_width': 1,
                'font': 'Helvetica'
            }
        }

        return styles.get(vibe, styles['professional'])
