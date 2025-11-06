from pydantic import BaseModel

class UserContext(BaseModel):
    user_id: str
    current_emotional_state: dict
    recent_conversations: list
    preferences: dict
    demographics: dict  # age, gender, etc. (if available)

    def update(self, response, emotional_state):
        self.current_emotional_state = emotional_state
        # Update other context as needed