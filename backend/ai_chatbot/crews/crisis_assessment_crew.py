from crewai import Crew, Process
from ..agents.crisis_detection_agent import CrisisDetectionAgent
from ..agents.emotional_support_agent import EmotionalSupportAgent
from ..config.agent_config import agent_configs

class CrisisAssessmentCrew(Crew):
    def __init__(self):
        agents = [
            CrisisDetectionAgent(**agent_configs['crisis_detection_agent']),
            EmotionalSupportAgent(**agent_configs['emotional_support_agent'])
        ]
        super().__init__(
            agents=agents,
            tasks=[],  # Tasks will be added when running
            verbose=2,
            process=Process.sequential
        )