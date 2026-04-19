# RC-01 — Demand Refresh Summary Writer

## Purpose

Produce the structured demand refresh summary document from WF-01 output. This is the primary deliverable of the Demand Signal Refresh workflow.

---

## Owner

**Primary:** Communications & Reporting Agent

---

## When This Skill Is Used

- At the end of WF-01 (Demand Signal Refresh)

---

## Inputs

1. **DI-12 output** — Enrollment counts by site, enrollment rates, data integrity checks, derived metrics
2. **Demand Analyst outputs** — Delta report, scenario matrix, enrollment trajectory, consumption analysis
3. **Compliance Manager output** — Compliance sign-off (if applicable)
4. **Supervisor context** — Study ID, data drop date, trigger reason

---

## Steps

1. **Lead with the headline** — What is the single most important demand finding?
2. **Present enrollment summary table** — Patient counts by site from DI-12 (for visual human checkpoint)
3. **Summarise the deltas** — Which items/countries have significant changes and in what direction?
4. **Present scenarios** — Base, optimistic, and pessimistic side by side
5. **Include enrollment trajectory** — Planned vs. projected completion, enrollment rates
6. **Note compliance status** — Did the Compliance Manager flag anything?
7. **State next steps** — Does this trigger a supply plan adjustment? Who needs to act?
8. **Include traceability** — Run ID, data sources, agents involved

---

## Output

- Structured demand refresh summary document following the standard report template
- Audience: ClinOps, Supply Team

---

## Report Sections

The demand refresh summary must include:

1. **Header** — Study ID, report date, data drop date, report type, prepared by, version
2. **Executive Summary** — Single most important finding in 2-3 sentences
3. **Enrollment Summary** — Table with patient counts by site (from DI-12):
   - Columns: Site ID, Site Name, Planned Enrollment, Actual Enrollment, Delta, Delta %, Enrollment Rate (patients/week)
   - Sorted by actual enrollment (descending)
   - Highlight any sites with enrollment >20% above or below plan
   - Include total row
4. **Key Findings** — Bullet points of critical data
5. **Demand Delta Analysis** — Which items/countries have significant changes
6. **Scenarios** — Base, optimistic, pessimistic with total demand and completion dates
7. **Risks and Flags** — Any issues requiring attention
8. **Recommendations** — Proposed actions (e.g., trigger supply plan, continue monitoring)
9. **Next Steps** — Who needs to act and by when
10. **Traceability** — Run ID, data sources, agents involved, workflow reference

## Notes

- The Enrollment Summary table (step 3) is the **visual human checkpoint** — it allows supply team to see enrollment patterns by site before any supply decisions are triggered
- This report must be self-explanatory — a reader should understand the situation without asking follow-up questions
- If any site shows anomalous enrollment patterns (e.g., spike, lag), flag it explicitly in the Risks section
