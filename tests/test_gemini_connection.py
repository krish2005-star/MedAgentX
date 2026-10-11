from app.planner import planner_agent


def test_gemini_planner_only():

    state = {
        "patient_case": "A patient has cough and fever.",
        "planner_output": None,
        "specialist_outputs": {},
        "errors": [],
        "metadata": {},
    }

    print("\nCalling Planner/Gemini...")

    result = planner_agent(state)

    print("\nPlanner finished.")

    print("Output:", result["planner_output"])
    print("Errors:", result["errors"])

    assert result["planner_output"] is not None