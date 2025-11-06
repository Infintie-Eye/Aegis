import json
import random
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio


class WellnessRecommender:
    def __init__(self):
        self.mindfulness_activities = {
            'beginner': [
                {
                    'name': 'Deep Breathing Exercise',
                    'duration': '5 minutes',
                    'instructions': 'Breathe in for 4 counts, hold for 4, exhale for 6. Repeat 10 times.',
                    'stress_relief': 0.7,
                    'anxiety_relief': 0.8
                },
                {
                    'name': 'Body Scan Meditation',
                    'duration': '10 minutes',
                    'instructions': 'Focus on each part of your body from toes to head, releasing tension.',
                    'stress_relief': 0.8,
                    'anxiety_relief': 0.7
                }
            ],
            'intermediate': [
                {
                    'name': 'Mindful Walking',
                    'duration': '15 minutes',
                    'instructions': 'Walk slowly, focusing on each step and your surroundings.',
                    'stress_relief': 0.8,
                    'mood_boost': 0.6
                },
                {
                    'name': 'Loving-Kindness Meditation',
                    'duration': '20 minutes',
                    'instructions': 'Send loving thoughts to yourself, loved ones, then all beings.',
                    'emotional_regulation': 0.9,
                    'self_compassion': 0.8
                }
            ],
            'advanced': [
                {
                    'name': 'Vipassana Meditation',
                    'duration': '30 minutes',
                    'instructions': 'Observe thoughts and sensations without judgment.',
                    'mindfulness': 0.9,
                    'emotional_stability': 0.8
                }
            ]
        }

        self.physical_activities = {
            'low_energy': [
                {
                    'name': 'Gentle Yoga Flow',
                    'duration': '15 minutes',
                    'type': 'yoga',
                    'benefits': ['flexibility', 'stress_relief', 'mindfulness'],
                    'energy_boost': 0.5,
                    'mood_improvement': 0.7
                },
                {
                    'name': 'Tai Chi Basics',
                    'duration': '20 minutes',
                    'type': 'movement',
                    'benefits': ['balance', 'calm', 'focus'],
                    'energy_boost': 0.4,
                    'stress_relief': 0.8
                }
            ],
            'moderate_energy': [
                {
                    'name': 'Hatha Yoga Session',
                    'duration': '30 minutes',
                    'type': 'yoga',
                    'benefits': ['strength', 'flexibility', 'mental_clarity'],
                    'energy_boost': 0.7,
                    'confidence': 0.6
                },
                {
                    'name': 'Nature Walk',
                    'duration': '25 minutes',
                    'type': 'outdoor',
                    'benefits': ['vitamin_d', 'fresh_air', 'mood_boost'],
                    'depression_relief': 0.8,
                    'anxiety_relief': 0.6
                }
            ],
            'high_energy': [
                {
                    'name': 'Power Yoga Flow',
                    'duration': '45 minutes',
                    'type': 'yoga',
                    'benefits': ['strength', 'endurance', 'confidence'],
                    'energy_boost': 0.9,
                    'self_esteem': 0.8
                },
                {
                    'name': 'Dance Therapy',
                    'duration': '30 minutes',
                    'type': 'movement',
                    'benefits': ['joy', 'expression', 'cardio'],
                    'mood_improvement': 0.9,
                    'self_expression': 0.8
                }
            ]
        }

        self.spiritual_activities = {
            'meditation': [
                {
                    'name': 'Centering Prayer',
                    'duration': '20 minutes',
                    'tradition': 'Christian',
                    'benefits': ['inner_peace', 'spiritual_connection']
                },
                {
                    'name': 'Buddhist Meditation',
                    'duration': '30 minutes',
                    'tradition': 'Buddhist',
                    'benefits': ['mindfulness', 'compassion', 'wisdom']
                }
            ],
            'prayer': [
                {
                    'name': 'Gratitude Prayer',
                    'duration': '10 minutes',
                    'tradition': 'Universal',
                    'benefits': ['gratitude', 'hope', 'perspective']
                },
                {
                    'name': 'Contemplative Reading',
                    'duration': '15 minutes',
                    'tradition': 'Various',
                    'benefits': ['wisdom', 'comfort', 'guidance']
                }
            ],
            'worship': [
                {
                    'name': 'Virtual Service Participation',
                    'duration': '60 minutes',
                    'tradition': 'Various',
                    'benefits': ['community', 'worship', 'inspiration']
                },
                {
                    'name': 'Sacred Music Listening',
                    'duration': '30 minutes',
                    'tradition': 'Various',
                    'benefits': ['peace', 'upliftment', 'transcendence']
                }
            ]
        }

        self.nutrition_recommendations = {
            'mood_boosting': [
                {
                    'meal': 'Omega-3 Rich Breakfast',
                    'ingredients': ['salmon', 'avocado', 'walnuts', 'spinach'],
                    'benefits': ['brain_health', 'mood_stability'],
                    'preparation_time': '15 minutes'
                },
                {
                    'meal': 'Antioxidant Berry Bowl',
                    'ingredients': ['blueberries', 'strawberries', 'yogurt', 'honey'],
                    'benefits': ['energy', 'cognitive_function'],
                    'preparation_time': '5 minutes'
                }
            ],
            'stress_reducing': [
                {
                    'meal': 'Herbal Tea Blend',
                    'ingredients': ['chamomile', 'lavender', 'lemon_balm'],
                    'benefits': ['relaxation', 'better_sleep'],
                    'preparation_time': '5 minutes'
                },
                {
                    'meal': 'Magnesium-Rich Dinner',
                    'ingredients': ['dark_chocolate', 'almonds', 'spinach', 'quinoa'],
                    'benefits': ['muscle_relaxation', 'anxiety_reduction'],
                    'preparation_time': '30 minutes'
                }
            ]
        }

        self.travel_therapy_suggestions = {
            'local': [
                {
                    'destination': 'Local Nature Park',
                    'type': 'nature_therapy',
                    'duration': '4 hours',
                    'benefits': ['fresh_air', 'exercise', 'perspective'],
                    'budget': 'low'
                },
                {
                    'destination': 'Botanical Garden',
                    'type': 'mindful_exploration',
                    'duration': '3 hours',
                    'benefits': ['beauty', 'calm', 'inspiration'],
                    'budget': 'low'
                }
            ],
            'regional': [
                {
                    'destination': 'Mountain Retreat',
                    'type': 'wilderness_therapy',
                    'duration': '2 days',
                    'benefits': ['solitude', 'reflection', 'adventure'],
                    'budget': 'moderate'
                },
                {
                    'destination': 'Beach Getaway',
                    'type': 'water_therapy',
                    'duration': '3 days',
                    'benefits': ['relaxation', 'vitamin_d', 'sound_therapy'],
                    'budget': 'moderate'
                }
            ],
            'distant': [
                {
                    'destination': 'Meditation Retreat',
                    'type': 'spiritual_journey',
                    'duration': '7 days',
                    'benefits': ['deep_healing', 'spiritual_growth', 'community'],
                    'budget': 'high'
                },
                {
                    'destination': 'Cultural Immersion',
                    'type': 'perspective_therapy',
                    'duration': '10 days',
                    'benefits': ['new_perspectives', 'growth', 'adventure'],
                    'budget': 'high'
                }
            ]
        }

    async def get_mindfulness_activities(self, stress_level: float, user_preferences: Dict) -> List[Dict]:
        """Get personalized mindfulness activities based on stress level and preferences"""
        experience_level = user_preferences.get('mindfulness_experience', 'beginner')
        available_time = user_preferences.get('available_time', 15)

        suitable_activities = []
        activities = self.mindfulness_activities.get(experience_level, self.mindfulness_activities['beginner'])

        for activity in activities:
            duration_minutes = int(activity['duration'].split()[0])
            if duration_minutes <= available_time:
                # Calculate effectiveness based on stress level
                effectiveness = self._calculate_activity_effectiveness(activity, stress_level, 'stress')
                activity['effectiveness_score'] = effectiveness
                suitable_activities.append(activity)

        # Sort by effectiveness and return top recommendations
        suitable_activities.sort(key=lambda x: x['effectiveness_score'], reverse=True)
        return suitable_activities[:3]

    async def get_physical_activities(self, energy_level: float, fitness_level: str) -> List[Dict]:
        """Get physical activities based on current energy and fitness level"""
        if energy_level < 0.3:
            activity_category = 'low_energy'
        elif energy_level < 0.7:
            activity_category = 'moderate_energy'
        else:
            activity_category = 'high_energy'

        available_activities = self.physical_activities[activity_category]
        personalized_activities = []

        for activity in available_activities:
            # Adjust based on fitness level
            adjusted_activity = activity.copy()
            if fitness_level == 'beginner' and activity.get('duration'):
                duration = int(activity['duration'].split()[0])
                adjusted_activity['duration'] = f"{max(10, duration // 2)} minutes"

            personalized_activities.append(adjusted_activity)

        return personalized_activities

    async def get_spiritual_activities(self, spiritual_preferences: Dict) -> List[Dict]:
        """Get spiritual activities based on user's spiritual interests"""
        preferred_traditions = spiritual_preferences.get('traditions', ['Universal'])
        activity_types = spiritual_preferences.get('types', ['meditation', 'prayer'])

        recommendations = []

        for activity_type in activity_types:
            if activity_type in self.spiritual_activities:
                for activity in self.spiritual_activities[activity_type]:
                    if (activity['tradition'] in preferred_traditions or
                            activity['tradition'] == 'Universal' or
                            'Various' in preferred_traditions):
                        recommendations.append(activity)

        return recommendations[:4]

    async def get_nutrition_recommendations(self, mood_state: float) -> List[Dict]:
        """Get nutrition recommendations based on mood state"""
        if mood_state < 0.4:
            return self.nutrition_recommendations['mood_boosting'][:2]
        else:
            return self.nutrition_recommendations['stress_reducing'][:2]

    async def get_travel_therapy_suggestions(self, budget: str, location: Optional[str] = None) -> List[Dict]:
        """Get travel therapy suggestions based on budget and location"""
        budget_mapping = {
            'low': ['local'],
            'moderate': ['local', 'regional'],
            'high': ['local', 'regional', 'distant']
        }

        available_categories = budget_mapping.get(budget, ['local'])
        suggestions = []

        for category in available_categories:
            if category in self.travel_therapy_suggestions:
                category_suggestions = self.travel_therapy_suggestions[category]
                suggestions.extend(category_suggestions)

        return suggestions

    async def get_emergency_coping_strategies(self) -> List[Dict]:
        """Get immediate coping strategies for crisis situations"""
        return [
            {
                'name': '5-4-3-2-1 Grounding Technique',
                'instructions': 'Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste',
                'duration': '3 minutes',
                'effectiveness': 'high'
            },
            {
                'name': 'Box Breathing',
                'instructions': 'Breathe in 4, hold 4, out 4, hold 4. Repeat.',
                'duration': '2 minutes',
                'effectiveness': 'high'
            },
            {
                'name': 'Progressive Muscle Relaxation',
                'instructions': 'Tense and release each muscle group for 5 seconds',
                'duration': '10 minutes',
                'effectiveness': 'moderate'
            }
        ]

    async def get_activity_streaks(self) -> Dict:
        """Get user's current wellness activity streaks"""
        # This would typically connect to a database
        # For now, return mock data
        return {
            'meditation_streak': 5,
            'exercise_streak': 3,
            'healthy_eating_streak': 7,
            'social_connection_streak': 2
        }

    def _calculate_activity_effectiveness(self, activity: Dict, user_state: float, target_area: str) -> float:
        """Calculate how effective an activity would be for the user's current state"""
        base_effectiveness = activity.get(f'{target_area}_relief', 0.5)

        # Adjust based on user state severity
        if user_state > 0.8:  # High severity
            effectiveness = base_effectiveness * 1.2  # Boost effectiveness for high need
        elif user_state < 0.3:  # Low severity
            effectiveness = base_effectiveness * 0.8  # Reduce for maintenance
        else:
            effectiveness = base_effectiveness

        return min(1.0, effectiveness)  # Cap at 1.0

    async def track_activity_completion(self, user_id: str, activity: Dict, completion_rating: float):
        """Track activity completion for personalization learning"""
        # This would store in database for learning user preferences
        activity_log = {
            'user_id': user_id,
            'activity': activity,
            'completion_rating': completion_rating,
            'timestamp': datetime.now().isoformat()
        }
        # Store in database or memory system
        pass

    async def get_personalized_schedule(self, user_preferences: Dict, mental_state: Dict) -> Dict:
        """Generate a personalized daily wellness schedule"""
        schedule = {
            'morning': [],
            'afternoon': [],
            'evening': []
        }

        # Morning activities - energy and mood boosting
        if mental_state.get('energy_level', 0.5) < 0.4:
            morning_activities = await self.get_physical_activities(0.3,
                                                                    user_preferences.get('fitness_level', 'moderate'))
            schedule['morning'].extend(morning_activities[:1])

        # Afternoon activities - stress management
        if mental_state.get('stress_indicators', 0) > 0.6:
            afternoon_activities = await self.get_mindfulness_activities(
                mental_state['stress_indicators'],
                user_preferences
            )
            schedule['afternoon'].extend(afternoon_activities[:1])

        # Evening activities - relaxation and reflection
        evening_activities = await self.get_spiritual_activities(
            user_preferences.get('spiritual_interests', {})
        )
        schedule['evening'].extend(evening_activities[:1])

        return schedule
