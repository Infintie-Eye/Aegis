from crewai_tools import BaseTool
from typing import Optional, Type, Any, Dict, List
from pydantic import BaseModel, Field
import json
import re


class AssessmentInput(BaseModel):
    """Input schema for Assessment Tools."""
    message: str = Field(..., description="The user's message to assess")
    context: Optional[str] = Field(None, description="Additional context about the user")


class CrisisAssessmentTool(BaseTool):
    name: str = "Crisis Assessment Tool"
    description: str = (
        "Assesses crisis risk level including suicidal ideation, self-harm, and immediate danger. "
        "Returns risk level (0-10), specific crisis indicators found, and urgency classification. "
        "Use this when user messages suggest distress, hopelessness, or mention self-harm."
    )
    args_schema: Type[BaseModel] = AssessmentInput

    def _run(self, message: str, context: Optional[str] = None) -> str:
        """Execute crisis assessment on user message."""
        message_lower = message.lower()

        # Crisis keyword categories with severity weights
        crisis_indicators = {
            'immediate_danger': {
                'keywords': [
                    'suicide', 'kill myself', 'end my life', 'want to die',
                    'better off dead', 'take my own life', 'end it all',
                    'overdose', 'jump off', 'hang myself', 'gun', 'pills'
                ],
                'weight': 10
            },
            'self_harm': {
                'keywords': [
                    'cut myself', 'cutting', 'self harm', 'hurt myself',
                    'burning myself', 'hitting myself', 'punish myself'
                ],
                'weight': 8
            },
            'severe_ideation': {
                'keywords': [
                    'plan to', 'thinking about ending', 'not worth living',
                    'everyone better off', 'burden to everyone', 'can\'t go on'
                ],
                'weight': 9
            },
            'moderate_risk': {
                'keywords': [
                    'hopeless', 'worthless', 'give up', 'no point',
                    'nothing matters', 'waste of space', 'tired of living'
                ],
                'weight': 6
            },
            'low_risk': {
                'keywords': [
                    'struggling', 'hard time', 'feeling down', 'depressed',
                    'anxious', 'stressed', 'overwhelmed'
                ],
                'weight': 3
            }
        }

        # Protective factors that reduce risk
        protective_factors = [
            'getting help', 'therapy', 'counselor', 'support group',
            'friends support', 'family helps', 'talking to someone',
            'want to get better', 'trying to cope'
        ]

        # Assessment results
        total_risk_score = 0
        found_indicators = {}
        found_protective = []

        # Check for crisis indicators
        for category, data in crisis_indicators.items():
            matches = [kw for kw in data['keywords'] if kw in message_lower]
            if matches:
                total_risk_score += data['weight'] * len(matches)
                found_indicators[category] = matches

        # Check for protective factors (reduce risk)
        for factor in protective_factors:
            if factor in message_lower:
                found_protective.append(factor)
                total_risk_score = max(0, total_risk_score - 2)

        # Normalize risk score to 0-10 scale
        risk_level = min(10, total_risk_score)

        # Determine urgency classification
        if risk_level >= 9:
            urgency = "CRITICAL - Immediate intervention required"
        elif risk_level >= 7:
            urgency = "HIGH - Urgent support needed"
        elif risk_level >= 5:
            urgency = "MODERATE - Close monitoring required"
        elif risk_level >= 3:
            urgency = "LOW-MODERATE - Supportive intervention"
        else:
            urgency = "LOW - Standard support"

        # Compile assessment report
        assessment = {
            "risk_level": risk_level,
            "urgency_classification": urgency,
            "crisis_indicators_found": found_indicators,
            "protective_factors": found_protective,
            "immediate_action_required": risk_level >= 7,
            "recommend_emergency_services": risk_level >= 9,
            "safety_plan_needed": risk_level >= 5,
            "assessment_summary": self._generate_summary(risk_level, found_indicators, found_protective)
        }

        return json.dumps(assessment, indent=2)

    def _generate_summary(self, risk_level: int, indicators: Dict, protective: List) -> str:
        """Generate human-readable assessment summary."""
        if risk_level >= 9:
            return (
                f"CRITICAL RISK DETECTED. Multiple severe crisis indicators found. "
                f"Immediate professional intervention and emergency services consideration required."
            )
        elif risk_level >= 7:
            return (
                f"High risk level identified with {len(indicators)} categories of concern. "
                f"Urgent mental health support and safety planning needed."
            )
        elif risk_level >= 5:
            return (
                f"Moderate risk present. User showing signs of distress. "
                f"Proactive support and safety planning recommended."
            )
        elif risk_level >= 3:
            return (
                f"User experiencing emotional difficulties but at lower risk. "
                f"Supportive therapeutic intervention appropriate."
            )
        else:
            return (
                f"Low risk assessment. Standard support and monitoring appropriate. "
                f"{len(protective)} protective factors identified."
            )


