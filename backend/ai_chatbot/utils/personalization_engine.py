import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
from collections import defaultdict, Counter
import numpy as np


class PersonalizationEngine:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile_file = f"memory/{user_id}_personalization_profile.json"
        self.interaction_history_file = f"memory/{user_id}_interaction_patterns.json"
        self.personalization_profile = self.load_personalization_profile()
        self.interaction_patterns = self.load_interaction_patterns()

        # Initialize learning algorithms
        self.communication_analyzer = CommunicationStyleAnalyzer()
        self.preference_learner = PreferenceLearner()
        self.cultural_adapter = CulturalAdapter()

    def load_personalization_profile(self) -> Dict:
        """Load user's personalization profile"""
        if os.path.exists(self.profile_file):
            with open(self.profile_file, 'r') as f:
                return json.load(f)
        return self._create_default_profile()

    def load_interaction_patterns(self) -> Dict:
        """Load user's interaction patterns"""
        if os.path.exists(self.interaction_history_file):
            with open(self.interaction_history_file, 'r') as f:
                return json.load(f)
        return self._create_default_patterns()

    def save_personalization_profile(self):
        """Save personalization profile to file"""
        os.makedirs(os.path.dirname(self.profile_file), exist_ok=True)
        with open(self.profile_file, 'w') as f:
            json.dump(self.personalization_profile, f, indent=2)

    def save_interaction_patterns(self):
        """Save interaction patterns to file"""
        os.makedirs(os.path.dirname(self.interaction_history_file), exist_ok=True)
        with open(self.interaction_history_file, 'w') as f:
            json.dump(self.interaction_patterns, f, indent=2)

    def _create_default_profile(self) -> Dict:
        """Create default personalization profile for new users"""
        return {
            'communication_style': {
                'formality_level': 'moderate',  # formal, moderate, casual
                'empathy_preference': 'high',  # low, moderate, high
                'directness': 'balanced',  # direct, balanced, gentle
                'length_preference': 'moderate',  # brief, moderate, detailed
                'encouragement_style': 'supportive'  # motivational, supportive, gentle
            },
            'cultural_factors': {
                'language_preference': 'english',
                'cultural_background': 'western',
                'religious_considerations': 'inclusive',
                'family_orientation': 'individual_focused'
            },
            'therapeutic_preferences': {
                'approach_preference': ['cbt', 'mindfulness'],
                'intervention_intensity': 'moderate',
                'homework_acceptance': 'willing',
                'group_vs_individual': 'both'
            },
            'learning_style': {
                'information_processing': 'balanced',  # visual, auditory, balanced
                'learning_pace': 'moderate',  # slow, moderate, fast
                'example_preference': 'practical',  # theoretical, practical, mixed
                'repetition_tolerance': 'moderate'  # low, moderate, high
            },
            'life_context': {
                'life_stage': 'adult',
                'relationship_status': 'unknown',
                'work_status': 'unknown',
                'support_system_strength': 'moderate',
                'current_stressors': []
            },
            'successful_approaches': [],
            'ineffective_approaches': [],
            'preference_confidence': 0.1  # How confident we are in these preferences
        }

    def _create_default_patterns(self) -> Dict:
        """Create default interaction patterns"""
        return {
            'response_quality_ratings': [],
            'engagement_patterns': {
                'preferred_session_length': 'moderate',
                'optimal_interaction_times': [],
                'response_latency_preferences': 'immediate'
            },
            'topic_preferences': {
                'most_discussed': [],
                'most_helpful': [],
                'avoided_topics': []
            },
            'emotional_response_patterns': {
                'receptive_emotions': [],
                'challenging_emotions': [],
                'emotional_triggers': []
            },
            'intervention_effectiveness': {
                'most_effective': [],
                'least_effective': [],
                'context_dependent': []
            }
        }

    async def get_personalization_profile(self) -> Dict:
        """Get current personalization profile for use in responses"""
        return self.personalization_profile.copy()

    async def get_task_personalization(self, strategy: str) -> Dict:
        """Get personalization context for task creation"""
        profile = self.personalization_profile

        # Adapt communication style based on strategy
        adapted_style = await self._adapt_communication_for_strategy(strategy)

        return {
            'communication_style': adapted_style,
            'cultural_factors': profile['cultural_factors'],
            'successful_approaches': profile['successful_approaches'][-5:],  # Last 5 successful approaches
            'life_context': profile['life_context'],
            'therapeutic_goals': await self._get_current_therapeutic_goals(strategy)
        }

    async def learn_from_interaction(self, message: str, emotional_analysis: Dict,
                                     response: str = None, user_feedback: Dict = None):
        """Learn from user interaction to improve personalization"""

        # Analyze communication patterns
        communication_insights = await self.communication_analyzer.analyze_message(message)
        await self._update_communication_preferences(communication_insights)

        # Learn from emotional patterns
        await self._learn_emotional_patterns(emotional_analysis)

        # If response and feedback available, learn from effectiveness
        if response and user_feedback:
            await self._learn_response_effectiveness(response, user_feedback)

        # Update interaction patterns
        await self._update_interaction_patterns(message, emotional_analysis)

        # Increase confidence in preferences
        self.personalization_profile['preference_confidence'] = min(
            1.0, self.personalization_profile['preference_confidence'] + 0.01
        )

        # Save updates
        self.save_personalization_profile()
        self.save_interaction_patterns()

    async def _adapt_communication_for_strategy(self, strategy: str) -> Dict:
        """Adapt communication style based on intervention strategy"""
        base_style = self.personalization_profile['communication_style'].copy()

        # Strategy-specific adaptations
        if strategy == 'crisis_intervention':
            base_style['directness'] = 'direct'
            base_style['empathy_preference'] = 'high'
            base_style['length_preference'] = 'brief'
        elif strategy == 'depression_focused':
            base_style['empathy_preference'] = 'high'
            base_style['encouragement_style'] = 'gentle'
            base_style['directness'] = 'gentle'
        elif strategy == 'anxiety_management':
            base_style['directness'] = 'balanced'
            base_style['length_preference'] = 'detailed'
            base_style['encouragement_style'] = 'supportive'
        elif strategy == 'motivation_building':
            base_style['encouragement_style'] = 'motivational'
            base_style['directness'] = 'direct'

        return base_style

    async def _get_current_therapeutic_goals(self, strategy: str) -> List[str]:
        """Get current therapeutic goals based on strategy and user context"""
        base_goals = {
            'depression_focused': [
                'Improve mood regulation',
                'Increase daily activity engagement',
                'Challenge negative thought patterns',
                'Build self-compassion'
            ],
            'anxiety_management': [
                'Develop coping strategies for anxiety',
                'Practice relaxation techniques',
                'Build confidence in handling triggers',
                'Improve stress management'
            ],
            'stress_reduction': [
                'Identify stress triggers',
                'Develop healthy boundaries',
                'Improve time management',
                'Practice self-care'
            ],
            'social_connection': [
                'Build social skills',
                'Increase social interactions',
                'Develop meaningful relationships',
                'Overcome social anxiety'
            ],
            'motivation_building': [
                'Set achievable goals',
                'Build momentum through small wins',
                'Develop intrinsic motivation',
                'Create accountability systems'
            ]
        }

        return base_goals.get(strategy, ['Improve overall well-being'])

    async def _update_communication_preferences(self, insights: Dict):
        """Update communication preferences based on analysis"""
        current_prefs = self.personalization_profile['communication_style']

        # Update formality level
        if insights.get('prefers_formal_language'):
            current_prefs['formality_level'] = 'formal'
        elif insights.get('prefers_casual_language'):
            current_prefs['formality_level'] = 'casual'

        # Update length preference
        if insights.get('message_length') == 'short' and insights.get('engagement_high'):
            current_prefs['length_preference'] = 'brief'
        elif insights.get('message_length') == 'long' and insights.get('engagement_high'):
            current_prefs['length_preference'] = 'detailed'

        # Update directness preference
        if insights.get('responds_well_to_direct_questions'):
            current_prefs['directness'] = 'direct'
        elif insights.get('prefers_gentle_approach'):
            current_prefs['directness'] = 'gentle'

    async def _learn_emotional_patterns(self, emotional_analysis: Dict):
        """Learn from emotional patterns in user messages"""
        patterns = self.interaction_patterns['emotional_response_patterns']

        # Track emotions user expresses most
        dominant_emotion = emotional_analysis.get('emotion', 'neutral')
        if dominant_emotion not in patterns['receptive_emotions']:
            patterns['receptive_emotions'].append(dominant_emotion)

        # Track emotional triggers if negative emotions are strong
        if (emotional_analysis.get('sentiment') == 'NEGATIVE' and
                emotional_analysis.get('emotion_score', 0) > 0.8):
            # In a real system, would analyze context for triggers
            pass

    async def _learn_response_effectiveness(self, response: str, feedback: Dict):
        """Learn from user feedback on response effectiveness"""
        effectiveness = feedback.get('effectiveness_rating', 0)  # 0-5 scale
        helpfulness = feedback.get('helpfulness_rating', 0)

        if effectiveness >= 4:  # Good response
            # Extract successful patterns
            response_features = await self._extract_response_features(response)
            self.personalization_profile['successful_approaches'].extend(response_features)
        elif effectiveness <= 2:  # Poor response
            # Extract ineffective patterns
            response_features = await self._extract_response_features(response)
            self.personalization_profile['ineffective_approaches'].extend(response_features)

        # Keep only recent patterns (last 20)
        self.personalization_profile['successful_approaches'] = \
            self.personalization_profile['successful_approaches'][-20:]
        self.personalization_profile['ineffective_approaches'] = \
            self.personalization_profile['ineffective_approaches'][-20:]

    async def _update_interaction_patterns(self, message: str, emotional_analysis: Dict):
        """Update interaction patterns based on current interaction"""
        patterns = self.interaction_patterns

        # Update topic preferences
        message_topics = await self._extract_topics(message)
        patterns['topic_preferences']['most_discussed'].extend(message_topics)

        # Update emotional context
        emotional_context = {
            'emotion': emotional_analysis.get('emotion', 'neutral'),
            'sentiment': emotional_analysis.get('sentiment', 'NEUTRAL'),
            'timestamp': datetime.now().isoformat()
        }

        # Keep recent emotional contexts (last 50)
        if 'emotional_contexts' not in patterns:
            patterns['emotional_contexts'] = []
        patterns['emotional_contexts'].append(emotional_context)
        patterns['emotional_contexts'] = patterns['emotional_contexts'][-50:]

    async def _extract_response_features(self, response: str) -> List[str]:
        """Extract features from a response for learning"""
        features = []

        # Analyze response characteristics
        if len(response) < 100:
            features.append('brief_response')
        elif len(response) > 300:
            features.append('detailed_response')
        else:
            features.append('moderate_response')

        # Check for specific therapeutic approaches
        if any(word in response.lower() for word in ['breathe', 'breathing', 'breath']):
            features.append('breathing_techniques')

        if any(word in response.lower() for word in ['thought', 'thinking', 'thoughts']):
            features.append('cognitive_approach')

        if any(word in response.lower() for word in ['feel', 'feelings', 'emotions']):
            features.append('emotional_focus')

        if any(word in response.lower() for word in ['goal', 'step', 'action']):
            features.append('action_oriented')

        return features

    async def _extract_topics(self, message: str) -> List[str]:
        """Extract topics from user message"""
        # Simplified topic extraction
        topics = []
        message_lower = message.lower()

        topic_keywords = {
            'work_stress': ['work', 'job', 'boss', 'career', 'workplace'],
            'relationships': ['relationship', 'partner', 'boyfriend', 'girlfriend', 'marriage'],
            'family': ['family', 'parents', 'mother', 'father', 'siblings'],
            'health': ['health', 'sick', 'illness', 'medical', 'doctor'],
            'finances': ['money', 'financial', 'debt', 'bills', 'salary'],
            'social': ['friends', 'social', 'lonely', 'isolated', 'people'],
            'self_esteem': ['confidence', 'self-worth', 'worthless', 'failure', 'success']
        }

        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                topics.append(topic)

        return topics

    async def get_personalized_recommendations(self, current_context: Dict) -> Dict:
        """Get personalized recommendations based on learned preferences"""
        recommendations = {
            'communication_adjustments': [],
            'intervention_suggestions': [],
            'timing_recommendations': [],
            'content_preferences': []
        }

        # Communication adjustments
        comm_style = self.personalization_profile['communication_style']
        if comm_style['length_preference'] == 'brief':
            recommendations['communication_adjustments'].append(
                'Keep responses concise and focused'
            )
        elif comm_style['length_preference'] == 'detailed':
            recommendations['communication_adjustments'].append(
                'Provide comprehensive explanations and examples'
            )

        # Intervention suggestions based on successful approaches
        successful = self.personalization_profile['successful_approaches']
        if 'breathing_techniques' in successful:
            recommendations['intervention_suggestions'].append(
                'Include breathing exercises in interventions'
            )
        if 'cognitive_approach' in successful:
            recommendations['intervention_suggestions'].append(
                'Use cognitive reframing techniques'
            )

        return recommendations

    async def adapt_for_cultural_context(self, base_response: str, cultural_context: Dict) -> str:
        """Adapt response for cultural context"""
        return await self.cultural_adapter.adapt_response(base_response, cultural_context)

    async def predict_response_effectiveness(self, proposed_response: str,
                                             current_context: Dict) -> float:
        """Predict how effective a proposed response will be"""
        # Extract features from proposed response
        response_features = await self._extract_response_features(proposed_response)

        # Check against successful and ineffective patterns
        successful_features = set(self.personalization_profile['successful_approaches'])
        ineffective_features = set(self.personalization_profile['ineffective_approaches'])

        # Calculate effectiveness score
        success_matches = len(set(response_features) & successful_features)
        ineffective_matches = len(set(response_features) & ineffective_features)

        # Normalize to 0-1 scale
        if len(successful_features) > 0:
            success_score = success_matches / len(successful_features)
        else:
            success_score = 0.5  # Default if no history

        if len(ineffective_features) > 0:
            ineffective_penalty = ineffective_matches / len(ineffective_features)
        else:
            ineffective_penalty = 0

        effectiveness_score = max(0.0, success_score - ineffective_penalty * 0.5)

        # Adjust based on confidence in preferences
        confidence = self.personalization_profile['preference_confidence']
        return effectiveness_score * confidence + 0.5 * (1 - confidence)

    async def generate_user_insights(self) -> Dict:
        """Generate insights about the user for therapeutic purposes"""
        insights = {
            'communication_preferences': self.personalization_profile['communication_style'],
            'most_effective_approaches': Counter(
                self.personalization_profile['successful_approaches']
            ).most_common(5),
            'primary_topics_of_concern': Counter([
                topic for topics in self.interaction_patterns['topic_preferences']['most_discussed']
                for topic in topics
            ]).most_common(5),
            'emotional_patterns': await self._analyze_emotional_patterns(),
            'engagement_insights': await self._analyze_engagement_patterns(),
            'therapeutic_progress_indicators': await self._identify_progress_indicators()
        }

        return insights

    async def _analyze_emotional_patterns(self) -> Dict:
        """Analyze patterns in user's emotional expressions"""
        if 'emotional_contexts' not in self.interaction_patterns:
            return {'message': 'Insufficient data for emotional pattern analysis'}

        emotional_contexts = self.interaction_patterns['emotional_contexts']

        # Analyze recent emotional trends
        recent_emotions = [ctx['emotion'] for ctx in emotional_contexts[-10:]]
        recent_sentiments = [ctx['sentiment'] for ctx in emotional_contexts[-10:]]

        return {
            'dominant_recent_emotions': Counter(recent_emotions).most_common(3),
            'sentiment_trend': Counter(recent_sentiments).most_common(3),
            'emotional_stability': len(set(recent_emotions)) / len(recent_emotions) if recent_emotions else 0,
            'total_interactions_analyzed': len(emotional_contexts)
        }

    async def _analyze_engagement_patterns(self) -> Dict:
        """Analyze user engagement patterns"""
        # This would analyze engagement metrics from stored data
        return {
            'preferred_session_characteristics': 'moderate_length_high_empathy',
            'optimal_interaction_style': self.personalization_profile['communication_style'],
            'engagement_trend': 'increasing'  # This would be calculated from actual data
        }

    async def _identify_progress_indicators(self) -> List[str]:
        """Identify indicators of therapeutic progress"""
        progress_indicators = []

        # Check for positive communication changes
        if len(self.personalization_profile['successful_approaches']) > 10:
            progress_indicators.append('Increased responsiveness to therapeutic interventions')

        # Check confidence in preferences (indicates engagement)
        if self.personalization_profile['preference_confidence'] > 0.7:
            progress_indicators.append('Strong therapeutic alliance development')

        # Check emotional pattern improvements (would need more sophisticated analysis)
        if 'emotional_contexts' in self.interaction_patterns:
            recent_contexts = self.interaction_patterns['emotional_contexts'][-10:]
            positive_contexts = sum(1 for ctx in recent_contexts if ctx['sentiment'] == 'POSITIVE')
            if positive_contexts > len(recent_contexts) * 0.6:
                progress_indicators.append('Increased positive emotional expressions')

        return progress_indicators


