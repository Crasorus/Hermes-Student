# Optimization Agent

<!-- ============================================================
     REFERENCE ANSWER — For instructor/student review after the lab.
     This README is the agent's "front door" — it explains what the
     agent does before you read the system prompt.
     ============================================================ -->

## What This Agent Does

<!-- WHAT IT DOES: 3-4 sentences. Explain the core purpose.
     Emphasise that this is a CURRENT STATE agent — no forecasting.
     The "meta-agent" framing is important — it crosses all domains. -->

The Optimization Agent identifies current-state supply chain inefficiencies. It reads inventory, expiry, site stock, and shipment data to find waste — excess holdings, expiry-risk lots, idle site stock, and poor flow patterns — then recommends 1–3 concrete actions to address the highest-priority findings.

This agent does not forecast demand or plan future supply. It evaluates what is happening right now and asks: **what is being wasted, and what can be done about it today?**

It is a cross-cutting agent — it draws on data from depots, sites, and shipment history that no single domain agent (demand, supply, logistics) examines together.

---

## What This Agent Is Not

<!-- WHAT IT IS NOT: Explicit scope boundaries.
     Students often confuse this agent with the Supply Analyst or Logistics Specialist. -->

- It does not forecast demand (that is the Demand Analyst)
- It does not calculate reorder quantities or generate supply plans (that is the Supply Analyst)
- It does not select vendors or generate shipping requests (that is the Logistics Specialist)
- It does not validate GxP compliance (that is the Compliance Manager)
- It does not generate stakeholder reports (that is the Reporting Agent)

---

## Skills This Agent Owns

<!-- SKILLS TABLE: List every skill with its ID and one-line description.
     IDs must match the file names in /skills/ exactly. -->

| Skill ID | Skill Name | What It Does |
|---|---|---|
| OA-01 | Excess Inventory Detector | Flags depots holding above max stock weeks policy |
| OA-02 | Expiry Exposure Analyser | Identifies lots at expiry risk vs. consumption rate |
| OA-03 | Idle Inventory Detector | Flags sites with stock not being consumed |
| OA-04 | Flow Inefficiency Detector | Detects emergency shipment and delay patterns |
| OA-05 | Optimization Recommender | Synthesises findings into 1–3 concrete actions |

Skills are defined in the shared `/skills/` folder at the project root.

---

## What This Agent Needs to Run

<!-- INPUTS SECTION: List every file the agent reads.
     Split into data files (change each cycle) and config files (set once per study).
     Students need to know exactly which files to check when the agent fails. -->

**Data files (from current data drop):**
- `data_drops/YYYY-MM-DD/erp_inventory.csv` — depot stock, batches, expiry dates, shipment records
- `data_drops/YYYY-MM-DD/site_inventory.csv` — site-level stock and weekly demand

**Configuration files:**
- `config/policies.json` — max stock weeks, shelf life thresholds
- `config/supply_network.json` — standard lead times per lane
- `config/study_config.json` — enrollment plan by site (context for idle stock)

**Context from prior agents (via workflow chain):**
- WF-01 Supervisor output — data validation result (agent will not run if HALT was emitted)

---

## What This Agent Produces

<!-- OUTPUTS TABLE: List every output document this agent can return.
     Keep it concrete — what file or section gets written? -->

| Output | Description |
|---|---|
| Excess Inventory Report | Depots exceeding max stock weeks, with excess quantified in weeks and units |
| Expiry Risk Report | Lots at risk of expiry before consumption, ranked by urgency |
| Idle Inventory Report | Sites with unconsumed stock, ranked by weeks of supply |
| Flow Inefficiency Report | Emergency shipments, repeat resupply, and delay patterns |
| Optimization Recommendations | 1–3 concrete, evidence-backed actions with priority and rationale |
| Routing Signal | `OPTIMIZATION_OPPORTUNITY`, `NO_ACTION`, or `CRITICAL_WASTE_RISK` |

---

## Files in This Folder

| File | Purpose |
|---|---|
| `README.md` | This file — agent overview and reference guide |
| `system_prompt.md` | Full agent instructions — identity, skills, procedure, rules |
