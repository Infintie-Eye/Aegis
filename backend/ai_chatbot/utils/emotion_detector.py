from transformers import pipeline
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from collections import Counter
import numpy as np


class MockSentimentPipeline:
    def __call__(self, text):
        # Simple rule-based sentiment for demo
        positive_words = ['happy', 'good', 'great', 'wonderful', 'amazing', 'excited', 'joy', 'love']
        negative_words = ['sad', 'terrible', 'awful', 'hate', 'angry', 'depressed', 'anxious', 'worried']

        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        if pos_count > neg_count:
            return [{'label': 'POSITIVE', 'score': min(0.9, 0.6 + pos_count * 0.1)}]
        elif neg_count > pos_count:
            return [{'label': 'NEGATIVE', 'score': min(0.9, 0.6 + neg_count * 0.1)}]
        else:
            return [{'label': 'NEUTRAL', 'score': 0.5}]


class MockEmotionPipeline:
    def __call__(self, text):
        # Simple rule-based emotion detection
        emotion_keywords = {
            'joy': ['happy', 'excited', 'wonderful', 'amazing', 'great'],
            'sadness': ['sad', 'depressed', 'down', 'miserable', 'heartbroken'],
            'anger': ['angry', 'mad', 'furious', 'annoyed', 'frustrated'],
            'fear': ['scared', 'afraid', 'anxious', 'worried', 'terrified'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished'],
            'disgust': ['disgusted', 'revolted', 'sick', 'repulsed']
        }

        text_lower = text.lower()
        scores = {}

        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[emotion] = score

        if scores:
            dominant_emotion = max(scores.keys(), key=lambda k: scores[k])
            score = min(0.9, 0.5 + scores[dominant_emotion] * 0.1)
        else:
            dominant_emotion = 'neutral'
            score = 0.5

        return [{'label': dominant_emotion, 'score': score}]


class EmotionalDetector:
    def __init__(self):
        # Initialize with mock pipelines (in production, would use actual transformers)
        self.sentiment_pipeline = MockSentimentPipeline()
        self.emotion_pipeline = MockEmotionPipeline()

        # Advanced emotion analysis components
        self.emotion_intensity_analyzer = EmotionIntensityAnalyzer()
        self.emotional_complexity_analyzer = EmotionalComplexityAnalyzer()
        self.emotional_regulation_assessor = EmotionalRegulationAssessor()
        self.contextual_emotion_analyzer = ContextualEmotionAnalyzer()

    async def comprehensive_analyze(self, text: str) -> Dict[str, Any]:
        """Comprehensive emotional analysis of text"""
        # Basic sentiment and emotion detection
        basic_analysis = self.detect(text)

        # Advanced emotional analysis
        intensity_analysis = await self.emotion_intensity_analyzer.analyze(text)
        complexity_analysis = await self.emotional_complexity_analyzer.analyze(text)
        regulation_analysis = await self.emotional_regulation_assessor.analyze(text)
        contextual_analysis = await self.contextual_emotion_analyzer.analyze(text)

        # Mental health indicators
        mental_health_indicators = await self._assess_mental_health_indicators(text)

        # Emotional trajectory analysis
        emotional_trajectory = await self._analyze_emotional_trajectory(text)

        # Coping mechanisms detection
        coping_mechanisms = await self._detect_coping_mechanisms(text)

        # Emotional needs assessment
        emotional_needs = await self._assess_emotional_needs(text, basic_analysis)

        return {
            # Basic analysis
            'sentiment': basic_analysis['sentiment'],
            'sentiment_score': basic_analysis['sentiment_score'],
            'emotion': basic_analysis['emotion'],
            'emotion_score': basic_analysis['emotion_score'],
            'crisis': basic_analysis['crisis'],

            # Advanced analysis
            'emotional_intensity': intensity_analysis,
            'emotional_complexity': complexity_analysis,
            'emotional_regulation': regulation_analysis,
            'contextual_factors': contextual_analysis,

            # Mental health insights
            'mental_health_indicators': mental_health_indicators,
            'emotional_trajectory': emotional_trajectory,
            'coping_mechanisms': coping_mechanisms,
            'emotional_needs': emotional_needs,

            # Summary metrics
            'dominant_emotion': basic_analysis['emotion'],
            'emotional_stability': regulation_analysis.get('stability_score', 0.5),
            'support_urgency': await self._calculate_support_urgency(basic_analysis, intensity_analysis),
            'therapeutic_focus_areas': await self._identify_therapeutic_focus_areas(text, basic_analysis)
        }

    def detect(self, text: str) -> Dict[str, Any]:
        """Basic emotion detection (maintaining compatibility)"""
        # Sentiment analysis
        sentiment = self.sentiment_pipeline(text)[0]
        
        # Emotion classification
        emotions = self.emotion_pipeline(text)[0]
        
        # Determine if there's a crisis (simplified)
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'hopeless', 'worthless']
        crisis = any(keyword in text.lower() for keyword in crisis_keywords)
        
        return {
            'sentiment': sentiment['label'],
            'sentiment_score': sentiment['score'],
            'emotion': emotions['label'],
            'emotion_score': emotions['score'],
            'crisis': crisis
        }

    async def _assess_mental_health_indicators(self, text: str) -> Dict[str, Any]:
        """Assess mental health indicators from emotional expression"""
        text_lower = text.lower()

        # Depression indicators
        depression_indicators = {
            'hopelessness': ['hopeless', 'no point', 'pointless', 'nothing matters'],
            'worthlessness': ['worthless', 'useless', 'failure', 'waste of space'],
            'anhedonia': ['don\'t enjoy', 'no pleasure', 'nothing is fun', 'lost interest'],
            'fatigue': ['exhausted', 'tired', 'no energy', 'drained', 'worn out'],
            'guilt': ['guilty', 'my fault', 'shame', 'regret', 'should have']
        }

        depression_score = 0
        found_depression_indicators = []

        for category, keywords in depression_indicators.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                depression_score += len(matches)
                found_depression_indicators.append({
                    'category': category,
                    'matches': matches
                })

        # Anxiety indicators
        anxiety_indicators = {
            'worry': ['worried', 'anxious', 'concerned', 'afraid'],
            'physical_symptoms': ['heart racing', 'sweating', 'shaking', 'nauseous'],
            'catastrophizing': ['worst case', 'terrible things', 'disaster', 'awful'],
            'avoidance': ['avoiding', 'can\'t face', 'putting off', 'hiding from']
        }

        anxiety_score = 0
        found_anxiety_indicators = []

        for category, keywords in anxiety_indicators.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                anxiety_score += len(matches)
                found_anxiety_indicators.append({
                    'category': category,
                    'matches': matches
                })

        # Stress indicators
        stress_indicators = ['overwhelmed', 'stressed', 'pressure', 'too much', 'can\'t cope']
        stress_score = sum(1 for indicator in stress_indicators if indicator in text_lower)

        return {
            'depression': {
                'score': min(1.0, depression_score / 10),  # Normalize to 0-1
                'indicators': found_depression_indicators,
                'risk_level': 'high' if depression_score >= 5 else 'moderate' if depression_score >= 2 else 'low'
            },
            'anxiety': {
                'score': min(1.0, anxiety_score / 8),
                'indicators': found_anxiety_indicators,
                'risk_level': 'high' if anxiety_score >= 4 else 'moderate' if anxiety_score >= 2 else 'low'
            },
            'stress': {
                'score': min(1.0, stress_score / 5),
                'risk_level': 'high' if stress_score >= 3 else 'moderate' if stress_score >= 1 else 'low'
            },
            'overall_risk': max(depression_score / 10, anxiety_score / 8, stress_score / 5)
        }

    async def _analyze_emotional_trajectory(self, text: str) -> Dict[str, Any]:
        """Analyze emotional trajectory within the message"""
        # Simple analysis of emotional progression through the message
        sentences = text.split('.')

        if len(sentences) < 2:
            return {'trajectory': 'stable', 'analysis': 'insufficient_data'}

        # Analyze sentiment of each sentence
        sentence_sentiments = []
        for sentence in sentences:
            if sentence.strip():
                sentiment = self.sentiment_pipeline(sentence.strip())[0]
                sentence_sentiments.append(
                    sentiment['score'] if sentiment['label'] == 'POSITIVE' else -sentiment['score'])

        if len(sentence_sentiments) < 2:
            return {'trajectory': 'stable', 'analysis': 'insufficient_data'}

        # Determine trajectory
        start_sentiment = np.mean(sentence_sentiments[:2])
        end_sentiment = np.mean(sentence_sentiments[-2:])

        if end_sentiment > start_sentiment + 0.2:
            trajectory = 'improving'
        elif end_sentiment < start_sentiment - 0.2:
            trajectory = 'declining'
        else:
            trajectory = 'stable'

        return {
            'trajectory': trajectory,
            'sentiment_progression': sentence_sentiments,
            'overall_change': end_sentiment - start_sentiment,
            'volatility': np.std(sentence_sentiments) if len(sentence_sentiments) > 1 else 0
        }

    async def _detect_coping_mechanisms(self, text: str) -> Dict[str, List[str]]:
        """Detect coping mechanisms mentioned in the text"""
        text_lower = text.lower()

        coping_mechanisms = {
            'healthy_coping': {
                'exercise': ['exercise', 'workout', 'gym', 'running', 'walking'],
                'mindfulness': ['meditation', 'mindfulness', 'breathing', 'yoga'],
                'social_support': ['talking to friends', 'family support', 'calling someone'],
                'creative': ['music', 'art', 'writing', 'drawing', 'creative'],
                'professional_help': ['therapy', 'counselor', 'therapist', 'professional help']
            },
            'unhealthy_coping': {
                'substance_use': ['drinking', 'alcohol', 'drugs', 'getting high'],
                'avoidance': ['avoiding', 'hiding', 'isolating', 'shutting down'],
                'self_harm': ['cutting', 'hurting myself', 'self harm'],
                'aggression': ['lashing out', 'getting angry', 'breaking things']
            },
            'neutral_coping': {
                'distraction': ['watching tv', 'movies', 'games', 'scrolling'],
                'sleep': ['sleeping', 'napping', 'going to bed'],
                'routine': ['keeping busy', 'work', 'daily routine']
            }
        }

        detected_mechanisms = {
            'healthy_coping': [],
            'unhealthy_coping': [],
            'neutral_coping': []
        }

        for category, mechanisms in coping_mechanisms.items():
            for mechanism_type, keywords in mechanisms.items():
                found_keywords = [kw for kw in keywords if kw in text_lower]
                if found_keywords:
                    detected_mechanisms[category].append({
                        'type': mechanism_type,
                        'indicators': found_keywords
                    })

        return detected_mechanisms

    async def _assess_emotional_needs(self, text: str, basic_analysis: Dict) -> Dict[str, Any]:
        """Assess what emotional needs the user might have"""
        text_lower = text.lower()

        needs_indicators = {
            'validation': ['nobody understands', 'no one gets it', 'feel alone', 'isolated'],
            'practical_support': ['don\'t know what to do', 'need help', 'how do i', 'what should'],
            'emotional_support': ['need someone to talk to', 'feeling alone', 'need comfort'],
            'hope': ['see no way out', 'hopeless', 'pointless', 'nothing will change'],
            'understanding': ['why is this happening', 'don\'t understand', 'confused'],
            'control': ['out of control', 'helpless', 'powerless', 'can\'t handle']
        }

        identified_needs = []
        for need, indicators in needs_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                identified_needs.append(need)

        # Infer needs from emotional state
        emotion = basic_analysis['emotion']
        if emotion == 'sadness':
            identified_needs.extend(['validation', 'emotional_support'])
        elif emotion == 'fear':
            identified_needs.extend(['reassurance', 'understanding'])
        elif emotion == 'anger':
            identified_needs.extend(['validation', 'control'])

        return {
            'primary_needs': list(set(identified_needs)),
            'urgency': 'high' if 'hope' in identified_needs else 'moderate' if identified_needs else 'low',
            'support_type_needed': await self._determine_support_type(identified_needs)
        }

    async def _determine_support_type(self, needs: List[str]) -> str:
        """Determine what type of support is most needed"""
        if 'hope' in needs or 'validation' in needs:
            return 'emotional_support'
        elif 'practical_support' in needs or 'control' in needs:
            return 'practical_guidance'
        elif 'understanding' in needs:
            return 'psychoeducation'
        else:
            return 'general_support'

    async def _calculate_support_urgency(self, basic_analysis: Dict, intensity_analysis: Dict) -> str:
        """Calculate how urgently support is needed"""
        urgency_score = 0

        # High negative emotion increases urgency
        if basic_analysis['sentiment'] == 'NEGATIVE':
            urgency_score += basic_analysis['sentiment_score']

        # Crisis indicators
        if basic_analysis['crisis']:
            urgency_score += 3

        # High intensity emotions
        if intensity_analysis.get('intensity_level') == 'high':
            urgency_score += 2
        elif intensity_analysis.get('intensity_level') == 'extreme':
            urgency_score += 3

        # Determine urgency level
        if urgency_score >= 4:
            return 'immediate'
        elif urgency_score >= 2:
            return 'high'
        elif urgency_score >= 1:
            return 'moderate'
        else:
            return 'low'

    async def _identify_therapeutic_focus_areas(self, text: str, basic_analysis: Dict) -> List[str]:
        """Identify areas that might benefit from therapeutic focus"""
        text_lower = text.lower()
        focus_areas = []

        # Cognitive patterns
        if any(phrase in text_lower for phrase in ['always', 'never', 'everything', 'nothing', 'all or nothing']):
            focus_areas.append('cognitive_restructuring')

        # Emotional regulation
        if any(phrase in text_lower for phrase in ['can\'t control', 'overwhelming emotions', 'intense feelings']):
            focus_areas.append('emotional_regulation')

        # Behavioral patterns
        if any(phrase in text_lower for phrase in ['avoiding', 'procrastinating', 'can\'t do']):
            focus_areas.append('behavioral_activation')

        # Social skills
        if any(phrase in text_lower for phrase in ['no friends', 'social anxiety', 'hard to talk to people']):
            focus_areas.append('social_skills')

        # Trauma indicators
        if any(phrase in text_lower for phrase in ['flashbacks', 'nightmares', 'triggered']):
            focus_areas.append('trauma_processing')

        # Self-esteem
        if any(phrase in text_lower for phrase in ['worthless', 'not good enough', 'failure']):
            focus_areas.append('self_esteem_building')

        return focus_areas


