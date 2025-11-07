crew_configs = {
    'crisis_intervention': {
        'agents': ['crisis_detection_agent', 'emotional_support_agent', 'trauma_informed_agent'],
        'description': 'Immediate crisis intervention and safety assessment for users in mental health crisis.',
        'expected_output': 'Comprehensive crisis assessment, immediate safety plan, and emergency resources with follow-up recommendations.',
        'process': 'hierarchical',
        'priority': 'urgent'
    },
    'crisis_assessment': {
        'agents': ['crisis_detection_agent', 'emotional_support_agent'],
        'description': 'Assess the user for crisis indicators and provide immediate support.',
        'expected_output': 'A crisis assessment report and immediate support message.',
        'process': 'sequential',
        'priority': 'high'
    },
    'depression_support': {
        'agents': ['cbt_therapist_agent', 'emotional_support_agent', 'motivational_coach_agent',
                   'wellness_advisor_agent'],
        'description': 'Comprehensive support for users experiencing depression using CBT, emotional validation, motivation building, and wellness planning.',
        'expected_output': 'Personalized depression support plan with cognitive strategies, emotional validation, motivation techniques, and wellness recommendations.',
        'process': 'sequential',
        'priority': 'high'
    },
    'anxiety_intervention': {
        'agents': ['cbt_therapist_agent', 'mindfulness_coach_agent', 'wellness_advisor_agent'],
        'description': 'Targeted intervention for anxiety using cognitive techniques, mindfulness practices, and lifestyle modifications.',
        'expected_output': 'Comprehensive anxiety management plan with cognitive strategies, mindfulness exercises, and wellness recommendations.',
        'process': 'sequential',
        'priority': 'high'
    },
    'stress_management': {
        'agents': ['mindfulness_coach_agent', 'wellness_advisor_agent', 'cbt_therapist_agent'],
        'description': 'Holistic stress management approach combining mindfulness, wellness practices, and cognitive strategies.',
        'expected_output': 'Personalized stress management plan with mindfulness techniques, lifestyle changes, and cognitive tools.',
        'process': 'sequential',
        'priority': 'moderate'
    },
    'intervention': {
        'agents': ['cbt_therapist_agent', 'mindfulness_coach_agent'],
        'description': 'Provide therapeutic intervention for the user\'s current emotional state.',
        'expected_output': 'A personalized intervention plan.',
        'process': 'sequential',
        'priority': 'moderate'
    },
    'mental_support': {
        'agents': ['emotional_support_agent', 'progress_tracker_agent'],
        'description': 'Provide ongoing emotional support and track progress.',
        'expected_output': 'An empathetic response and progress update.',
        'process': 'sequential',
        'priority': 'standard'
    },
    'community_building': {
        'agents': ['community_connector_agent', 'emotional_support_agent', 'family_systems_agent'],
        'description': 'Help users build social connections, find peer support, and improve relationships.',
        'expected_output': 'Community connection plan with support group recommendations, peer matching, and relationship guidance.',
        'process': 'sequential',
        'priority': 'moderate'
    },
    'motivation_enhancement': {
        'agents': ['motivational_coach_agent', 'cbt_therapist_agent', 'wellness_advisor_agent'],
        'description': 'Build motivation, set achievable goals, and develop self-efficacy using motivational interviewing and behavioral strategies.',
        'expected_output': 'Motivation enhancement plan with goal-setting framework, behavioral activation strategies, and wellness integration.',
        'process': 'sequential',
        'priority': 'moderate'
    },
    'trauma_processing': {
        'agents': ['trauma_informed_agent', 'emotional_support_agent', 'mindfulness_coach_agent'],
        'description': 'Trauma-informed support for processing traumatic experiences with safety-first approach.',
        'expected_output': 'Trauma-informed support plan with safety strategies, emotional validation, and grounding techniques.',
        'process': 'sequential',
        'priority': 'high'
    },
    'substance_abuse_support': {
        'agents': ['substance_abuse_counselor_agent', 'motivational_coach_agent', 'community_connector_agent'],
        'description': 'Comprehensive support for substance use issues including motivation building and peer support connections.',
        'expected_output': 'Substance abuse support plan with recovery strategies, motivation enhancement, and community resources.',
        'process': 'sequential',
        'priority': 'high'
    },
    'grief_support': {
        'agents': ['grief_counselor_agent', 'emotional_support_agent', 'community_connector_agent'],
        'description': 'Compassionate support for individuals processing grief, loss, and bereavement.',
        'expected_output': 'Grief support plan with processing techniques, emotional validation, and bereavement resources.',
        'process': 'sequential',
        'priority': 'high'
    },
    'eating_disorder_support': {
        'agents': ['eating_disorder_specialist_agent', 'cbt_therapist_agent', 'family_systems_agent'],
        'description': 'Specialized support for eating disorders addressing psychological, behavioral, and family system factors.',
        'expected_output': 'Eating disorder support plan with therapeutic strategies, family involvement, and recovery planning.',
        'process': 'sequential',
        'priority': 'high'
    },
    'adolescent_support': {
        'agents': ['adolescent_specialist_agent', 'family_systems_agent', 'community_connector_agent'],
        'description': 'Age-appropriate mental health support for teenagers and young adults addressing developmental challenges.',
        'expected_output': 'Adolescent support plan with developmental considerations, family dynamics, and peer connections.',
        'process': 'sequential',
        'priority': 'moderate'
    },
    'cultural_responsive_care': {
        'agents': ['cultural_competency_agent', 'emotional_support_agent', 'community_connector_agent'],
        'description': 'Culturally responsive mental health support adapted for diverse backgrounds and identities.',
        'expected_output': 'Culturally adapted support plan with inclusive practices and culturally relevant resources.',
        'process': 'sequential',
        'priority': 'standard'
    },
    'wellness_optimization': {
        'agents': ['wellness_advisor_agent', 'mindfulness_coach_agent', 'motivational_coach_agent'],
        'description': 'Comprehensive wellness planning integrating physical health, mindfulness, and motivation for optimal mental health.',
        'expected_output': 'Holistic wellness plan with lifestyle recommendations, mindfulness practices, and motivation strategies.',
        'process': 'sequential',
        'priority': 'standard'
    },
    'relationship_support': {
        'agents': ['family_systems_agent', 'emotional_support_agent', 'community_connector_agent'],
        'description': 'Support for relationship challenges, family dynamics, and interpersonal difficulties.',
        'expected_output': 'Relationship support plan with communication strategies, family therapy insights, and social resources.',
        'process': 'sequential',
        'priority': 'moderate'
    },
    'progress_review': {
        'agents': ['progress_tracker_agent', 'cbt_therapist_agent'],
        'description': 'Review the user\'s progress over time and adjust the support plan.',
        'expected_output': 'A progress review report and updated recommendations.',
        'process': 'sequential',
        'priority': 'standard'
    },
    'comprehensive_assessment': {
        'agents': ['progress_tracker_agent', 'cbt_therapist_agent', 'emotional_support_agent',
                   'wellness_advisor_agent'],
        'description': 'Comprehensive mental health assessment covering psychological, emotional, and wellness factors.',
        'expected_output': 'Complete mental health assessment with treatment recommendations across multiple domains.',
        'process': 'hierarchical',
        'priority': 'standard'
    },
    'crisis_follow_up': {
        'agents': ['crisis_detection_agent', 'progress_tracker_agent', 'community_connector_agent'],
        'description': 'Follow-up support after crisis intervention to ensure ongoing safety and connection to resources.',
        'expected_output': 'Crisis follow-up plan with safety monitoring, progress tracking, and resource connections.',
        'process': 'sequential',
        'priority': 'high'
    },
    'specialized_referral': {
        'agents': ['progress_tracker_agent', 'cultural_competency_agent', 'community_connector_agent'],
        'description': 'Identify and coordinate referrals to specialized mental health services and providers.',
        'expected_output': 'Specialized referral recommendations with culturally appropriate provider matching and resource coordination.',
        'process': 'sequential',
        'priority': 'moderate'
    }
}