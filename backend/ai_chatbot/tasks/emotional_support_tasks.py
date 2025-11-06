from .base_task import BaseTask

class EmotionalSupportTask(BaseTask):
    def __init__(self, **kwargs):
        description = "Provide emotional support and validation to the user."
        expected_output = "An empathetic and supportive response."
        super().__init__(description=description, expected_output=expected_output, **kwargs)