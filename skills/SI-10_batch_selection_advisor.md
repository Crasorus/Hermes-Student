# SI-10 — Batch Selection Advisor

## Purpose

Recommend which specific batches to ship for each order, based on expiry dates, shelf life requirements, and FEFO (First Expiry, First Out) rules.

---

## Owner

**Primary:** Supply & Inventory Analyst, GxP Compliance Manager (shared)

---

## When This Skill Is Used

- After order quantities are determined (SI-06) and before shipping requests are generated (LT-06)
- Ensures the right batches are selected for each shipment

---

## Inputs

1. **Order recommendations** — Output from SI-06
2. **Expiry profile** — Output from SI-03
3. **Shelf life requirements** — From reference documents (DI-08)
4. **Stock position** — Output from SI-01 (batch-level detail)

---

## Steps

1. **For each order**, identify available batches at the source location
2. **Apply FEFO** — Prioritise batches with the shortest remaining shelf life
3. **Check shelf life compliance** — Ensure the selected batch meets the minimum remaining shelf life requirement for the destination country
4. **If shortest-dated batch fails shelf life check**, move to the next batch
5. **Recommend batch allocation** — Which batch(es) to use for each order, and in what quantities
6. **Flag any issues** — Batches that cannot meet shelf life, insufficient batch quantity, etc.

---

## Output

- Recommended batch(es) for each order (batch ID, quantity, expiry date)
- Shelf life compliance status for each recommendation
- Any batches skipped and why
- Flags for orders where no compliant batch is available

---

## Notes

- FEFO is the default rule — ship the shortest-dated stock first, as long as it meets shelf life requirements
- If no batch meets shelf life for the destination, flag the issue for the Compliance Manager
- This skill bridges supply planning and compliance — both agents use its output
