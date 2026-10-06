import os

from langchain_google_genai import ChatGoogleGenerativeAI

from ..schemas import SpecialistOutput
from ..state import PlannerState
from ..prompts import PULMONOLOGY_PROMPT


MODEL_NAME = os.getenv("SPECIALIST_MODEL") or os.getenv("PLANNER_MODEL")

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0,
)

structured_llm = llm.with_structured_output(
    SpecialistOutput,
    method="json_schema",
)


def pulmonology_agent(state: PlannerState) -> dict:
    planner_output = state.get("planner_output")

    if planner_output is None:
        return {
            "errors": state["errors"] + [
                "Pulmonology skipped: Planner output is unavailable."
            ]
        }

    if "Pulmonology" not in planner_output.selected_specialists:
        return {}

    tasks = "\n".join(
        f"- {task}" for task in planner_output.reasoning_tasks
    )
    prompt = PULMONOLOGY_PROMPT.format(
        patient_case=state["patient_case"],
        case_summary=planner_output.case_summary,
        reasoning_tasks=tasks,
    )

    try:
        output = structured_llm.invoke(prompt)
        if output.specialist.lower() != "pulmonology":
            raise ValueError(
                f"Unexpected specialist name: {output.specialist}"
            )
        return {
            "specialist_outputs": {
                **state.get("specialist_outputs", {}),
                "Pulmonology": output,
            }
        }
    except Exception as exc:
        return {
            "errors": state["errors"] + [
                f"Pulmonology Agent error: {exc}"
            ]
        }