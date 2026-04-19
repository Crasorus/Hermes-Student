# LT-02 — Shipping Window Planner

## Purpose

Determine the latest possible ship date and recommended ship date for each shipment, given the required-by date and lane lead time.

---

## Owner

**Primary:** Trade & Logistics Specialist

---

## When This Skill Is Used

- After lead times are calculated (LT-01) and order quantities are determined (SI-06)
- Determines urgency and feasibility of each shipment

---

## Inputs

1. **Lead times** — Output from LT-01
2. **Order recommendations** — Output from SI-06 (with required-by dates)

---

## Steps

1. **For each shipment**, subtract the lead time from the required-by date to get the latest ship date
2. **Calculate recommended ship date** — Latest ship date minus a buffer (to account for delays)
3. **Classify shipping window**:
   - **OPEN** — Sufficient time to ship comfortably
   - **TIGHT** — Ship date is approaching, limited buffer
   - **CLOSED** — The latest ship date has already passed; the shipment cannot arrive on time
4. **Produce shipping window plan** — All shipments with dates and status

---

## Output

- Latest ship date for each shipment
- Recommended ship date (with buffer)
- Window status (OPEN, TIGHT, CLOSED)
- Buffer days remaining
- Flags for any shipments where the window is closed

---

## Notes

- A CLOSED window requires escalation — the shipment either needs an expedited route or the required-by date needs to be reconsidered
- Feeds into LT-06 (Shipping Request Generator)