class CommunicationStyleAnalyzer:
    """Analyzes user communication patterns to understand preferences"""

    async def analyze_message(self, message: str) -> Dict:
        """Analyze a message for communication style indicators"""
        analysis = {
            'message_length': 'short' if len(message) < 50 else 'medium' if len(message) < 200 else 'long',
            'formality_indicators': await self._analyze_formality(message),
            'emotional_openness': await self._analyze_emotional_openness(message),
            'question_patterns': await self._analyze_question_patterns(message),
            'response_style_preferences': await self._infer_response_preferences(message)
        }
        return analysis

    async def _analyze_formality(self, message: str) -> Dict:
        """Analyze formality level of message"""
        formal_indicators = ['please', 'thank you', 'would', 'could', 'might']
        casual_indicators = ['hey', 'yeah', 'gonna', 'wanna', 'kinda']

        formal_count = sum(1 for indicator in formal_indicators if indicator in message.lower())
        casual_count = sum(1 for indicator in casual_indicators if indicator in message.lower())

        return {
            'formal_score': formal_count / len(message.split()) if message.split() else 0,
            'casual_score': casual_count / len(message.split()) if message.split() else 0,
            'likely_preference': 'formal' if formal_count > casual_count else 'casual' if casual_count > 0 else 'neutral'
        }

    async def _analyze_emotional_openness(self, message: str) -> Dict:
        """Analyze emotional openness in message"""
        emotion_words = ['feel', 'feeling', 'emotions', 'sad', 'happy', 'angry', 'anxious', 'worried']
        emotion_count = sum(1 for word in emotion_words if word in message.lower())

        return {
            'emotional_words_count': emotion_count,
            'openness_level': 'high' if emotion_count > 2 else 'moderate' if emotion_count > 0 else 'low'
        }

    async def _analyze_question_patterns(self, message: str) -> Dict:
        """Analyze question patterns to understand information seeking style"""
        question_count = message.count('?')
        seeks_specific_help = any(phrase in message.lower() for phrase in ['how do i', 'what should', 'can you help'])

        return {
            'question_count': question_count,
            'seeks_specific_help': seeks_specific_help,
            'information_seeking_style': 'direct' if seeks_specific_help else 'exploratory' if question_count > 0 else 'sharing'
        }

    async def _infer_response_preferences(self, message: str) -> Dict:
        """Infer what kind of responses the user might prefer"""
        preferences = {
            'likely_wants_practical_advice': any(
                phrase in message.lower() for phrase in ['what should i do', 'how can i', 'what steps']),
            'likely_wants_emotional_support': any(
                phrase in message.lower() for phrase in ['feeling', 'struggling', 'hard time']),
            'likely_wants_information': any(phrase in message.lower() for phrase in ['what is', 'why does', 'explain'])
        }
        return preferences