class MentalHealthScreeningTool(BaseTool):
    name: str = "Mental Health Screening Tool"
    description: str = (
        "Screens for common mental health conditions including depression, anxiety, "
        "PTSD, and stress disorders. Returns symptom indicators and severity levels. "
        "Use when you need to understand the user's mental health presentation."
    )
    args_schema: Type[BaseModel] = AssessmentInput

    def _run(self, message: str, context: Optional[str] = None) -> str:
        """Screen for mental health conditions."""
        message_lower = message.lower()

        # Depression symptom clusters (DSM-5 aligned)
        depression_symptoms = {
            'mood': ['depressed', 'sad', 'down', 'empty', 'hopeless', 'miserable'],
            'anhedonia': ['no pleasure', 'don\'t enjoy', 'lost interest', 'nothing is fun'],
            'sleep': ['can\'t sleep', 'insomnia', 'sleeping too much', 'sleep all day'],
            'energy': ['tired', 'exhausted', 'no energy', 'fatigue', 'drained'],
            'appetite': ['no appetite', 'not eating', 'eating too much', 'weight'],
            'concentration': ['can\'t focus', 'can\'t concentrate', 'memory problems'],
            'worthlessness': ['worthless', 'failure', 'useless', 'not good enough'],
            'psychomotor': ['agitated', 'restless', 'slowed down', 'moving slowly'],
            'death_thoughts': ['death', 'dying', 'better off dead', 'suicide']
        }

        # Anxiety symptom clusters (DSM-5 aligned)
        anxiety_symptoms = {
            'worry': ['worried', 'anxious', 'nervous', 'on edge', 'tense'],
            'physical': ['heart racing', 'sweating', 'shaking', 'trembling', 'shortness of breath'],
            'restlessness': ['restless', 'keyed up', 'can\'t relax', 'fidgety'],
            'fatigue': ['tired', 'exhausted', 'worn out'],
            'concentration': ['can\'t concentrate', 'mind goes blank', 'can\'t focus'],
            'irritability': ['irritable', 'on edge', 'snappy', 'angry'],
            'muscle_tension': ['tense', 'tight muscles', 'sore', 'aching'],
            'sleep_disturbance': ['can\'t sleep', 'trouble falling asleep', 'restless sleep'],
            'avoidance': ['avoiding', 'can\'t face', 'staying away from']
        }

        # PTSD symptoms
        ptsd_symptoms = {
            'intrusion': ['flashbacks', 'nightmares', 'intrusive thoughts', 'reliving'],
            'avoidance': ['avoiding reminders', 'can\'t think about', 'blocking out'],
            'negative_cognition': ['blame myself', 'negative beliefs', 'can\'t remember'],
            'arousal': ['hypervigilant', 'easily startled', 'on guard', 'trouble sleeping']
        }

        # Stress indicators
        stress_symptoms = {
            'overwhelm': ['overwhelmed', 'too much', 'can\'t cope', 'drowning'],
            'pressure': ['pressure', 'stressed', 'burden', 'weight on shoulders'],
            'physical': ['headaches', 'stomach problems', 'tension', 'pain']
        }

        # Screen for each condition
        def screen_condition(symptom_dict: Dict) -> Dict:
            found_symptoms = {}
            total_score = 0
            for cluster, symptoms in symptom_dict.items():
                matches = [s for s in symptoms if s in message_lower]
                if matches:
                    found_symptoms[cluster] = matches
                    total_score += len(matches)

            severity = (
                'severe' if total_score >= 7 else
                'moderate' if total_score >= 4 else
                'mild' if total_score >= 2 else
                'minimal'
            )

            return {
                'symptom_clusters': found_symptoms,
                'total_indicators': total_score,
                'severity': severity,
                'clusters_affected': len(found_symptoms)
            }

        # Perform screening
        results = {
            'depression_screening': screen_condition(depression_symptoms),
            'anxiety_screening': screen_condition(anxiety_symptoms),
            'ptsd_screening': screen_condition(ptsd_symptoms),
            'stress_screening': screen_condition(stress_symptoms),
            'primary_concern': None,
            'comorbidity_present': False,
            'clinical_features': []
        }

        # Determine primary concern
        severity_scores = {
            'depression': results['depression_screening']['total_indicators'],
            'anxiety': results['anxiety_screening']['total_indicators'],
            'ptsd': results['ptsd_screening']['total_indicators'],
            'stress': results['stress_screening']['total_indicators']
        }

        if max(severity_scores.values()) > 0:
            results['primary_concern'] = max(severity_scores, key=severity_scores.get)

            # Check for comorbidity (multiple conditions)
            significant_conditions = sum(1 for score in severity_scores.values() if score >= 3)
            results['comorbidity_present'] = significant_conditions >= 2

        # Add clinical features summary
        results['clinical_features'] = self._identify_clinical_features(message_lower, results)
        results['screening_summary'] = self._generate_screening_summary(results)

        return json.dumps(results, indent=2)

    def _identify_clinical_features(self, message: str, screening_results: Dict) -> List[str]:
        """Identify notable clinical features."""
        features = []

        # Check for cognitive distortions
        distortions = {
            'all_or_nothing': ['always', 'never', 'everyone', 'no one', 'nothing'],
            'catastrophizing': ['worst', 'terrible', 'disaster', 'awful', 'horrible'],
            'overgeneralization': ['always happens', 'never works', 'everything'],
            'mind_reading': ['they think', 'knows I', 'everyone sees']
        }

        for distortion_type, indicators in distortions.items():
            if any(ind in message for ind in indicators):
                features.append(f"cognitive_distortion_{distortion_type}")

        # Check severity
        if screening_results['depression_screening']['severity'] in ['moderate', 'severe']:
            features.append("significant_depressive_symptoms")
        if screening_results['anxiety_screening']['severity'] in ['moderate', 'severe']:
            features.append("significant_anxiety_symptoms")

        return features

    def _generate_screening_summary(self, results: Dict) -> str:
        """Generate screening summary."""
        primary = results['primary_concern']
        if not primary:
            return "Screening indicates subclinical symptom presentation."

        severity = results[f'{primary}_screening']['severity']
        comorbid = "with comorbid symptoms" if results['comorbidity_present'] else ""

        return (
            f"Screening indicates {severity} {primary} symptoms {comorbid}. "
            f"{len(results['clinical_features'])} clinical features identified."
        )


