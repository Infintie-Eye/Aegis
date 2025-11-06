from .base_task import BaseTask

class ProgressAnalysisTask(BaseTask):
    def __init__(self, **kwargs):
        description = "Analyze the user's progress over time and provide insights."
        expected_output = "A progress analysis report."
        super().__init__(description=description, expected_output=expected_output, **kwargs)