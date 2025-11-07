from .base_agent import BaseAgent
from ..tools.assessment_tools import AssessmentTools

class CrisisDetectionAgent(BaseAgent):
    def __init__(self, **kwargs):
        tools = [AssessmentTools()]
        super().__init__(tools=tools, **kwargs)