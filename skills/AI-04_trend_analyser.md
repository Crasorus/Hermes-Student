# AI-04 — Trend Analyser

## Purpose

Identify directional trends in consumption, enrollment, waste, and cost over time. This skill looks across multiple cycles to spot patterns that point-in-time analysis would miss.

---

## Owner

**Primary:** Clinical Data & Insights Analyst

---

## When This Skill Is Used

- During reporting workflows (future workflows — Executive Reporting, Budget Review) to provide trend context
- During plan scoring to assess whether trends are improving or deteriorating

---

## Inputs

1. **Current cycle data** — Latest outputs from Demand Analyst and Supply Analyst
2. **Previous cycle data** — Historical outputs for comparison (if available)

---

## Steps

1. **Compare key metrics across cycles** — Consumption rate, enrollment rate, waste percentage, cost per patient, service level
2. **Identify direction** — Is each metric INCREASING, DECREASING, or STABLE?
3. **Assess magnitude** — How fast is the trend moving?
4. **Flag concerning trends** — Metrics moving in an undesirable direction (e.g., waste increasing, service level decreasing)
5. **Produce trend summary** — Each metric with direction, magnitude, and concern level

---

## Output

- Trends for each key metric (direction, magnitude, period)
- Concern level for each trend (HIGH, MEDIUM, LOW, NONE)
- Plain English commentary on what the trends mean

---

## Notes

- Trend analysis requires data from at least two cycles — if only one cycle is available, trends cannot be calculated
- Trends provide context that makes point-in-time metrics more meaningful
