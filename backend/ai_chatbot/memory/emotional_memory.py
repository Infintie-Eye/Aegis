import json
import os
from datetime import datetime

class EmotionalMemory:
    def __init__(self, user_id):
        self.user_id = user_id
        self.file_path = f"memory/{user_id}_emotional_state.json"
        self.emotional_states = self.load_emotional_states()

    def load_emotional_states(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return []

    def save_emotional_states(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w') as f:
            json.dump(self.emotional_states, f)

    def update(self, emotional_state):
        emotional_state['timestamp'] = str(datetime.now())
        self.emotional_states.append(emotional_state)
        self.save_emotional_states()

    def get_recent_emotional_states(self, limit=10):
        return self.emotional_states[-limit:]