# WF-OA-01 — Optimization Analysis

> **Reference document only.** Runtime step definitions and task descriptions are in `workflows/workflows.json`. This file is for human understanding of the workflow design.

## Purpose

Analyse the current state of the clinical supply chain to identify waste and inefficiency. This workflow finds excess inventory, expiry-risk lots, idle site stock, and poor shipment flow patterns — then produces 1–3 concrete, evidence-backed recommendations.

This workflow does not forecast demand or generate a supply plan. It evaluates what is happening right now and asks: **what is being wasted, and what can be done about it today?**

---

## Trigger

Run on demand after a data drop, or chained after WF-01 (Demand Signal Refresh) to add an optimization perspective to a demand cycle.

Typical chain: `/run-workflow-chain MY-STUDY-01 WF-01 WF-OA-01`

---

## Agents Involved

1. **Supervisor** *(via WF-01 pre-chain)* — Data validation and intake
2. **Optimization Agent** — Inefficiency detection and recommendation

> **Note:** WF-OA-01 assumes WF-01 has already run in the same chain. The Optimization Agent will HALT if Supervisor emitted HALT in the prior step.

---

## Workflow Phases

### Phase 1 — Optimization Agent: Data Check

| Step | Action | Halt If |
|------|--------|---------|
| 1.1 | Confirm `erp_inventory.csv` is present in the current data drop | File missing or empty |
| 1.2 | Confirm `site_inventory.csv` is present in the current data drop | File missing or empty |
| 1.3 | Confirm `policies.json` is readable and contains `max_stock_weeks` | File missing |

If all files are present, proceed. If any are missing, HALT and report which file is needed.

---

### Phase 2 — Optimization Agent: Evidence Collection (OA-01 through OA-04)

All four evidence skills run in sequence. Each skill reads data independently and returns a findings list (which may be empty — that is a valid result).

| Step | Skill | Action | Data Source |
|------|-------|--------|-------------|
| 2.1 | OA-01 | Excess Inventory Detector — flag depots above max stock weeks policy | `erp_inventory.csv` + `policies.json` |
| 2.2 | OA-02 | Expiry Exposure Analyser — identify lots at expiry risk vs. consumption rate | `erp_inventory.csv` + `policies.json` |
| 2.3 | OA-03 | Idle Inventory Detector — flag sites with unconsumed stock | `site_inventory.csv` + `study_config.json` |
| 2.4 | OA-04 | Flow Inefficiency Detector — detect emergency shipment and delay patterns | `erp_inventory.csv` + `supply_network.json` |

Steps 2.1–2.4 are logically independent and read from different data perspectives (depot stock, lot expiry, site velocity, shipment history).

---

### Phase 3 — Optimization Agent: Synthesis (OA-05)

| Step | Skill | Action | Depends On |
|------|-------|--------|------------|
| 3.1 | OA-05 | Optimization Recommender — synthesise all findings into 1–3 concrete actions and emit routing signal | All Phase 2 outputs |

**Signal decision logic:**

| Condition | Signal Emitted |
|-----------|---------------|
| All four evidence skills returned empty lists | `NO_ACTION` |
| Any findings exist | `OPTIMIZATION_OPPORTUNITY` |
| OA-02 has CRITICAL-risk lots AND OA-01 has excess at the same location | `CRITICAL_WASTE_RISK` |

---

### Phase 4 — Optimization Agent: Output

| Step | Action |
|------|--------|
| 4.1 | Package findings summary (counts by category), findings detail (named depots/lots/sites), recommendations (1–3 with priority and evidence), routing signal, and audit trail |
| 4.2 | Return output to Supervisor (or workflow chain runner) |

---

## Halt Conditions

| Condition | Detected At | Action |
|-----------|-------------|--------|
| `erp_inventory.csv` missing or empty | Phase 1, Step 1.1 | HALT — report missing file |
| `site_inventory.csv` missing or empty | Phase 1, Step 1.2 | HALT — report missing file |
| `policies.json` missing | Phase 1, Step 1.3 | HALT — report missing file |
| Supervisor emitted HALT in prior workflow | Before Phase 1 | HALT — do not run |

---

## Outputs

| Output | Description | Audience |
|--------|-------------|----------|
| Excess Inventory Report | Depots above policy max, excess quantified in weeks and units | Supply team |
| Expiry Risk Report | Lots ranked by days to expiry and projected waste units | Supply team, Logistics |
| Idle Inventory Report | Sites with unconsumed stock, ranked by weeks of supply | ClinOps, Supply team |
| Flow Inefficiency Report | Emergency shipments, repeat resupply, shipping delays | Logistics, Supply team |
| Optimization Recommendations | 1–3 evidence-backed actions with priority (CRITICAL/HIGH/MEDIUM/LOW) | Supply team, ClinOps |
| Routing Signal | `OPTIMIZATION_OPPORTUNITY`, `NO_ACTION`, or `CRITICAL_WASTE_RISK` | Workflow runner |

---

## Skill Chain Summary

```
[WF-01 Supervisor validation — must complete before WF-OA-01 runs]
        ↓
  erp_inventory.csv ─┐
  site_inventory.csv ─┤─ Data Check (Phase 1)
  policies.json ──────┘
        ↓
  OA-01 (depot excess)    ─┐
  OA-02 (expiry risk)     ─┤─ Evidence Collection (Phase 2, sequential)
  OA-03 (idle sites)      ─┤
  OA-04 (flow patterns)   ─┘
        ↓
  OA-05 (synthesise + recommend + emit signal)
        ↓
  [NO_ACTION] ──────────────────────── end
  [OPTIMIZATION_OPPORTUNITY] ────────── output recommendations
  [CRITICAL_WASTE_RISK] ─────────────── output + escalate
```

---

## Notes

- This workflow is intentionally read-only — it never writes back to the study package
- All recommendations are labelled RECOMMENDATION; none are executed automatically
- The four evidence skills (OA-01 through OA-04) cover different inefficiency types and do not overlap: OA-01 is depot-level quantity, OA-02 is lot-level time-to-expiry, OA-03 is site-level consumption velocity, OA-04 is shipment flow patterns
- `CRITICAL_WASTE_RISK` requires both an expiry problem (OA-02) AND an excess problem (OA-01) at the same location — a single signal alone is not enough to escalate
- Best run as part of a chain: `/run-workflow-chain MY-STUDY-01 WF-01 WF-OA-01`