class EmotionalStateAssessmentTool(BaseTool):
    name: str = "Emotional State Assessment Tool"
    description: str = (
        "Assesses current emotional state including intensity, regulation capacity, "
        "and emotional needs. Use this to understand the user's immediate emotional experience."
    )
    args_schema: Type[BaseModel] = AssessmentInput

    def _run(self, message: str, context: Optional[str] = None) -> str:
        """Assess emotional state from message."""
        message_lower = message.lower()

        # Emotion categories with intensity markers
        emotions = {
            'sadness': ['sad', 'depressed', 'down', 'miserable', 'heartbroken', 'devastated'],
            'anxiety': ['anxious', 'worried', 'nervous', 'scared', 'afraid', 'terrified'],
            'anger': ['angry', 'mad', 'furious', 'frustrated', 'irritated', 'rage'],
            'fear': ['afraid', 'scared', 'terrified', 'frightened', 'panic'],
            'shame': ['ashamed', 'embarrassed', 'humiliated', 'guilty'],
            'loneliness': ['lonely', 'alone', 'isolated', 'abandoned'],
            'hopelessness': ['hopeless', 'pointless', 'no hope', 'futile']
        }

        # Intensity modifiers
        high_intensity = ['extremely', 'very', 'so', 'really', 'completely', 'totally']

        # Detect emotions
        detected_emotions = {}
        for emotion, keywords in emotions.items():
            matches = [kw for kw in keywords if kw in message_lower]
            if matches:
                # Calculate intensity
                intensity = 'moderate'
                for modifier in high_intensity:
                    if any(f"{modifier} {kw}" in message_lower for kw in matches):
                        intensity = 'high'
                        break

                detected_emotions[emotion] = {
                    'present': True,
                    'intensity': intensity,
                    'indicators': matches
                }

        # Assess emotional regulation
        regulation_indicators = {
            'good': ['trying to cope', 'using strategies', 'working on it', 'managing'],
            'struggling': ['can\'t control', 'overwhelming', 'out of control', 'drowning'],
            'absent': ['don\'t care', 'given up', 'not even trying']
        }

        regulation_status = 'moderate'
        for status, indicators in regulation_indicators.items():
            if any(ind in message_lower for ind in indicators):
                regulation_status = status
                break

        # Identify emotional needs
        needs = []
        if detected_emotions:
            if 'sadness' in detected_emotions or 'loneliness' in detected_emotions:
                needs.extend(['validation', 'emotional_support', 'connection'])
            if 'anxiety' in detected_emotions or 'fear' in detected_emotions:
                needs.extend(['reassurance', 'safety', 'grounding'])
            if 'anger' in detected_emotions:
                needs.extend(['validation', 'healthy_expression', 'boundaries'])
            if 'hopelessness' in detected_emotions:
                needs.extend(['hope_building', 'perspective', 'meaning'])

        # Compile assessment
        assessment = {
            'detected_emotions': detected_emotions,
            'dominant_emotion': max(detected_emotions.keys(), key=lambda k: len(
                detected_emotions[k]['indicators'])) if detected_emotions else 'neutral',
            'emotional_complexity': 'high' if len(detected_emotions) >= 3 else 'moderate' if len(
                detected_emotions) == 2 else 'low',
            'overall_intensity': self._calculate_overall_intensity(detected_emotions),
            'emotional_regulation': regulation_status,
            'emotional_needs': list(set(needs)),
            'support_type_recommended': self._recommend_support_type(detected_emotions, regulation_status)
        }

        return json.dumps(assessment, indent=2)

    def _calculate_overall_intensity(self, emotions: Dict) -> str:
        """Calculate overall emotional intensity."""
        if not emotions:
            return 'low'

        high_intensity_count = sum(1 for e in emotions.values() if e['intensity'] == 'high')

        if high_intensity_count >= 2:
            return 'very_high'
        elif high_intensity_count == 1:
            return 'high'
        elif len(emotions) >= 2:
            return 'moderate'
        else:
            return 'mild'

    def _recommend_support_type(self, emotions: Dict, regulation: str) -> str:
        """Recommend type of support needed."""
        if not emotions:
            return 'general_support'

        if regulation in ['struggling', 'absent']:
            return 'crisis_intervention_or_intensive_support'

        if any(e in emotions for e in ['hopelessness', 'anxiety']):
            return 'structured_therapeutic_intervention'

        return 'supportive_counseling'
