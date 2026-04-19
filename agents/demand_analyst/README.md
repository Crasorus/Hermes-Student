# Demand & Forecast Analyst Agent

## What This Agent Does

The Demand & Forecast Analyst is the agent responsible for understanding how much clinical supply is needed, where, and when. It processes actual consumption data from RTSM, compares it against the clinical operations plan from CTMS, and calculates whether the study is on track or drifting.

When demand has shifted significantly, this agent generates scenario forecasts — base case, optimistic, and pessimistic — so that downstream agents and human reviewers can plan accordingly.

---

## What the Demand Analyst Is Not

- It does not manage inventory or stock levels (that is the Supply Analyst)
- It does not produce shipping requests (that is the Logistics Specialist)
- It does not make compliance judgments (that is the Compliance Manager)
- It does not communicate with stakeholders (that is the Reporting Agent)

---

## Skills This Agent Owns

| Skill ID | Skill Name                        |
|----------|-----------------------------------|
| DI-03    | RTSM Data Parser                  |
| DI-05    | CTMS Plan Parser                  |
| DF-01    | Consumption Rate Calculator       |
| DF-02    | Enrollment Trajectory Modeller    |
| DF-03    | Demand Delta Calculator           |
| DF-04    | Threshold Evaluator               |
| DF-05    | Scenario Modeller                 |
| DF-06    | What-If Scenario Engine           |
| DF-07    | Visit & Dispensing Calculator     |
| DF-08    | Screen Failure & Dropout Adjuster |
| DF-09    | Demand Baseline Updater           |

**Shared Skills (borrowed):**
| Skill ID | Skill Name                      | Owner              |
|----------|---------------------------------|--------------------|
| CO-05    | Protocol Change Impact Assessor | Compliance Manager |
| DF-04    | Threshold Evaluator             | Shared with Supervisor |

Skills are defined in the shared `/skills/` folder at the project root.

---

## What the Demand Analyst Needs to Run

**Data files (from Study Package):**
- `data_drops/YYYY-MM-DD/rtsm_actuals.csv` — Kit dispensing, randomisations, screen failures, returns
- `data_drops/YYYY-MM-DD/ctms_plan.csv` — Enrollment plan, site activation, visit schedules

**Configuration files:**
- `config/study_config.json` — Thresholds, treatment arms, pack sizes

**Context from Supervisor:**
- Current approved demand baseline
- Trigger reason (scheduled, event-driven, protocol change)

---

## What the Demand Analyst Produces

| Output | Description |
|--------|-------------|
| Delta Report | Quantified demand delta by country, site, treatment arm, and item — with significance flag |
| Scenario Demand Matrix | Base, optimistic, and pessimistic demand forecasts across the planning horizon |
| Enrollment Trajectory | Current enrollment rate vs. plan, with projected completion date |
| Consumption Analysis | Actual kit consumption rates by site, country, arm compared to modelled rates |
| Updated Demand Baseline | New approved baseline (if delta is confirmed and accepted) |

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file — overview and reference guide |
| `system_prompt.md` | The agent's full instructions — its identity, behaviour rules, and skill references |