class EmotionIntensityAnalyzer:
    """Analyzes the intensity of emotions in text"""

    async def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze emotional intensity"""
        text_lower = text.lower()

        # Intensity markers
        high_intensity_markers = ['extremely', 'completely', 'totally', 'absolutely']
        medium_intensity_markers = ['very', 'really', 'quite', 'pretty']

        # Count markers
        high_count = sum(1 for marker in high_intensity_markers if marker in text_lower)
        medium_count = sum(1 for marker in medium_intensity_markers if marker in text_lower)

        # Punctuation analysis
        exclamation_count = text.count('!')
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0

        # Calculate intensity score
        intensity_score = high_count * 3 + medium_count * 2 + exclamation_count * 1 + caps_ratio * 5

        # Determine intensity level
        if intensity_score >= 8:
            intensity_level = 'extreme'
        elif intensity_score >= 5:
            intensity_level = 'high'
        elif intensity_score >= 2:
            intensity_level = 'moderate'
        else:
            intensity_level = 'low'

        return {
            'intensity_score': min(10, intensity_score),
            'intensity_level': intensity_level,
            'markers_found': {
                'high_intensity': high_count,
                'medium_intensity': medium_count,
                'exclamations': exclamation_count,
                'caps_ratio': caps_ratio
            }
        }


class EmotionalComplexityAnalyzer:
    """Analyzes the complexity of emotional expression"""

    async def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze emotional complexity"""
        # This would analyze mixed emotions, emotional nuance, etc.
        # Simplified implementation for demo

        emotion_words = [
            'happy', 'sad', 'angry', 'afraid', 'excited', 'worried',
            'frustrated', 'disappointed', 'hopeful', 'confused'
        ]

        found_emotions = [word for word in emotion_words if word in text.lower()]

        complexity_level = (
            'high' if len(found_emotions) >= 3 else
            'moderate' if len(found_emotions) == 2 else
            'low'
        )

        return {
            'complexity_level': complexity_level,
            'emotion_count': len(found_emotions),
            'emotions_detected': found_emotions,
            'mixed_emotions': len(found_emotions) > 1
        }


