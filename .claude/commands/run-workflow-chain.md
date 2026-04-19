# Run Hermes Workflow Chain

Execute multiple Hermes clinical supply chain workflows sequentially in a single session, with context and findings flowing between steps.

## Arguments

The user provides: `$ARGUMENTS`

Parse the arguments as: `<study_id> <workflow_id_1> [workflow_id_2] ... [data_drop_date]`

- **study_id** (required): the protocol number, e.g. PULSE-01 or 105321 — must match the folder name and `protocol_number` in study_config.json
- **workflow_id_N** (required, 1 or more): e.g. WF-01, WF-02, WF-03, WF-04, WF-05
- **data_drop_date** (optional): YYYY-MM-DD format. If omitted, use the most recent dated folder in `studies/<study_id>/data_drops/`. Must be the last argument if provided.

All workflows in the chain use the same study package and data drop.

If arguments are missing or invalid, ask the user for them. Do not guess.

## Usage Examples

/run-workflow-chain PULSE-01 WF-01 WF-02 WF-05
/run-workflow-chain PULSE-01 WF-01 WF-02 WF-05 2026-03-10
/run-workflow-chain PULSE-01 WF-03 WF-02 # Amendment impact
/run-workflow-chain PULSE-01 WF-04 # Monitoring alone
/run-workflow-chain 244087 WF-01 WF-02 WF-05 2026-03-09d

---

## Procedure

Follow these steps exactly, in order. Do not skip steps.

### Step 1: Parse and validate arguments

Extract study_id, workflow IDs, and data_drop_date from the user's input.

If data_drop_date is not provided, list the folders in `studies/<study_id>/data_drops/` and use the most recent by date. inform the user of this decision.

If any workflow_id is not in the valid list (WF-01, WF-02, WF-03, WF-04, WF-05), tell the user which workflows are available and ask them to correct the input. Do not continue.

### Step 2: Load workflow definitions

Read `workflows/workflows.json` once. Extract:

- The `routing_signals` list (global)
- The `steps` array for each requested workflow_id

Print a chain confirmation:

```
Hermes Workflow Chain Runner (Chat Mode)
=========================================
Study:       <study_id>
Data drop:   <data_drop_date>
Chain:       <workflow_id_1> → <workflow_id_2> → ...
Total steps: <sum of steps across all workflows>
```

### Step 3: Validate study package

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

### Step 4: Read configuration files once

Read these files into your context — you will need them for all agent executions:

- `studies/<study_id>/config/study_config.json`
- `studies/<study_id>/config/supply_network.json`
- `studies/<study_id>/config/policies.json`

run di_12_aggregate_data_query.py to be absolutely sure you are working with the correct data.
Do not guess or make data up. Do not skip this step.

### Step 5: Execute workflow chain

Initialize:

- **active_signals** = empty list (shared across ALL workflows in the chain)
- **workflow_index** = 0
- **halt_triggered** = false

For each workflow in the chain (in order):

#### 5a. Skip if HALT was triggered

If halt_triggered is true, print:

```
Workflow chain halted. Remaining workflows skipped.
```

Stop executing further workflows.

#### 5b. Execute workflow steps

For each step in this workflow, in order:

##### 5b-i. Check conditions

If the step has a `"condition"` with `"requires_signal"`, check whether that signal is in **active_signals**. If not, print:

```
## <workflow_id> Step N/M: <agent_name> — SKIPPED
Signal <signal_name> not detected. This step is not required.
```

Then move to the next step.

##### 5b-ii. Load agent persona

Read the agent's system prompt from `agents/<agent_name>/system_prompt.md`. This tells you:

- Who you are for this step (identity, role, expertise)
- What skills and procedures to follow
- What output format to use
- What halt conditions to watch for

##### 5b-iii. Read data files

Read the data drop CSV files that are relevant to this agent's task:

- `studies/<study_id>/data_drops/<data_drop_date>/rtsm_actuals.csv`
- `studies/<study_id>/data_drops/<data_drop_date>/erp_inventory.csv`
- `studies/<study_id>/data_drops/<data_drop_date>/ctms_plan.csv`

