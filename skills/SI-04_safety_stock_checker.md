# SI-04 — Safety Stock Checker

## Purpose

Compare current stock levels against policy-defined minimum safety stock thresholds. This skill identifies locations that are at risk of running out of supply.

---

## Owner

**Primary:** Supply & Inventory Analyst

---

## When This Skill Is Used

- During supply planning after weeks of supply have been calculated
- As part of hot spot surveillance (WF-04)

---

## Inputs

1. **Weeks of supply** — Output from SI-02
2. **Policies** — Safety stock thresholds from DI-07

---

## Steps

1. **Load safety stock thresholds** — Apply the most specific threshold available (per-item > per-country > per-depot > global default)
2. **Compare each location's weeks of supply** to its applicable threshold
3. **Classify**:
   - **ABOVE** — Comfortably above safety stock
   - **AT** — At or near the threshold
   - **BELOW** — Below the threshold
   - **CRITICAL** — Significantly below threshold, immediate action needed
4. **Produce safety stock status report** — All locations with their status

---

## Output

- Safety stock status by location and item
- Locations below threshold, ranked by severity
- Threshold applied to each location (noting any overrides)

---

## Notes

- Safety stock thresholds can be defined at multiple levels in `policies.json` — always apply the most specific available
- Feeds into SI-05 (Reorder Trigger Evaluator) to determine if replenishment is needed
