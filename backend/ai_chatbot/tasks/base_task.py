from crewai import Task

class BaseTask(Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)