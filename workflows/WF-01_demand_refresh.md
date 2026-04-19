# WF-01 — Demand Signal Refresh

> **Reference document only.** Runtime step definitions and task descriptions are in `workflows/workflows.json`. This file is for human understanding of the workflow design.

## Purpose

Ingest new data, recalculate demand, compare to baseline, and produce a demand refresh summary for human review. This is the primary recurring workflow in Hermes.

---

## Trigger

New data drop lands in `data_drops/{date}/` containing RTSM actuals, ERP inventory, and CTMS plan files.

---

## Agents Involved

1. **Supervisor** — Intake, validation, routing, run closure
2. **Demand & Forecast Analyst** — Parsing, analysis, scenario generation
3. **Communications & Reporting Agent** — Summary report production

---

## Workflow Phases

### Phase 1 — Supervisor: Intake & Validation

| Step | Skill | Action | Halt If |
|------|-------|--------|---------|
| 1.1 | DI-09 | Load study_config.json — single source of truth for the run | File missing or unreadable |
| 1.2 | DI-01 | Check file manifest — verify all critical files are present | Any critical file missing |
| 1.3 | DI-02 | Validate file schemas against definitions in study_config | Schema validation failure |
| 1.4 | DI-12 | Run Aggregate Data Query — compute verified aggregations, run integrity checks, calculate supply coverage and enrollment deltas | `overall_data_integrity` flag = FAIL |
| 1.5 | DI-10 | Score data quality across all ingested sources and DI-12 output | Quality flag = CRITICAL |
| 1.6 | SO-01 | Route workflow to Demand & Forecast Analyst | — |

**Phase 1 output passed to Demand Analyst:** study config, DI-12 output (verified aggregations, integrity checks, derived metrics), data quality flag, file paths, validation results.

---

### Phase 2 — Demand Analyst: Parse Source Data

| Step | Skill | Action | Halt If |
|------|-------|--------|---------|
| 2.1 | DI-03 | Parse RTSM actuals — dispensing, randomisation, screen failures, returns, site inventory, site shipments | File unparseable or >threshold% critical issues |
| 2.2 | DI-05 | Parse CTMS plan — enrollment plan, site information, visit schedules | File unparseable or enrollment plan missing |

Steps 2.1 and 2.2 are independent and can run in parallel.

---

### Phase 3 — Demand Analyst: Analyse & Calculate

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 3.1 | DF-01 | Calculate consumption rates by site, country, treatment arm | 2.1 (RTSM data) |
| 3.2 | DF-02 | Model enrollment trajectory — actual vs. plan, projected completion | 2.1 + 2.2 (RTSM + CTMS) |
| 3.3 | DF-07 | Calculate visit/dispensing demand — translate protocol into kit numbers | 2.2 (CTMS visit schedules) |
| 3.4 | DF-08 | Adjust demand for screen failures and dropouts | 3.2 + 3.3 (enrollment + visit demand) |
| 3.5 | DF-03 | Calculate demand delta — current forecast vs. approved baseline | 3.1 + 3.4 (consumption + adjusted demand) |
| 3.6 | DF-04 | Evaluate delta against significance thresholds | 3.5 (delta values) |

Steps 3.1, 3.2, and 3.3 can run in parallel (all depend only on Phase 2 outputs).
Steps 3.4 onwards are sequential.

---

### Phase 4 — Branch on Significance

| Delta Result | Path | Rationale |
|--------------|------|-----------|
| **MINOR** (below threshold) | Skip to Phase 6 | No material change — fast-track to summary report |
| **SIGNIFICANT** (at or above threshold) | Continue to Phase 5 | Material shift — full scenario analysis required |

The threshold default is 10%, configurable per study/item/country in study_config.json.

---

### Phase 5 — Demand Analyst: Scenario Analysis *(significant delta only)*

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 5.1 | DF-05 | Generate three scenarios: base case, optimistic, pessimistic — each with total demand, completion date, breakdown by country/arm/item | 3.1 through 3.6 (full analysis) |

