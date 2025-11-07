from crewai_tools import BaseTool
from typing import Optional, Type, Dict, List
from pydantic import BaseModel, Field
import json


class EmotionalInput(BaseModel):
    """Input schema for Emotional Tools."""
    emotional_expression: str = Field(..., description="The user's emotional expression or statement")
    context: Optional[str] = Field(None, description="Context about the emotional situation")


class EmotionalValidationTool(BaseTool):
    name: str = "Emotional Validation Tool"
    description: str = (
        "Provides empathetic validation and normalization of emotions. Helps users feel heard, "
        "understood, and validated in their emotional experience. Use when user expresses difficult emotions."
    )
    args_schema: Type[BaseModel] = EmotionalInput

    def _run(self, emotional_expression: str, context: Optional[str] = None) -> str:
        """Provide empathetic validation for emotional expression."""

        # Identify emotions present
        emotions_identified = self._identify_emotions(emotional_expression)

        # Generate validation statements
        validation_responses = self._generate_validation(emotions_identified, emotional_expression)

        # Provide normalization
        normalization = self._normalize_emotions(emotions_identified)

        # Offer reflection
        reflection = self._offer_reflection(emotional_expression)

        result = {
            "validation_response": validation_responses['primary_validation'],
            "additional_validation": validation_responses['additional_statements'],
            "normalization": normalization,
            "reflective_statement": reflection,
            "next_steps_suggestion": self._suggest_next_steps(emotions_identified),
            "empathy_strategies": self._get_empathy_strategies()
        }

        return json.dumps(result, indent=2)

    def _identify_emotions(self, text: str) -> List[str]:
        """Identify emotions expressed in text."""
        text_lower = text.lower()
        emotions_found = []

        emotion_keywords = {
            'sadness': ['sad', 'depressed', 'down', 'miserable', 'grief', 'heartbroken'],
            'anxiety': ['anxious', 'worried', 'nervous', 'scared', 'afraid', 'panic'],
            'anger': ['angry', 'mad', 'furious', 'frustrated', 'annoyed', 'rage'],
            'loneliness': ['lonely', 'alone', 'isolated', 'abandoned', 'disconnected'],
            'hopelessness': ['hopeless', 'helpless', 'pointless', 'give up'],
            'shame': ['ashamed', 'embarrassed', 'humiliated', 'guilty'],
            'overwhelm': ['overwhelmed', 'too much', 'drowning', 'can\'t cope'],
            'confusion': ['confused', 'don\'t understand', 'lost', 'uncertain']
        }

        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                emotions_found.append(emotion)

        return emotions_found if emotions_found else ['distress']

    def _generate_validation(self, emotions: List[str], expression: str) -> Dict:
        """Generate validation statements."""
        validation_templates = {
            'sadness': "It's completely understandable to feel sad given what you're going through. Your feelings are valid and important.",
            'anxiety': "Feeling anxious in this situation makes perfect sense. It's your mind trying to protect you, and it's okay to feel this way.",
            'anger': "Your anger is valid. It's a natural response when we feel hurt, frustrated, or when our boundaries are crossed.",
            'loneliness': "Feeling lonely is one of the most difficult emotions to experience. Your need for connection is fundamental and real.",
            'hopelessness': "I hear that you're feeling hopeless right now. That's an incredibly heavy feeling, and it takes courage to express it.",
            'shame': "Shame is such a painful emotion. Thank you for trusting me with this. You deserve compassion, not judgment.",
            'overwhelm': "Feeling overwhelmed is completely natural when you're dealing with so much. It's okay to feel like it's too much right now.",
            'confusion': "It makes sense to feel confused. You're navigating a complex situation, and uncertainty is uncomfortable.",
            'distress': "I can hear how difficult this is for you. Your feelings are completely valid, and I'm here to support you."
        }

        primary_emotion = emotions[0] if emotions else 'distress'

        additional = []
        for emotion in emotions[1:3]:  # Include up to 2 additional validations
            if emotion in validation_templates:
                additional.append(validation_templates[emotion])

        return {
            'primary_validation': validation_templates.get(primary_emotion, validation_templates['distress']),
            'additional_statements': additional
        }

    def _normalize_emotions(self, emotions: List[str]) -> Dict:
        """Provide normalization for emotions."""
        normalization_statements = {
            'sadness': {
                'message': "Sadness is a natural human emotion that everyone experiences. It's not a sign of weakness.",
                'facts': [
                    "Sadness helps us process loss and difficult experiences",
                    "Research shows that allowing yourself to feel sad actually helps healing",
                    "Even the strongest people experience deep sadness"
                ]
            },
            'anxiety': {
                'message': "Anxiety is your body's natural alarm system. Millions of people experience anxiety.",
                'facts': [
                    "Anxiety disorders affect 40 million adults in the US alone",
                    "Anxiety served an evolutionary purpose to keep us safe",
                    "Even confident people experience anxiety in challenging situations"
                ]
            },
            'anger': {
                'message': "Anger is a valid emotion that often signals that something important to us is threatened.",
                'facts': [
                    "Anger can be a healthy response to injustice or boundary violations",
                    "Learning to express anger constructively is a sign of emotional maturity",
                    "Suppressing anger can lead to other problems - it needs healthy expression"
                ]
            },
            'loneliness': {
                'message': "Loneliness is one of the most common human experiences, especially in modern society.",
                'facts': [
                    "Studies show that loneliness affects people across all demographics",
                    "Loneliness is actually a survival mechanism signaling our need for connection",
                    "Many successful, socially active people still experience profound loneliness"
                ]
            },
            'default': {
                'message': "What you're feeling is a valid human response to your circumstances.",
                'facts': [
                    "All emotions serve a purpose in our psychological functioning",
                    "There are no 'bad' emotions - only emotions that are uncomfortable",
                    "Emotional experience is highly individual and valid"
                ]
            }
        }

        primary_emotion = emotions[0] if emotions else 'default'
        return normalization_statements.get(primary_emotion, normalization_statements['default'])

    def _offer_reflection(self, expression: str) -> str:
        """Offer reflective statement."""
        return (
            "What I'm hearing is that you're going through something really difficult, "
            "and it's affecting you deeply. Your willingness to share this shows strength and self-awareness."
        )

    def _suggest_next_steps(self, emotions: List[str]) -> List[str]:
        """Suggest supportive next steps."""
        return [
            "Would it help to talk more about what you're experiencing?",
            "Let's explore what might help you feel supported right now.",
            "We can work together to find ways to cope with these feelings.",
            "You don't have to go through this alone."
        ]

    def _get_empathy_strategies(self) -> List[Dict]:
        """Get empathy and support strategies."""
        return [
            {
                "strategy": "Active Listening",
                "description": "Fully focus on understanding without judgment or rushing to fix"
            },
            {
                "strategy": "Emotional Reflection",
                "description": "Mirror back the emotions you're hearing to show understanding"
            },
            {
                "strategy": "Validation",
                "description": "Acknowledge that feelings make sense given the circumstances"
            },
            {
                "strategy": "Normalize",
                "description": "Help understand that their emotional experience is understandable and common"
            },
            {
                "strategy": "Express Compassion",
                "description": "Show genuine care and concern for their wellbeing"
            }
        ]


