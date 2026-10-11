# MedAgentX -- Development Process & Command Reference

> Documentation of the work completed so far: Gemini setup,
> Planner/Router, Pulmonology, Cardiology, testing, and Git/GitHub
> workflow.

## 1. Project Overview

**MedAgentX** is an Agentic AI Clinical Decision Support (CDS) project.

The current implementation focuses on:

-   Patient case input
-   Planner/Router Agent
-   Dynamic specialist selection
-   Role-specific Specialist Agents
-   Structured outputs using Pydantic
-   Gemini as the LLM backend
-   Unit/mock testing
-   Live Gemini integration testing
-   Git/GitHub feature-branch workflow

Current flow:

``` text
Patient Case
     ↓
Planner / Router Agent
     ↓
Selected Specialist(s)
     ↓
Specialist Agent(s)
     ↓
Structured Specialist Output
```

------------------------------------------------------------------------

## 2. Development Process Completed So Far

### Step 1 -- Project environment

Project location:

``` text
D:\MedAgentX
```

Virtual environment:

``` text
D:\MedAgentX\venv
```

The project is developed in Python using a virtual environment.

### Step 2 -- Gemini API setup

The project was moved to Gemini as the LLM backend.

The `.env` configuration follows this structure:

``` text
GOOGLE_API_KEY=<your Gemini API key>
PLANNER_MODEL=gemini-3.8-flash
SPECIALIST_MODEL=gemini-3.8-flash
```

**Important:** Never commit the real API key to GitHub. Keep `.env` in
`.gitignore`.

### Step 3 -- Planner / Router Agent

The Planner receives a patient case and determines:

-   Case summary
-   Complexity: `LOW`, `MEDIUM`, or `HIGH`
-   Relevant specialist agents
-   Reasoning tasks
-   Routing rationale
-   Whether multiple specialists are required

The Planner uses structured output through `PlannerOutput`.

Example:

``` text
Patient Case
    ↓
Planner
    ↓
Complexity: MEDIUM
Selected Specialists:
    - Cardiology
    - Neurology
```

### Step 4 -- Planner output validation

Pydantic validation was added so that:

-   Only registered specialists can be selected.
-   `requires_multi_specialist` matches the number of selected
    specialists.
-   The Planner returns a predictable structured object.

### Step 5 -- Pulmonology Specialist Agent

The first specialist integration was Pulmonology.

The flow was tested successfully:

``` text
Patient Case
    ↓
Planner
    ↓
Pulmonology
    ↓
SpecialistOutput
```

A simple respiratory case was successfully processed using Gemini.

### Step 6 -- Git/GitHub workflow

Development was organized using feature branches instead of developing
directly on `main`.

General workflow:

``` text
main
  ↓
feature branch
  ↓
implement
  ↓
test
  ↓
commit
  ↓
push
  ↓
Pull Request
  ↓
review
  ↓
merge
  ↓
main
```

The Pulmonology feature branch was pushed and successfully merged
through a Pull Request.

### Step 7 -- Cardiology Specialist Agent

Cardiology was added using the same specialist-agent pattern.

The Cardiology Agent:

1.  Reads Planner output.
2.  Checks whether Cardiology was selected.
3.  Builds a Cardiology-specific prompt.
4.  Calls the structured Gemini model.
5.  Validates the returned specialist name.
6.  Stores the result in:

``` python
state["specialist_outputs"]["Cardiology"]
```

### Step 8 -- Cardiology mock testing

Mock testing was added so Cardiology could be tested without calling
Gemini.

The tests cover:

1.  Cardiology is selected → agent runs.
2.  Cardiology is not selected → agent skips.

There was an initial mocking issue because `structured_llm.invoke` was
patched directly. The solution was to patch the complete
`structured_llm` object with `unittest.mock.Mock`.

Final result:

``` text
2 passed
```

### Step 9 -- Cardiology live integration test

A live test was created for:

``` text
Planner → Cardiology → Gemini
```

Test case:

``` text
A 62-year-old patient has chest discomfort,
shortness of breath, dizziness, and occasional
left-arm numbness.
```

