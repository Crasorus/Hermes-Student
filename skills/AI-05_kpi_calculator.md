# AI-05 — KPI Calculator

## Purpose

Calculate standard supply chain KPIs that measure the health and efficiency of the clinical supply operation.

---

## Owner

**Primary:** Clinical Data & Insights Analyst

---

## When This Skill Is Used

- During reporting workflows to provide performance metrics
- During plan scoring to assess plan quality
- For dashboard data publishing (RC-09)

---

## Inputs

1. **Stock position** — From SI-01
2. **Consumption rates** — From DF-01
3. **Waste estimate** — From SI-08
4. **In-transit status** — From LT-07
5. **Budget data** — From DI-07
6. **Previous cycle KPIs** — For comparison (if available)

---

## Steps

1. **Calculate service level** — Percentage of demand that was fulfilled on time
2. **Calculate waste percentage** — Projected waste as a percentage of total supply
3. **Calculate on-time delivery** — Percentage of shipments that arrived by the required-by date
4. **Calculate cost per patient** — Total supply chain spend divided by enrolled patients
5. **Calculate inventory turnover** — How quickly stock is being consumed relative to holdings
6. **Compare to previous cycle** — Show the change for each KPI
7. **Compare to targets** — If target values are defined, show performance vs. target

---

## Output

- KPI values for the current cycle
- Change vs. previous cycle (where available)
- Performance vs. targets (where defined)
- Summary assessment of supply chain health

---

## Notes

- KPIs should be consistent across cycles to enable meaningful comparison
- Feeds into RC-09 (Dashboard Data Publisher) and reporting workflows
