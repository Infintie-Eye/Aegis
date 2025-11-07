from .base_agent import BaseAgent
from ..tools.emotional_tools import EmotionalTools

class EmotionalSupportAgent(BaseAgent):
    def __init__(self, **kwargs):
        tools = [EmotionalTools()]
        super().__init__(tools=tools, **kwargs)