Read reference files if the agent's task requires them (e.g. shelf life, label requirements, approved vendors).

##### 5b-iv. Execute the task

Adopt the agent's persona and execute the task description from workflows.json. Follow the agent's skills and procedures as described in their system prompt. Use the actual data from the files you read.

**Important**: Reference prior workflow outputs and active_signals when relevant. Each workflow is aware of what previous workflows discovered.

Produce a **concise** output — key findings, decisions, numbers, and signals. Not verbose prose. Structure it as:

```
## <workflow_id> Step N/M: <agent_name>
**Task:** <task description from workflows.json>
**Findings:**
- <key finding 1>
- <key finding 2>
- ...
**Signals:** <any routing signals emitted, or "None">
**Status:** Complete
```

##### 5b-v. Detect routing signals

After producing output, check whether your output contains any of the keywords from the `routing_signals` list in workflows.json. Add any detected signals to **active_signals**.

##### 5b-vi. Check for HALT

If HALT is in **active_signals**, print:

```
HALT signalled by <agent_name>. Workflow chain stopping.
```

Set halt_triggered = true. Do not execute further steps in this workflow or any subsequent workflows.

##### 5b-vii. Carry context forward

Your output from this step is now available as context for:

- Subsequent steps in the same workflow
- Subsequent workflows in the chain

Prior agent outputs accumulate naturally in the conversation — you do not need to do anything special here.

#### 5c. Workflow complete marker

After all steps in a workflow have executed (or a HALT occurred), print a workflow separator:

```
=========================================
<workflow_id> — <workflow_name>: Complete
Active signals: <list of all active_signals, or "None">
=========================================
```

### Step 6: Chain complete summary

After all workflows in the chain have executed (or a HALT occurred), print a final summary:

```
===================================
Workflow chain complete
Study:            <study_id>
Data drop:        <data_drop_date>
Chain executed:   <list of executed workflows>
Workflows halted: <list of workflows not executed, if any>
Total steps run:  <count>
Total steps skipped: <count>
Final signals:    <list of all active_signals, or "None">
===================================
```

Then ask: **"Would you like me to save the outputs to `studies/<study_id>/outputs/`?"**

If the user says yes:

- Create folder `studies/<study_id>/outputs/<data_drop_date>/` if it doesn't exist
- Write a `chain_<workflow_1>_<workflow_2>_..._run_summary.md` file containing all agent outputs (in order)
- Write a `chain_<workflow_1>_<workflow_2>_..._outputs.json` file containing all agent outputs as a structured JSON array with workflow_id and step metadata
- Confirm the file paths to the user

If the user says no, end the conversation.

---

## Rules

- Execute ALL steps autonomously. Do not pause between workflows to ask the user for confirmation.
- Keep each agent's output concise: key findings, numbers, decisions, and signals. Not full reports.
- When reading CSV files, parse the actual data. Do not summarise file contents — calculate real numbers.
- Respect conditional steps strictly. If the required signal was not emitted, skip the step.
- HALT is a hard stop. No further workflows execute after HALT — this applies chain-wide.
- active_signals accumulate across the entire chain — signals from earlier workflows are visible to later ones.
- Do not invent data. If a file is empty or data is missing, report that fact.
- Each agent step should reference the prior agents' findings when relevant, including findings from earlier workflows in the chain.
- Workflows in the chain all operate on the same data drop. Do not allow mixed data drops.

---

## Common Workflow Chains

These are typical end-to-end scenarios:

**Plan-then-Execute** (full cycle):

```
/run-workflow-chain PULSE-01 WF-01 WF-02 WF-05
```

Demand Refresh → Supply Plan → Execution

**Monitoring Only** (read-only):

```
/run-workflow-chain PULSE-01 WF-04
```

Routine Monitoring (single workflow, still uses chain runner for consistency)

**Amendment Analysis** (conditional):

```
/run-workflow-chain PULSE-01 WF-03 WF-02
```

Protocol Amendment Impact → re-run Supply Plan if inventory changed

**Full Cycle with Monitoring**:

```
/run-workflow-chain PULSE-01 WF-01 WF-02 WF-05 WF-04
```

Demand → Plan → Execute → Monitor
