from pydantic import BaseModel

class EmotionalState(BaseModel):
    user_id: str
    emotion: str
    intensity: float  # 0.0 to 1.0
    timestamp: str
    crisis: bool = False