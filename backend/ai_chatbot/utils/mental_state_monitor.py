import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pickle


class MentalStateMonitor:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.data_file = f"memory/{user_id}_mental_state_history.json"
        self.state_history = self.load_state_history()
        self.depression_indicators = [
            'hopelessness', 'worthlessness', 'fatigue', 'loss_of_interest',
            'sleep_disturbance', 'appetite_change', 'concentration_difficulty'
        ]
        self.anxiety_indicators = [
            'worry', 'restlessness', 'tension', 'fear', 'panic',
            'avoidance', 'physical_symptoms', 'racing_thoughts'
        ]
        self.stress_indicators = [
            'overwhelm', 'pressure', 'irritability', 'muscle_tension',
            'headaches', 'difficulty_relaxing', 'time_pressure'
        ]

        # Initialize ML models for pattern recognition
        self.pattern_analyzer = self._initialize_pattern_analyzer()

    def load_state_history(self) -> List[Dict]:
        """Load user's mental state history from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []

    def save_state_history(self):
        """Save mental state history to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.state_history, f, indent=2)

    async def assess_current_state(self, message: str, emotional_analysis: Dict, user_context: Any) -> Dict:
        """Comprehensive assessment of current mental state"""
        # Analyze message content for mental health indicators
        content_indicators = await self._analyze_message_content(message)

        # Assess emotional patterns
        emotional_patterns = await self._assess_emotional_patterns(emotional_analysis)

        # Calculate risk factors
        risk_assessment = await self._calculate_risk_factors(content_indicators, emotional_patterns)

        # Determine intervention needs
        intervention_priority = await self._determine_intervention_priority(risk_assessment)

        # Generate overall mental state score
        overall_score = await self._calculate_overall_score(risk_assessment)

        current_state = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': overall_score,
            'depression_indicators': risk_assessment['depression_score'],
            'anxiety_indicators': risk_assessment['anxiety_score'],
            'stress_indicators': risk_assessment['stress_score'],
            'energy_level': emotional_patterns.get('energy_level', 0.5),
            'motivation_level': emotional_patterns.get('motivation_level', 0.5),
            'mood_indicators': emotional_patterns.get('mood_score', 0.5),
            'social_connection': emotional_patterns.get('social_indicators', 0.5),
            'coping_effectiveness': await self._assess_coping_effectiveness(),
            'stagnation_indicators': await self._detect_stagnation_patterns(),
            'intervention_priority': intervention_priority,
            'warning_signs': content_indicators.get('warning_signs', []),
            'positive_indicators': content_indicators.get('positive_indicators', [])
        }

        # Store in history for pattern analysis
        self.state_history.append(current_state)
        self.save_state_history()

        # Update pattern analyzer
        await self._update_pattern_analysis(current_state)

        return current_state

    async def _analyze_message_content(self, message: str) -> Dict:
        """Analyze message content for mental health indicators"""
        message_lower = message.lower()

        # Depression indicators analysis
        depression_matches = []
        for indicator in self.depression_indicators:
            related_terms = self._get_related_terms(indicator)
            if any(term in message_lower for term in related_terms):
                depression_matches.append(indicator)

        # Anxiety indicators analysis
        anxiety_matches = []
        for indicator in self.anxiety_indicators:
            related_terms = self._get_related_terms(indicator)
            if any(term in message_lower for term in related_terms):
                anxiety_matches.append(indicator)

        # Stress indicators analysis
        stress_matches = []
        for indicator in self.stress_indicators:
            related_terms = self._get_related_terms(indicator)
            if any(term in message_lower for term in related_terms):
                stress_matches.append(indicator)

        # Positive indicators
        positive_indicators = self._detect_positive_indicators(message_lower)

        # Warning signs
        warning_signs = self._detect_warning_signs(message_lower)

        return {
            'depression_matches': depression_matches,
            'anxiety_matches': anxiety_matches,
            'stress_matches': stress_matches,
            'positive_indicators': positive_indicators,
            'warning_signs': warning_signs,
            'message_length': len(message),
            'emotional_words_count': self._count_emotional_words(message_lower)
        }

    async def _assess_emotional_patterns(self, emotional_analysis: Dict) -> Dict:
        """Assess patterns in emotional analysis"""
        # Get recent emotional history for comparison
        recent_states = self.get_recent_states(days=7)

        # Calculate emotional trajectory
        emotional_trajectory = self._calculate_emotional_trajectory(recent_states)

        # Assess energy levels based on language patterns
        energy_level = self._assess_energy_level(emotional_analysis)

        # Assess motivation level
        motivation_level = self._assess_motivation_level(emotional_analysis)

        # Calculate mood score
        mood_score = self._calculate_mood_score(emotional_analysis)

        # Assess social connection indicators
        social_indicators = self._assess_social_connection(emotional_analysis)

        return {
            'emotional_trajectory': emotional_trajectory,
            'energy_level': energy_level,
            'motivation_level': motivation_level,
            'mood_score': mood_score,
            'social_indicators': social_indicators,
            'emotional_stability': emotional_trajectory.get('stability', 0.5),
            'emotional_trend': emotional_trajectory.get('trend', 'stable')
        }

    async def _calculate_risk_factors(self, content_indicators: Dict, emotional_patterns: Dict) -> Dict:
        """Calculate comprehensive risk factors"""
        # Depression risk calculation
        depression_content_score = len(content_indicators['depression_matches']) / len(self.depression_indicators)
        depression_emotional_score = 1.0 - emotional_patterns['mood_score']
        depression_score = (depression_content_score * 0.6 + depression_emotional_score * 0.4)

        # Anxiety risk calculation
        anxiety_content_score = len(content_indicators['anxiety_matches']) / len(self.anxiety_indicators)
        anxiety_emotional_score = emotional_patterns.get('anxiety_indicators', 0.3)
        anxiety_score = (anxiety_content_score * 0.7 + anxiety_emotional_score * 0.3)

        # Stress risk calculation
        stress_content_score = len(content_indicators['stress_matches']) / len(self.stress_indicators)
        stress_emotional_score = 1.0 - emotional_patterns['energy_level']
        stress_score = (stress_content_score * 0.5 + stress_emotional_score * 0.5)

        # Overall risk factors
        warning_signs_weight = len(content_indicators['warning_signs']) * 0.2
        positive_factors_weight = len(content_indicators['positive_indicators']) * -0.1

        return {
            'depression_score': min(1.0, depression_score + warning_signs_weight + positive_factors_weight),
            'anxiety_score': min(1.0, anxiety_score + warning_signs_weight + positive_factors_weight),
            'stress_score': min(1.0, stress_score + warning_signs_weight + positive_factors_weight),
            'overall_risk': (depression_score + anxiety_score + stress_score) / 3
        }

    async def _determine_intervention_priority(self, risk_assessment: Dict) -> str:
        """Determine the priority level for intervention"""
        max_risk = max(
            risk_assessment['depression_score'],
            risk_assessment['anxiety_score'],
            risk_assessment['stress_score']
        )

        if max_risk >= 0.8:
            return 'high'
        elif max_risk >= 0.6:
            return 'moderate'
        elif max_risk >= 0.4:
            return 'low'
        else:
            return 'maintenance'

    async def _calculate_overall_score(self, risk_assessment: Dict) -> float:
        """Calculate overall mental health score (0-1, higher is better)"""
        return 1.0 - risk_assessment['overall_risk']

    async def get_current_struggles(self) -> List[str]:
        """Get current primary struggles based on recent assessments"""
        if not self.state_history:
            return ['general_support_needed']

        recent_state = self.state_history[-1]
        struggles = []

        if recent_state['depression_indicators'] > 0.6:
            struggles.append('depression')
        if recent_state['anxiety_indicators'] > 0.6:
            struggles.append('anxiety')
        if recent_state['stress_indicators'] > 0.6:
            struggles.append('stress')
        if recent_state['energy_level'] < 0.3:
            struggles.append('low_energy')
        if recent_state['motivation_level'] < 0.3:
            struggles.append('motivation_issues')
        if recent_state['social_connection'] < 0.4:
            struggles.append('social_isolation')

        return struggles if struggles else ['general_support_needed']

    def get_recent_states(self, days: int = 7) -> List[Dict]:
        """Get mental states from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_states = []

        for state in self.state_history:
            state_date = datetime.fromisoformat(state['timestamp'])
            if state_date >= cutoff_date:
                recent_states.append(state)

        return recent_states

    async def _assess_coping_effectiveness(self) -> float:
        """Assess how effectively the user is coping based on patterns"""
        recent_states = self.get_recent_states(days=14)

        if len(recent_states) < 3:
            return 0.5  # Default if insufficient data

        # Calculate trend in overall scores
        scores = [state['overall_score'] for state in recent_states]
        if len(scores) > 1:
            trend = (scores[-1] - scores[0]) / len(scores)
            return max(0.0, min(1.0, 0.5 + trend))

        return 0.5

    async def _detect_stagnation_patterns(self) -> float:
        """Detect if user is stuck in negative patterns"""
        recent_states = self.get_recent_states(days=30)

        if len(recent_states) < 5:
            return 0.0

        # Check for lack of improvement over time
        scores = [state['overall_score'] for state in recent_states]
        variance = np.var(scores) if scores else 0
        mean_score = np.mean(scores) if scores else 0.5

        # High stagnation if low variance and low mean score
        if variance < 0.01 and mean_score < 0.4:
            return 0.8
        elif variance < 0.05 and mean_score < 0.5:
            return 0.6
        else:
            return max(0.0, 0.4 - variance * 10)

    def _get_related_terms(self, indicator: str) -> List[str]:
        """Get related terms for each mental health indicator"""
        term_mapping = {
            'hopelessness': ['hopeless', 'no point', 'give up', 'nothing matters', 'no future'],
            'worthlessness': ['worthless', 'useless', 'failure', 'not good enough', 'waste of space'],
            'fatigue': ['tired', 'exhausted', 'drained', 'no energy', 'worn out'],
            'loss_of_interest': ['don\'t care', 'nothing interests', 'bored', 'apathetic'],
            'worry': ['worried', 'anxious', 'concerned', 'afraid', 'scared'],
            'restlessness': ['restless', 'can\'t sit still', 'agitated', 'fidgety'],
            'overwhelm': ['overwhelmed', 'too much', 'can\'t handle', 'drowning'],
            'pressure': ['pressure', 'stressed', 'burden', 'weight on shoulders']
        }
        return term_mapping.get(indicator, [indicator])

    def _detect_positive_indicators(self, message: str) -> List[str]:
        """Detect positive indicators in the message"""
        positive_terms = {
            'gratitude': ['grateful', 'thankful', 'appreciate', 'blessed'],
            'hope': ['hope', 'optimistic', 'looking forward', 'excited'],
            'achievement': ['accomplished', 'proud', 'success', 'achieved'],
            'connection': ['friends', 'family', 'loved ones', 'support'],
            'growth': ['learning', 'growing', 'improving', 'better']
        }

        detected = []
        for category, terms in positive_terms.items():
            if any(term in message for term in terms):
                detected.append(category)

        return detected

    def _detect_warning_signs(self, message: str) -> List[str]:
        """Detect serious warning signs in the message"""
        warning_terms = {
            'self_harm': ['hurt myself', 'self harm', 'cut myself', 'harm myself'],
            'suicidal_ideation': ['kill myself', 'end it all', 'not worth living', 'better off dead'],
            'substance_abuse': ['drinking too much', 'using drugs', 'getting high', 'numbing'],
            'social_isolation': ['no one cares', 'all alone', 'nobody understands', 'isolated']
        }

        detected = []
        for category, terms in warning_terms.items():
            if any(term in message for term in terms):
                detected.append(category)

        return detected

    def _count_emotional_words(self, message: str) -> int:
        """Count emotional words in the message"""
        emotional_words = [
            'happy', 'sad', 'angry', 'frustrated', 'excited', 'worried',
            'anxious', 'depressed', 'hopeful', 'fearful', 'lonely', 'loved'
        ]
        return sum(1 for word in emotional_words if word in message)

    def _calculate_emotional_trajectory(self, recent_states: List[Dict]) -> Dict:
        """Calculate emotional trajectory over recent states"""
        if len(recent_states) < 2:
            return {'trend': 'stable', 'stability': 0.5}

        scores = [state['overall_score'] for state in recent_states]

        # Calculate trend
        if scores[-1] > scores[0] + 0.1:
            trend = 'improving'
        elif scores[-1] < scores[0] - 0.1:
            trend = 'declining'
        else:
            trend = 'stable'

        # Calculate stability (inverse of variance)
        stability = max(0.0, 1.0 - np.var(scores) * 4)

        return {
            'trend': trend,
            'stability': stability,
            'average_score': np.mean(scores),
            'score_range': max(scores) - min(scores)
        }

    def _assess_energy_level(self, emotional_analysis: Dict) -> float:
        """Assess energy level from emotional analysis"""
        # This would be more sophisticated in a real implementation
        sentiment_score = emotional_analysis.get('sentiment_score', 0.5)
        emotion_score = emotional_analysis.get('emotion_score', 0.5)

        return (sentiment_score + emotion_score) / 2

    def _assess_motivation_level(self, emotional_analysis: Dict) -> float:
        """Assess motivation level from emotional analysis"""
        # Check for motivation-related keywords and sentiment
        base_score = emotional_analysis.get('sentiment_score', 0.5)

        # Adjust based on detected emotions
        dominant_emotion = emotional_analysis.get('emotion', 'neutral')
        if dominant_emotion in ['joy', 'excitement', 'hope']:
            return min(1.0, base_score + 0.2)
        elif dominant_emotion in ['sadness', 'fear', 'anger']:
            return max(0.0, base_score - 0.2)

        return base_score

    def _calculate_mood_score(self, emotional_analysis: Dict) -> float:
        """Calculate overall mood score"""
        sentiment_score = emotional_analysis.get('sentiment_score', 0.5)

        # Adjust for sentiment label
        sentiment_label = emotional_analysis.get('sentiment', 'NEUTRAL')
        if sentiment_label == 'POSITIVE':
            return min(1.0, sentiment_score + 0.1)
        elif sentiment_label == 'NEGATIVE':
            return max(0.0, sentiment_score - 0.1)

        return sentiment_score

    def _assess_social_connection(self, emotional_analysis: Dict) -> float:
        """Assess social connection indicators"""
        # This would analyze language patterns for social connection
        # For now, return a default value
        return 0.5

    def _initialize_pattern_analyzer(self):
        """Initialize ML models for pattern analysis"""
        # This would load pre-trained models or initialize new ones
        # For now, return a simple placeholder
        return None

    async def _update_pattern_analysis(self, current_state: Dict):
        """Update pattern analysis with new state data"""
        # This would update ML models with new data
        pass

    async def generate_insights_report(self) -> Dict:
        """Generate comprehensive insights report"""
        recent_states = self.get_recent_states(days=30)

        if not recent_states:
            return {'message': 'Insufficient data for insights'}

        # Calculate trends
        scores = [state['overall_score'] for state in recent_states]
        trend_analysis = self._calculate_emotional_trajectory(recent_states)

        # Identify patterns
        patterns = await self._identify_patterns(recent_states)

        # Generate recommendations
        recommendations = await self._generate_personalized_recommendations(recent_states)

        return {
            'timeframe': '30 days',
            'data_points': len(recent_states),
            'overall_trend': trend_analysis['trend'],
            'stability_score': trend_analysis['stability'],
            'average_mental_health_score': trend_analysis['average_score'],
            'identified_patterns': patterns,
            'recommendations': recommendations,
            'current_struggles': await self.get_current_struggles(),
            'progress_indicators': await self._identify_progress_indicators(recent_states)
        }

    async def _identify_patterns(self, states: List[Dict]) -> List[str]:
        """Identify patterns in mental health states"""
        patterns = []

        # Check for weekly patterns
        if len(states) >= 7:
            # Analyze day of week patterns, time patterns, etc.
            patterns.append("Weekly pattern analysis available")

        # Check for intervention effectiveness
        # This would analyze if certain interventions correlate with improvements

        return patterns

    async def _generate_personalized_recommendations(self, states: List[Dict]) -> List[Dict]:
        """Generate personalized recommendations based on patterns"""
        if not states:
            return []

        latest_state = states[-1]
        recommendations = []

        # Depression-focused recommendations
        if latest_state['depression_indicators'] > 0.6:
            recommendations.append({
                'type': 'intervention',
                'priority': 'high',
                'recommendation': 'Consider CBT-based interventions for depression',
                'rationale': 'High depression indicators detected'
            })

        # Anxiety management recommendations
        if latest_state['anxiety_indicators'] > 0.6:
            recommendations.append({
                'type': 'wellness',
                'priority': 'high',
                'recommendation': 'Practice daily mindfulness and breathing exercises',
                'rationale': 'High anxiety indicators detected'
            })

        # Energy and motivation recommendations
        if latest_state['energy_level'] < 0.3:
            recommendations.append({
                'type': 'lifestyle',
                'priority': 'moderate',
                'recommendation': 'Incorporate gentle physical activity and proper sleep hygiene',
                'rationale': 'Low energy levels detected'
            })

        return recommendations

    async def _identify_progress_indicators(self, states: List[Dict]) -> List[str]:
        """Identify positive progress indicators"""
        if len(states) < 2:
            return []

        progress_indicators = []
        latest = states[-1]
        previous = states[-2]

        if latest['overall_score'] > previous['overall_score']:
            progress_indicators.append("Overall mental health score improving")

        if latest['coping_effectiveness'] > previous['coping_effectiveness']:
            progress_indicators.append("Coping strategies becoming more effective")

        if len(latest['positive_indicators']) > len(previous['positive_indicators']):
            progress_indicators.append("Increased positive emotional expressions")

        return progress_indicators
