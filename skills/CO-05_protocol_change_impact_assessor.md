# CO-05 — Protocol Change Impact Assessor

## Purpose

Read a protocol amendment and identify all supply chain implications — changes to treatment arms, doses, visit schedules, countries, or sites that affect demand, inventory, or logistics.

---

## Owner

**Primary:** GxP Compliance Manager, Demand & Forecast Analyst (shared)

---

## When This Skill Is Used

- When a protocol amendment is received (WF-03 — Protocol Amendment Impact)

---

## Inputs

1. **Protocol amendment document** — The amendment content
2. **Study configuration** — Current protocol parameters for comparison

---

## Steps

1. **Parse the amendment** — Identify what is changing (arms, doses, visits, countries, sites, pack sizes, etc.)
2. **Assess demand impact** — Will the change increase or decrease demand? By how much?
3. **Assess inventory impact** — Does existing stock become obsolete? Is relabelling needed?
4. **Assess logistics impact** — Are new shipping lanes or vendors needed? Do lead times change?
5. **Assess compliance impact** — Do label requirements, shelf life rules, or import requirements change?
6. **Produce impact report** — All implications categorised by area and severity

---

## Output

- List of changes identified in the amendment
- Impact assessment by area (demand, inventory, logistics, compliance)
- Severity of each impact (HIGH, MEDIUM, LOW)
- Recommended actions for each impact
- Whether the amendment triggers a demand re-forecast (DF-06)

---

## Notes

- Protocol amendments can have cascading supply chain effects — this skill ensures nothing is overlooked
- The impact report feeds into the Reporting Agent (RC-06) for the Protocol Change Impact Report