**Scenario assumptions must be explicitly stated** so the human reviewer can judge whether they are reasonable.

---

### Phase 6 — Reporting Agent: Produce Output

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 6.1 | RC-01 | Write demand refresh summary with: enrollment summary table by site (from DI-12), deltas, scenarios (if generated), enrollment trajectory, compliance status, next steps, traceability | All prior phase outputs + DI-12 enrollment data |

**Enrollment Summary Table (visual human checkpoint):**
- Displays patient counts by site (planned vs. actual)
- Shows enrollment rates and deltas per site
- Allows supply team to detect anomalies (e.g., hotspots, lags) before supply decisions
- Sourced directly from DI-12 output

The report must be self-explanatory — the reader should understand the situation without follow-up questions.

---

### Phase 7 — Supervisor: Close Run

| Step | Skill | Action |
|------|-------|--------|
| 7.1 | SO-07 | Generate run summary — run ID, timing, agents invoked, quality flags, key findings |
| 7.2 | CO-08 | Log full audit trail — all agent actions with timestamps |

---

### Phase 8 — Post-Approval *(human-triggered, not automatic)*

| Step | Skill | Action | Gate |
|------|-------|--------|------|
| 8.1 | DF-09 | Update demand baseline in study package — archive previous, write new, log change | Human must explicitly approve |

This phase only runs after the human reviewer confirms the new demand baseline. It never runs automatically.

---

## Halt Conditions

The workflow halts and does not proceed if any of the following occur:

| Condition | Detected At | Skill |
|-----------|-------------|-------|
| Study config missing or unreadable | Phase 1, Step 1.1 | DI-09 |
| Critical file missing from data drop | Phase 1, Step 1.2 | DI-01 |
| Schema validation failure | Phase 1, Step 1.3 | DI-02 |
| Data integrity check failed | Phase 1, Step 1.4 | DI-12 |
| Data quality scored CRITICAL | Phase 1, Step 1.5 | DI-10 |
| RTSM file unparseable | Phase 2, Step 2.1 | DI-03 |
| CTMS file unparseable or enrollment missing | Phase 2, Step 2.2 | DI-05 |
| Contradictory data between sources | Phase 3 | DF-01/DF-02 |

On halt, the Supervisor logs the halt reason via CO-08 and produces a run summary via SO-07 explaining why the workflow stopped.

---

## Outputs

| Output | Produced By | Audience |
|--------|-------------|----------|
| Demand refresh summary report | RC-01 | ClinOps, Supply Team |
| Run summary with audit trail | SO-07 + CO-08 | Internal / GxP compliance |
| Updated demand baseline *(post-approval only)* | DF-09 | Study package (reference for next cycle) |

---

## Skill Chain Summary

```
DI-09 → DI-01 → DI-02 → DI-12 → DI-10 → SO-01
               ↓
             (DI-12 output: verified aggregations, integrity checks, derived metrics)
               ↓
  → DI-03 ┐
  → DI-05 ┘ (parallel)
    → DF-01 ┐
    → DF-02 ┤ (parallel, use DI-12 verified counts instead of raw CSV parsing)
    → DF-07 ┘
      → DF-08 → DF-03 → DF-04
        → [MINOR?] ──────────→ RC-01 → SO-07 + CO-08
        → [SIGNIFICANT?] → DF-05 → RC-01 → SO-07 + CO-08
          → [human approval] → DF-09
```

---

## Notes

- This workflow runs end-to-end without human intervention until the report is produced
- The branch at Phase 4 prevents unnecessary scenario work for routine fluctuations
- DF-07 and DF-08 run before DF-03 so the delta compares adjusted demand, not raw numbers
- The baseline (DF-09) is the only skill that writes back to the study package, and only after explicit human approval
- All agent outputs include audit trail entries for GxP compliance
