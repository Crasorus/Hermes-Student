# WF-04 — Routine Monitoring

> **Reference document only.** Runtime step definitions and task descriptions are in `workflows/workflows.json`. This file is for human understanding of the workflow design.

## Purpose

Continuously scan supply chain data for emerging risks, anomalies, and hot spots without waiting for a full demand refresh or supply plan cycle. This is the early warning system — it detects problems before they become crises.

---

## Trigger

- Scheduled run (daily, weekly, or per study cadence)
- Ad hoc run when the Supervisor or a human reviewer requests a risk check
- Can also be triggered automatically after any data drop lands

---

## Agents Involved

1. **Supervisor** — Intake, validation, routing, escalation decisions, run closure
2. **Supply & Inventory Analyst** — Stock position and safety stock assessment
3. **Trade & Logistics Specialist** — In-transit shipment status
4. **Demand & Forecast Analyst** — Current consumption rates and enrollment trajectory
5. **Clinical Data & Insights Analyst** — Hot spot detection, anomaly detection, risk scoring, shortage modelling
6. **Compliance Manager** — Reference document change detection, audit trail
7. **Communications & Reporting Agent** — Hot spot alert production

---

## Workflow Phases

### Phase 1 — Supervisor: Intake & Validation

| Step | Skill | Action | Halt If |
|------|-------|--------|---------|
| 1.1 | DI-09 | Load study_config.json | File missing or unreadable |
| 1.2 | DI-01 | Check file manifest — verify data files are present | Critical files missing |
| 1.3 | DI-10 | Score data quality | Quality flag = CRITICAL |
| 1.4 | SO-01 | Route to monitoring workflow — activate agents in parallel | — |

---

### Phase 2 — Gather Current State *(agents run in parallel)*

Three agents gather the latest state simultaneously. These feeds supply the Insights Analyst in Phase 3.

**Supply Analyst — Stock Snapshot:**

| Step | Skill | Action |
|------|-------|--------|
| 2.1 | DI-04 | Parse ERP inventory — stock on hand, batches, open orders |
| 2.2 | SI-01 | Calculate stock position by depot, country, arm, item |
| 2.3 | SI-02 | Calculate weeks of supply at current consumption rate |
| 2.4 | SI-03 | Profile batch expiry dates — identify expiry risk |
| 2.5 | SI-04 | Check safety stock — flag locations AT, BELOW, or APPROACHING |

**Logistics Specialist — In-Transit Status:**

| Step | Skill | Action |
|------|-------|--------|
| 2.6 | LT-07 | Check in-transit shipments — flag any delayed or at-risk |

**Demand Analyst — Consumption & Enrollment:**

| Step | Skill | Action |
|------|-------|--------|
| 2.7 | DI-03 | Parse RTSM actuals |
| 2.8 | DI-05 | Parse CTMS plan |
| 2.9 | DF-01 | Calculate current consumption rates by site, country, arm |
| 2.10 | DF-02 | Model current enrollment trajectory — actual vs. plan |

Steps 2.7 and 2.8 run in parallel, then 2.9 and 2.10 run in parallel after them.

---

### Phase 3 — Insights Analyst: Detect & Score

The Insights Analyst receives all Phase 2 outputs and runs its surveillance suite.

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 3.1 | AI-01 | Detect hot spots — stock-out risk, expiry clusters, shipment delays, consumption anomalies | All Phase 2 outputs |
| 3.2 | AI-02 | Detect anomalies — statistical outliers in consumption, enrollment, or inventory | All Phase 2 outputs |
| 3.3 | AI-03 | Score risk for each site, country, and depot — composite score from all signals | 3.1 + 3.2 + Phase 2 outputs |
| 3.4 | AI-06 | Model shortage probability at 4, 8, and 12 weeks per location | Phase 2 stock + consumption data |

Steps 3.1 and 3.2 can run in parallel. Step 3.3 runs after both. Step 3.4 can run in parallel with 3.3.

---

### Phase 4 — Compliance Manager: Reference Document Check

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 4.1 | DI-08 | Load reference documents | — |
| 4.2 | CO-10 | Check for reference document changes since last run — flag if shelf life rules, label requirements, or approved vendors have changed | 4.1 |

Phase 4 runs in parallel with Phase 3.

---

