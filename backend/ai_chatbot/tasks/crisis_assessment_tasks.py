from .base_task import BaseTask

class CrisisAssessmentTask(BaseTask):
    def __init__(self, **kwargs):
        description = "Assess the user's message for signs of crisis and provide immediate support."
        expected_output = "A crisis assessment report and immediate support message."
        super().__init__(description=description, expected_output=expected_output, **kwargs)