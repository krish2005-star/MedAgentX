
import json
from pathlib import Path

from langgraph.graph import StateGraph, START, END
from .state import PlannerState
from .planner import planner_agent


# Build the LangGraph
builder = StateGraph(PlannerState)
builder.add_node("planner_agent", planner_agent)
builder.add_edge(START, "planner_agent")
builder.add_edge("planner_agent", END)

graph = builder.compile()


def run_planner(patient_case: str):
    initial_state: PlannerState = {
        "patient_case": patient_case,
        "planner_output": None,
        "errors": [],
        "metadata": {}
    }

    return graph.invoke(initial_state)


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parent.parent / "data" / "sample_cases.json"

    with open(data_path, "r", encoding="utf-8") as file:
        test_cases = json.load(file)

    for case in test_cases:
        print("\n" + "=" * 60)
        print(f"TEST CASE: {case['id']} ({case['type']})")
        print("=" * 60)

        print("\nPatient Case:")
        print(case["patient_case"])

        result = run_planner(case["patient_case"])

        if result["planner_output"] is not None:
            output = result["planner_output"]

            print("\nPlanner Output:")
            print("-" * 60)
            print(f"Summary: {output.case_summary}")
            print(f"Complexity: {output.complexity}")
            print(f"Specialists: {output.selected_specialists}")
            print(f"Tasks: {output.reasoning_tasks}")
            print(f"Rationale: {output.routing_rationale}")
            print(
                "Multi-specialist:",
                output.requires_multi_specialist
            )
        else:
            print("\nPlanner failed to produce an output.")

        if result["errors"]:
            print("\nErrors:")
            for error in result["errors"]:
                print(error)

    print("\nAll test cases processed.")