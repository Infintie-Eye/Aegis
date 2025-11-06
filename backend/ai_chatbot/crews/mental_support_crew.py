from crewai import Crew, Process
from ..agents.emotional_support_agent import EmotionalSupportAgent
from ..agents.progress_tracker_agent import ProgressTrackerAgent
from ..config.agent_config import agent_configs

class MentalSupportCrew(Crew):
    def __init__(self):
        agents = [
            EmotionalSupportAgent(**agent_configs['emotional_support_agent']),
            ProgressTrackerAgent(**agent_configs['progress_tracker_agent'])
        ]
        super().__init__(
            agents=agents,
            tasks=[],
            verbose=2,
            process=Process.sequential
        )