The Planner successfully produced:

``` text
Complexity: MEDIUM
Selected Specialists: ['Cardiology', 'Neurology']
```

This confirms that the Planner can dynamically identify more than one
relevant specialty.

The Cardiology Gemini request then returned:

``` text
503 UNAVAILABLE
This model is currently experiencing high demand.
```

This is a temporary model/service availability issue. The Planner and
Cardiology routing logic were reached successfully.

------------------------------------------------------------------------

# 3. Commands Used and What They Are For

## Activate virtual environment

``` powershell
.\venv\Scripts\Activate.ps1
```

**Purpose:** Activates the project's Python virtual environment in
PowerShell.

------------------------------------------------------------------------

## Check Git status

``` powershell
git status
```

**Purpose:** Shows the current branch, modified files, staged files, and
untracked files.

------------------------------------------------------------------------

## Switch to main

``` powershell
git switch main
```

**Purpose:** Moves to the `main` branch.

If uncommitted changes would be overwritten, Git will prevent the
switch.

------------------------------------------------------------------------

## Update local main

``` powershell
git pull origin main
```

**Purpose:** Downloads and integrates the latest changes from the GitHub
`main` branch.

------------------------------------------------------------------------

## Create a feature branch

``` powershell
git switch -c feature/cardiology-specialist
```

**Purpose:** Creates and switches to a new branch for Cardiology
development.

General form:

``` powershell
git switch -c feature/<feature-name>
```

------------------------------------------------------------------------

## Stage changes

``` powershell
git add .
```

**Purpose:** Stages changed/new files for the next commit.

Do not stage `.env` or API keys.

------------------------------------------------------------------------

## Commit changes

``` powershell
git commit -m "Add Cardiology specialist"
```

**Purpose:** Saves the staged changes as a Git commit.

------------------------------------------------------------------------

## Push a feature branch for the first time

``` powershell
git push -u origin feature/cardiology-specialist
```

**Purpose:** Pushes the feature branch to GitHub and establishes its
upstream branch.

After the upstream is configured, normal pushes can usually use:

``` powershell
git push
```

------------------------------------------------------------------------

## Stash local changes

``` powershell
git stash push -m "local changes before switching branches"
```

**Purpose:** Temporarily stores uncommitted changes so you can safely
switch branches.

This was relevant when local Pulmonology changes prevented switching to
`main`.

------------------------------------------------------------------------

# 4. Testing Commands

## Run the complete pytest suite

``` powershell
python -m pytest -v
```

**Purpose:** Runs all discovered tests with verbose output.

------------------------------------------------------------------------

## Run Cardiology mock tests

``` powershell
python -m pytest tests/test_cardiology_mock.py -v
```

**Purpose:** Tests Cardiology without calling Gemini.

Current result:

``` text
2 passed
```

These tests verify:

``` text
Cardiology selected
    → Cardiology runs

Cardiology not selected
    → Cardiology skips
```

------------------------------------------------------------------------

## Run Cardiology live Gemini test

``` powershell
python -m pytest tests/test_cardiology_live.py -v -s
```

**Purpose:** Runs the Planner and then the Cardiology Agent using the
real Gemini API.

The `-s` option displays the `print()` output from the test.

Current live-test behavior:

``` text
Planner
  ↓
MEDIUM complexity
  ↓
Cardiology + Neurology selected
  ↓
Cardiology Agent
  ↓
Gemini
  ↓
503 UNAVAILABLE
```

The `503` indicates temporary model high demand, not a Python assertion
or Cardiology routing problem.

------------------------------------------------------------------------

# 5. Current Test Status

  -----------------------------------------------------------------------
  Test                    Status                  What it proves
  ----------------------- ----------------------- -----------------------
  Cardiology selected --  PASS                    Cardiology executes and
  mock                                            stores structured
                                                  output

  Cardiology not selected PASS                    Cardiology correctly
  -- mock                                         skips

  Planner → Cardiology -- Temporarily blocked by  Planner routing
  live                    503                     succeeded; Gemini
                                                  Cardiology request hit
                                                  model availability
                                                  issue
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 6. Current Architecture

