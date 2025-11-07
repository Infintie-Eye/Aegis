from .base_agent import BaseAgent
from ..tools.therapeutic_tools import TherapeuticTools

class CBTTherapistAgent(BaseAgent):
    def __init__(self, **kwargs):
        tools = [TherapeuticTools()]
        super().__init__(tools=tools, **kwargs)