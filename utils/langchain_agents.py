
import os
import logging
from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.schema import SystemMessage, HumanMessage
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
import streamlit as st
import json

logger = logging.getLogger(__name__)

class VibeAnalysisAgent:
    """LangChain agent for video content vibe analysis"""

    def __init__(self):
        self.llm = None
        self.agent = None
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.setup_llm()
        self.setup_tools()
        self.setup_agent()

    def setup_llm(self):
        """Initialize the LLM (Groq or Hugging Face)"""
        try:
            # Try Groq first (faster)
            groq_api_key = os.getenv("GROQ_API_KEY")
            if groq_api_key:
                self.llm = ChatGroq(
                    groq_api_key=groq_api_key,
                    model_name="mixtral-8x7b-32768",
                    temperature=0.1,
                    max_tokens=1000
                )
                logger.info("✅ Groq LLM initialized")
                return

            # Fallback to Hugging Face
            hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
            if hf_api_key:
                hf_endpoint = HuggingFaceEndpoint(
                    repo_id="microsoft/DialoGPT-medium",
                    huggingfacehub_api_token=hf_api_key,
                    task="text-generation",
                    max_new_tokens=500
                )
                self.llm = ChatHuggingFace(llm=hf_endpoint)
                logger.info("✅ Hugging Face LLM initialized")
                return

            # No API keys available
            logger.warning("No API keys found. Using mock responses.")
            self.llm = None

        except Exception as e:
            logger.error(f"Error setting up LLM: {e}")
            self.llm = None

    def setup_tools(self):
        """Setup tools for the agent"""
        self.tools = [
            Tool(
                name="analyze_transcript_sentiment",
                description="Analyze the sentiment and emotional tone of transcript text",
                func=self.analyze_sentiment
            ),
            Tool(
                name="identify_key_moments",
                description="Identify key moments or highlights in the transcript",
                func=self.identify_key_moments
            ),
            Tool(
                name="suggest_music_style",
                description="Suggest appropriate music style based on content vibe",
                func=self.suggest_music_style
            ),
            Tool(
                name="recommend_visual_effects",
                description="Recommend visual effects and transitions based on vibe",
                func=self.recommend_visual_effects
            ),
            Tool(
                name="generate_editing_suggestions",
                description="Generate specific editing suggestions for the video",
                func=self.generate_editing_suggestions
            )
        ]

    def setup_agent(self):
        """Setup the ReAct agent"""
        if not self.llm:
            return

        try:
            # Create prompt template
            prompt_template = """You are an expert video content analyzer and editor. You help users understand their video content and suggest improvements.

            You have access to the following tools:
            {tools}

            Use the following format:
            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question

            Question: {input}
            Thought: {agent_scratchpad}
            """

            prompt = PromptTemplate.from_template(prompt_template)

            # Create ReAct agent
            self.agent = create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt
            )

            self.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                memory=self.memory,
                verbose=True,
                max_iterations=3,
                handle_parsing_errors=True
            )

            logger.info("✅ LangChain agent setup complete")

        except Exception as e:
            logger.error(f"Error setting up agent: {e}")
            self.agent = None

    def analyze_video_content(self, transcript: List[Dict], callback_handler=None) -> Dict[str, Any]:
        """Main method to analyze video content using the agent"""
        if not self.agent:
            return self._fallback_analysis(transcript)

        try:
            # Prepare transcript text
            transcript_text = " ".join([segment['text'] for segment in transcript])

            # Create analysis query
            query = f"""Analyze this video transcript and determine:
            1. The overall vibe/mood (energetic, calm, professional, fun, dramatic, minimalist)
            2. Key moments or highlights
            3. Suggested music style
            4. Recommended visual effects
            5. Specific editing suggestions

            Transcript: {transcript_text[:2000]}...
            """

            # Execute agent
            if callback_handler:
                result = self.agent_executor.invoke(
                    {"input": query},
                    {"callbacks": [callback_handler]}
                )
            else:
                result = self.agent_executor.invoke({"input": query})

            # Parse result
            return self._parse_agent_result(result)

        except Exception as e:
            logger.error(f"Error in agent analysis: {e}")
            return self._fallback_analysis(transcript)

    def analyze_sentiment(self, text: str) -> str:
        """Tool: Analyze sentiment of text"""
        try:
            # Simple keyword-based sentiment analysis
            positive_words = ['amazing', 'great', 'awesome', 'fantastic', 'excellent', 'wonderful']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing']
            neutral_words = ['okay', 'fine', 'normal', 'standard', 'regular']

            text_lower = text.lower()

            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            neu_count = sum(1 for word in neutral_words if word in text_lower)

            if pos_count > neg_count and pos_count > neu_count:
                sentiment = "positive"
                confidence = min(0.9, pos_count * 0.2 + 0.5)
            elif neg_count > pos_count and neg_count > neu_count:
                sentiment = "negative" 
                confidence = min(0.9, neg_count * 0.2 + 0.5)
            else:
                sentiment = "neutral"
                confidence = 0.6

            return f"Sentiment: {sentiment} (confidence: {confidence:.2f})"

        except Exception as e:
            return f"Error analyzing sentiment: {e}"

    def identify_key_moments(self, text: str) -> str:
        """Tool: Identify key moments in transcript"""
        try:
            # Look for key phrases that indicate important moments
            key_phrases = [
                'important', 'key point', 'remember', 'crucial', 'essential',
                'breakthrough', 'discovery', 'solution', 'result', 'conclusion'
            ]

            sentences = text.split('.')
            key_moments = []

            for i, sentence in enumerate(sentences):
                sentence_lower = sentence.lower()
                if any(phrase in sentence_lower for phrase in key_phrases):
                    key_moments.append(f"Moment {i+1}: {sentence.strip()}")

            if key_moments:
                return "Key moments found:\n" + "\n".join(key_moments[:3])
            else:
                return "No specific key moments identified. Content appears to have consistent importance throughout."

        except Exception as e:
            return f"Error identifying key moments: {e}"

    def suggest_music_style(self, vibe: str) -> str:
        """Tool: Suggest music style based on vibe"""
        music_suggestions = {
            'energetic': 'Upbeat electronic music, rock anthems, or high-energy pop tracks',
            'calm': 'Ambient music, soft piano, nature sounds, or meditative tracks',
            'professional': 'Corporate background music, minimal electronic, or sophisticated jazz',
            'fun': 'Pop music, upbeat indie, comedy music, or playful electronic beats',
            'dramatic': 'Cinematic orchestral music, emotional piano, or dramatic film scores',
            'minimalist': 'Minimal techno, ambient soundscapes, or simple acoustic guitar'
        }

        return f"Recommended music style for {vibe} vibe: {music_suggestions.get(vibe, music_suggestions['professional'])}"

    def recommend_visual_effects(self, vibe: str) -> str:
        """Tool: Recommend visual effects based on vibe"""
        effects_suggestions = {
            'energetic': 'Quick cuts, zoom transitions, high contrast, vibrant colors, motion blur effects',
            'calm': 'Slow fades, gentle transitions, soft lighting, cool color grading, minimal effects',
            'professional': 'Clean cuts, corporate templates, neutral color grading, subtle transitions',
            'fun': 'Playful transitions, bright colors, creative overlays, animated elements, bounce effects',
            'dramatic': 'Slow motion, dramatic lighting, high contrast, cinematic color grading, fade to black',
            'minimalist': 'Simple cuts, clean typography, monochrome effects, geometric shapes, negative space'
        }

        return f"Visual effects for {vibe} vibe: {effects_suggestions.get(vibe, effects_suggestions['professional'])}"

    def generate_editing_suggestions(self, content: str) -> str:
        """Tool: Generate specific editing suggestions"""
        suggestions = [
            "Consider removing filler words (um, uh, like) for cleaner audio",
            "Add subtitles for better accessibility and engagement",
            "Create thumbnail from the most engaging moment",
            "Add intro/outro sections with branding",
            "Include call-to-action overlays at key moments",
            "Consider adding B-roll footage to illustrate key points",
            "Normalize audio levels for consistent volume",
            "Add chapter markers for longer content"
        ]

        # Return a subset of suggestions
        import random
        selected_suggestions = random.sample(suggestions, 3)
        return "Editing suggestions:\n" + "\n".join([f"• {s}" for s in selected_suggestions])

    def _fallback_analysis(self, transcript: List[Dict]) -> Dict[str, Any]:
        """Fallback analysis when agent is not available"""
        transcript_text = " ".join([segment['text'] for segment in transcript])

        # Simple keyword-based vibe detection
        vibe_keywords = {
            'energetic': ['amazing', 'incredible', 'exciting', 'awesome', 'energy'],
            'professional': ['business', 'corporate', 'professional', 'strategy'],
            'fun': ['fun', 'funny', 'entertaining', 'comedy', 'hilarious'],
            'calm': ['peaceful', 'relaxing', 'calm', 'meditation', 'serene'],
            'dramatic': ['dramatic', 'emotional', 'intense', 'powerful'],
            'minimalist': ['simple', 'clean', 'minimal', 'basic', 'essential']
        }

        text_lower = transcript_text.lower()
        scores = {}

        for vibe, keywords in vibe_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[vibe] = score

        detected_vibe = max(scores, key=scores.get) if any(scores.values()) else 'professional'
        confidence = min(0.9, scores[detected_vibe] * 0.15 + 0.6)

        return {
            'vibe': detected_vibe,
            'confidence': confidence,
            'sentiment': 'positive',
            'key_moments': ['Beginning of content', 'Main discussion', 'Conclusion'],
            'music_suggestion': f'Music appropriate for {detected_vibe} content',
            'visual_effects': f'Visual effects suitable for {detected_vibe} vibe',
            'editing_suggestions': [
                'Remove filler words',
                'Add subtitles', 
                'Improve audio quality'
            ]
        }

    def _parse_agent_result(self, result: Dict) -> Dict[str, Any]:
        """Parse agent execution result"""
        try:
            output = result.get('output', '')

            # Extract information from agent output
            analysis = {
                'vibe': 'professional',
                'confidence': 0.7,
                'sentiment': 'neutral',
                'key_moments': [],
                'music_suggestion': '',
                'visual_effects': '',
                'editing_suggestions': []
            }

            # Simple parsing of agent output
            lines = output.split('\n')
            for line in lines:
                line_lower = line.lower()

                # Extract vibe
                for vibe in ['energetic', 'calm', 'professional', 'fun', 'dramatic', 'minimalist']:
                    if vibe in line_lower:
                        analysis['vibe'] = vibe
                        break

                # Extract other information based on keywords
                if 'music' in line_lower:
                    analysis['music_suggestion'] = line
                elif 'effect' in line_lower:
                    analysis['visual_effects'] = line
                elif 'suggest' in line_lower:
                    analysis['editing_suggestions'].append(line)

            return analysis

        except Exception as e:
            logger.error(f"Error parsing agent result: {e}")
            return self._fallback_analysis([])


