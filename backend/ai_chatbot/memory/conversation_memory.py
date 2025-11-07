import json
import os
from datetime import datetime

class ConversationMemory:
    def __init__(self, user_id):
        self.user_id = user_id
        self.file_path = f"memory/{user_id}_conversations.json"
        self.conversations = self.load_conversations()

    def load_conversations(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return []

    def save_conversations(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w') as f:
            json.dump(self.conversations, f)

    def add_message(self, message, is_response=False):
        self.conversations.append({
            'message': message,
            'is_response': is_response,
            'timestamp': str(datetime.now())
        })
        self.save_conversations()

    def get_conversation_history(self, limit=10):
        return self.conversations[-limit:]