from app.planner import planner_agent
from app.specialists.cardiology import cardiology_agent


def test_cardiology_live():

    state = {
        "patient_case": (
            "A 62-year-old patient has chest discomfort, "
            "shortness of breath, dizziness, and occasional "
            "left-arm numbness."
        ),
        "planner_output": None,
        "specialist_outputs": {},
        "errors": [],
        "metadata": {},
    }

    # Step 1: Run Planner
    state = planner_agent(state)

    print("\n--- PLANNER OUTPUT ---")

    assert state["planner_output"] is not None

    planner_output = state["planner_output"]

    print("Case Summary:", planner_output.case_summary)
    print("Complexity:", planner_output.complexity)
    print("Selected Specialists:", planner_output.selected_specialists)
    print("Reasoning Tasks:", planner_output.reasoning_tasks)
    print("Routing Rationale:", planner_output.routing_rationale)

    # Cardiology should be selected for this case
    assert "Cardiology" in planner_output.selected_specialists

    # Step 2: Run Cardiology Agent
    result = cardiology_agent(state)

    print("\n--- CARDIOLOGY OUTPUT ---")

    assert "specialist_outputs" in result
    assert "Cardiology" in result["specialist_outputs"]

    cardiology_output = result["specialist_outputs"]["Cardiology"]

    print("Specialist:", cardiology_output.specialist)
    print("Assessment:", cardiology_output.assessment)
    print("Possible Conditions:", cardiology_output.possible_conditions)
    print("Supporting Findings:", cardiology_output.supporting_findings)
    print("Missing Information:", cardiology_output.missing_information)
    print("Risk Level:", cardiology_output.risk_level)
    print("Rationale:", cardiology_output.rationale)
    print("Limitations:", cardiology_output.limitations)

    assert cardiology_output.specialist == "Cardiology"