from .base_agent import BaseAgent
from ..tools.assessment_tools import AssessmentTools
from ..tools.emotional_tools import EmotionalTools

class ProgressTrackerAgent(BaseAgent):
    def __init__(self, **kwargs):
        tools = [AssessmentTools(), EmotionalTools()]
        super().__init__(tools=tools, **kwargs)