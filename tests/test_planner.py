import json
from pathlib import Path

from app.schemas import PlannerOutput


def load_test_cases():
    data_path = Path("data/sample_cases.json")

    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


def test_sample_cases():
    cases = load_test_cases()

    assert len(cases) == 3

    for case in cases:
        assert "id" in case
        assert "type" in case
        assert "patient_case" in case
        assert case["patient_case"]


if __name__ == "__main__":
    cases = load_test_cases()

    print(f"Loaded {len(cases)} test cases:\n")

    for case in cases:
        print(f"ID: {case['id']}")
        print(f"Type: {case['type']}")
        print(f"Case: {case['patient_case']}")
        print("-" * 60)

    print("\nAll sample cases loaded successfully.")