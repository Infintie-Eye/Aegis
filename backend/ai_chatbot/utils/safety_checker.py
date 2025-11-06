class SafetyChecker:
    def __init__(self):
        self.crisis_keywords = ['suicide', 'kill myself', 'end it all', 'hopeless', 'worthless', 'self-harm']
        self.harmful_keywords = ['hate', 'violence', 'abuse']

    def check(self, message):
        crisis_detected = any(keyword in message.lower() for keyword in self.crisis_keywords)
        harmful_content = any(keyword in message.lower() for keyword in self.harmful_keywords)
        
        return {
            'crisis_detected': crisis_detected,
            'harmful_content': harmful_content,
            'safe': not (crisis_detected or harmful_content)
        }