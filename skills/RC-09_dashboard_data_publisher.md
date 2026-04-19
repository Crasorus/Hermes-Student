# RC-09 — Dashboard Data Publisher

## Purpose

Format and publish key metrics into a structured output file that can be consumed by a dashboard tool or visualisation system.

---

## Owner

**Primary:** Communications & Reporting Agent

---

## When This Skill Is Used

- At the end of every cycle that produces metrics
- Alongside any report that generates KPIs or status data

---

## Inputs

1. **KPIs** — From AI-05
2. **Risk scores** — From AI-03
3. **Stock position summary** — From SI-01
4. **Hot spots** — From AI-01 (if any)

---

## Steps

1. **Collect all publishable metrics** from agent outputs
2. **Format each metric** with name, value, unit, comparison to target, comparison to previous cycle, and trend direction
3. **Structure as a machine-readable output** — Consistent format that a dashboard tool can ingest
4. **Include metadata** — Study ID, date, data drop date, run ID

---

## Output

- Structured dashboard data file with all key metrics
- Each metric includes: name, value, unit, vs. target, vs. previous, trend

---

## Notes

- The dashboard data format should be simple and consistent across cycles
- This skill does not create visualisations — it produces the data that a dashboard tool would consume
