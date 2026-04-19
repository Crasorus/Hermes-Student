# Run Hermes Workflow

Execute a Hermes clinical supply chain workflow directly from the chat window.

## Arguments

The user provides: `$ARGUMENTS`

Parse the arguments as: `<workflow_id> <study_id> [data_drop_date]`

- **workflow_id** (required): e.g. WF-01, WF-02, WF-03, WF-04, WF-05
- **study_id** (required): the protocol number, e.g. PULSE-01 or 105321 — must match the folder name and `protocol_number` in study_config.json
- **data_drop_date** (optional): YYYY-MM-DD format. If omitted, use the most recent dated folder in `studies/<study_id>/data_drops/`.

If arguments are missing or invalid, ask the user for them. Do not guess.

---

## Procedure

Follow these steps exactly, in order. Do not skip steps.

### Step 1: Load workflow definition

Read `workflows/workflows.json`. Extract:
- The workflow entry matching the requested workflow_id
- The `routing_signals` list
- The `steps` array for this workflow

If the workflow_id is not found, tell the user which workflows are available and stop.

### Step 2: Validate study package

Check that these files exist:
- `studies/<study_id>/config/study_config.json`
- `studies/<study_id>/config/supply_network.json`
- `studies/<study_id>/config/policies.json`
- `studies/<study_id>/data_drops/<data_drop_date>/rtsm_actuals.csv`
- `studies/<study_id>/data_drops/<data_drop_date>/erp_inventory.csv`
- `studies/<study_id>/data_drops/<data_drop_date>/ctms_plan.csv`

After reading study_config.json, verify that `study_identity.protocol_number` equals `<study_id>`. If not, stop immediately with:
```
ERROR: Study package mismatch.
  study_id argument:          <study_id>
  protocol_number in config:  <value from file>
  These must match. Aborting to prevent wrong study data being used.
```

If any files are missing, report which files are missing and stop.

Print a confirmation:
```
Hermes Workflow Runner (Chat Mode)
===================================
Workflow:   <workflow_id> — <workflow name>
Study:      <study_id>
Data drop:  <data_drop_date>
Steps:      <N>
```

### Step 3: Read configuration files

Read these files into your context — you will need them for agent execution:
- `studies/<study_id>/config/study_config.json`
- `studies/<study_id>/config/supply_network.json`
- `studies/<study_id>/config/policies.json`

### Step 4: Execute workflow steps

Initialise an empty list of **active_signals** (routing signals detected so far).

For each step in the workflow, in order:

#### 4a. Check conditions

If the step has a `"condition"` with `"requires_signal"`, check whether that signal is in **active_signals**. If not, print:

```
## Step N/T: <agent_name> — SKIPPED
Signal <signal_name> not detected. This step is not required.
```

Then move to the next step.

#### 4b. Load agent persona

Read the agent's system prompt from `agents/<agent_name>/system_prompt.md`. This tells you:
- Who you are for this step (identity, role, expertise)
- What skills and procedures to follow
- What output format to use
- What halt conditions to watch for

#### 4c. Read data files

Read the data drop CSV files that are relevant to this agent's task:
- `studies/<study_id>/data_drops/<data_drop_date>/rtsm_actuals.csv`
- `studies/<study_id>/data_drops/<data_drop_date>/erp_inventory.csv`
- `studies/<study_id>/data_drops/<data_drop_date>/ctms_plan.csv`

Read reference files if the agent's task requires them (e.g. shelf life, label requirements, approved vendors).

#### 4d. Execute the task

Adopt the agent's persona and execute the task description from workflows.json. Follow the agent's skills and procedures as described in their system prompt. Use the actual data from the files you read.

Produce a **concise** output — key findings, decisions, numbers, and signals. Not verbose prose. Structure it as:

```
## Step N/T: <agent_name>
**Task:** <task description from workflows.json>
**Findings:**
- <key finding 1>
- <key finding 2>
- ...
**Signals:** <any routing signals emitted, or "None">
**Status:** Complete
```

#### 4e. Detect routing signals

After producing output, check whether your output contains any of the keywords from the `routing_signals` list in workflows.json. Add any detected signals to **active_signals**.

#### 4f. Check for HALT

If HALT is in **active_signals**, print:

```
HALT signalled by <agent_name>. Workflow stopped.
```

Stop executing further steps.

#### 4g. Carry context forward

Your output from this step is now available as context for subsequent agent steps. Prior agent outputs accumulate naturally in the conversation — you do not need to do anything special here.

### Step 5: Workflow complete

After all steps have executed (or a HALT occurred), print a summary:

```
===================================
Workflow complete: <workflow_id> — <workflow name>
Steps executed: <count>
Steps skipped: <count>
Signals detected: <list of all active_signals, or "None">
===================================
```

Then ask: **"Would you like me to save the outputs to `studies/<study_id>/outputs/`?"**

If the user says yes:
- Create folder `studies/<study_id>/outputs/<data_drop_date>/` if it doesn't exist
- Write a `<workflow_id>_run_summary.md` file containing the final agent's output
- Write a `<workflow_id>_outputs.json` file containing all agent outputs as a JSON array
- Confirm the file paths to the user

If the user says no, end the conversation.

---

## Rules

- Execute ALL steps autonomously. Do not pause between agents to ask the user for confirmation.
- Keep each agent's output concise: key findings, numbers, decisions, and signals. Not full reports.
- When reading CSV files, parse the actual data. Do not summarise file contents — calculate real numbers.
- Respect conditional steps strictly. If the required signal was not emitted, skip the step.
- HALT is a hard stop. No further steps execute after HALT.
- Do not invent data. If a file is empty or data is missing, report that fact.
- Each agent step should reference the prior agents' findings when relevant.