class EmotionalRegulationAssessor:
    """Assesses emotional regulation capabilities"""

    async def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze emotional regulation indicators"""
        text_lower = text.lower()

        regulation_indicators = {
            'self_awareness': ['i feel', 'i notice', 'i realize', 'i understand'],
            'coping_attempts': ['trying to', 'working on', 'practicing', 'using'],
            'reflection': ['thinking about', 'reflecting', 'considering', 'wondering'],
            'seeking_help': ['need help', 'asking for', 'looking for', 'want to learn']
        }

        regulation_score = 0
        found_indicators = {}

        for category, indicators in regulation_indicators.items():
            matches = [ind for ind in indicators if ind in text_lower]
            if matches:
                regulation_score += len(matches)
                found_indicators[category] = matches

        stability_score = min(1.0, regulation_score / 10)

        return {
            'regulation_score': regulation_score,
            'stability_score': stability_score,
            'found_indicators': found_indicators,
            'regulation_level': (
                'good' if regulation_score >= 4 else
                'moderate' if regulation_score >= 2 else
                'needs_support'
            )
        }


class ContextualEmotionAnalyzer:
    """Analyzes contextual factors affecting emotions"""

    async def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze contextual emotional factors"""
        text_lower = text.lower()

        context_categories = {
            'interpersonal': ['relationship', 'friend', 'family', 'partner', 'people'],
            'work_academic': ['work', 'job', 'school', 'study', 'boss', 'teacher'],
            'health': ['sick', 'illness', 'pain', 'medical', 'health'],
            'financial': ['money', 'bills', 'debt', 'financial', 'afford'],
            'life_changes': ['moving', 'change', 'transition', 'new', 'different']
        }

        identified_contexts = []
        for category, keywords in context_categories.items():
            if any(keyword in text_lower for keyword in keywords):
                identified_contexts.append(category)

        return {
            'primary_contexts': identified_contexts,
            'context_complexity': len(identified_contexts),
            'multiple_stressors': len(identified_contexts) > 1
        }
