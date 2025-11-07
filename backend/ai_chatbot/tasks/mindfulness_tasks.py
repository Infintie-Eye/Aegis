from .base_task import BaseTask

class MindfulnessTask(BaseTask):
    def __init__(self, **kwargs):
        description = "Guide the user through a mindfulness exercise."
        expected_output = "A guided mindfulness exercise script."
        super().__init__(description=description, expected_output=expected_output, **kwargs)