
import os
import logging
from typing import List, Dict, Any, Optional
from groq import Groq
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.schema import SystemMessage, HumanMessage
import streamlit as st

logger = logging.getLogger(__name__)

class AIAgent:
    def __init__(self):
        self.groq_client = None
        self.hf_client = None
        self.setup_clients()

    def setup_clients(self):
        """Initialize AI clients"""
        try:
            # Setup Groq client
            groq_api_key = os.getenv("GROQ_API_KEY")
            if groq_api_key:
                self.groq_client = ChatGroq(
                    groq_api_key=groq_api_key,
                    model_name="mixtral-8x7b-32768",
                    temperature=0.1
                )
                logger.info("✅ Groq client initialized successfully")

            # Setup Hugging Face client
            hf_api_key = os.getenv("HUGGINGFACE_API_KEY") 
            if hf_api_key:
                hf_endpoint = HuggingFaceEndpoint(
                    repo_id="microsoft/DialoGPT-medium",
                    huggingfacehub_api_token=hf_api_key
                )
                self.hf_client = ChatHuggingFace(llm=hf_endpoint)
                logger.info("✅ Hugging Face client initialized successfully")

        except Exception as e:
            logger.error(f"Error setting up AI clients: {e}")
            st.warning("⚠️ Some AI features may not be available. Please check your API keys.")

    def analyze_content_vibe(self, transcript_text: str) -> Dict[str, Any]:
        """Analyze content vibe using AI"""
        if not self.groq_client:
            return self._mock_vibe_analysis(transcript_text)

        try:
            system_prompt = """You are an expert video content analyzer. Analyze the provided transcript and determine the overall vibe/mood.

            Available vibes:
            - energetic: High energy, fast-paced, exciting
            - calm: Peaceful, relaxing, meditative  
            - professional: Business, corporate, formal
            - fun: Entertainment, comedy, playful
            - dramatic: Emotional, storytelling, intense
            - minimalist: Clean, simple, understated

            Provide analysis in JSON format:
            {
                "vibe": "detected_vibe",
                "confidence": 0.85,
                "reasoning": "Brief explanation",
                "keywords": ["key", "words", "found"],
                "suggestions": ["Suggestion 1", "Suggestion 2"]
            }
            """

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Analyze this transcript: {transcript_text}")
            ]

            response = self.groq_client(messages)

            # Parse JSON response
            import json
            try:
                result = json.loads(response.content)
                return result
            except:
                # Fallback to text parsing
                return self._parse_text_response(response.content)

        except Exception as e:
            logger.error(f"Error in vibe analysis: {e}")
            return self._mock_vibe_analysis(transcript_text)

    def generate_transcript_improvements(self, transcript: List[Dict]) -> List[Dict]:
        """Generate suggestions for transcript improvements"""
        if not self.groq_client:
            return self._mock_transcript_improvements(transcript)

        try:
            transcript_text = " ".join([seg['text'] for seg in transcript])

            system_prompt = """You are a transcript editor. Analyze the transcript and suggest improvements for:
            1. Grammar and punctuation
            2. Filler word removal
            3. Better structure and flow
            4. Key moments identification

            Return suggestions as JSON array with format:
            [
                {
                    "type": "grammar|filler|structure|highlight",
                    "segment_index": 0,
                    "original": "original text",
                    "suggested": "improved text",
                    "reason": "explanation"
                }
            ]
            """

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Improve this transcript: {transcript_text}")
            ]

            response = self.groq_client(messages)

            import json
            try:
                suggestions = json.loads(response.content)
                return suggestions
            except:
                return self._mock_transcript_improvements(transcript)

        except Exception as e:
            logger.error(f"Error generating transcript improvements: {e}")
            return self._mock_transcript_improvements(transcript)

    def suggest_music_and_effects(self, vibe: str, content_type: str) -> Dict[str, Any]:
        """Suggest music and effects based on vibe"""
        try:
            system_prompt = f"""You are a video production expert. Based on the vibe "{vibe}" and content type "{content_type}", suggest:
            1. Background music style and tracks
            2. Visual effects and transitions
            3. Color palettes
            4. Typography recommendations

            Return as JSON:
            {{
                "music": {{
                    "style": "description",
                    "tracks": ["track1", "track2"],
                    "volume": 0.3
                }},
                "effects": {{
                    "transitions": ["fade", "cut"],
                    "filters": ["color_grade", "contrast"],
                    "pace": "fast|medium|slow"
                }},
                "colors": ["#hex1", "#hex2", "#hex3"],
                "typography": "font_style_description"
            }}
            """

            if self.groq_client:
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=f"Generate suggestions for {vibe} vibe content")
                ]

                response = self.groq_client(messages)

                import json
                try:
                    return json.loads(response.content)
                except:
                    pass

            # Fallback to predefined suggestions
            return self._get_predefined_suggestions(vibe)

        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return self._get_predefined_suggestions(vibe)

    def _mock_vibe_analysis(self, text: str) -> Dict[str, Any]:
        """Mock vibe analysis for demo/fallback"""
        text_lower = text.lower()

        vibe_keywords = {
            'energetic': ['amazing', 'incredible', 'exciting', 'awesome', 'fantastic', 'energy'],
            'professional': ['business', 'corporate', 'professional', 'strategy', 'solution'],
            'fun': ['fun', 'funny', 'hilarious', 'entertaining', 'comedy', 'joke'],
            'calm': ['peaceful', 'relaxing', 'calm', 'meditation', 'serene', 'quiet'],
            'dramatic': ['dramatic', 'emotional', 'intense', 'powerful', 'moving'],
            'minimalist': ['simple', 'clean', 'minimal', 'basic', 'essential']
        }

        scores = {}
        for vibe, keywords in vibe_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[vibe] = score

        detected_vibe = max(scores, key=scores.get) if any(scores.values()) else 'professional'
        confidence = min(0.9, scores[detected_vibe] * 0.15 + 0.5)

        return {
            'vibe': detected_vibe,
            'confidence': confidence,
            'reasoning': f'Detected based on keyword analysis',
            'keywords': [kw for kw in vibe_keywords[detected_vibe] if kw in text_lower],
            'suggestions': [f'Consider {detected_vibe} music style', f'Use {detected_vibe} visual effects']
        }

    def _mock_transcript_improvements(self, transcript: List[Dict]) -> List[Dict]:
        """Mock transcript improvements"""
        improvements = []

        for i, segment in enumerate(transcript):
            text = segment['text']

            # Check for filler words
            if any(filler in text.lower() for filler in ['um', 'uh', 'like', 'you know']):
                improvements.append({
                    'type': 'filler',
                    'segment_index': i,
                    'original': text,
                    'suggested': text.replace(' um ', ' ').replace(' uh ', ' '),
                    'reason': 'Remove filler words for clarity'
                })

            # Check punctuation
            if text and not text.strip().endswith(('.', '!', '?')):
                improvements.append({
                    'type': 'grammar',
                    'segment_index': i,
                    'original': text,
                    'suggested': text.strip() + '.',
                    'reason': 'Add proper punctuation'
                })

        return improvements[:5]  # Return max 5 suggestions

    def _get_predefined_suggestions(self, vibe: str) -> Dict[str, Any]:
        """Get predefined suggestions based on vibe"""
        suggestions = {
            'energetic': {
                'music': {'style': 'Upbeat electronic', 'tracks': ['Electronic Beat 1', 'Rock Anthem'], 'volume': 0.4},
                'effects': {'transitions': ['quick cut', 'zoom'], 'filters': ['high contrast'], 'pace': 'fast'},
                'colors': ['#ff6b35', '#f7931e', '#ffcb47'],
                'typography': 'Bold, modern sans-serif'
            },
            'calm': {
                'music': {'style': 'Ambient peaceful', 'tracks': ['Nature Sounds', 'Gentle Piano'], 'volume': 0.2},
                'effects': {'transitions': ['fade', 'dissolve'], 'filters': ['soft glow'], 'pace': 'slow'},
                'colors': ['#6b73ff', '#9b59b6', '#3498db'],
                'typography': 'Soft, rounded fonts'
            },
            'professional': {
                'music': {'style': 'Corporate minimal', 'tracks': ['Business Theme', 'Corporate Success'], 'volume': 0.2},
                'effects': {'transitions': ['clean cut'], 'filters': ['professional grade'], 'pace': 'medium'},
                'colors': ['#2c3e50', '#34495e', '#1abc9c'],
                'typography': 'Clean, professional serif'
            }
        }

        return suggestions.get(vibe, suggestions['professional'])

    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Parse AI text response when JSON parsing fails"""
        # Simple text parsing fallback
        lines = text.split('\n')
        vibe = 'professional'
        confidence = 0.7

        for line in lines:
            if 'vibe' in line.lower():
                for v in ['energetic', 'calm', 'professional', 'fun', 'dramatic', 'minimalist']:
                    if v in line.lower():
                        vibe = v
                        break
            elif 'confidence' in line.lower():
                try:
                    import re
                    conf_match = re.search(r'(0\.\d+|\d+%)', line)
                    if conf_match:
                        conf_str = conf_match.group(1)
                        if '%' in conf_str:
                            confidence = float(conf_str.replace('%', '')) / 100
                        else:
                            confidence = float(conf_str)
                except:
                    pass

        return {
            'vibe': vibe,
            'confidence': confidence,
            'reasoning': 'Parsed from AI response',
            'keywords': [],
            'suggestions': []
        }
