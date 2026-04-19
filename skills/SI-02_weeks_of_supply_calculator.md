# SI-02 — Weeks of Supply Calculator

## Purpose

Calculate how many weeks of supply remain at each location based on current stock levels and consumption rate. This is the most intuitive measure of whether stock is sufficient.

---

## Owner

**Primary:** Supply & Inventory Analyst

---

## When This Skill Is Used

- After SI-01 (Stock Position Calculator) has produced the inventory snapshot
- Used to assess whether stock levels are adequate across the network

---

## Inputs

1. **Stock position** — Output from SI-01
2. **Consumption rates** — Output from DF-01
3. **Policies** — Safety stock thresholds from DI-07

---

## Steps

1. **For each location and item**, divide total available stock by the weekly consumption rate
2. **Compare to safety stock threshold** — Flag locations below or approaching the minimum weeks of supply
3. **Classify each location** — ABOVE, AT, BELOW, or CRITICAL relative to safety stock threshold
4. **Produce weeks of supply report** — All locations with their weeks of supply and status

---

## Output

- Weeks of supply by depot, country, and item
- Safety stock status for each location (ABOVE, AT, BELOW, CRITICAL)
- Locations ranked by urgency (lowest weeks of supply first)

---

## Notes

- Weeks of supply is calculated using the current consumption rate — if consumption changes, weeks of supply will shift
- This skill feeds into SI-04 (Safety Stock Checker) and SI-05 (Reorder Trigger Evaluator)
