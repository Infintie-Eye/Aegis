import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
import random


class CommunityMatcher:
    def __init__(self):
        self.support_groups_db = self._initialize_support_groups()
        self.peer_mentors_db = self._initialize_peer_mentors()
        self.community_events_db = self._initialize_community_events()
        self.user_interests_cache = {}

    def _initialize_support_groups(self) -> List[Dict]:
        """Initialize database of available support groups"""
        return [
            {
                'id': 'depression_support_1',
                'name': 'Depression Support Circle',
                'focus_areas': ['depression', 'mood_disorders', 'low_energy'],
                'meeting_schedule': 'Weekly, Wednesdays 7PM EST',
                'format': 'virtual',
                'size': 'small',  # 6-12 people
                'facilitator_type': 'peer_led',
                'demographics': {
                    'age_range': '18-65',
                    'gender': 'mixed',
                    'experience_level': 'all_levels'
                },
                'description': 'Safe space for sharing experiences with depression and supporting each other',
                'privacy_level': 'anonymous',
                'waiting_list': False
            },
            {
                'id': 'anxiety_warriors',
                'name': 'Anxiety Warriors',
                'focus_areas': ['anxiety', 'panic_disorders', 'social_anxiety'],
                'meeting_schedule': 'Bi-weekly, Saturdays 2PM EST',
                'format': 'virtual',
                'size': 'medium',  # 12-20 people
                'facilitator_type': 'professional_led',
                'demographics': {
                    'age_range': '22-45',
                    'gender': 'mixed',
                    'experience_level': 'all_levels'
                },
                'description': 'Learn coping strategies and connect with others managing anxiety',
                'privacy_level': 'semi_anonymous',
                'waiting_list': False
            },
            {
                'id': 'mens_mental_health',
                'name': 'Men\'s Mental Health Alliance',
                'focus_areas': ['male_specific_issues', 'emotional_expression', 'stress'],
                'meeting_schedule': 'Weekly, Tuesdays 8PM EST',
                'format': 'virtual',
                'size': 'small',
                'facilitator_type': 'peer_led',
                'demographics': {
                    'age_range': '25-55',
                    'gender': 'male_only',
                    'experience_level': 'all_levels'
                },
                'description': 'Brotherhood for men breaking the silence around mental health',
                'privacy_level': 'confidential',
                'waiting_list': False
            },
            {
                'id': 'young_adults_support',
                'name': 'Young Adults Navigating Life',
                'focus_areas': ['life_transitions', 'career_stress', 'relationships'],
                'meeting_schedule': 'Weekly, Sundays 6PM EST',
                'format': 'virtual',
                'size': 'medium',
                'facilitator_type': 'professional_led',
                'demographics': {
                    'age_range': '18-30',
                    'gender': 'mixed',
                    'experience_level': 'all_levels'
                },
                'description': 'Support for young adults facing life\'s challenges',
                'privacy_level': 'semi_anonymous',
                'waiting_list': False
            },
            {
                'id': 'mindfulness_circle',
                'name': 'Mindfulness & Meditation Circle',
                'focus_areas': ['mindfulness', 'stress_reduction', 'spiritual_growth'],
                'meeting_schedule': 'Daily, Various times',
                'format': 'virtual',
                'size': 'large',  # 20+ people
                'facilitator_type': 'rotating_leadership',
                'demographics': {
                    'age_range': '18-80',
                    'gender': 'mixed',
                    'experience_level': 'all_levels'
                },
                'description': 'Practice mindfulness together and share spiritual insights',
                'privacy_level': 'open',
                'waiting_list': False
            }
        ]

    def _initialize_peer_mentors(self) -> List[Dict]:
        """Initialize database of available peer mentors"""
        return [
            {
                'id': 'mentor_1',
                'name': 'Alex M.',
                'specialties': ['depression_recovery', 'life_transitions', 'career_change'],
                'recovery_stage': 'stable_recovery',
                'experience_years': 3,
                'demographics': {
                    'age_range': '28-32',
                    'gender': 'male',
                    'location': 'US_EST'
                },
                'availability': {
                    'days': ['Monday', 'Wednesday', 'Friday'],
                    'times': ['evening'],
                    'frequency': 'weekly'
                },
                'communication_style': ['supportive', 'practical', 'goal_oriented'],
                'bio': 'Overcame severe depression, now helps others navigate similar challenges',
                'languages': ['English'],
                'certifications': ['Peer Support Specialist'],
                'rating': 4.8,
                'active_mentees': 3,
                'max_mentees': 5
            },
            {
                'id': 'mentor_2',
                'name': 'Sarah K.',
                'specialties': ['anxiety_management', 'social_anxiety', 'workplace_stress'],
                'recovery_stage': 'thriving',
                'experience_years': 5,
                'demographics': {
                    'age_range': '30-35',
                    'gender': 'female',
                    'location': 'US_PST'
                },
                'availability': {
                    'days': ['Tuesday', 'Thursday', 'Saturday'],
                    'times': ['morning', 'afternoon'],
                    'frequency': 'bi_weekly'
                },
                'communication_style': ['empathetic', 'analytical', 'encouraging'],
                'bio': 'Former anxiety sufferer, now successful professional helping others',
                'languages': ['English', 'Spanish'],
                'certifications': ['Certified Peer Recovery Specialist'],
                'rating': 4.9,
                'active_mentees': 4,
                'max_mentees': 6
            },
            {
                'id': 'mentor_3',
                'name': 'Marcus J.',
                'specialties': ['male_mental_health', 'emotional_expression', 'relationship_issues'],
                'recovery_stage': 'stable_recovery',
                'experience_years': 2,
                'demographics': {
                    'age_range': '35-40',
                    'gender': 'male',
                    'location': 'US_CST'
                },
                'availability': {
                    'days': ['Monday', 'Thursday', 'Sunday'],
                    'times': ['evening'],
                    'frequency': 'weekly'
                },
                'communication_style': ['direct', 'honest', 'brotherhood_focused'],
                'bio': 'Breaking stigma around men\'s mental health, one conversation at a time',
                'languages': ['English'],
                'certifications': ['Men\'s Mental Health Advocate'],
                'rating': 4.7,
                'active_mentees': 2,
                'max_mentees': 4
            }
        ]

    def _initialize_community_events(self) -> List[Dict]:
        """Initialize upcoming community events"""
        base_date = datetime.now()
        return [
            {
                'id': 'event_1',
                'name': 'Mental Health Awareness Workshop',
                'type': 'educational',
                'date': (base_date + timedelta(days=3)).isoformat(),
                'duration': '2 hours',
                'format': 'virtual',
                'target_audience': ['general', 'newly_diagnosed'],
                'topics': ['understanding_mental_health', 'self_care', 'resources'],
                'facilitator': 'Dr. Jennifer Smith, Licensed Therapist',
                'capacity': 100,
                'registered': 45,
                'cost': 'free',
                'registration_required': True
            },
            {
                'id': 'event_2',
                'name': 'Mindfulness & Nature Walk',
                'type': 'wellness_activity',
                'date': (base_date + timedelta(days=5)).isoformat(),
                'duration': '1.5 hours',
                'format': 'in_person',
                'location': 'Central Park, NYC',
                'target_audience': ['anxiety', 'stress', 'mindfulness_seekers'],
                'topics': ['mindful_walking', 'nature_therapy', 'stress_reduction'],
                'facilitator': 'Community Volunteers',
                'capacity': 20,
                'registered': 12,
                'cost': 'free',
                'registration_required': True
            },
            {
                'id': 'event_3',
                'name': 'Men\'s Mental Health Panel',
                'type': 'discussion_panel',
                'date': (base_date + timedelta(days=7)).isoformat(),
                'duration': '90 minutes',
                'format': 'virtual',
                'target_audience': ['male', 'men_supporters'],
                'topics': ['masculinity_myths', 'emotional_expression', 'seeking_help'],
                'facilitator': 'Panel of Experts and Advocates',
                'capacity': 200,
                'registered': 78,
                'cost': 'free',
                'registration_required': True
            },
            {
                'id': 'event_4',
                'name': 'Creative Expression Therapy Session',
                'type': 'therapeutic_activity',
                'date': (base_date + timedelta(days=10)).isoformat(),
                'duration': '2 hours',
                'format': 'virtual',
                'target_audience': ['depression', 'creative_seekers', 'alternative_therapy'],
                'topics': ['art_therapy', 'music_therapy', 'creative_expression'],
                'facilitator': 'Licensed Art Therapist',
                'capacity': 30,
                'registered': 18,
                'cost': '$10',
                'registration_required': True
            }
        ]

    async def find_matching_groups(self, struggles: List[str], demographics: Dict, preferences: Dict) -> List[Dict]:
        """Find support groups matching user's struggles and preferences"""
        matching_groups = []

        for group in self.support_groups_db:
            match_score = await self._calculate_group_match_score(
                group, struggles, demographics, preferences
            )

            if match_score >= 0.6:  # Minimum match threshold
                group_recommendation = group.copy()
                group_recommendation['match_score'] = match_score
                group_recommendation['match_reasons'] = await self._get_match_reasons(
                    group, struggles, demographics, preferences
                )
                matching_groups.append(group_recommendation)

        # Sort by match score and return top matches
        matching_groups.sort(key=lambda x: x['match_score'], reverse=True)
        return matching_groups[:5]

    async def find_peer_mentors(self, current_state: List[str], recovery_stage: str) -> List[Dict]:
        """Find peer mentors based on current struggles and recovery stage"""
        suitable_mentors = []

        for mentor in self.peer_mentors_db:
            if mentor['active_mentees'] >= mentor['max_mentees']:
                continue  # Mentor is at capacity

            compatibility_score = await self._calculate_mentor_compatibility(
                mentor, current_state, recovery_stage
            )

            if compatibility_score >= 0.7:  # Higher threshold for mentors
                mentor_recommendation = mentor.copy()
                mentor_recommendation['compatibility_score'] = compatibility_score
                mentor_recommendation['why_good_match'] = await self._get_mentor_match_reasons(
                    mentor, current_state
                )
                suitable_mentors.append(mentor_recommendation)

        # Sort by compatibility score
        suitable_mentors.sort(key=lambda x: x['compatibility_score'], reverse=True)
        return suitable_mentors[:3]

    async def get_upcoming_events(self, interests: List[str] = None) -> List[Dict]:
        """Get upcoming community events, optionally filtered by interests"""
        upcoming_events = []
        current_time = datetime.now()

        for event in self.community_events_db:
            event_date = datetime.fromisoformat(event['date'])

            # Only include future events
            if event_date > current_time:
                if interests:
                    # Check if event matches user interests
                    if any(interest in event['target_audience'] for interest in interests):
                        upcoming_events.append(event)
                else:
                    upcoming_events.append(event)

        # Sort by date
        upcoming_events.sort(key=lambda x: x['date'])
        return upcoming_events[:10]

    async def get_engagement_metrics(self) -> Dict:
        """Get user's community engagement metrics"""
        # This would typically come from a database
        # For now, return mock data
        return {
            'support_group_sessions_attended': 12,
            'peer_mentor_sessions_completed': 8,
            'community_events_participated': 5,
            'connections_made': 15,
            'help_given_to_others': 23,
            'engagement_level': 'high',
            'community_impact_score': 8.2
        }

    async def _calculate_group_match_score(self, group: Dict, struggles: List[str],
                                           demographics: Dict, preferences: Dict) -> float:
        """Calculate how well a support group matches user needs"""
        score = 0.0

        # Struggle alignment (40% weight)
        struggle_matches = len(set(struggles) & set(group['focus_areas']))
        if group['focus_areas']:
            struggle_score = struggle_matches / len(group['focus_areas'])
            score += struggle_score * 0.4

        # Demographic compatibility (25% weight)
        demo_score = await self._calculate_demographic_compatibility(
            group['demographics'], demographics
        )
        score += demo_score * 0.25

        # Size preference (15% weight)
        size_preference = preferences.get('group_size_preference', 'any')
        size_score = 1.0 if size_preference == 'any' or size_preference == group['size'] else 0.7
        score += size_score * 0.15

        # Schedule compatibility (10% weight)
        # Simplified - in real implementation would check actual availability
        schedule_score = 0.8  # Default assumption of reasonable compatibility
        score += schedule_score * 0.10

        # Privacy level preference (10% weight)
        privacy_preference = preferences.get('privacy_level', 'semi_anonymous')
        privacy_score = 1.0 if privacy_preference == group['privacy_level'] else 0.8
        score += privacy_score * 0.10

        return min(1.0, score)

    async def _calculate_mentor_compatibility(self, mentor: Dict, struggles: List[str],
                                              recovery_stage: str) -> float:
        """Calculate compatibility between user and potential mentor"""
        score = 0.0

        # Specialty alignment (50% weight)
        specialty_matches = len(set(struggles) & set(mentor['specialties']))
        if mentor['specialties']:
            specialty_score = specialty_matches / len(mentor['specialties'])
            score += specialty_score * 0.5

        # Recovery stage compatibility (20% weight)
        stage_compatibility = {
            'beginning': {'stable_recovery': 1.0, 'thriving': 0.9},
            'progress': {'stable_recovery': 0.9, 'thriving': 1.0},
            'stable': {'thriving': 1.0, 'stable_recovery': 0.8}
        }
        stage_score = stage_compatibility.get(recovery_stage, {}).get(
            mentor['recovery_stage'], 0.7
        )
        score += stage_score * 0.2

        # Experience level (15% weight)
        experience_score = min(1.0, mentor['experience_years'] / 5)  # Max at 5 years
        score += experience_score * 0.15

        # Rating (10% weight)
        rating_score = mentor['rating'] / 5.0  # Convert 5-star rating to 0-1
        score += rating_score * 0.10

        # Availability (5% weight)
        # Simplified - assume good availability
        availability_score = 0.9
        score += availability_score * 0.05

        return min(1.0, score)

    async def _calculate_demographic_compatibility(self, group_demo: Dict, user_demo: Dict) -> float:
        """Calculate demographic compatibility score"""
        score = 0.0
        weight_per_factor = 1.0 / 3  # Equal weight for age, gender, location

        # Age compatibility
        user_age = user_demo.get('age')
        group_age_range = group_demo.get('age_range', '18-80')
        if user_age:
            age_min, age_max = map(int, group_age_range.split('-'))
            if age_min <= user_age <= age_max:
                score += weight_per_factor
            else:
                score += weight_per_factor * 0.5  # Partial credit for close ranges
        else:
            score += weight_per_factor * 0.8  # Default if age not provided

        # Gender compatibility
        user_gender = user_demo.get('gender')
        group_gender = group_demo.get('gender', 'mixed')
        if group_gender == 'mixed' or user_gender == group_gender:
            score += weight_per_factor
        else:
            score += weight_per_factor * 0.3  # Lower score for gender mismatch

        # Location/timezone compatibility (simplified)
        score += weight_per_factor * 0.9  # Assume reasonable compatibility

        return min(1.0, score)

    async def _get_match_reasons(self, group: Dict, struggles: List[str],
                                 demographics: Dict, preferences: Dict) -> List[str]:
        """Get human-readable reasons why this group is a good match"""
        reasons = []

        # Check struggle alignment
        matching_struggles = set(struggles) & set(group['focus_areas'])
        if matching_struggles:
            reasons.append(f"Focuses on your areas of concern: {', '.join(matching_struggles)}")

        # Check facilitator type
        if group['facilitator_type'] == 'professional_led':
            reasons.append("Led by mental health professionals")
        elif group['facilitator_type'] == 'peer_led':
            reasons.append("Peer-led environment for authentic sharing")

        # Check group size
        size_benefits = {
            'small': 'Intimate setting for deeper connections',
            'medium': 'Balanced group size for diverse perspectives',
            'large': 'Larger community with varied experiences'
        }
        if group['size'] in size_benefits:
            reasons.append(size_benefits[group['size']])

        # Check meeting frequency
        if 'Weekly' in group['meeting_schedule']:
            reasons.append("Regular weekly meetings for consistent support")
        elif 'Daily' in group['meeting_schedule']:
            reasons.append("Daily sessions available for intensive support")

        return reasons

    async def _get_mentor_match_reasons(self, mentor: Dict, struggles: List[str]) -> List[str]:
        """Get reasons why this mentor is a good match"""
        reasons = []

        # Check specialty alignment
        matching_specialties = set(struggles) & set(mentor['specialties'])
        if matching_specialties:
            reasons.append(f"Specializes in: {', '.join(matching_specialties)}")

        # Check experience
        if mentor['experience_years'] >= 3:
            reasons.append(f"{mentor['experience_years']} years of peer support experience")

        # Check rating
        if mentor['rating'] >= 4.5:
            reasons.append(f"Highly rated by previous mentees ({mentor['rating']}/5.0)")

        # Check recovery stage
        if mentor['recovery_stage'] == 'thriving':
            reasons.append("Successfully thriving in recovery, inspiring success story")
        elif mentor['recovery_stage'] == 'stable_recovery':
            reasons.append("Stable in recovery with fresh perspective on challenges")

        # Check communication style
        styles = mentor.get('communication_style', [])
        if styles:
            reasons.append(f"Communication style: {', '.join(styles)}")

        return reasons

    async def recommend_community_activities(self, user_profile: Dict, current_mood: str) -> List[Dict]:
        """Recommend community activities based on user profile and current mood"""
        activities = []

        if current_mood in ['lonely', 'isolated']:
            activities.extend([
                {
                    'type': 'support_group',
                    'name': 'Drop-in Support Circle',
                    'description': 'Connect with others who understand',
                    'time_commitment': '1 hour',
                    'benefits': ['social_connection', 'shared_understanding', 'reduced_isolation']
                },
                {
                    'type': 'buddy_system',
                    'name': 'Accountability Partner Matching',
                    'description': 'Get matched with someone for mutual support',
                    'time_commitment': '30 minutes weekly',
                    'benefits': ['consistent_check_ins', 'mutual_accountability', 'friendship']
                }
            ])

        if current_mood in ['anxious', 'stressed']:
            activities.extend([
                {
                    'type': 'wellness_group',
                    'name': 'Group Meditation Session',
                    'description': 'Practice mindfulness with others',
                    'time_commitment': '45 minutes',
                    'benefits': ['stress_reduction', 'mindfulness', 'group_energy']
                }
            ])

        if current_mood in ['hopeless', 'depressed']:
            activities.extend([
                {
                    'type': 'peer_support',
                    'name': 'Hope Sharing Circle',
                    'description': 'Hear stories of recovery and resilience',
                    'time_commitment': '90 minutes',
                    'benefits': ['hope_restoration', 'inspiration', 'proof_of_possibility']
                }
            ])

        return activities

    async def track_community_engagement(self, user_id: str, activity_type: str,
                                         engagement_data: Dict):
        """Track user's community engagement for personalization"""
        # In a real system, this would store in database
        engagement_log = {
            'user_id': user_id,
            'activity_type': activity_type,
            'engagement_data': engagement_data,
            'timestamp': datetime.now().isoformat()
        }
        # Store engagement data for learning and recommendations
        pass

    async def get_community_insights(self, user_id: str) -> Dict:
        """Get insights about user's community engagement patterns"""
        # This would analyze stored engagement data
        return {
            'preferred_group_types': ['peer_led', 'small_groups'],
            'optimal_meeting_times': ['evening', 'weekends'],
            'engagement_trends': 'increasing',
            'social_battery_patterns': 'moderate_duration_preferred',
            'connection_quality': 'deep_connections_preferred'
        }
