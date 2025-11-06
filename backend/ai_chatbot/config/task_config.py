task_configs = {
    'crisis_intervention': {
        'description': '''URGENT CRISIS INTERVENTION REQUIRED:
        
        User Message: {message}
        User Context: {user_context}
        Crisis Level: {crisis_level}/10
        Crisis Indicators: {crisis_indicators}
        
        IMMEDIATE ACTIONS REQUIRED:
        1. Conduct rapid risk assessment
        2. Implement immediate safety interventions
        3. Provide crisis resources and emergency contacts
        4. Create safety plan with user
        5. Establish follow-up protocols
        
        Prioritize user safety above all else. Use trauma-informed, non-judgmental approach. 
        If crisis level is 9+, recommend immediate emergency services contact.
        Provide hope while acknowledging pain. Connect to immediate resources.''',
        'expected_output': 'Comprehensive crisis response including immediate safety plan, emergency resources, risk mitigation strategies, and follow-up recommendations.'
    },
    'crisis_assessment': {
        'description': 'Assess the user\'s message for signs of crisis and provide immediate support. The user message is: {message}. User context: {user_context}.',
        'expected_output': 'A crisis assessment report and immediate support message.'
    },
    'depression_support': {
        'description': '''DEPRESSION SUPPORT INTERVENTION:
        
        User Message: {message}
        User Context: {user_context}
        Mental Health Indicators: {mental_health_indicators}
        
        COMPREHENSIVE DEPRESSION SUPPORT APPROACH:
        1. Validate emotional experience without minimizing
        2. Assess for cognitive distortions and negative thought patterns
        3. Introduce behavioral activation strategies
        4. Explore motivation and values-based goals
        5. Recommend holistic wellness interventions
        6. Address hopelessness with evidence-based hope building
        
        Use collaborative, empathetic approach. Focus on small, achievable steps.
        Integrate cognitive restructuring with emotional validation and practical wellness strategies.''',
        'expected_output': 'Comprehensive depression support plan addressing cognitive, behavioral, motivational, and wellness aspects with specific action steps.'
    },
    'anxiety_intervention': {
        'description': '''ANXIETY MANAGEMENT INTERVENTION:
        
        User Message: {message}
        User Context: {user_context}
        Anxiety Indicators: {anxiety_indicators}
        
        TARGETED ANXIETY INTERVENTION APPROACH:
        1. Validate anxiety experience and normalize physiological responses
        2. Teach grounding and breathing techniques for immediate relief
        3. Identify anxiety triggers and catastrophic thinking patterns
        4. Introduce mindfulness and present-moment awareness practices
        5. Develop gradual exposure and behavioral strategies
        6. Recommend lifestyle modifications for anxiety management
        
        Provide immediate coping tools while building long-term resilience.
        Balance cognitive techniques with somatic approaches.''',
        'expected_output': 'Comprehensive anxiety management plan with immediate coping strategies, cognitive tools, mindfulness practices, and lifestyle recommendations.'
    },
    'stress_management': {
        'description': '''STRESS MANAGEMENT INTERVENTION:
        
        User Message: {message}
        User Context: {user_context}
        Stress Indicators: {stress_indicators}
        
        HOLISTIC STRESS MANAGEMENT APPROACH:
        1. Assess stress sources and contributing factors
        2. Teach immediate stress relief techniques
        3. Introduce mindfulness and meditation practices
        4. Develop healthy boundaries and time management
        5. Address cognitive patterns that amplify stress
        6. Create sustainable wellness and self-care routine
        
        Focus on both immediate relief and long-term stress resilience.
        Integrate mind-body approaches with practical life management skills.''',
        'expected_output': 'Personalized stress management plan with immediate relief techniques, mindfulness practices, boundary setting, and sustainable wellness strategies.'
    },
    'intervention': {
        'description': 'Based on the user\'s message: {message} and their current context: {user_context}, provide a therapeutic intervention using CBT and mindfulness techniques.',
        'expected_output': 'A personalized intervention plan with specific steps.'
    },
    'mental_support': {
        'description': 'Provide emotional support to the user based on their message: {message} and context: {user_context}. Show empathy and validate their feelings.',
        'expected_output': 'An empathetic and supportive response.'
    },
    'community_building': {
        'description': '''COMMUNITY CONNECTION AND SOCIAL SUPPORT:
        
        User Message: {message}
        User Context: {user_context}
        Social Connection Needs: {social_needs}
        
        COMPREHENSIVE COMMUNITY BUILDING APPROACH:
        1. Assess current social support and isolation factors
        2. Identify barriers to social connection
        3. Match with appropriate peer support groups
        4. Recommend community mental health resources
        5. Address family and relationship dynamics
        6. Develop social skills and communication strategies
        
        Focus on reducing isolation while respecting user's comfort level.
        Provide both online and offline community options.''',
        'expected_output': 'Community connection plan with peer support recommendations, social skill building, and relationship enhancement strategies.'
    },
    'motivation_enhancement': {
        'description': '''MOTIVATION BUILDING AND GOAL SETTING:
        
        User Message: {message}
        User Context: {user_context}
        Motivation Level: {motivation_level}
        
        MOTIVATIONAL ENHANCEMENT APPROACH:
        1. Explore user's values and intrinsic motivations
        2. Address motivation barriers and ambivalence
        3. Set SMART, values-aligned goals
        4. Develop behavioral activation strategies
        5. Create accountability and reward systems
        6. Integrate wellness activities that boost energy
        
        Use motivational interviewing principles. Start with small wins.
        Connect goals to personal values and meaningful activities.''',
        'expected_output': 'Motivation enhancement plan with values-based goal setting, behavioral activation, and sustainable motivation strategies.'
    },
    'trauma_processing': {
        'description': '''TRAUMA-INFORMED SUPPORT AND PROCESSING:
        
        User Message: {message}
        User Context: {user_context}
        Trauma Indicators: {trauma_indicators}
        
        TRAUMA-INFORMED CARE APPROACH:
        1. Prioritize safety and stabilization
        2. Validate trauma experience without re-traumatization
        3. Teach grounding and self-regulation techniques
        4. Address trauma-related symptoms (flashbacks, hypervigilance)
        5. Build resilience and post-traumatic growth
        6. Connect to trauma-specialized resources
        
        Always prioritize user safety and choice. Use gentle, non-invasive approaches.
        Focus on empowerment and rebuilding sense of control.''',
        'expected_output': 'Trauma-informed support plan with safety strategies, grounding techniques, symptom management, and specialized resource connections.'
    },
    'substance_abuse_support': {
        'description': '''SUBSTANCE ABUSE AND ADDICTION SUPPORT:
        
        User Message: {message}
        User Context: {user_context}
        Substance Use Indicators: {substance_indicators}
        
        ADDICTION SUPPORT APPROACH:
        1. Assess substance use patterns without judgment
        2. Explore motivation for change and recovery goals
        3. Address underlying mental health issues
        4. Develop healthy coping alternatives
        5. Connect to recovery support groups and resources
        6. Create relapse prevention and safety planning
        
        Use harm reduction and motivational interviewing approaches.
        Address co-occurring mental health conditions.''',
        'expected_output': 'Substance abuse support plan with motivational enhancement, coping strategies, recovery resources, and relapse prevention.'
    },
    'grief_support': {
        'description': '''GRIEF AND LOSS SUPPORT:
        
        User Message: {message}
        User Context: {user_context}
        Loss Details: {loss_context}
        
        GRIEF COUNSELING APPROACH:
        1. Validate grief experience and normalize reactions
        2. Explore the nature and meaning of the loss
        3. Support healthy grief processing
        4. Address complicated grief symptoms if present
        5. Help find meaning and continue bonds
        6. Connect to bereavement support resources
        
        Honor the uniqueness of each grief journey. Avoid rushing the process.
        Focus on supporting natural healing while addressing complications.''',
        'expected_output': 'Grief support plan with validation, processing techniques, meaning-making, and bereavement resources.'
    },
    'eating_disorder_support': {
        'description': '''EATING DISORDER SPECIALIZED SUPPORT:
        
        User Message: {message}
        User Context: {user_context}
        ED Indicators: {eating_disorder_indicators}
        
        EATING DISORDER SUPPORT APPROACH:
        1. Address both behavioral and psychological aspects
        2. Normalize relationship with food and body
        3. Identify triggers and underlying emotions
        4. Involve family support when appropriate
        5. Address co-occurring mental health issues
        6. Connect to specialized ED treatment resources
        
        Use non-diet, health-at-every-size approach. Avoid triggering language.
        Focus on recovery and healing relationship with food and body.''',
        'expected_output': 'Eating disorder support plan with behavioral strategies, body image work, family involvement, and specialized treatment connections.'
    },
    'adolescent_support': {
        'description': '''ADOLESCENT AND YOUNG ADULT MENTAL HEALTH SUPPORT:
        
        User Message: {message}
        User Context: {user_context}
        Developmental Stage: {developmental_stage}
        
        ADOLESCENT-FOCUSED APPROACH:
        1. Use age-appropriate communication and interventions
        2. Address identity formation and developmental challenges
        3. Navigate family dynamics and autonomy issues
        4. Address peer relationships and social pressures
        5. Support academic and future planning stress
        6. Connect to youth-specific resources and support
        
        Respect developmental autonomy while providing guidance.
        Address unique challenges of adolescence and young adulthood.''',
        'expected_output': 'Adolescent support plan with developmental considerations, family dynamics, peer relationships, and youth-specific resources.'
    },
    'cultural_responsive_care': {
        'description': '''CULTURALLY RESPONSIVE MENTAL HEALTH SUPPORT:
        
        User Message: {message}
        User Context: {user_context}
        Cultural Background: {cultural_context}
        
        CULTURAL COMPETENCY APPROACH:
        1. Honor cultural values and beliefs in treatment
        2. Address cultural factors affecting mental health
        3. Adapt interventions for cultural appropriateness
        4. Consider language and communication preferences
        5. Address discrimination and cultural trauma if relevant
        6. Connect to culturally specific resources and providers
        
        Demonstrate cultural humility and avoid assumptions.
        Integrate cultural strengths into healing process.''',
        'expected_output': 'Culturally adapted support plan with inclusive practices, cultural considerations, and culturally relevant resources.'
    },
    'wellness_optimization': {
        'description': '''HOLISTIC WELLNESS OPTIMIZATION:
        
        User Message: {message}
        User Context: {user_context}
        Current Wellness Level: {wellness_indicators}
        
        COMPREHENSIVE WELLNESS APPROACH:
        1. Assess current lifestyle and wellness practices
        2. Create personalized nutrition and exercise recommendations
        3. Develop mindfulness and stress management routine
        4. Optimize sleep hygiene and recovery
        5. Build motivation for sustainable lifestyle changes
        6. Integrate mental health with physical wellness
        
        Focus on sustainable, enjoyable wellness practices.
        Address barriers to wellness engagement.''',
        'expected_output': 'Holistic wellness plan with lifestyle modifications, mindfulness practices, motivation strategies, and sustainable health habits.'
    },
    'relationship_support': {
        'description': '''RELATIONSHIP AND FAMILY DYNAMICS SUPPORT:
        
        User Message: {message}
        User Context: {user_context}
        Relationship Issues: {relationship_context}
        
        FAMILY SYSTEMS APPROACH:
        1. Assess relationship patterns and dynamics
        2. Improve communication and conflict resolution skills
        3. Address family-of-origin influences
        4. Support healthy boundaries and assertiveness
        5. Strengthen social support networks
        6. Connect to couples/family therapy resources if needed
        
        Focus on improving relationship quality and communication.
        Address both individual and systemic factors.''',
        'expected_output': 'Relationship support plan with communication strategies, boundary setting, family insights, and social resource connections.'
    },
    'progress_review': {
        'description': 'Review the user\'s progress over time. The user\'s current message is: {message} and their context is: {user_context}.',
        'expected_output': 'A progress review report and updated recommendations.'
    },
    'comprehensive_assessment': {
        'description': '''COMPREHENSIVE MENTAL HEALTH ASSESSMENT:
        
        User Message: {message}
        User Context: {user_context}
        Assessment Areas: {assessment_domains}
        
        MULTI-DOMAIN ASSESSMENT APPROACH:
        1. Evaluate psychological symptoms and functioning
        2. Assess emotional regulation and coping skills
        3. Review social support and relationship quality
        4. Examine lifestyle and wellness factors
        5. Identify strengths and protective factors
        6. Develop integrated treatment recommendations
        
        Provide thorough but non-overwhelming assessment.
        Focus on user strengths alongside areas for growth.''',
        'expected_output': 'Comprehensive mental health assessment with multi-domain analysis, strengths identification, and integrated treatment recommendations.'
    },
    'crisis_follow_up': {
        'description': '''CRISIS FOLLOW-UP AND SAFETY MONITORING:
        
        User Message: {message}
        User Context: {user_context}
        Previous Crisis Level: {previous_crisis_level}
        
        CRISIS FOLLOW-UP APPROACH:
        1. Assess current safety and risk level
        2. Review effectiveness of previous safety interventions
        3. Monitor mental state and progress since crisis
        4. Adjust safety plan as needed
        5. Ensure connection to ongoing support resources
        6. Plan for continued monitoring and support
        
        Maintain focus on safety while building hope and connection.
        Ensure continuity of care and resource access.''',
        'expected_output': 'Crisis follow-up plan with safety assessment, intervention review, resource connections, and ongoing monitoring strategies.'
    },
    'specialized_referral': {
        'description': '''SPECIALIZED MENTAL HEALTH REFERRAL COORDINATION:
        
        User Message: {message}
        User Context: {user_context}
        Referral Needs: {referral_requirements}
        
        REFERRAL COORDINATION APPROACH:
        1. Assess need for specialized mental health services
        2. Consider cultural and accessibility factors
        3. Match with appropriate providers and programs
        4. Coordinate care transitions and communication
        5. Provide resources for accessing specialized care
        6. Plan for continued support during referral process
        
        Ensure seamless transitions to specialized care.
        Address barriers to accessing mental health services.''',
        'expected_output': 'Specialized referral plan with provider matching, care coordination, accessibility considerations, and transition support.'
    }
}