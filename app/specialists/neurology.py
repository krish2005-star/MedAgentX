import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from ..schemas import SpecialistOutput
from ..state import PlannerState
from ..prompts import NEUROLOGY_PROMPT

load_dotenv()
MODEL_NAME = os.getenv("SPECIALIST_MODEL") or os.getenv("PLANNER_MODEL")
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0, timeout=60)
structured_llm = llm.with_structured_output(SpecialistOutput, method="json_schema")

def neurology_agent(state: PlannerState) -> dict:
    planner_output = state.get("planner_output")
    if planner_output is None:
        return {"errors": state.get("errors", []) + [
            "Neurology skipped: Planner output is unavailable."
        ]}
    if "Neurology" not in planner_output.selected_specialists:
        return {}

    prompt = NEUROLOGY_PROMPT.format(
        patient_case=state["patient_case"],
        case_summary=planner_output.case_summary,
        reasoning_tasks="; ".join(planner_output.reasoning_tasks),
        routing_rationale=planner_output.routing_rationale,
    )
    try:
        output = structured_llm.invoke(prompt)
        accepted = ("neurology", "neurology specialist")
        if output.specialist.strip().lower() not in accepted:
            raise ValueError(f"Unexpected specialist name: {output.specialist}")
        output.specialist = "Neurology"
        return {"specialist_outputs": {
            **state.get("specialist_outputs", {}),
            "Neurology": output,
        }}
    except Exception as exc:
        return {"errors": state.get("errors", []) + [
            f"Neurology Agent error: {exc}"
        ]}
