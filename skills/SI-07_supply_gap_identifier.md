# SI-07 — Supply Gap Identifier

## Purpose

Identify where projected demand exceeds available supply across the planning horizon. This skill surfaces the gaps that orders alone may not close — production constraints, long lead times, or insufficient total supply.

---

## Owner

**Primary:** Supply & Inventory Analyst

---

## When This Skill Is Used

- After order quantities are calculated (SI-06) to verify that the plan closes all gaps
- As part of risk assessment to identify structural supply shortfalls

---

## Inputs

1. **Stock position** — Output from SI-01
2. **Demand scenarios** — Output from DF-05
3. **Order recommendations** — Output from SI-06
4. **Supply network** — Lead times and capacities from DI-06

---

## Steps

1. **Project supply forward** — Current stock + expected deliveries from open orders and recommended orders
2. **Project demand forward** — Using the selected demand scenario across the planning horizon
3. **Compare supply to demand** — At each time period (weekly or monthly), does supply cover demand?
4. **Identify gaps** — Time periods and locations where demand exceeds supply
5. **Classify gaps** by severity:
   - **CRITICAL** — Gap occurs within the near term and will cause stock-outs
   - **MODERATE** — Gap occurs in the medium term and may be closeable with action
   - **LOW** — Gap is far out and may resolve with normal ordering
6. **Produce gap analysis** — Gaps by location, item, time period, and severity

---

## Output

- Supply gaps by location, item, and time period
- Gap severity classification
- Total units short across the planning horizon
- Recommendations for closing gaps (accelerate orders, reallocate stock, etc.)

---

## Notes

- Gaps may exist even after orders are placed if lead times are too long or total production capacity is insufficient
- This skill provides a forward-looking view that complements the point-in-time snapshot from SI-01
