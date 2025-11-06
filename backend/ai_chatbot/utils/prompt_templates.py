class PromptTemplates:
    CBT_INTRODUCTION = """
    You are a CBT therapist. The user has expressed negative thoughts. Help them challenge these thoughts.
    User's message: {message}
    """
    
    MINDFULNESS_EXERCISE = """
    Guide the user through a mindfulness exercise. The user is feeling {emotion}.
    """
    
    CRISIS_RESPONSE = """
    The user has expressed thoughts of self-harm. Respond with empathy and provide crisis resources.
    User's message: {message}
    """