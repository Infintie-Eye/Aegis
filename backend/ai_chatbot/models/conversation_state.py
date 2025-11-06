from pydantic import BaseModel

class ConversationState(BaseModel):
    user_id: str
    session_id: str
    current_topic: str
    conversation_history: list
    is_active: bool