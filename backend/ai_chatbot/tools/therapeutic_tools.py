from crewai_tools import BaseTool
from typing import Optional, Type, Dict, List
from pydantic import BaseModel, Field
import json


class TherapeuticInput(BaseModel):
    """Input schema for Therapeutic Tools."""
    situation: str = Field(..., description="The situation or thought pattern to address")
    emotion: Optional[str] = Field(None, description="The dominant emotion being experienced")
    intensity: Optional[str] = Field(None, description="Intensity level: low, moderate, high")


class CBTCognitiveRestructuringTool(BaseTool):
    name: str = "CBT Cognitive Restructuring Tool"
    description: str = (
        "Helps identify cognitive distortions and reframe negative thought patterns using CBT techniques. "
        "Input a negative thought or belief, and receive structured cognitive restructuring guidance. "
        "Use when user expresses distorted thinking patterns."
    )
    args_schema: Type[BaseModel] = TherapeuticInput

    def _run(self, situation: str, emotion: Optional[str] = None, intensity: Optional[str] = None) -> str:
        """Apply CBT cognitive restructuring to a thought or situation."""

        # Identify cognitive distortions
        distortions = self._identify_distortions(situation)

        # Generate Socratic questions
        questions = self._generate_socratic_questions(situation, distortions)

        # Provide alternative perspectives
        alternatives = self._generate_alternative_thoughts(situation, distortions)

        # Create balanced thought
        balanced_thought = self._create_balanced_thought(situation, distortions)

        result = {
            "original_thought": situation,
            "identified_distortions": distortions,
            "socratic_questions": questions,
            "alternative_perspectives": alternatives,
            "balanced_thought": balanced_thought,
            "action_steps": self._generate_action_steps(distortions),
            "evidence_for_and_against": self._evidence_analysis(situation)
        }

        return json.dumps(result, indent=2)

    def _identify_distortions(self, text: str) -> List[Dict]:
        """Identify cognitive distortions in the text."""
        text_lower = text.lower()
        distortions_found = []

        distortion_patterns = {
            "all_or_nothing_thinking": {
                "keywords": ["always", "never", "everyone", "no one", "everything", "nothing"],
                "description": "Viewing situations in black-and-white categories"
            },
            "overgeneralization": {
                "keywords": ["always happens", "never works", "every time", "constantly"],
                "description": "Drawing broad conclusions from single events"
            },
            "mental_filter": {
                "keywords": ["only", "just", "nothing but"],
                "description": "Focusing exclusively on negative details"
            },
            "discounting_positives": {
                "keywords": ["doesn't count", "doesn't matter", "luck", "fluke"],
                "description": "Rejecting positive experiences"
            },
            "jumping_to_conclusions": {
                "keywords": ["probably", "must be", "they think", "will happen"],
                "description": "Making negative interpretations without evidence"
            },
            "catastrophizing": {
                "keywords": ["terrible", "disaster", "awful", "worst", "horrible"],
                "description": "Expecting the worst possible outcome"
            },
            "emotional_reasoning": {
                "keywords": ["i feel", "makes me feel like"],
                "description": "Assuming feelings reflect reality"
            },
            "should_statements": {
                "keywords": ["should", "must", "ought to", "have to"],
                "description": "Using rigid rules for self or others"
            },
            "labeling": {
                "keywords": ["i am a", "they are", "loser", "failure", "idiot"],
                "description": "Attaching negative labels to self or others"
            },
            "personalization": {
                "keywords": ["my fault", "because of me", "i caused"],
                "description": "Taking responsibility for things outside your control"
            }
        }

        for distortion_name, data in distortion_patterns.items():
            matches = [kw for kw in data['keywords'] if kw in text_lower]
            if matches:
                distortions_found.append({
                    "type": distortion_name,
                    "description": data['description'],
                    "indicators": matches
                })

        return distortions_found

    def _generate_socratic_questions(self, situation: str, distortions: List[Dict]) -> List[str]:
        """Generate Socratic questions to challenge the thought."""
        questions = [
            "What evidence supports this thought?",
            "What evidence contradicts this thought?",
            "Is there an alternative way to view this situation?",
            "What would you tell a friend who had this thought?",
            "How might you view this situation in 5 years?",
        ]

        # Add distortion-specific questions
        for distortion in distortions:
            if distortion['type'] == 'all_or_nothing_thinking':
                questions.append("Are there any shades of gray in this situation?")
            elif distortion['type'] == 'catastrophizing':
                questions.append("What's the most realistic outcome?")
            elif distortion['type'] == 'overgeneralization':
                questions.append("Can you think of times when this wasn't the case?")
            elif distortion['type'] == 'personalization':
                questions.append("What other factors might have contributed to this situation?")

        return questions[:7]  # Return top 7 most relevant

    def _generate_alternative_thoughts(self, situation: str, distortions: List[Dict]) -> List[str]:
        """Generate alternative, more balanced thoughts."""
        alternatives = []

        if any(d['type'] == 'all_or_nothing_thinking' for d in distortions):
            alternatives.append(
                "Perhaps this situation isn't entirely one way or the other. "
                "There might be middle ground or partial success here."
            )

        if any(d['type'] == 'catastrophizing' for d in distortions):
            alternatives.append(
                "While this is challenging, the most likely outcome is probably less extreme. "
                "I've handled difficult situations before."
            )

        if any(d['type'] == 'overgeneralization' for d in distortions):
            alternatives.append(
                "This happened in this specific instance, but that doesn't mean it always happens. "
                "Each situation is unique."
            )

        if any(d['type'] == 'personalization' for d in distortions):
            alternatives.append(
                "Many factors contribute to any situation. This isn't entirely within my control "
                "or responsibility."
            )

        # Generic alternative
        alternatives.append(
            "I'm having this thought, but thoughts aren't facts. I can observe this thought "
            "without accepting it as absolute truth."
        )

        return alternatives

    def _create_balanced_thought(self, situation: str, distortions: List[Dict]) -> str:
        """Create a balanced alternative thought."""
        if not distortions:
            return "This is a challenging situation, and I can handle it one step at a time."

        primary_distortion = distortions[0]['type']

        balanced_thoughts = {
            "all_or_nothing_thinking": (
                "Rather than seeing this as all good or all bad, I can acknowledge both "
                "the challenges and the positive aspects of this situation."
            ),
            "catastrophizing": (
                "While I'm worried about negative outcomes, I can focus on realistic possibilities "
                "and trust my ability to cope with whatever happens."
            ),
            "overgeneralization": (
                "This is one experience, not a pattern. I can learn from this without assuming "
                "it defines all future situations."
            ),
            "personalization": (
                "I'm one part of a complex situation with many contributing factors. I can take "
                "appropriate responsibility without blaming myself for everything."
            )
        }

        return balanced_thoughts.get(primary_distortion,
                                     "I can approach this situation with flexibility, acknowledging my feelings while "
                                     "considering alternative perspectives."
                                     )

    def _generate_action_steps(self, distortions: List[Dict]) -> List[str]:
        """Generate actionable steps based on identified distortions."""
        return [
            "Write down the evidence for and against this thought",
            "Practice catching this thought pattern when it arises",
            "Use the balanced thought as an alternative response",
            "Notice how your emotions change when you challenge the thought",
            "Track situations where this thought pattern occurs"
        ]

    def _evidence_analysis(self, situation: str) -> Dict:
        """Provide framework for evidence analysis."""
        return {
            "evidence_for": "List specific, objective facts that support this thought",
            "evidence_against": "List specific, objective facts that contradict this thought",
            "alternative_explanations": "What other ways could you interpret this situation?"
        }


