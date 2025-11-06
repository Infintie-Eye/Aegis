crew_configs = {
    'crisis_assessment': {
        'agents': ['crisis_detection_agent', 'emotional_support_agent'],
        'description': 'Assess the user for crisis and provide immediate support.',
        'expected_output': 'A crisis assessment report and immediate support message.'
    },
    'intervention': {
        'agents': ['cbt_therapist_agent', 'mindfulness_coach_agent'],
        'description': 'Provide therapeutic intervention for the user\'s current emotional state.',
        'expected_output': 'A personalized intervention plan.'
    },
    'mental_support': {
        'agents': ['emotional_support_agent', 'progress_tracker_agent'],
        'description': 'Provide ongoing emotional support and track progress.',
        'expected_output': 'An empathetic response and progress update.'
    },
    'progress_review': {
        'agents': ['progress_tracker_agent', 'cbt_therapist_agent'],
        'description': 'Review the user\'s progress over time and adjust the support plan.',
        'expected_output': 'A progress review report and updated recommendations.'
    }
}