class TranscriptEditingAgent:
    """LangChain agent for transcript editing and improvement"""

    def __init__(self, llm=None):
        self.llm = llm
        self.setup_tools()

    def setup_tools(self):
        """Setup tools for transcript editing"""
        self.tools = [
            Tool(
                name="remove_filler_words",
                description="Remove filler words from transcript segments",
                func=self.remove_filler_words
            ),
            Tool(
                name="fix_punctuation",
                description="Fix punctuation and capitalization in transcript",
                func=self.fix_punctuation
            ),
            Tool(
                name="improve_readability",
                description="Improve transcript readability and flow",
                func=self.improve_readability
            ),
            Tool(
                name="identify_speaker_changes",
                description="Identify potential speaker changes in transcript",
                func=self.identify_speaker_changes
            )
        ]

    def remove_filler_words(self, text: str) -> str:
        """Remove common filler words"""
        filler_words = [
            'um', 'uh', 'like', 'you know', 'so', 'well', 'actually', 
            'basically', 'literally', 'kind of', 'sort of'
        ]

        cleaned_text = text
        for filler in filler_words:
            # Remove with word boundaries
            import re
            pattern = r'\b' + re.escape(filler) + r'\b'
            cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)

        # Clean up extra spaces
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text

    def fix_punctuation(self, text: str) -> str:
        """Fix basic punctuation issues"""
        import re

        # Add periods at end of sentences
        text = re.sub(r'([a-zA-Z])\s*$', r'\1.', text)

        # Fix capitalization after periods
        text = re.sub(r'\.\s+([a-z])', lambda m: '. ' + m.group(1).upper(), text)

        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]

        return text

    def improve_readability(self, text: str) -> str:
        """Improve text readability"""
        # This is a simplified version - in practice, you might use NLP libraries
        improved_text = text

        # Replace common spoken phrases with written equivalents
        replacements = {
            "gonna": "going to",
            "wanna": "want to", 
            "gotta": "got to",
            "kinda": "kind of",
            "sorta": "sort of"
        }

        for spoken, written in replacements.items():
            improved_text = improved_text.replace(spoken, written)

        return improved_text

    def identify_speaker_changes(self, text: str) -> str:
        """Identify potential speaker changes"""
        # Simple heuristic - look for conversation patterns
        indicators = [
            "he said", "she said", "they said", "i said",
            "according to", "as mentioned", "someone asked"
        ]

        changes = []
        for indicator in indicators:
            if indicator in text.lower():
                changes.append(f"Potential speaker change near: '{indicator}'")

        return "\n".join(changes) if changes else "No clear speaker changes detected"
