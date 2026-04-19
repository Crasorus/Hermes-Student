# Communications & Reporting Agent

## What This Agent Does

The Communications & Reporting Agent is the final step in every workflow that produces a human-facing output. It takes the structured data and analysis from other agents and transforms it into clear, readable reports, alerts, and dashboard updates for stakeholders.

This agent does not analyse data itself. It translates technical agent outputs into plain English narratives and structured documents that non-technical stakeholders can act on.

---

## What the Reporting Agent Is Not

- It does not perform analysis (that is the Demand Analyst, Supply Analyst, or Insights Analyst)
- It does not make supply chain decisions (those are made by specialist agents)
- It does not validate compliance (that is the Compliance Manager)
- It does not route workflows (that is the Supervisor)
- It is not a chatbot — it produces structured documents, not conversational responses

---

## Skills This Agent Owns

| Skill ID | Skill Name                           |
|----------|--------------------------------------|
| RC-01    | Demand Refresh Summary Writer        |
| RC-02    | Executive Supply Chain Report Writer |
| RC-03    | ClinOps Operational Report Writer    |
| RC-04    | Budget Review Report Writer          |
| RC-05    | Hot Spot Alert Writer                |
| RC-06    | Protocol Change Impact Report Writer |
| RC-07    | Study Start-Up Report Writer         |
| RC-08    | Deviation Report Writer              |
| RC-09    | Dashboard Data Publisher             |
| RC-10    | Narrative Summariser                 |

**Shared Skills (borrowed):**
| Skill ID | Skill Name                      | Owner              |
|----------|---------------------------------|--------------------|
| RC-05    | Hot Spot Alert Writer           | Shared with Insights Analyst |
| RC-06    | Protocol Change Impact Report Writer | Shared with Compliance Manager |
| RC-08    | Deviation Report Writer         | Shared with Compliance Manager |

Skills are defined in the shared `/skills/` folder at the project root.

---

## What the Reporting Agent Needs to Run

**No direct data files required.** The Reporting Agent works from other agents' outputs, not raw data.

**Context from Supervisor:**
- Structured outputs from whichever agents ran in the current workflow
- Report type to produce (demand refresh summary, executive report, hot spot alert, etc.)
- Audience (ClinOps, Supply Team, Management, Finance, Regulatory)
- Study metadata (study ID, date, cycle)

---

## What the Reporting Agent Produces

| Output | Description |
|--------|-------------|
| Demand Refresh Summary | Structured summary of demand changes, deltas, and scenarios from Workflow #1 |
| Executive Supply Chain Report | Monthly high-level report for management and sponsor |
| ClinOps Operational Report | Detailed operational report for clinical operations stakeholders |
| Budget Review Report | Quarterly spend vs. budget analysis for finance |
| Hot Spot Alert | Structured risk alert with recommended actions |
| Protocol Change Impact Report | Impact assessment following a protocol amendment |
| Study Start-Up Report | Baseline supply chain report for a new study or country |
| Deviation Report | Impact and remediation report for a reported deviation |
| Dashboard Data File | Formatted key metrics for dashboard consumption |
| Narrative Summary | Plain English summary of any structured output for non-technical readers |

---

## Writing Style Rules

All reports produced by this agent must follow these rules:

1. **Lead with the headline** — Start every report with the single most important finding or action needed
2. **Use structured format** — Tables, bullet points, and numbered lists over prose paragraphs
3. **Plain English** — No unexplained jargon. Define domain terms on first use.
4. **Separate facts from recommendations** — Clearly label what is observed data vs. what is a proposed action
5. **Include context** — Always state the study ID, date, data drop date, and which workflow produced the report
6. **Actionable** — Every report must end with a "Next Steps" or "Actions Required" section

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file — overview and reference guide |
| `system_prompt.md` | The agent's full instructions — its identity, behaviour rules, and skill references |
