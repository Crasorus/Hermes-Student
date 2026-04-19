# GxP Compliance Manager Agent

## What This Agent Does

The GxP Compliance Manager is the guardrail agent. It ensures that every decision, recommendation, and action across the agent team is compliant with the study protocol, regulatory requirements, and company SOPs.

Unlike other agents that run in specific workflows, the Compliance Manager is **cross-cutting** — its audit trail skill (CO-08) is implicitly active in every workflow. It validates protocol compliance, label requirements, shelf life rules, and expiry dating. It also assesses the supply chain impact of protocol amendments and deviations.

---

## What the Compliance Manager Is Not

- It does not forecast demand (that is the Demand Analyst)
- It does not manage inventory or calculate orders (that is the Supply Analyst)
- It does not plan shipments (that is the Logistics Specialist)
- It does not write stakeholder reports (that is the Reporting Agent)
- It does not make supply chain decisions — it validates that decisions made by other agents are compliant

---

## Skills This Agent Owns

| Skill ID | Skill Name                      |
|----------|---------------------------------|
| DI-08    | Reference Document Loader       |
| CO-01    | Protocol Compliance Checker     |
| CO-02    | Label Requirements Validator    |
| CO-03    | Shelf Life Compliance Checker   |
| CO-04    | Expiry Date Rule Enforcer       |
| CO-05    | Protocol Change Impact Assessor |
| CO-06    | Deviation Impact Assessor       |
| CO-07    | Destruction Eligibility Checker |
| CO-08    | Audit Trail Logger              |
| CO-09    | SOP Reference Checker           |
| CO-10    | Regulatory Change Alerter       |

**Shared Skills (borrowed):**
| Skill ID | Skill Name                | Owner              |
|----------|---------------------------|--------------------|
| SI-03    | Expiry Profile Analyser   | Supply Analyst     |
| SI-10    | Batch Selection Advisor   | Supply Analyst     |
| DI-07    | Policy Loader             | Supply Analyst     |
| LT-08    | Customs Documentation Checker | Logistics Specialist |
| CO-08    | Audit Trail Logger        | Shared with Supervisor |

Skills are defined in the shared `/skills/` folder at the project root.

---

## What the Compliance Manager Needs to Run

**Reference files (from Study Package):**
- `reference/shelf_life_by_country.json` — Minimum remaining shelf life at shipment per country
- `reference/label_requirements.json` — Language, content, format requirements per country
- `reference/approved_vendors.json` — Approved vendors with lane assignments

**Configuration files:**
- `config/study_config.json` — Protocol parameters, treatment arms
- `config/policies.json` — Safety stock rules, expiry rules, SOP references

**Context from Supervisor:**
- Outputs from other agents requiring compliance validation
- Protocol amendment documents (for change assessments)
- Deviation reports (for impact assessments)

---

## What the Compliance Manager Produces

| Output | Description |
|--------|-------------|
| Compliance Sign-off Record | Confirms that demand assumptions or supply decisions are protocol-compliant |
| Label Validation Report | Confirms label requirements are met for each country in the plan |
| Shelf Life Compliance Report | Confirms batches meet minimum shelf life for destination countries |
| Protocol Change Impact Report | Full assessment of a protocol amendment's supply chain implications |
| Deviation Impact Report | Assessment of a reported deviation's impact on supply chain |
| Destruction Eligibility Report | Which stock is eligible for destruction and why |
| Audit Trail | Timestamped log of every agent action, decision, and data reference |
| Regulatory Change Alert | Flags when reference documents have changed since the last run |

---

## Cross-Cutting Behaviour

The Compliance Manager's **CO-08: Audit Trail Logger** skill is active in every workflow — not just when the Compliance Manager is explicitly invoked. The Supervisor ensures this by including audit trail entries in every run output.

When the Compliance Manager detects a compliance issue:
- It returns a **NON-COMPLIANT** flag with detailed explanation
- The Supervisor may loop the originating agent back to revise its output
- The Compliance Manager does not block or override — it flags and explains

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file — overview and reference guide |
| `system_prompt.md` | The agent's full instructions — its identity, behaviour rules, and skill references |
