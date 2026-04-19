# WF-05 — Supply Plan Execution

> **Reference document only.** Runtime step definitions and task descriptions are in `workflows/workflows.json`. This file is for human understanding of the workflow design.

## Purpose

Take an approved supply plan and drive it through to execution — validate compliance, generate shipping documents, and track shipments to delivery. This is where recommendations become action.

---

## Trigger

- Human approves a supply plan (or subset of orders) from WF-02 (Supply Plan Generation)
- Human may approve all orders, modify quantities/dates, or approve selectively — only approved orders proceed

---

## Prerequisite

An approved supply plan from WF-02 must exist. This workflow does not generate orders — it executes them.

---

## Agents Involved

1. **Supervisor** — Intake, coordination, run closure
2. **Supply & Inventory Analyst** — Pre-execution stock verification and batch confirmation
3. **Compliance Manager** — Pre-shipment compliance gate (hard block, not advisory)
4. **Trade & Logistics Specialist** — Shipping execution and in-transit tracking
5. **Communications & Reporting Agent** — Execution report

---

## Workflow Phases

### Phase 1 — Supervisor: Receive Approved Plan

| Step | Skill | Action | Halt If |
|------|-------|--------|---------|
| 1.1 | DI-09 | Load study_config.json | File missing |
| 1.2 | SO-01 | Receive approved orders from human reviewer, route to Supply Analyst for pre-execution check | No approved orders |

The Supervisor records which orders were approved, modified, or rejected. Only approved orders proceed.

---

### Phase 2 — Supply Analyst: Pre-Execution Verification

Time may have passed between plan generation (WF-02) and approval. This phase catches changes.

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 2.1 | DI-04 | Parse latest ERP inventory — refresh stock position | — |
| 2.2 | SI-01 | Calculate current stock position — has anything changed since the plan was generated? | 2.1 |
| 2.3 | SI-10 | Confirm batch selection — are the recommended batches still available and still the best FEFO choice? | 2.2 |
| 2.4 | — | Compare current stock position to the position at plan generation — flag material changes | 2.2 |

**Branch:**

| Finding | Action |
|---------|--------|
| Stock position unchanged or minor variation | Continue to Phase 3 |
| Material change (stock consumed, batch expired, new stock arrived) | Flag to Supervisor — may need to return to WF-02 for plan revision |

---

### Phase 3 — Compliance Manager: Pre-Shipment Validation *(hard gate)*

Unlike WF-02 where compliance checks are advisory flags, here they are **blocking**. A NON-COMPLIANT result stops that shipment from proceeding.

| Step | Skill | Action | Halt If |
|------|-------|--------|---------|
| 3.1 | DI-08 | Load reference documents — shelf life by country, label requirements, approved vendors | Reference files missing |
| 3.2 | CO-03 | Check shelf-life compliance — will each selected batch meet minimum remaining shelf life at the destination country on arrival? | — |
| 3.3 | CO-04 | Enforce expiry date rules — apply country-specific and sponsor-specific expiry rules beyond standard shelf life | — |
| 3.4 | CO-02 | Validate label requirements — correct labels for each destination country? | — |
| 3.5 | CO-09 | Check SOP adherence — does the execution plan follow ordering and shipping SOPs? | — |
| 3.6 | CO-10 | Check for reference document changes since WF-02 ran — any new rules that affect this shipment? | — |

Steps 3.2, 3.3, 3.4, 3.5, and 3.6 can run in parallel after 3.1.

**Per-shipment compliance result:**

| Result | Action |
|--------|--------|
| **COMPLIANT** | Shipment proceeds to Phase 4 |
| **NON-COMPLIANT (CRITICAL/MAJOR)** | Shipment blocked — Supervisor notifies human with remediation details |
| **NON-COMPLIANT (MINOR/OBSERVATION)** | Shipment proceeds with flag noted in audit trail |

---

### Phase 4 — Logistics Specialist: Prepare Shipments

For each compliant, approved order:

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 4.1 | LT-01 | Confirm lead times for each shipping lane — may have changed since WF-02 | Approved orders |
| 4.2 | LT-07 | Check in-transit shipments — confirm nothing already in transit covers this need | ERP data |
| 4.3 | LT-02 | Calculate final shipping windows — latest and recommended ship dates | 4.1 (confirmed lead times) |
| 4.4 | LT-03 | Confirm cold chain capability for temperature-sensitive items | 4.1 (lanes identified) |
| 4.5 | LT-04 | Confirm import requirements — all licences and permits current | 4.1 (destinations identified) |
| 4.6 | LT-05 | Confirm vendor selection — approved vendor still available and appropriate | 4.4 + 4.5 (requirements confirmed) |
| 4.7 | LT-08 | Validate customs documentation — all required documents in place | 4.5 (import requirements known) |
| 4.8 | LT-06 | Generate shipping requests — final execution documents with all details | 4.3 + 4.6 + 4.7 (windows + vendor + docs) |

