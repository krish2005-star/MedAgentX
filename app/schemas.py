from typing import Literal
from pydantic import BaseModel, Field, field_validator, model_validator

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


class SpecialistOutput(BaseModel):
    specialist: str
    assessment: str
    possible_conditions: list[str] = Field(default_factory=list)
    supporting_findings: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    risk_level: Literal["LOW", "MODERATE", "HIGH", "UNCERTAIN"]
    rationale: str
    limitations: list[str] = Field(default_factory=list)