class MindfulnessExerciseTool(BaseTool):
    name: str = "Mindfulness Exercise Tool"
    description: str = (
        "Provides guided mindfulness and grounding exercises for stress reduction, emotional regulation, "
        "and present-moment awareness. Specify emotion and intensity for personalized exercises. "
        "Use when user needs immediate calming or grounding techniques."
    )
    args_schema: Type[BaseModel] = TherapeuticInput

    def _run(self, situation: str, emotion: Optional[str] = None, intensity: Optional[str] = None) -> str:
        """Provide personalized mindfulness exercises."""

        # Select appropriate exercises based on emotion and intensity
        exercises = self._select_exercises(emotion, intensity)

        result = {
            "recommended_exercises": exercises,
            "quick_grounding_technique": self._get_quick_grounding(),
            "breathing_exercises": self._get_breathing_exercises(),
            "body_awareness_practices": self._get_body_awareness(),
            "mindful_observation": self._get_mindful_observation(),
            "practice_tips": self._get_practice_tips()
        }

        return json.dumps(result, indent=2)

    def _select_exercises(self, emotion: Optional[str], intensity: Optional[str]) -> List[Dict]:
        """Select exercises based on emotional state."""
        exercises = []

        if intensity in ['high', 'very_high'] or emotion in ['anxiety', 'panic', 'fear']:
            exercises.append({
                "name": "5-4-3-2-1 Grounding Technique",
                "duration": "3-5 minutes",
                "instructions": [
                    "Name 5 things you can see around you",
                    "Name 4 things you can physically touch",
                    "Name 3 things you can hear",
                    "Name 2 things you can smell",
                    "Name 1 thing you can taste"
                ],
                "purpose": "Brings attention back to present moment, reduces anxiety"
            })

        if emotion in ['sadness', 'depression', 'hopelessness']:
            exercises.append({
                "name": "Self-Compassion Meditation",
                "duration": "10 minutes",
                "instructions": [
                    "Place hand on heart and feel your chest rising and falling",
                    "Acknowledge your suffering: 'This is a moment of difficulty'",
                    "Remember shared humanity: 'Suffering is part of life; I'm not alone'",
                    "Offer yourself kindness: 'May I be kind to myself in this moment'",
                    "Continue with gentle, compassionate breathing"
                ],
                "purpose": "Cultivates self-compassion and emotional warmth"
            })

        # Universal exercises
        exercises.append({
            "name": "Mindful Breathing",
            "duration": "5-10 minutes",
            "instructions": [
                "Find a comfortable position, close eyes if comfortable",
                "Notice the natural rhythm of your breath",
                "Count 1 on inhale, 2 on exhale, up to 10, then restart",
                "When mind wanders, gently return attention to breath",
                "End with three deep, intentional breaths"
            ],
            "purpose": "Calms nervous system, improves focus"
        })

        exercises.append({
            "name": "Body Scan Meditation",
            "duration": "10-15 minutes",
            "instructions": [
                "Lie down or sit comfortably",
                "Bring awareness to your feet, notice sensations",
                "Slowly move attention up through each body part",
                "Notice tension without trying to change it",
                "End at the crown of your head, taking three deep breaths"
            ],
            "purpose": "Releases physical tension, develops body awareness"
        })

        return exercises[:3]  # Return top 3 most relevant

    def _get_quick_grounding(self) -> Dict:
        """Get quick grounding technique."""
        return {
            "name": "STOP Technique",
            "duration": "1 minute",
            "steps": [
                "S - Stop what you're doing",
                "T - Take a deep breath",
                "O - Observe your thoughts, feelings, and sensations",
                "P - Proceed with awareness and intention"
            ],
            "use_when": "Feeling overwhelmed or emotionally reactive"
        }

    def _get_breathing_exercises(self) -> List[Dict]:
        """Get breathing exercises."""
        return [
            {
                "name": "Box Breathing",
                "pattern": "Inhale 4, Hold 4, Exhale 4, Hold 4",
                "duration": "2-5 minutes",
                "benefits": "Reduces anxiety, improves focus"
            },
            {
                "name": "4-7-8 Breathing",
                "pattern": "Inhale 4, Hold 7, Exhale 8",
                "duration": "4 cycles minimum",
                "benefits": "Promotes relaxation, helps with sleep"
            },
            {
                "name": "Diaphragmatic Breathing",
                "pattern": "Deep belly breaths, hand on stomach rises",
                "duration": "5-10 minutes",
                "benefits": "Activates parasympathetic nervous system"
            }
        ]

    def _get_body_awareness(self) -> Dict:
        """Get body awareness practice."""
        return {
            "name": "Progressive Muscle Relaxation",
            "steps": [
                "Start with feet: tense for 5 seconds, then release",
                "Move up through calves, thighs, abdomen",
                "Continue through chest, arms, hands",
                "Finish with face and jaw muscles",
                "Notice the difference between tension and relaxation"
            ],
            "duration": "10-15 minutes",
            "benefits": "Releases physical tension, promotes relaxation"
        }

    def _get_mindful_observation(self) -> Dict:
        """Get mindful observation exercise."""
        return {
            "name": "Single Object Meditation",
            "instructions": [
                "Choose an object (leaf, stone, any item)",
                "Observe it as if seeing for the first time",
                "Notice colors, textures, shapes, weight",
                "When mind wanders, gently return focus to object",
                "Practice for 5-10 minutes"
            ],
            "purpose": "Develops concentration and present-moment awareness"
        }

    def _get_practice_tips(self) -> List[str]:
        """Get mindfulness practice tips."""
        return [
            "Start with just 2-3 minutes daily and gradually increase",
            "Practice at the same time each day to build habit",
            "Be patient with yourself - mind wandering is normal",
            "Return attention gently without self-criticism",
            "Use apps or guided recordings if helpful",
            "Practice informally - mindful eating, walking, etc.",
            "Join a meditation group for support and motivation"
        ]