class EmotionalProcessingGuideTool(BaseTool):
    name: str = "Emotional Processing Guide Tool"
    description: str = (
        "Guides users through healthy emotional processing using evidence-based techniques. "
        "Helps identify, understand, express, and work through difficult emotions. "
        "Use when user needs help processing complex or overwhelming emotions."
    )
    args_schema: Type[BaseModel] = EmotionalInput

    def _run(self, emotional_expression: str, context: Optional[str] = None) -> str:
        """Guide emotional processing."""

        result = {
            "processing_framework": self._get_processing_framework(),
            "emotion_identification": self._guide_emotion_identification(),
            "healthy_expression": self._get_healthy_expression_methods(),
            "emotional_regulation": self._get_regulation_strategies(),
            "integration_steps": self._get_integration_steps(),
            "when_to_seek_additional_support": self._when_to_seek_support()
        }

        return json.dumps(result, indent=2)

    def _get_processing_framework(self) -> Dict:
        """Get emotional processing framework."""
        return {
            "step_1_acknowledge": {
                "title": "Acknowledge the Emotion",
                "description": "Recognize and name what you're feeling without judgment",
                "prompt": "I notice I'm feeling ___. This emotion is present right now."
            },
            "step_2_accept": {
                "title": "Accept the Emotion",
                "description": "Allow the emotion to be present without trying to push it away",
                "prompt": "It's okay to feel this way. I can let this emotion exist without fighting it."
            },
            "step_3_investigate": {
                "title": "Investigate with Curiosity",
                "description": "Explore the emotion with gentle curiosity",
                "questions": [
                    "What triggered this emotion?",
                    "What is this emotion trying to tell me?",
                    "Where do I feel this in my body?",
                    "What thoughts accompany this emotion?"
                ]
            },
            "step_4_express": {
                "title": "Express the Emotion",
                "description": "Find healthy ways to express what you're feeling",
                "methods": ["Talk to someone", "Journal", "Creative expression", "Physical movement"]
            },
            "step_5_respond": {
                "title": "Respond with Care",
                "description": "Choose how to respond to your emotional needs",
                "prompt": "What do I need right now? How can I care for myself?"
            }
        }

    def _guide_emotion_identification(self) -> Dict:
        """Guide for identifying emotions accurately."""
        return {
            "emotion_wheel": {
                "description": "Use an emotion wheel to identify specific emotions",
                "basic_emotions": ["Sad", "Mad", "Glad", "Scared", "Ashamed", "Surprised"],
                "refinement": "Start with basic emotion, then identify more specific variants"
            },
            "body_cues": {
                "description": "Physical sensations can help identify emotions",
                "examples": {
                    "anxiety": "Tight chest, racing heart, shallow breathing",
                    "sadness": "Heaviness, low energy, tears",
                    "anger": "Heat, tension, clenched jaw",
                    "fear": "Cold, trembling, stomach upset"
                }
            },
            "intensity_scale": {
                "description": "Rate emotion intensity 0-10",
                "benefit": "Helps track changes and communicate needs"
            }
        }

    def _get_healthy_expression_methods(self) -> List[Dict]:
        """Get healthy emotional expression methods."""
        return [
            {
                "method": "Verbal Expression",
                "techniques": [
                    "Talk to trusted friend or therapist",
                    "Use 'I feel' statements: 'I feel ___ when ___ because ___'",
                    "Name emotions out loud to yourself",
                    "Record voice memos expressing feelings"
                ]
            },
            {
                "method": "Written Expression",
                "techniques": [
                    "Free-writing journal without editing",
                    "Letter writing (send or don't send)",
                    "Emotion tracking log",
                    "Poetry or creative writing"
                ]
            },
            {
                "method": "Creative Expression",
                "techniques": [
                    "Art (painting, drawing, collage)",
                    "Music (playing, listening, creating)",
                    "Dance or movement",
                    "Crafts or building"
                ]
            },
            {
                "method": "Physical Expression",
                "techniques": [
                    "Exercise or sports",
                    "Yoga or tai chi",
                    "Walking in nature",
                    "Physical labor or cleaning"
                ]
            },
            {
                "method": "Symbolic Expression",
                "techniques": [
                    "Rituals (burning old letters, planting seeds)",
                    "Creating memory boxes",
                    "Releasing balloons or lanterns",
                    "Building something meaningful"
                ]
            }
        ]

    def _get_regulation_strategies(self) -> Dict:
        """Get emotion regulation strategies."""
        return {
            "in_the_moment_strategies": [
                {
                    "name": "STOP Technique",
                    "description": "Stop, Take a breath, Observe, Proceed mindfully"
                },
                {
                    "name": "Temperature Change",
                    "description": "Splash cold water, hold ice cube, take cool shower"
                },
                {
                    "name": "Intense Exercise",
                    "description": "Quick burst of physical activity to release tension"
                },
                {
                    "name": "Grounding Techniques",
                    "description": "5-4-3-2-1 sensory awareness"
                }
            ],
            "longer_term_strategies": [
                {
                    "name": "Emotion Labeling",
                    "description": "Regular practice of naming emotions reduces their intensity"
                },
                {
                    "name": "Mindfulness Meditation",
                    "description": "Develops capacity to observe emotions without being overwhelmed"
                },
                {
                    "name": "Values Clarification",
                    "description": "Connect actions to personal values even when emotions are difficult"
                },
                {
                    "name": "Self-Compassion Practice",
                    "description": "Treat yourself with kindness during emotional difficulty"
                }
            ],
            "opposite_action": {
                "description": "When emotion doesn't fit the facts, act opposite to the emotional urge",
                "examples": {
                    "unjustified_anger": "Act gently and kindly",
                    "unwarranted_fear": "Approach rather than avoid",
                    "inappropriate_shame": "Make eye contact, stand tall"
                }
            }
        }

    def _get_integration_steps(self) -> List[Dict]:
        """Get steps for integrating emotional experiences."""
        return [
            {
                "step": "Reflection",
                "description": "Look back on the emotional experience with perspective",
                "prompts": [
                    "What did I learn from this emotion?",
                    "How did I cope, and what worked?",
                    "What would I do differently next time?"
                ]
            },
            {
                "step": "Meaning-Making",
                "description": "Find personal significance or growth from the experience",
                "prompts": [
                    "How has this experience changed me?",
                    "What strengths did I discover?",
                    "What's important to me now?"
                ]
            },
            {
                "step": "Forward Planning",
                "description": "Prepare for future emotional challenges",
                "actions": [
                    "Create coping plan for similar situations",
                    "Identify early warning signs",
                    "Build support systems",
                    "Practice preventive self-care"
                ]
            }
        ]

    def _when_to_seek_support(self) -> Dict:
        """When to seek additional support."""
        return {
            "seek_immediate_help_if": [
                "Thoughts of self-harm or suicide",
                "Unable to function in daily life",
                "Emotions feel completely out of control",
                "Risk of harming self or others"
            ],
            "seek_professional_support_if": [
                "Emotions persist for weeks without improvement",
                "Interfering significantly with work, relationships, or health",
                "Using unhealthy coping mechanisms (substance abuse, etc.)",
                "Previous trauma is being triggered",
                "Feeling stuck and unable to process alone"
            ],
            "types_of_support": {
                "crisis_support": "Crisis hotline, emergency services",
                "professional_therapy": "Therapist, counselor, psychologist",
                "medical_support": "Psychiatrist for medication evaluation",
                "peer_support": "Support groups, peer counseling",
                "informal_support": "Trusted friends, family, mentors"
            }
        }


