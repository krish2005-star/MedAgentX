
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from .state import PlannerState
from .schemas import PlannerOutput
from .prompts import PLANNER_PROMPT

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=os.getenv("PLANNER_MODEL"),
    timeout=60,
    max_retries=2,
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
        print("[PLANNER] Sending request to Gemini...")

        planner_output = structured_llm.invoke(prompt)

        print("[PLANNER] Gemini response received.")
        print("[PLANNER] Complexity:", planner_output.complexity)
        print(
            "[PLANNER] Selected specialists:",
            planner_output.selected_specialists
        )

        state["planner_output"] = planner_output

    except Exception as e:
        print("[PLANNER] Request failed:")
        print(type(e).__name__, str(e))

        state["planner_output"] = None
        state["errors"].append(
            f"Planner error: {type(e).__name__}: {str(e)}"
        )

    return state