class BehavioralActivationTool(BaseTool):
    name: str = "Behavioral Activation Tool"
    description: str = (
        "Creates behavioral activation plans to increase engagement in meaningful activities "
        "and break cycles of avoidance and depression. Use when user shows low motivation "
        "or behavioral inertia."
    )
    args_schema: Type[BaseModel] = TherapeuticInput

    def _run(self, situation: str, emotion: Optional[str] = None, intensity: Optional[str] = None) -> str:
        """Generate behavioral activation plan."""

        result = {
            "activity_categories": self._get_activity_categories(),
            "activity_hierarchy": self._create_activity_hierarchy(),
            "scheduling_strategy": self._get_scheduling_strategy(),
            "motivation_techniques": self._get_motivation_techniques(),
            "tracking_methods": self._get_tracking_methods(),
            "troubleshooting": self._get_troubleshooting_tips()
        }

        return json.dumps(result, indent=2)

    def _get_activity_categories(self) -> Dict:
        """Get different categories of activities."""
        return {
            "pleasure_activities": {
                "description": "Activities that bring joy or satisfaction",
                "examples": [
                    "Listen to favorite music",
                    "Watch a comedy show",
                    "Take a warm bath",
                    "Spend time in nature",
                    "Engage in a hobby"
                ]
            },
            "mastery_activities": {
                "description": "Activities that provide sense of accomplishment",
                "examples": [
                    "Complete a small task",
                    "Learn something new",
                    "Organize a small space",
                    "Cook a meal",
                    "Exercise for 10 minutes"
                ]
            },
            "social_activities": {
                "description": "Activities involving connection with others",
                "examples": [
                    "Call a friend",
                    "Text someone supportive",
                    "Join an online community",
                    "Attend a support group",
                    "Have coffee with someone"
                ]
            },
            "self_care_activities": {
                "description": "Activities for physical and emotional wellbeing",
                "examples": [
                    "Take a shower",
                    "Get adequate sleep",
                    "Eat a nutritious meal",
                    "Practice hygiene routine",
                    "Gentle stretching"
                ]
            }
        }

    def _create_activity_hierarchy(self) -> Dict:
        """Create hierarchy from easy to challenging activities."""
        return {
            "level_1_minimal_effort": [
                "Get out of bed",
                "Open curtains",
                "Drink a glass of water",
                "Listen to one song",
                "Sit outside for 2 minutes"
            ],
            "level_2_low_effort": [
                "Take a 5-minute walk",
                "Make your bed",
                "Text a friend",
                "Eat a meal at the table",
                "Watch a short video"
            ],
            "level_3_moderate_effort": [
                "Go for a 15-minute walk",
                "Cook a simple meal",
                "Call someone",
                "Engage in hobby for 20 minutes",
                "Complete a household task"
            ],
            "level_4_higher_effort": [
                "Exercise for 30 minutes",
                "Meet friend in person",
                "Work on a project",
                "Attend social event",
                "Try something new"
            ],
            "progression_principle": "Start at level where you can succeed 80% of the time"
        }

    def _get_scheduling_strategy(self) -> Dict:
        """Get activity scheduling strategy."""
        return {
            "time_blocking": "Schedule specific activities at specific times",
            "start_small": "Begin with 1-2 activities per day",
            "morning_activation": "Plan one activity within 1 hour of waking",
            "balanced_day": "Mix pleasure, mastery, and self-care activities",
            "flexibility": "Have backup activities for low-energy days",
            "consistency": "Same time/place helps build habits",
            "gradual_increase": "Add one new activity per week"
        }

    def _get_motivation_techniques(self) -> List[Dict]:
        """Get motivation-building techniques."""
        return [
            {
                "technique": "The 5-Minute Rule",
                "description": "Commit to just 5 minutes; often you'll continue longer"
            },
            {
                "technique": "Activity Before Motivation",
                "description": "Action creates motivation, not the other way around"
            },
            {
                "technique": "Values Connection",
                "description": "Link activities to personal values and what matters"
            },
            {
                "technique": "Social Accountability",
                "description": "Share plans with supportive person for accountability"
            },
            {
                "technique": "Reward System",
                "description": "Acknowledge completion with positive self-talk or small reward"
            },
            {
                "technique": "Environmental Cues",
                "description": "Set up environment to make activity easier (lay out exercise clothes)"
            }
        ]

    def _get_tracking_methods(self) -> Dict:
        """Get activity tracking methods."""
        return {
            "activity_log": {
                "what_to_track": "Activity, time, mood before/after (0-10), sense of accomplishment (0-10)",
                "purpose": "Identify which activities most improve mood"
            },
            "mood_monitoring": {
                "frequency": "Rate mood 3x daily (morning, afternoon, evening)",
                "purpose": "See relationship between activities and mood"
            },
            "success_tracking": {
                "method": "Check off completed activities",
                "purpose": "Visual proof of progress, builds momentum"
            }
        }

    def _get_troubleshooting_tips(self) -> List[Dict]:
        """Get troubleshooting tips."""
        return [
            {
                "problem": "Too hard to start",
                "solution": "Break into smaller steps; do just first step"
            },
            {
                "problem": "No motivation",
                "solution": "Start anyway; motivation follows action"
            },
            {
                "problem": "Forgot to do activity",
                "solution": "Set reminders/alarms; link to existing habits"
            },
            {
                "problem": "Didn't enjoy activity",
                "solution": "Try different activities; takes time to find what works"
            },
            {
                "problem": "Feel guilty for resting",
                "solution": "Rest is necessary; schedule it like other activities"
            }
        ]