Steps 4.1 and 4.2 can run in parallel.
Steps 4.3, 4.4, and 4.5 can run in parallel after 4.1.
Steps 4.6 and 4.7 can run in parallel after 4.4/4.5.
Step 4.8 runs last.

**Halt if:**
- Shipping window CLOSED for any shipment (required-by date cannot be met)
- No approved vendor available for a required lane
- Critical cold chain gap (no capability on required lane for temperature-sensitive item)
- Critical documentation gaps that cannot be resolved before ship date

---

### Phase 5 — Logistics Specialist: Track Execution *(ongoing)*

| Step | Skill | Action |
|------|-------|--------|
| 5.1 | LT-07 | Monitor in-transit shipments — track status until delivery confirmed |

This phase is ongoing and produces updates as shipments progress:
- **ON TRACK** — No action needed
- **DELAYED** — Flag to Supervisor, may trigger WF-04 (Routine Monitoring) hot spot detection
- **DELIVERED** — Log delivery confirmation in audit trail

Phase 5 runs asynchronously — it does not block the workflow from closing.

---

### Phase 6 — Reporting Agent: Produce Execution Report

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 6.1 | RC-03 | Write ClinOps operational report — shipments executed, compliance status, tracking details, any blocked shipments with reasons | Phases 3 + 4 outputs |

---

### Phase 7 — Supervisor: Close Run

| Step | Skill | Action |
|------|-------|--------|
| 7.1 | SO-07 | Generate run summary — run ID, orders approved/executed/blocked, compliance results, shipping request count |
| 7.2 | CO-08 | Log full audit trail — every compliance check, every shipping request, every decision |

---

## Halt Conditions

| Condition | Detected At | Skill |
|-----------|-------------|-------|
| No approved orders received | Phase 1 | SO-01 |
| Study config missing | Phase 1 | DI-09 |
| ERP data missing (cannot verify stock) | Phase 2 | DI-04 |
| Reference documents missing | Phase 3 | DI-08 |
| CRITICAL/MAJOR non-compliance on a shipment | Phase 3 | CO-02/CO-03/CO-04/CO-09 |
| Material stock position change since plan generation | Phase 2 | SI-01 |
| Shipping window closed (cannot meet required-by date) | Phase 4 | LT-02 |
| No approved vendor for a required lane | Phase 4 | LT-05 |
| Critical cold chain gap | Phase 4 | LT-03 |

Note: Halt conditions in Phases 3 and 4 block **individual shipments**, not necessarily the entire workflow. Other compliant shipments can still proceed.

---

## Outputs

| Output | Produced By | Audience |
|--------|-------------|----------|
| Shipping requests (execution documents) | LT-06 | Logistics, Execution Team |
| Compliance validation results per shipment | CO-02, CO-03, CO-04, CO-09 | Quality, Regulatory |
| Blocked shipment notifications with remediation | Compliance Manager | Supply Team, Quality |
| In-transit tracking updates | LT-07 | Supply Team, ClinOps |
| ClinOps operational report | RC-03 | Clinical Operations |
| Run summary with audit trail | SO-07 + CO-08 | Internal / GxP compliance |

---

## Skill Chain Summary

```
DI-09 → SO-01
  → DI-04 → SI-01 → SI-10
    → [material change?] → back to WF-02
    → [OK]
      → DI-08
        → CO-03 ┐
        → CO-04 ┤
        → CO-02 ┤ (parallel)
        → CO-09 ┤
        → CO-10 ┘
          → [per shipment: COMPLIANT?]
            → [NO] → blocked, notify human
            → [YES]
              → LT-01 ┐
              → LT-07 ┘ (parallel)
                → LT-02 ┐
                → LT-03 ┤ (parallel)
                → LT-04 ┘
                  → LT-05 ┐
                  → LT-08 ┘ (parallel)
                    → LT-06
                      → LT-07 (ongoing tracking)
                        → RC-03 → SO-07 + CO-08
```

---

## Relationship to Other Workflows

| Workflow | Relationship |
|----------|-------------|
| **WF-02** | Upstream — produces the supply plan that this workflow executes |
| **WF-04** | May be triggered if in-transit shipments are delayed (hot spot detection) |
| **WF-02** | May loop back if pre-execution verification finds material stock changes |

---

## Notes

- This workflow bridges planning and execution — WF-02 ends with recommendations, WF-05 makes them real
- Compliance checks are **hard gates** here, not advisory — NON-COMPLIANT blocks the shipment
- CO-04 (Expiry Date Rule Enforcer) is used here for the first time — it applies country/sponsor-specific rules beyond standard shelf life
- Pre-execution verification (Phase 2) is a safety net — time between plan approval and execution can change the stock picture
- Individual shipments can be blocked without stopping the entire workflow — other compliant shipments proceed
- LT-07 tracking in Phase 5 is asynchronous and ongoing — the workflow closes after shipping requests are generated, but tracking continues
- All shipping requests are EXECUTION documents, not recommendations — they have been through compliance validation
