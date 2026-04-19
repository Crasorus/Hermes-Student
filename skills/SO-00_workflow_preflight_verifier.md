# SO-00: Workflow Pre-Flight Verifier

**Skill ID:** SO-00
**Category:** Supervisor & Orchestration
**Owner:** Supervisor Agent
**Depends on:** DI-12 (Aggregate Data Query Tool)

---

## Purpose

SO-00 defines the **mandatory pre-flight policy** that must run at the start of every workflow, before any agent processes data. It delegates data loading and validation to **DI-12: Aggregate Data Query Tool**, which is the mechanic. SO-00 is the enforcement rule.

This skill exists to prevent a class of errors that occurred before its introduction: agents counting directly from raw CSV files, producing inconsistent figures, and generating reports with contradictory numbers. SO-00 eliminates that possibility by making a single, verified, pre-computed data summary the only source of truth for all downstream agents.

---

## When This Skill Runs

**Always. Without exception.**

SO-00 is Step 0 of every workflow execution. It runs before:
- SO-01 (Workflow Router)
- Any data ingestion skill
- Any agent invocation

There are no workflows for which SO-00 is optional.

---

## Steps

### Step 1: Execute DI-12

Invoke **DI-12: Aggregate Data Query Tool** (see `skills/DI-12_aggregate_data_query_tool.md`) passing the study's data drop files:
- RTSM actuals CSV
- CTMS plan CSV
- ERP inventory CSV
- Study config JSON

DI-12 will load all CSV files, compute aggregations, run 8 data integrity checks, and return a structured JSON output. How DI-12 is invoked depends on the execution environment — the runner handles this automatically.

### Step 2: Evaluate the Integrity Status

Read the `overall_data_integrity` field from DI-12 output:

| Status | Action |
|--------|--------|
| **PASS** | Log success. Continue to Step 3. |
| **WARNING** | Log all warnings. Set `data_quality_flag = "WARNINGS"`. Continue to Step 3 with caution. |
| **FAIL** | **HALT IMMEDIATELY.** Report all issues from `data_integrity_checks` and `recommendations`. Do not proceed. |

When halting on FAIL:
- Document halt reason in audit trail with full DI-12 output
- Return a structured error report explaining which integrity checks failed
- Do not invoke any downstream agent

### Step 3: Store and Distribute DI-12 Output

- Store the complete DI-12 JSON as `context.di12_output`
- Pass `context.di12_output` to **every agent** invoked in this workflow run
- All agents MUST extract counts from `di12_output` — never from raw CSV

### Step 4: Log Pre-Flight in Audit Trail

Record in the audit trail:
- Timestamp of SO-00 execution
- DI-12 status (PASS / WARNING / FAIL)
- Any warnings or recommendations returned by DI-12
- Reference key: `di12_preflight_<timestamp>`

---

## Rules All Downstream Agents Must Follow

These rules are enforced by SO-00. All agents receive them as part of their invocation context:

1. **NO MANUAL COUNTING** — All numeric figures come from `di12_output`. Agents must never count rows from raw CSV files.
2. **CHECK INTEGRITY FIRST** — Each agent must verify `di12_output["overall_data_integrity"]` before processing. Halt if "FAIL".
3. **HALT IF DI-12 MISSING** — If `context.di12_output` is absent, halt and request it from Supervisor. Never proceed without it.
4. **AUDIT TRAIL TRACEABILITY** — All count references must use the format: `"DI-12 verified: [count] [metric]"` (e.g., "DI-12 verified: 72 randomisations").
5. **WARNING FLAG PROPAGATION** — If DI-12 status is "WARNING", all agent outputs must carry `data_quality_flag: "WARNINGS"`.

---

## Data Structure Reference

DI-12 output contains the following sections that agents draw from:

| Section | Contains |
|---------|----------|
| `rtsm_aggregations` | Randomisations, dispensings, screen failures — by site, arm, item |
| `ctms_aggregations` | Enrollment plan by site, country, visit schedules |
| `erp_aggregations` | Stock on hand, in-transit, on-order, batch expiry |
| `site_inventory_aggregations` | Site-level current inventory and reorder status |
| `derived_metrics` | Pre-computed: enrollment delta, demand rate, supply coverage |
| `data_integrity_checks` | Results of 8 validation checks |
| `overall_data_integrity` | PASS / WARNING / FAIL — the gate |

---

## Relationship to DI-12

SO-00 is the **policy**. DI-12 is the **tool**.

- SO-00 defines when DI-12 runs (always, first), what to do with its output, and what happens if it fails
- DI-12 defines how data is loaded, aggregated, and validated
- Neither replaces the other — both are required for the system to function correctly

See `skills/DI-12_aggregate_data_query_tool.md` for the full DI-12 specification.
