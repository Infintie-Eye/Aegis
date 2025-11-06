import json
import os

class UserPreferences:
    def __init__(self, user_id):
        self.user_id = user_id
        self.file_path = f"memory/{user_id}_preferences.json"
        self.preferences = self.load_preferences()

    def load_preferences(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {
            'preferred_interventions': [],
            'avoided_topics': [],
            'communication_style': 'empathetic'
        }

    def save_preferences(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w') as f:
            json.dump(self.preferences, f)

    def update_from_interaction(self, response, emotional_state):
        # Update preferences based on the interaction
        # This is a placeholder for more complex logic
        pass