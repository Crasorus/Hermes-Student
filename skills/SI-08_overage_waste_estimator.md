# SI-08 — Overage & Waste Estimator

## Purpose

Estimate projected overage and waste at study end under the current supply plan. This skill helps planners balance the risk of shortage against the cost of over-supply.

---

## Owner

**Primary:** Supply & Inventory Analyst

---

## When This Skill Is Used

- After the supply plan is drafted to assess efficiency
- During budget review and plan scoring

---

## Inputs

1. **Stock position** — Output from SI-01
2. **Demand scenarios** — Output from DF-05
3. **Order recommendations** — Output from SI-06
4. **Expiry profile** — Output from SI-03

---

## Steps

1. **Project total supply** at study end — Current stock + all planned orders
2. **Project total demand** through to study end — Using the selected scenario
3. **Calculate overage** — Supply minus demand = projected surplus
4. **Estimate waste sources**:
   - Stock that will expire before use (from SI-03)
   - Stock that will remain unused at study end
5. **Express waste as percentage** of total supply and as estimated cost (if cost data available)
6. **Identify primary waste drivers** — Is it over-ordering, expiry, or protocol changes?

---

## Output

- Projected overage (units and percentage)
- Projected waste by source (expiry, unused at study end)
- Estimated cost of waste (if cost data available)
- Primary waste drivers
- Recommendations to reduce waste

---

## Notes

- Some overage is expected and acceptable — the goal is to balance shortage risk against waste cost
- This feeds into SI-09 (Supply Plan Scorer) as the efficiency dimension
- Also feeds into AI-09 (Waste Root Cause Analyser) for deeper analysis
