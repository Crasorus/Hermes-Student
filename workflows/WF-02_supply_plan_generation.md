# WF-02 — Supply Plan Generation

> **Reference document only.** Runtime step definitions and task descriptions are in `workflows/workflows.json`. This file is for human understanding of the workflow design.

## Purpose

Take the demand forecast from WF-01 and translate it into a concrete supply plan: what to order, where to ship it from, where it goes, and by when. Then assess the plan for gaps, waste, and overall quality before presenting it for human review.

---

## Trigger

- Completed WF-01 (Demand Signal Refresh) — Supervisor chains into this workflow automatically
- Can also be triggered independently when demand is unchanged but supply conditions have changed (e.g., new ERP data drop, batch expiry update, protocol amendment)

---

## Prerequisite

A demand forecast must exist — either fresh from WF-01 or an existing approved baseline. The Supply Analyst cannot plan without knowing what is needed.

---

## Agents Involved

1. **Supervisor** — Routing, coordination, run closure
2. **Supply & Inventory Analyst** — Stock analysis, order calculation, plan scoring
3. **Trade & Logistics Specialist** — Lead times, shipping windows, vendor selection, shipping requests
4. **Compliance Manager** — Shelf-life and label compliance checks
5. **Communications & Reporting Agent** — Supply plan report production

---

## Workflow Phases

### Phase 1 — Supervisor: Route to Supply Analyst

| Step | Skill | Action | Halt If |
|------|-------|--------|---------|
| 1.1 | SO-01 | Route workflow to Supply & Inventory Analyst, passing demand forecast and data quality flag | No demand input available |

If chained from WF-01, the Supervisor already has the study config, data quality flag, and demand output in context. If triggered independently, the Supervisor runs DI-09 and DI-10 first.

---

### Phase 2 — Supply Analyst: Load Configuration & Inventory

> **Note:** ERP inventory data (DI-04) is processed and validated by the Supervisor via DI-12 before this phase begins. The Supply Analyst receives DI-12 aggregated output directly — it does not re-parse raw ERP files. Steps 2.2 and 2.3 are loaded directly by the Supply Analyst.

| Step | Skill | Action | Halt If |
|------|-------|--------|---------|
| 2.1 | DI-12 | Receive verified ERP aggregations from Supervisor (stock on hand, in-transit, on-order, batch expiry profile) — sourced from DI-12 output, not raw CSV | DI-12 output not in context |
| 2.2 | DI-06 | Load supply network — depots, lanes, lead times, manufacturing sites | Config missing |
| 2.3 | DI-07 | Load policies — safety stock rules, reorder points, min/max order quantities, budget envelope | Config missing |

Steps 2.1, 2.2, and 2.3 are independent and can run in parallel.

---

### Phase 3 — Supply Analyst: Assess Current Stock Position

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 3.1 | SI-01 | Calculate stock on hand by depot, country, arm, item — include in-transit and on-order | 2.1 (ERP data) |
| 3.2 | SI-02 | Calculate weeks of supply at current consumption rate per location | 3.1 + demand forecast |
| 3.3 | SI-03 | Profile batch expiry dates against projected consumption — quantify expiry risk | 3.1 (stock position) |
| 3.4 | SI-10 | Recommend batch priority using FEFO rules | 3.3 (expiry profile) |

Steps 3.1 runs first. Steps 3.2 and 3.3 can run in parallel after 3.1. Step 3.4 follows 3.3.

---

### Phase 4 — Supply Analyst: Evaluate Reorder Needs

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 4.1 | SI-04 | Check safety stock — flag locations AT, BELOW, or APPROACHING safety stock | 3.1 + 3.2 (stock position + weeks of supply) |
| 4.2 | SI-05 | Evaluate reorder triggers — which locations have breached or will breach reorder point within lead time | 4.1 (safety stock status) |

---

### Phase 5 — Supply Analyst: Build the Supply Plan

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 5.1 | SI-06 | Calculate order quantities for each location needing replenishment — demand during coverage period, safety stock, pipeline stock, min/max constraints, pack-size rounding, shelf-life check | 4.2 (reorder triggers) + demand forecast |
| 5.2 | SI-07 | Identify supply gaps — where projected demand exceeds available supply even after planned orders | 5.1 (order recommendations) + 3.1 (stock position) |
| 5.3 | SI-08 | Estimate overage and waste at study end under current plan | 5.1 + 3.3 (orders + expiry profile) |
| 5.4 | SI-09 | Score the supply plan on efficiency, risk, cost, and complexity — composite score + commentary | 5.1 + 5.2 + 5.3 + 4.1 (full plan context) |

Steps 5.2 and 5.3 can run in parallel after 5.1. Step 5.4 runs after 5.2 and 5.3.

---

### Phase 6 — Logistics Specialist: Plan Shipments

