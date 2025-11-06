from crewai import Crew, Process
from ..agents.progress_tracker_agent import ProgressTrackerAgent
from ..agents.cbt_therapist_agent import CBTTherapistAgent
from ..config.agent_config import agent_configs

class ProgressReviewCrew(Crew):
    def __init__(self):
        agents = [
            ProgressTrackerAgent(**agent_configs['progress_tracker_agent']),
            CBTTherapistAgent(**agent_configs['cbt_therapist_agent'])
        ]
        super().__init__(
            agents=agents,
            tasks=[],
            verbose=2,
            process=Process.sequential
        )