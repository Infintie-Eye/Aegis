from crewai import Crew, Process
from ..agents.cbt_therapist_agent import CBTTherapistAgent
from ..agents.mindfulness_coach_agent import MindfulnessCoachAgent
from ..config.agent_config import agent_configs

class InterventionCrew(Crew):
    def __init__(self):
        agents = [
            CBTTherapistAgent(**agent_configs['cbt_therapist_agent']),
            MindfulnessCoachAgent(**agent_configs['mindfulness_coach_agent'])
        ]
        super().__init__(
            agents=agents,
            tasks=[],
            verbose=2,
            process=Process.sequential
        )