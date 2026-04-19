# AI-06 — Shortage Probability Modeller

## Purpose

Estimate the probability of stock-out at each site or country within defined time horizons (4, 8, and 12 weeks). This forward-looking assessment helps prioritise replenishment urgency.

---

## Owner

**Primary:** Clinical Data & Insights Analyst

---

## When This Skill Is Used

- During hot spot surveillance to identify locations at risk of stock-out
- During plan scoring to assess the risk dimension of a supply plan

---

## Inputs

1. **Stock position** — From SI-01
2. **Consumption rates** — From DF-01
3. **Open orders and in-transit** — From SI-01 and LT-07
4. **Lead times** — From LT-01

---

## Steps

1. **For each location and item**, project stock depletion based on current consumption rate
2. **Factor in expected arrivals** — Open orders and in-transit shipments
3. **Estimate probability of stock-out** at 4 weeks, 8 weeks, and 12 weeks
4. **Identify the primary driver** for each risk (high consumption, low stock, delayed shipment, etc.)
5. **Rank locations** by shortage probability

---

## Output

- Shortage probability by location and item at 4, 8, and 12 weeks
- Primary risk driver for each location
- Locations ranked by probability (highest first)

---

## Notes

- Probability estimates are based on current data and trends — they are projections, not predictions
- High-probability locations should trigger immediate attention from the Supply Analyst
