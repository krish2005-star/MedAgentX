from typing import TypedDict, Optional
from .schemas import PlannerOutput


class PlannerState(TypedDict):
    patient_case: str
    planner_output: Optional[PlannerOutput]
    errors: list[str]
    metadata: dict