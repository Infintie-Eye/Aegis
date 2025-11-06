from pydantic import BaseModel

class InterventionPlan(BaseModel):
    user_id: str
    intervention_type: str
    description: str
    steps: list
    expected_outcome: str