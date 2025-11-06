from crewai import Agent

class BaseAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Additional initialization if needed