### Phase 5 — Supervisor: Evaluate & Escalate

The Supervisor reviews the Insights Analyst's findings and decides on escalation.

| Finding | Action |
|---------|--------|
| No hot spots, all risk scores LOW/MEDIUM | Proceed to Phase 6 — routine report only |
| CRITICAL or HIGH hot spots detected | Proceed to Phase 6 — alert report, then consider triggering WF-02 (Supply Plan Generation) |
| Anomalies suggest data quality issues | Flag for human review — possible data investigation needed |
| Reference documents changed | Flag for Compliance Manager to re-validate current plan |
| Shortage probability HIGH at any location | Highlight in alert and consider triggering WF-02 |

---

### Phase 6 — Reporting Agent: Produce Output

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 6.1 | RC-05 | Write hot spot alert — critical risks first, actions, urgency levels | Phase 3 + Phase 4 outputs |

If no hot spots are detected, RC-05 produces a brief "all clear" summary confirming monitoring ran and no action is needed.

---

### Phase 7 — Supervisor: Close Run

| Step | Skill | Action |
|------|-------|--------|
| 7.1 | SO-07 | Generate run summary — run ID, timing, hot spot count, risk scores, escalation decisions |
| 7.2 | CO-08 | Log full audit trail |

---

### Phase 8 — Escalation Chaining *(conditional, may be automatic or human-triggered)*

| Condition | Action | Automatic? |
|-----------|--------|------------|
| CRITICAL hot spot — imminent stock-out | Trigger **WF-02** (Supply Plan Generation) for affected locations | Supervisor may auto-trigger |
| HIGH hot spot — approaching risk | Flag for human review — recommend WF-02 | Human decision |
| Reference document change with supply plan impact | Trigger compliance re-validation of current plan | Supervisor may auto-trigger |
| Anomaly suggesting protocol deviation | Flag for human investigation | Human decision |

---

## Halt Conditions

| Condition | Detected At | Skill |
|-----------|-------------|-------|
| Study config missing | Phase 1, Step 1.1 | DI-09 |
| Critical data files missing | Phase 1, Step 1.2 | DI-01 |
| Data quality CRITICAL | Phase 1, Step 1.3 | DI-10 |
| No data files available at all | Phase 2 | DI-03/DI-04 |

On halt, the Supervisor logs the halt reason via CO-08 and produces a run summary via SO-07.

---

## Outputs

| Output | Produced By | Audience |
|--------|-------------|----------|
| Hot spot alert | RC-05 | Supply Team, ClinOps, Management |
| Risk scores by location | AI-03 | Supply Team |
| Shortage probability report | AI-06 | Supply Team |
| Anomaly flags | AI-02 | Supply Team, Data Management |
| Reference document change alerts | CO-10 | Quality, Regulatory |
| Run summary with audit trail | SO-07 + CO-08 | Internal / GxP compliance |

---

## Skill Chain Summary

```
DI-09 → DI-01 → DI-10 → SO-01
  → DI-04 → SI-01 → SI-02 ┐
                   → SI-03 ┤ (parallel)
                   → SI-04 ┘                   ─┐
  → LT-07                                       ├─ all feed into Phase 3
  → DI-03 ┐                                     │
  → DI-05 ┘ (parallel)                          │
    → DF-01 ┐                                   │
    → DF-02 ┘ (parallel)                       ─┘
      → AI-01 ┐
      → AI-02 ┘ (parallel)
        → AI-03
        → AI-06 (parallel with AI-03)
  → DI-08 → CO-10 (parallel with Phase 3)
    → [Supervisor evaluates]
      → RC-05 → SO-07 + CO-08
        → [WF-02? / compliance re-validation?]
```

---

## Notes

- This is the lightest-weight workflow — it reads data and looks for problems, it does not produce supply plans or orders
- Designed to run frequently (daily or per data drop) without being heavyweight
- Phase 2 runs three agents in parallel to minimise elapsed time
- The Insights Analyst is the lead analytical agent — it synthesises signals from all other agents
- Routine monitoring builds an ongoing risk picture — over multiple runs, trends and patterns become visible
- CRITICAL escalations may auto-trigger WF-02 without waiting for human review, depending on study policy
- If no issues are found, the output is a brief "all clear" — not every run produces a long report
- This workflow never modifies the study package — it is read-only
