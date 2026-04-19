# Supervisor Agent

## What This Agent Does

The Supervisor is the orchestrator of the Hermes Clinical Supply Chain AI Agent Team. It is the entry point for every workflow. No other agent runs without the Supervisor first validating the data, logging the run, and issuing routing instructions.

The Supervisor does not perform supply chain analysis itself. Its job is to:

- Check that all required data is present and valid before any work begins
- Decide which workflow to run and which agents to activate
- Coordinate the sequence of agent activity within a workflow
- Resolve any conflicts between agent outputs
- Track progress and log every run for the audit trail
- Produce a run summary at the end of every workflow

---

## What the Supervisor Is Not

- It does not analyse demand, inventory, or logistics
- It does not make supply chain recommendations
- It does not communicate directly with stakeholders (that is the Reporting Agent's role)

---

## Skills This Agent Owns

| Skill ID | Skill Name                    |
|----------|-------------------------------|
| SO-01    | Workflow Router               |
| SO-02    | Study Registry Manager        |
| SO-03    | Inter-Agent Conflict Resolver |
| SO-04    | Workflow Status Tracker       |
| SO-05    | Priority Ranker               |
| SO-06    | Exception Handler             |
| SO-07    | Run Summary Generator         |
| DI-01    | Data Manifest Checker         |
| DI-02    | Schema Validator              |
| DI-09    | Study Config Loader           |
| DI-10    | Data Quality Scorer           |

Skills are defined in the shared `/skills/` folder at the project root.

---

## What the Supervisor Needs to Run

Before the Supervisor can start any workflow, the following must be in place:

**Study Package — Static Layer** (set up once per study):
- `config/study_config.json`
- `config/supply_network.json`
- `config/policies.json`

**Study Package — Dynamic Layer** (delivered each cycle):
- `data_drops/YYYY-MM-DD/rtsm_actuals.csv`
- `data_drops/YYYY-MM-DD/erp_inventory.csv`
- `data_drops/YYYY-MM-DD/ctms_plan.csv`

If any critical file is missing, the Supervisor will **HALT** and produce a manifest error report. No other agent will run.

---

## What the Supervisor Produces

| Output | Description |
|--------|-------------|
| Manifest Check Report | Confirms which files were found, which were missing, and whether the run can proceed |
| Workflow Routing Decision | States which workflow is being triggered and which agents will run |
| Audit Log Entry | A timestamped record of the run: study ID, trigger reason, files loaded, decisions taken |
| Run Summary | A concise end-of-workflow summary of what ran, what was found, and what was actioned |

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file — overview and reference guide |
| `system_prompt.md` | The agent's full instructions — its identity, behaviour rules, and skill references |
