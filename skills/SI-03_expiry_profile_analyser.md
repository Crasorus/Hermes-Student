# SI-03 — Expiry Profile Analyser

## Purpose

Profile batch expiry dates against projected consumption to identify stock at risk of expiring before it can be used. This skill helps prevent waste and ensures patients receive in-date medication.

---

## Owner

**Primary:** Supply & Inventory Analyst, GxP Compliance Manager (shared)

---

## When This Skill Is Used

- During supply planning to assess expiry risk
- During compliance checking to validate shelf life adequacy

---

## Inputs

1. **Parsed ERP data** — Batch details with expiry dates from DI-04
2. **Consumption rates** — Output from DF-01
3. **Stock position** — Output from SI-01

---

## Steps

1. **List all batches** with their expiry dates, quantities, and locations
2. **Project consumption** — At the current rate, when will each batch be consumed?
3. **Compare consumption to expiry** — Will the batch be fully consumed before it expires?
4. **Classify each batch**:
   - **SAFE** — Will be consumed well before expiry
   - **AT RISK** — May not be fully consumed before expiry
   - **WILL EXPIRE** — Will definitely expire before consumption at current rate
5. **Quantify total expiry risk** — Total units at risk by location and item

---

## Output

- Batch-level expiry profile (batch ID, item, location, expiry date, quantity, projected consumption date, risk classification)
- Total units at expiry risk by location and item
- Batches recommended for priority use (shortest dated first)

---

## Notes

- This skill applies FEFO (First Expiry, First Out) logic — shortest-dated batches should be used first
- Expiry risk is both a waste issue and a compliance issue — the Compliance Manager uses this output for shelf life validation
- Feeds into SI-10 (Batch Selection Advisor) for shipping recommendations
