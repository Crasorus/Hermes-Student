# Trade & Logistics Specialist Agent

## What This Agent Does

The Trade & Logistics Specialist handles everything involved in getting clinical supply from a depot to a site. It calculates lead times, plans shipping windows, checks cold chain requirements, validates import documentation, selects approved vendors, and generates the structured shipping request documents that are ready for execution.

This agent turns the Supply Analyst's replenishment decisions into actionable logistics instructions.

---

## What the Logistics Specialist Is Not

- It does not decide how much to order (that is the Supply Analyst)
- It does not forecast demand (that is the Demand Analyst)
- It does not make regulatory compliance decisions (that is the Compliance Manager)
- It does not write stakeholder reports (that is the Reporting Agent)

---

## Skills This Agent Owns

| Skill ID | Skill Name                     |
|----------|--------------------------------|
| LT-01    | Lead Time Calculator           |
| LT-02    | Shipping Window Planner        |
| LT-03    | Cold Chain Requirement Checker |
| LT-04    | Import Requirement Checker     |
| LT-05    | Approved Vendor Selector       |
| LT-06    | Shipping Request Generator     |
| LT-07    | In-Transit Tracker             |
| LT-08    | Customs Documentation Checker  |

**Shared Skills (borrowed):**
| Skill ID | Skill Name                | Owner              |
|----------|---------------------------|--------------------|
| DI-06    | Supply Network Loader     | Shared with Supply Analyst |
| LT-08    | Customs Documentation Checker | Shared with Compliance Manager |

Skills are defined in the shared `/skills/` folder at the project root.

---

## What the Logistics Specialist Needs to Run

**Data files (from Study Package):**
- `data_drops/YYYY-MM-DD/erp_inventory.csv` — Shipments in transit

**Configuration files:**
- `config/supply_network.json` — Depots, countries, lanes, lead times, manufacturing sites

**Reference files:**
- `reference/approved_vendors.json` — Approved couriers, brokers, CMOs with lane assignments

**Context from Supervisor:**
- Supply Analyst outputs (supply plan, order quantities, reorder triggers)
- Required-by dates for shipments
- Temperature sensitivity flags

---

## What the Logistics Specialist Produces

| Output | Description |
|--------|-------------|
| Lead Time Analysis | End-to-end lead time for each shipping lane |
| Shipping Window Plan | Latest ship dates mapped against required-by dates |
| Cold Chain Assessment | Temperature control requirements and lane capability validation |
| Import Requirements Summary | Country-specific permits, licences, documentation needed |
| Vendor Selection | Recommended courier/broker for each lane with rationale |
| Shipping Request | Structured document ready for execution — origin, destination, items, quantities, vendor, dates |
| In-Transit Status Report | Current status of all shipments in transit |

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file — overview and reference guide |
| `system_prompt.md` | The agent's full instructions — its identity, behaviour rules, and skill references |
