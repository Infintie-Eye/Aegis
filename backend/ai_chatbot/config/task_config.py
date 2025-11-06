task_configs = {
    'crisis_assessment': {
        'description': 'Assess the user\'s message for signs of crisis and provide immediate support. The user message is: {message}. User context: {user_context}.',
        'expected_output': 'A crisis assessment report and immediate support message.'
    },
    'intervention': {
        'description': 'Based on the user\'s message: {message} and their current context: {user_context}, provide a therapeutic intervention using CBT and mindfulness techniques.',
        'expected_output': 'A personalized intervention plan with specific steps.'
    },
    'mental_support': {
        'description': 'Provide emotional support to the user based on their message: {message} and context: {user_context}. Show empathy and validate their feelings.',
        'expected_output': 'An empathetic and supportive response.'
    },
    'progress_review': {
        'description': 'Review the user\'s progress over time. The user\'s current message is: {message} and their context is: {user_context}.',
        'expected_output': 'A progress review report and updated recommendations.'
    }
}