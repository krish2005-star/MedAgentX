from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from app.schemas import PlannerOutput
from app.prompts import PLANNER_PROMPT
import json
import os
import traceback

load_dotenv()

with open("data/sample_cases.json", "r", encoding="utf-8") as f:
    cases = json.load(f)

print("Available cases:", [case.get("case_id") for case in cases])

patient_case = cases[0]

prompt = PLANNER_PROMPT.format(
    patient_case=json.dumps(patient_case, ensure_ascii=False)
)

llm = ChatGoogleGenerativeAI(
    model=os.getenv("PLANNER_MODEL"),
    temperature=0,
    timeout=60,
    max_retries=0,
)

structured_llm = llm.with_structured_output(
    PlannerOutput,
    method="json_schema",
)

try:
    print("\nTesting full planner prompt...")
    result = structured_llm.invoke(prompt)

    print("\nSUCCESS")
    print(result.model_dump_json(indent=2))

except Exception as e:
    print("\nFAILED")
    print(type(e).__name__, str(e))
    traceback.print_exc()