``` text
                    Patient Case
                         │
                         ▼
                ┌─────────────────┐
                │ Planner / Router │
                └────────┬────────┘
                         │
              Selected Specialists
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        Cardiology             Neurology
        Specialist             Specialist
              │
              ▼
       SpecialistOutput
```

Current implemented specialist agents include:

-   Pulmonology
-   Cardiology

Neurology has been identified by the Planner in the current test case
but is not yet part of the completed specialist implementation.

------------------------------------------------------------------------

# 7. Important LangGraph State Behavior

Specialist nodes can return **partial state updates** rather than the
entire state.

For example, Cardiology may return:

``` python
{
    "specialist_outputs": {
        "Cardiology": output
    }
}
```

It does not necessarily return:

``` python
{
    "patient_case": ...,
    "planner_output": ...,
    "specialist_outputs": ...,
    "errors": ...,
    "metadata": ...
}
```

Therefore, tests should check for keys that the node is expected to
update instead of assuming the returned dictionary is the complete
state.

------------------------------------------------------------------------

# 8. What Has Been Completed

-   [x] Python virtual environment
-   [x] Gemini API configuration
-   [x] Planner / Router Agent
-   [x] Planner structured output
-   [x] Specialist registry validation
-   [x] Pulmonology Specialist Agent
-   [x] Pulmonology live testing
-   [x] GitHub feature-branch workflow
-   [x] Pulmonology Pull Request and merge
-   [x] Cardiology Specialist Agent
-   [x] Cardiology mock tests
-   [x] Cardiology Planner routing test
-   [ ] Successful Cardiology live Gemini response
-   [ ] Neurology Specialist Agent
-   [ ] Dynamic execution of all selected specialists
-   [ ] RAG evidence retrieval
-   [ ] Medical Knowledge Graph
-   [ ] Consensus Agent
-   [ ] Critic / verification Agent
-   [ ] Final CDS report generation
-   [ ] Complete end-to-end evaluation

------------------------------------------------------------------------

# 9. Recommended Next Steps

### Immediate

Retry:

``` powershell
python -m pytest tests/test_cardiology_live.py -v -s
```

after the Gemini 503 issue clears.

### Next implementation milestone

Implement dynamic multi-specialist execution:

``` text
Patient Case
     ↓
Planner
     ↓
Cardiology + Neurology
     ↓
┌─────────────┬─────────────┐
│ Cardiology  │  Neurology  │
└──────┬──────┴──────┬──────┘
       │             │
       └──────┬──────┘
              ▼
      specialist_outputs
```

After that, the project can move toward:

``` text
Specialists
    ↓
RAG + Medical Evidence
    ↓
Knowledge Graph
    ↓
Consensus
    ↓
Critic / Verification
    ↓
CDS Report
```

------------------------------------------------------------------------

# 10. Quick Command Reference

``` powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Check Git state
git status

# Update main
git switch main
git pull origin main

# Create feature branch
git switch -c feature/<feature-name>

# Run all tests
python -m pytest -v

# Cardiology mock tests
python -m pytest tests/test_cardiology_mock.py -v

# Cardiology live Gemini test
python -m pytest tests/test_cardiology_live.py -v -s

# Stage
git add .

# Commit
git commit -m "<message>"

# First push of a feature branch
git push -u origin feature/<feature-name>

# Later pushes
git push
```

------------------------------------------------------------------------

## 11. Important Notes

-   Never expose or commit the Gemini API key.
-   Keep `.env` in `.gitignore`.
-   Mock tests are preferable for repeated local unit testing because
    they do not consume Gemini requests.
-   Live tests consume Gemini API requests and may encounter quotas,
    rate limits, 503 availability errors, or temporary model demand.
-   A Gemini `503 UNAVAILABLE` is different from an application-code
    failure.
-   MedAgentX is a Clinical Decision Support research/software project;
    outputs should not be treated as medical diagnosis or treatment
    advice.
