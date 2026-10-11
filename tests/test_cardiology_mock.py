from unittest.mock import Mock, patch

from app.schemas import PlannerOutput, SpecialistOutput
from app.specialists.cardiology import cardiology_agent


def test_cardiology_runs_when_selected():

    planner = PlannerOutput(
        case_summary="Chest discomfort and shortness of breath.",
        complexity="MEDIUM",
        selected_specialists=["Cardiology"],
        reasoning_tasks=[
            "Assess cardiovascular causes."
        ],
        routing_rationale="Cardiac symptoms are present.",
        requires_multi_specialist=False,
    )

    fake = SpecialistOutput(
        specialist="Cardiology",
        assessment="Mock assessment.",
        possible_conditions=["Condition A"],
        supporting_findings=["Chest discomfort"],
        missing_information=["ECG and vital signs"],
        risk_level="UNCERTAIN",
        rationale="Mock rationale.",
        limitations=[
            "Mock only; not clinical advice."
        ],
    )

    state = {
        "patient_case": "A patient has chest discomfort.",
        "planner_output": planner,
        "specialist_outputs": {},
        "errors": [],
        "metadata": {},
    }

    mock_structured_llm = Mock()
    mock_structured_llm.invoke.return_value = fake

    with patch(
        "app.specialists.cardiology.structured_llm",
        mock_structured_llm,
    ):
        result = cardiology_agent(state)

    # Cardiology output should be produced
    assert "specialist_outputs" in result

    assert "Cardiology" in result["specialist_outputs"]

    assert (
        result["specialist_outputs"]["Cardiology"]
        == fake
    )

    # No error update should be returned
    assert "errors" not in result

    # Gemini should have been called exactly once
    mock_structured_llm.invoke.assert_called_once()


def test_cardiology_skips_when_not_selected():

    planner = PlannerOutput(
        case_summary="Cough and wheezing.",
        complexity="LOW",
        selected_specialists=["Pulmonology"],
        reasoning_tasks=[
            "Assess respiratory causes."
        ],
        routing_rationale="Respiratory symptoms.",
        requires_multi_specialist=False,
    )

    state = {
        "patient_case": "A patient has cough and wheezing.",
        "planner_output": planner,
        "specialist_outputs": {},
        "errors": [],
        "metadata": {},
    }

    mock_structured_llm = Mock()

    with patch(
        "app.specialists.cardiology.structured_llm",
        mock_structured_llm,
    ):
        result = cardiology_agent(state)

    # Agent should return no update because Cardiology
    # was not selected
    assert result == {}

    # Gemini must NOT be called
    mock_structured_llm.invoke.assert_not_called()