The Supervisor passes the Supply Analyst's output (orders, batch selection, supply gaps) to the Logistics Specialist.

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 6.1 | LT-01 | Calculate lead times for each required shipping lane | Supply Analyst orders |
| 6.2 | LT-07 | Check in-transit shipments — what is already moving, any delays? | ERP data |
| 6.3 | LT-02 | Plan shipping windows — latest and recommended ship dates based on required-by dates and lead times | 6.1 (lead times) |
| 6.4 | LT-03 | Check cold chain requirements — validate lane/vendor capability for temperature-sensitive items | 6.1 (lanes identified) |
| 6.5 | LT-04 | Check import requirements — licences, permits, documentation for destination countries | 6.1 (lanes identified) |
| 6.6 | LT-05 | Select approved vendors for each lane | 6.4 + 6.5 (requirements known) |
| 6.7 | LT-08 | Validate customs documentation — all required docs in place? | 6.5 (import requirements) |
| 6.8 | LT-06 | Generate shipping requests — structured documents ready for execution | 6.3 + 6.6 + 6.7 (windows + vendors + docs) |

Steps 6.1 and 6.2 can run in parallel.
Steps 6.3, 6.4, and 6.5 can run in parallel after 6.1.
Steps 6.6 and 6.7 can run in parallel after 6.4/6.5.
Step 6.8 runs last.

---

### Phase 7 — Compliance Manager: Validate Plan

| Step | Skill | Action | Depends On |
|------|-------|--------|---------|
| 7.1 | CO-03 | Check shelf-life compliance — will shipped stock meet minimum remaining shelf-life requirements at destination? | Logistics output + batch selection |
| 7.2 | CO-02 | Validate label requirements — correct labels for destination country? | Logistics output |

Steps 7.1 and 7.2 can run in parallel. Compliance flags are appended to the plan, not halt conditions (unless critical).

---

### Phase 8 — Reporting Agent: Produce Output

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 8.1 | RC-03 | Write ClinOps operational report — stock positions, orders, shipments, risks, site-level detail | All prior phase outputs |

---

### Phase 9 — Supervisor: Close Run

| Step | Skill | Action |
|------|-------|--------|
| 9.1 | SO-07 | Generate run summary — run ID, timing, agents invoked, quality flags, plan score, key findings |
| 9.2 | CO-08 | Log full audit trail — all agent actions with timestamps |

---

## Halt Conditions

| Condition | Detected At | Skill |
|-----------|-------------|-------|
| No demand input (no forecast or baseline) | Phase 1 | SO-01 |
| DI-12 output missing or data integrity FAIL | Phase 2, Step 2.1 | DI-12 |
| Supply network config missing | Phase 2, Step 2.2 | DI-06 |
| Policies config missing | Phase 2, Step 2.3 | DI-07 |
| Critical cold chain gap — no capability on required lane | Phase 6, Step 6.4 | LT-03 |
| No approved vendor for a required lane | Phase 6, Step 6.6 | LT-05 |

On halt, the Supervisor logs the halt reason via CO-08 and produces a run summary via SO-07.

---

## Outputs

| Output | Produced By | Audience |
|--------|-------------|----------|
| Supply plan (orders, quantities, sources, required-by dates) | SI-06 | Supply Team |
| Supply plan score card | SI-09 | Supply Team, Management |
| Supply gap analysis | SI-07 | Supply Team |
| Waste estimate | SI-08 | Supply Team, Finance |
| Shipping requests | LT-06 | Logistics, Execution |
| Compliance flags | CO-02, CO-03 | Quality, Regulatory |
| ClinOps operational report | RC-03 | Clinical Operations |
| Run summary with audit trail | SO-07 + CO-08 | Internal / GxP compliance |

---

## Skill Chain Summary

```
SO-01
  → DI-12 [receive from Supervisor] ┐
  → DI-06                           ┤ (parallel)
  → DI-07                           ┘
    → SI-01
      → SI-02 ┐
      → SI-03 ┘ (parallel)
        → SI-10
      → SI-04 → SI-05
        → SI-06
          → SI-07 ┐
          → SI-08 ┘ (parallel)
            → SI-09
              → LT-01 ┐
              → LT-07 ┘ (parallel)
                → LT-02 ┐
                → LT-03 ┤ (parallel)
                → LT-04 ┘
                  → LT-05 ┐
                  → LT-08 ┘ (parallel)
                    → LT-06
                      → CO-03 ┐
                      → CO-02 ┘ (parallel)
                        → RC-03 → SO-07 + CO-08
```

---

## Notes

- This workflow is typically chained from WF-01 but can run independently when supply conditions change
- The Supply Analyst plans for the scenario specified by the Supervisor (base case by default)
- Batch selection follows FEFO (First Expiry, First Out) throughout
- The Logistics Specialist considers what is already in transit before recommending new shipments
- Compliance checks are non-blocking flags unless severity is critical
- All outputs are RECOMMENDATIONS — human reviewers approve before execution
- The supply plan score gives reviewers a quick quality assessment before diving into detail
