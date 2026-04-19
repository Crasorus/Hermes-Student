# LT-07 — In-Transit Tracker

## Purpose

Read ERP shipment data to report the current status of all in-transit shipments. This ensures that new shipping decisions account for what is already on the way.

---

## Owner

**Primary:** Trade & Logistics Specialist

---

## When This Skill Is Used

- During shipping planning to avoid duplicate shipments
- During hot spot surveillance to flag delayed shipments

---

## Inputs

1. **Parsed ERP data** — Shipment records from DI-04 (in-transit and shipment history)

---

## Steps

1. **List all current in-transit shipments** with origin, destination, item, quantity, and expected arrival date
2. **Classify each shipment**:
   - **ON TRACK** — Expected to arrive on time
   - **DELAYED** — Behind schedule based on expected arrival date
   - **DELIVERED** — Already received (for reference)
3. **Flag delayed shipments** with estimated delay and potential impact
4. **Produce in-transit status report**

---

## Output

- All in-transit shipments with status (on track, delayed, delivered)
- Expected arrival dates
- Flags for delayed or at-risk shipments
- Summary of total units in transit by destination

---

## Notes

- Always check in-transit shipments before recommending new ones — incoming stock may reduce or eliminate the need for a new order
- Delayed shipments should be flagged to the Insights Analyst for hot spot surveillance
