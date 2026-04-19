# Clinical Data & Insights Analyst Agent

## What This Agent Does

The Clinical Data & Insights Analyst is the risk intelligence agent. It continuously scans supply chain data for patterns that indicate emerging problems — hot spots, anomalies, trends, and shortage risks. It also calculates KPIs, scores supply plans, and models the probability of stock-outs.

Where other agents focus on "what is" and "what to do", this agent focuses on "what could go wrong" and "what does the data tell us."

---

## What the Insights Analyst Is Not

- It does not calculate demand or enrollment projections (that is the Demand Analyst)
- It does not manage inventory or place orders (that is the Supply Analyst)
- It does not handle logistics (that is the Logistics Specialist)
- It does not enforce compliance rules (that is the Compliance Manager)
- It does not write stakeholder-facing reports (that is the Reporting Agent)

---

## Skills This Agent Owns

| Skill ID | Skill Name                    |
|----------|-------------------------------|
| AI-01    | Hot Spot Detector             |
| AI-02    | Anomaly Detector              |
| AI-03    | Risk Scorer                   |
| AI-04    | Trend Analyser                |
| AI-05    | KPI Calculator                |
| AI-06    | Shortage Probability Modeller |
| AI-07    | Budget Variance Analyser      |
| AI-08    | Comparator Analysis Engine    |
| AI-09    | Waste Root Cause Analyser     |

**Shared Skills (borrowed):**
| Skill ID | Skill Name           | Owner          |
|----------|----------------------|----------------|
| SI-09    | Supply Plan Scorer   | Supply Analyst |

Skills are defined in the shared `/skills/` folder at the project root.

---

## What the Insights Analyst Needs to Run

**Data files (from Study Package):**
- `data_drops/YYYY-MM-DD/rtsm_actuals.csv` — Consumption and enrollment actuals
- `data_drops/YYYY-MM-DD/erp_inventory.csv` — Inventory and shipment data
- `data_drops/YYYY-MM-DD/ctms_plan.csv` — Enrollment plan baseline

**Configuration files:**
- `config/study_config.json` — Thresholds, study parameters
- `config/policies.json` — Budget envelope, safety stock rules

**Context from Supervisor:**
- Outputs from Demand Analyst and Supply Analyst (for trend and risk analysis)
- Historical run data (for trend comparison across cycles)
- Specific risk questions or surveillance requests

---

## What the Insights Analyst Produces

| Output | Description |
|--------|-------------|
| Hot Spot Alert | Sites, countries, or depots showing risk patterns (stock-outs, expiry clusters, shipment delays) |
| Anomaly Report | Statistical anomalies in consumption, enrollment, or inventory data |
| Risk Score Card | Risk scores by site, country, and depot — with contributing factors |
| Trend Analysis | Directional trends in consumption, enrollment, waste, and cost over time |
| KPI Dashboard Data | Standard supply chain KPIs: service level, waste %, on-time delivery, cost per patient |
| Shortage Probability Model | Estimated probability of stock-out by site/country within defined time horizon |
| Budget Variance Report | Actual spend vs. budget envelope — with variance explanations |
| Waste Root Cause Analysis | Patterns in overage and waste with identified root causes |

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file — overview and reference guide |
| `system_prompt.md` | The agent's full instructions — its identity, behaviour rules, and skill references |