class SelfCompassionTool(BaseTool):
    name: str = "Self-Compassion Tool"
    description: str = (
        "Guides users in developing self-compassion using evidence-based practices. "
        "Helps replace self-criticism with self-kindness. Use when user is being "
        "self-critical or experiencing shame."
    )
    args_schema: Type[BaseModel] = EmotionalInput

    def _run(self, emotional_expression: str, context: Optional[str] = None) -> str:
        """Guide self-compassion practice."""

        result = {
            "self_compassion_components": self._get_sc_components(),
            "self_compassion_break": self._get_sc_break(),
            "self_kindness_practices": self._get_kindness_practices(),
            "common_humanity_reminders": self._get_common_humanity(),
            "mindful_self_compassion_exercises": self._get_msc_exercises(),
            "overcoming_obstacles": self._get_obstacles_guide()
        }

        return json.dumps(result, indent=2)

    def _get_sc_components(self) -> Dict:
        """Get three components of self-compassion."""
        return {
            "1_self_kindness": {
                "description": "Being warm and understanding toward ourselves when we suffer or feel inadequate",
                "instead_of": "Self-judgment and harsh self-criticism",
                "practice": "Speak to yourself as you would to a good friend"
            },
            "2_common_humanity": {
                "description": "Recognizing that suffering and imperfection are part of the shared human experience",
                "instead_of": "Isolation and feeling alone in your struggles",
                "practice": "Remember that everyone struggles; you're not alone"
            },
            "3_mindfulness": {
                "description": "Holding painful thoughts and feelings in balanced awareness",
                "instead_of": "Over-identification with painful thoughts and emotions",
                "practice": "Observe your experience without suppressing or exaggerating"
            }
        }

    def _get_sc_break(self) -> Dict:
        """Get self-compassion break practice."""
        return {
            "name": "Self-Compassion Break",
            "duration": "3-5 minutes",
            "when_to_use": "When experiencing difficult emotions or self-criticism",
            "steps": [
                {
                    "step": 1,
                    "component": "Mindfulness",
                    "phrase": "This is a moment of suffering / This is really hard right now",
                    "action": "Acknowledge your pain"
                },
                {
                    "step": 2,
                    "component": "Common Humanity",
                    "phrase": "Suffering is part of life / I'm not alone in this / Everyone struggles",
                    "action": "Remember you're not alone"
                },
                {
                    "step": 3,
                    "component": "Self-Kindness",
                    "phrase": "May I be kind to myself / May I give myself the compassion I need",
                    "action": "Offer yourself kindness"
                }
            ],
            "optional_addition": "Place hands over heart or give yourself a gentle hug"
        }

    def _get_kindness_practices(self) -> List[Dict]:
        """Get self-kindness practices."""
        return [
            {
                "practice": "Supportive Touch",
                "description": "Hand on heart, self-hug, gentle hand on cheek",
                "benefit": "Activates caregiving system, releases oxytocin"
            },
            {
                "practice": "Self-Compassionate Letter",
                "description": "Write to yourself from perspective of compassionate friend",
                "benefit": "Gains perspective, reduces self-criticism"
            },
            {
                "practice": "Self-Compassion Phrases",
                "description": "Repeat: 'May I be safe, May I be peaceful, May I be kind to myself, May I accept myself as I am'",
                "benefit": "Creates new neural pathways of self-kindness"
            },
            {
                "practice": "Change the Tone",
                "description": "Notice self-critical voice; respond with kinder tone",
                "benefit": "Interrupts automatic self-criticism"
            }
        ]

    def _get_common_humanity(self) -> List[str]:
        """Get common humanity reminders."""
        return [
            "Everyone makes mistakes - it's part of being human",
            "Millions of people are struggling with similar challenges right now",
            "Imperfection and difficulty are universal human experiences",
            "Your struggles don't make you defective - they make you human",
            "Other people also have these thoughts and feelings, even if they don't show it",
            "Suffering and hardship are inevitable parts of life for everyone",
            "You don't have to be perfect to be worthy of love and compassion"
        ]

    def _get_msc_exercises(self) -> List[Dict]:
        """Get mindful self-compassion exercises."""
        return [
            {
                "exercise": "Loving-Kindness Meditation for Self",
                "duration": "10-15 minutes",
                "instructions": [
                    "Sit comfortably and close eyes",
                    "Visualize yourself as deserving of love",
                    "Repeat phrases: 'May I be happy, May I be healthy, May I be safe, May I live with ease'",
                    "Feel the warmth of these wishes for yourself"
                ]
            },
            {
                "exercise": "Self-Compassion Journal",
                "frequency": "Daily for 2 weeks",
                "prompts": [
                    "What was difficult for me today?",
                    "How did I feel?",
                    "How can I be kind to myself about this?",
                    "What would I say to a friend in this situation?"
                ]
            },
            {
                "exercise": "Finding Your Compassionate Voice",
                "description": "Develop an inner compassionate voice to counter the critic",
                "method": [
                    "Notice the critical voice",
                    "Ask: What does the compassionate voice say?",
                    "Practice responding with understanding and kindness",
                    "Over time, compassionate voice becomes stronger"
                ]
            }
        ]

    def _get_obstacles_guide(self) -> Dict:
        """Get guide for overcoming obstacles to self-compassion."""
        return {
            "obstacle_1_fear_of_selfindulgence": {
                "belief": "Self-compassion will make me lazy or self-indulgent",
                "reality": "Research shows self-compassion increases motivation and personal growth",
                "response": "Self-compassion provides support to help you grow, not excuse to avoid effort"
            },
            "obstacle_2_unworthiness": {
                "belief": "I don't deserve compassion",
                "reality": "All humans deserve compassion simply by being human",
                "response": "Worthiness isn't earned - it's inherent"
            },
            "obstacle_3_feeling_too_hard": {
                "belief": "Self-compassion feels fake or uncomfortable",
                "reality": "New skills feel awkward at first; becomes natural with practice",
                "response": "Start small; even tiny amounts of self-kindness matter"
            },
            "obstacle_4_resistance_to_feeling": {
                "belief": "If I'm kind to myself, I'll fall apart",
                "reality": "Self-compassion actually helps regulate difficult emotions",
                "response": "You can offer yourself kindness while still staying functional"
            }
        }
