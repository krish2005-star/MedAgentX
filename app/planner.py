
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from .state import PlannerState
from .schemas import PlannerOutput
from .prompts import PLANNER_PROMPT

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=os.getenv("PLANNER_MODEL"),
    temperature=0
)

structured_llm = llm.with_structured_output(
    PlannerOutput,
    method="json_schema"
)


def planner_agent(state: PlannerState) -> PlannerState:
    patient_case = state["patient_case"]

    prompt = PLANNER_PROMPT.format(
        patient_case=patient_case
    )

    try:
        planner_output = structured_llm.invoke(prompt)
        state["planner_output"] = planner_output

    except Exception as e:
        state["planner_output"] = None
        state["errors"].append(
            f"Planner error: {str(e)}"
        )

    return state