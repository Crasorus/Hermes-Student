# Your Task: Build the Optimization Agent

<!-- ============================================================
     STUDENT HANDOUT — Read this before starting Module 4.
     This tells you WHAT the agent should do.
     YOU must decide HOW to build it.
     ============================================================ -->

## What Is the Optimization Agent?

The Optimization Agent looks for waste in the clinical supply chain. It reads the current state of inventory, batches, and shipments — and finds things that should be fixed **right now**.

It is not a forecasting agent. It does not predict the future. It evaluates what is happening today and asks:

> **"What is being wasted, and what can we do about it?"**

This agent sits alongside the existing team:

| Agent | Focus |
|---|---|
| Demand Analyst | What is needed |
| Supply Analyst | What is available |
| Logistics Specialist | What is moving |
| **Your Agent** | **What is being wasted** |

---

## What Should Your Agent Be Able to Find?

Here are examples of the kinds of findings your agent should produce. Use these as inspiration — your agent should be able to detect these patterns from the data.

### Excess Inventory
- Depot EU-01 is holding **14 weeks** of supply. The policy maximum is **10 weeks**.
- Depot AP-02 has **180 units** above the reorder ceiling for ARM-B.

### Expiry Risk
- Lot **A123** expires in **6 weeks**. At the current consumption rate, only 40% of the lot will be used.
- Lot **B456** at depot US-01 has a remaining shelf life of **35 days** with minimal dispensing activity.

### Idle Inventory
- Site **US-05** holds **8 weeks** of supply but has had **zero dispensing events** in the last 3 weeks.
- Site **DE-03** has enrollment paused but received a full resupply shipment 10 days ago.

### Flow Inefficiencies
- **3 emergency shipments** were triggered on the EU-01 → UK-02 lane in the last 30 days.
- Site **FR-01** has received **4 resupply shipments** in 30 days for the same item — the replenishment trigger may be set too low.

---

## What Should Your Agent Recommend?

After finding these issues, your agent should recommend **1–3 concrete actions**. Examples:

> *"Rebalance 40 units from Depot EU-01 to Site US-05, which is below safety stock."*

> *"Prioritise Lot A123 for dispensing at DE-03 to reduce expiry waste. Expected waste if no action: 24 units."*

> *"Review the replenishment trigger for ARM-A at FR-01 — 4 resupply events in 30 days indicates over-triggering."*

**Rules for good recommendations:**
- Always name the specific depot, lot, or site — never be vague
- Always cite the evidence (what number made you say this?)
- Maximum 3 recommendations — prioritise the most urgent

---

## What Signals Should Your Agent Emit?

At the end of its analysis, your agent must emit one of these signals:

| Signal | When to Emit |
|---|---|
| `OPTIMIZATION_OPPORTUNITY` | One or more inefficiencies were found |
| `NO_ACTION` | No significant inefficiencies detected |
| `CRITICAL_WASTE_RISK` | Severe expiry or excess risk requiring urgent escalation |

These signals are how your agent communicates with the workflow runner and other agents.

---

## What Data Does Your Agent Have Access To?

Your agent can read these files (already in your study package):

| File | What It Contains |
|---|---|
| `data_drops/YYYY-MM-DD/erp_inventory.csv` | Depot stock levels, batch expiry dates, shipment records |
| `data_drops/YYYY-MM-DD/site_inventory.csv` | Site-level stock, weekly demand, reorder points |
| `config/policies.json` | Max stock weeks, shelf life thresholds |
| `config/supply_network.json` | Lead times, depot and site network |
| `config/study_config.json` | Enrollment plan, treatment arms |

---

## What You Must Build

By the end of the lab, you need:

1. **4–5 skill files** in `/skills/` — one for each type of analysis your agent can do
   - Use `lab/templates/skill_template.md` as your template
   - Name them with the prefix `OA-` (e.g., `OA-01_my_skill_name.md`)

2. **An agent folder** in `/agents/optimization_agent/` with:
   - `README.md` — what your agent does, what it needs, what it produces
   - `system_prompt.md` — the full instructions your agent follows

3. **A workflow** `WF-OA-01` added to `workflows/workflows.json`
   - One step: your optimization_agent, with a task description

Then run:
```
/run-workflow-chain MY-STUDY-01 WF-01 WF-OA-01
```

---

## Tips

> **Tip:** Write your skills before your system prompt. The system prompt references the skills — it is easier to write when the skills already exist.

> **Tip:** Look at `agents/supervisor/system_prompt.md` as a completed example before writing your own.

> **Tip:** Your skills do not need to be perfect. Focus on: clear purpose, clear inputs, clear steps, clear output.

> **Tip:** Ask Claude Code: *"Does my system_prompt.md reference all my OA- skills?"*