class PreferenceLearner:
    """Learns user preferences from interaction patterns"""

    def __init__(self):
        self.preference_weights = {
            'response_length': 0.0,
            'empathy_level': 0.0,
            'directness': 0.0,
            'practical_vs_emotional': 0.0
        }

    async def update_preferences(self, interaction_data: Dict, feedback: Dict):
        """Update preference weights based on interaction feedback"""
        # Implementation would adjust weights based on feedback
        pass


class CulturalAdapter:
    """Adapts responses for cultural sensitivity"""

    async def adapt_response(self, response: str, cultural_context: Dict) -> str:
        """Adapt response for cultural context"""
        # This would implement cultural adaptations
        # For now, return response as-is
        return response

    async def get_cultural_considerations(self, cultural_background: str) -> Dict:
        """Get cultural considerations for a specific background"""
        considerations = {
            'western': {
                'individualism_focus': True,
                'direct_communication': 'acceptable',
                'family_involvement': 'optional'
            },
            'eastern': {
                'collectivism_focus': True,
                'indirect_communication': 'preferred',
                'family_involvement': 'important'
            },
            'latin': {
                'family_orientation': 'high',
                'religious_considerations': 'important',
                'community_focus': 'strong'
            }
        }
        return considerations.get(cultural_background, considerations['western'])
