# LT-01 — Lead Time Calculator

## Purpose

Calculate the end-to-end lead time for a given shipping lane, covering every stage from manufacturing or release through to final delivery.

---

## Owner

**Primary:** Trade & Logistics Specialist

---

## When This Skill Is Used

- During supply planning to determine when orders need to be placed
- During shipping window planning (LT-02) to calculate latest ship dates

---

## Inputs

1. **Supply network** — Lane definitions and lead times from DI-06
2. **Order recommendations** — Origin, destination, item, quantity, and required-by date from SI-06

---

## Steps

1. **Identify the shipping lane** — Origin to destination
2. **Sum all lead time components**:
   - Manufacturing or release/QC time (if applicable)
   - Transit time
   - Customs clearance time
   - Last-mile delivery time
3. **Express as total business days** from order placement to receipt
4. **Flag any lanes with unusually long or uncertain lead times**

---

## Output

- Total end-to-end lead time per lane (business days)
- Breakdown by component (manufacturing, transit, customs, last mile)
- Flags for lanes with long or uncertain lead times

---

## Notes

- Lead times come from the supply network configuration — this skill reads and applies them, not estimates them
- Feeds into SI-05 (Reorder Trigger Evaluator) and LT-02 (Shipping Window Planner)
