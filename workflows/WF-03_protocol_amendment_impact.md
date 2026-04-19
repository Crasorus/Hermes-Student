# WF-03 — Protocol Amendment Impact

> **Reference document only.** Runtime step definitions and task descriptions are in `workflows/workflows.json`. This file is for human understanding of the workflow design.

## Purpose

Assess the supply chain impact of a protocol amendment — what changes, what is affected, what needs to happen. This workflow identifies implications across demand, inventory, logistics, and compliance, then produces a structured impact report for human review.

---

## Trigger

- Protocol amendment document received (new or revised)
- Notification of an upcoming protocol change that requires impact assessment

---

## Agents Involved

1. **Supervisor** — Intake, routing, coordination, run closure
2. **Compliance Manager** — Amendment parsing and impact assessment (lead agent for this workflow)
3. **Demand & Forecast Analyst** — Demand re-modelling under amended protocol
4. **Supply & Inventory Analyst** — Inventory impact and gap analysis
5. **Communications & Reporting Agent** — Impact report production

---

## Workflow Phases

### Phase 1 — Supervisor: Intake & Route

| Step | Skill | Action | Halt If |
|------|-------|--------|---------|
| 1.1 | DI-09 | Load study_config.json — current protocol parameters for comparison | File missing or unreadable |
| 1.2 | SO-01 | Route to Compliance Manager in protocol change mode, passing amendment document and study config | Amendment document missing |

---

### Phase 2 — Compliance Manager: Assess Impact

| Step | Skill | Action | Halt If |
|------|-------|--------|---------|
| 2.1 | DI-08 | Load reference documents — shelf life by country, label requirements, approved vendors | Reference files missing |
| 2.2 | CO-05 | Parse amendment and assess impact across all areas: demand, inventory, logistics, compliance, labelling | — |

CO-05 produces:
- List of changes identified in the amendment
- Impact assessment by area with severity (HIGH / MEDIUM / LOW)
- Whether each area requires downstream agent analysis
- Recommended actions per impact

**The CO-05 output determines which of Phases 3 and 4 are needed.** Not every amendment affects all areas.

---

### Phase 3 — Demand Analyst: Re-model Demand *(only if amendment affects demand)*

Triggered when CO-05 identifies demand impact — changes to treatment arms, visit schedules, doses, randomisation ratio, countries, or enrollment targets.

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 3.1 | DI-03 | Parse current RTSM actuals (if not already in context) | — |
| 3.2 | DI-05 | Parse current CTMS plan (if not already in context) | — |
| 3.3 | DF-01 | Calculate current consumption rates as baseline reference | 3.1 (RTSM data) |
| 3.4 | DF-02 | Model current enrollment trajectory | 3.1 + 3.2 |
| 3.5 | DF-06 | Run what-if scenario modelling the amended protocol — adjust parameters per amendment, project demand, compare to current baseline | 3.3 + 3.4 + CO-05 output |

Steps 3.1 and 3.2 can run in parallel.
Steps 3.3 and 3.4 can run in parallel after 3.1/3.2.

If current data is already in context from a recent WF-01 run, steps 3.1–3.4 can be skipped and DF-06 runs directly against existing outputs.

---

### Phase 4 — Supply Analyst: Assess Inventory Impact *(only if amendment affects inventory or supply)*

Triggered when CO-05 identifies inventory impact — existing stock becomes obsolete, pack configurations change, items are added or removed, or supply requirements shift.

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 4.1 | DI-04 | Parse current ERP inventory (if not already in context) | — |
| 4.2 | SI-01 | Calculate current stock position — identify affected stock by item, location, batch | 4.1 |
| 4.3 | SI-03 | Profile expiry risk for affected batches — will they be consumed before the amendment takes effect? | 4.2 |
| 4.4 | SI-07 | Identify supply gaps — does the amendment create new demand that current supply cannot meet? | 4.2 + DF-06 output (if available) |

If current inventory data is already in context from a recent WF-02 run, step 4.1 can be skipped.

---

