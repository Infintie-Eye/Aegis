import uuid
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.now()
        self.last_activity = self.start_time

    def update_activity(self):
        self.last_activity = datetime.now()

    def is_session_expired(self, timeout_minutes=30):
        return datetime.now() - self.last_activity > timedelta(minutes=timeout_minutes)

    def end_session(self):
        # Perform any cleanup or save session data
        pass