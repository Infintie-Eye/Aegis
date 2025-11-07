from .base_task import BaseTask

class CBTInterventionTask(BaseTask):
    def __init__(self, **kwargs):
        description = "Provide a CBT-based intervention for the user's negative thought patterns."
        expected_output = "A structured CBT intervention plan."
        super().__init__(description=description, expected_output=expected_output, **kwargs)