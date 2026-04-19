# Supply & Inventory Analyst Agent

## What This Agent Does

The Supply & Inventory Analyst is responsible for understanding what stock is available, where it is, and whether it is sufficient to meet projected demand. It analyses inventory positions across depots and countries, profiles batch expiry dates, checks safety stock thresholds, and calculates order quantities when replenishment is needed.

This agent bridges the gap between what the Demand Analyst says is needed and what the Logistics Specialist needs to ship. It produces the supply plan.

---

## What the Supply Analyst Is Not

- It does not calculate demand or forecast enrollment (that is the Demand Analyst)
- It does not handle shipping logistics or vendor selection (that is the Logistics Specialist)
- It does not validate regulatory compliance (that is the Compliance Manager)
- It does not produce stakeholder reports (that is the Reporting Agent)

---

## Skills This Agent Owns

| Skill ID | Skill Name                 |
|----------|----------------------------|
| DI-04    | ERP Inventory Parser       |
| DI-06    | Supply Network Loader      |
| DI-07    | Policy Loader              |
| SI-01    | Stock Position Calculator  |
| SI-02    | Weeks of Supply Calculator |
| SI-03    | Expiry Profile Analyser    |
| SI-04    | Safety Stock Checker       |
| SI-05    | Reorder Trigger Evaluator  |
| SI-06    | Order Quantity Calculator  |
| SI-07    | Supply Gap Identifier      |
| SI-08    | Overage & Waste Estimator  |
| SI-09    | Supply Plan Scorer         |
| SI-10    | Batch Selection Advisor    |

**Shared Skills (borrowed):**
| Skill ID | Skill Name                    | Owner              |
|----------|-------------------------------|--------------------|
| SI-09    | Supply Plan Scorer            | Shared with Insights Analyst |
| SI-03    | Expiry Profile Analyser       | Shared with Compliance Manager |
| SI-10    | Batch Selection Advisor       | Shared with Compliance Manager |
| DI-06    | Supply Network Loader         | Shared with Logistics Specialist |
| DI-07    | Policy Loader                 | Shared with Compliance Manager |

Skills are defined in the shared `/skills/` folder at the project root.

---

## What the Supply Analyst Needs to Run

**Data files (from Study Package):**
- `data_drops/YYYY-MM-DD/erp_inventory.csv` — Stock on hand, batches, orders, shipments in transit

**Configuration files:**
- `config/study_config.json` — Treatment arms, pack sizes
- `config/supply_network.json` — Depots, countries, lanes, lead times
- `config/policies.json` — Safety stock rules, reorder points, budget envelope

**Context from Supervisor:**
- Demand Analyst outputs (delta report, scenario demand matrix)
- Workflow context (which workflow triggered this, data quality flag)

---

## What the Supply Analyst Produces

| Output | Description |
|--------|-------------|
| Stock Position Report | Current stock by depot, country, treatment arm, item — with weeks of supply |
| Expiry Profile | Batch expiry dates mapped against projected consumption — flags expiry risk |
| Safety Stock Status | Which locations are at, below, or approaching safety stock thresholds |
| Supply Plan | Recommended order quantities, reorder triggers, and replenishment schedule |
| Supply Gap Analysis | Where projected demand exceeds available supply across the planning horizon |
| Overage & Waste Estimate | Projected overage and waste at study end under current supply plan |
| Supply Plan Score Card | Plan scored on efficiency, risk, cost, and complexity |

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file — overview and reference guide |
| `system_prompt.md` | The agent's full instructions — its identity, behaviour rules, and skill references |
