from pydantic import BaseModel, field_validator, model_validator
from typing import Literal

from .registry import SPECIALIST_REGISTRY


class PlannerOutput(BaseModel):
    case_summary: str
    complexity: Literal["LOW", "MEDIUM", "HIGH"]
    selected_specialists: list[str]
    reasoning_tasks: list[str]
    routing_rationale: str
    requires_multi_specialist: bool

    @field_validator("selected_specialists")
    @classmethod
    def validate_specialists(cls, specialists):
        for specialist in specialists:
            if specialist not in SPECIALIST_REGISTRY:
                raise ValueError(
                    f"Invalid specialist selected: {specialist}"
                )
        return specialists

    @model_validator(mode="after")
    def validate_multi_specialist(self):
        expected = len(self.selected_specialists) > 1

        if self.requires_multi_specialist != expected:
            raise ValueError(
                "requires_multi_specialist must match "
                "the number of selected specialists"
            )

        return self