### Phase 5 — Compliance Manager: Validate Amended Parameters

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 5.1 | CO-01 | Check that amended protocol parameters are internally consistent and that any re-modelled demand aligns with the amendment | DF-06 output (if Phase 3 ran) |
| 5.2 | CO-02 | Check label requirements — does the amendment change labelling needs for any country? | CO-05 output |
| 5.3 | CO-03 | Check shelf-life compliance — do amended timelines or new countries introduce shelf-life constraints? | CO-05 output |
| 5.4 | CO-09 | Check SOP adherence — does the amendment require changes to operational procedures? | CO-05 output |

Steps 5.1, 5.2, 5.3, and 5.4 can run in parallel.

---

### Phase 6 — Reporting Agent: Produce Impact Report

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 6.1 | RC-06 | Write protocol change impact report — headline impact, amendment description, impacts by area, quantified where possible, recommended actions, timeline, traceability | All prior phase outputs |

The report audience is ClinOps, Regulatory, and Supply Team.

---

### Phase 7 — Supervisor: Close Run

| Step | Skill | Action |
|------|-------|--------|
| 7.1 | SO-07 | Generate run summary — run ID, timing, agents invoked, amendment reference, key findings |
| 7.2 | CO-08 | Log full audit trail — all agent actions with timestamps |

---

### Phase 8 — Post-Review Chaining *(human-triggered)*

After the human reviewer assesses the impact report, they may trigger follow-on workflows:

| Decision | Action |
|----------|--------|
| Amendment requires full demand refresh | Trigger **WF-01** (Demand Signal Refresh) with updated protocol parameters |
| Amendment requires new supply plan | Trigger **WF-02** (Supply Plan Generation) with re-modelled demand |
| Amendment is minor, no supply chain action needed | Close — no further workflow |
| Existing stock needs disposition | Compliance Manager runs **CO-07** (Destruction Eligibility Checker) for obsolete stock |

These chained workflows are not automatic — the human decides based on the impact report.

---

## Halt Conditions

| Condition | Detected At | Skill |
|-----------|-------------|-------|
| Study config missing or unreadable | Phase 1, Step 1.1 | DI-09 |
| Amendment document missing | Phase 1, Step 1.2 | SO-01 |
| Reference documents missing | Phase 2, Step 2.1 | DI-08 |
| Critical non-compliance with patient safety implications | Phase 5 | CO-01/CO-02/CO-03 |

On halt, the Supervisor logs the halt reason via CO-08 and produces a run summary via SO-07.

---

## Outputs

| Output | Produced By | Audience |
|--------|-------------|----------|
| Protocol change impact report | RC-06 | ClinOps, Regulatory, Supply Team |
| What-if demand scenario (if applicable) | DF-06 | Supply Team |
| Affected inventory analysis (if applicable) | SI-01, SI-03, SI-07 | Supply Team |
| Compliance validation results | CO-01, CO-02, CO-03, CO-09 | Quality, Regulatory |
| Run summary with audit trail | SO-07 + CO-08 | Internal / GxP compliance |

---

## Skill Chain Summary

```
DI-09 → SO-01
  → DI-08 → CO-05
    → [demand impact?]
        → DI-03 ┐
        → DI-05 ┘ (parallel)
          → DF-01 ┐
          → DF-02 ┘ (parallel)
            → DF-06
    → [inventory impact?]
        → DI-04 → SI-01
          → SI-03
          → SI-07
    → CO-01 ┐
    → CO-02 ┤
    → CO-03 ┤ (parallel)
    → CO-09 ┘
      → RC-06 → SO-07 + CO-08
        → [human review]
          → WF-01? / WF-02? / CO-07?
```

---

## Notes

- The Compliance Manager is the lead agent in this workflow — it owns the amendment assessment
- CO-05 is the gating skill — its output determines which downstream agents are activated
- Not every amendment triggers all phases — a minor labelling change may only need Phases 1, 2, 5, and 6
- DF-06 (what-if engine) is used here, not DF-05 (standard scenarios) — this is a specific scenario, not a range
- This workflow identifies impact and recommends actions — it does not execute supply chain changes
- Follow-on workflows (WF-01, WF-02) are triggered by human decision after reviewing the impact report
- Protocol amendments can be urgent — the report should clearly flag time-sensitive actions
