# LT-05 — Approved Vendor Selector

## Purpose

Select the appropriate courier, broker, or CMO for each shipping lane from the approved vendor list.

---

## Owner

**Primary:** Trade & Logistics Specialist

---

## When This Skill Is Used

- During shipping planning after lead times and cold chain requirements are established
- Before shipping requests are generated (LT-06)

---

## Inputs

1. **Approved vendors** — From DI-08 (vendor list with lane assignments and capabilities)
2. **Cold chain assessment** — Output from LT-03
3. **Shipment details** — Lane, item type, urgency

---

## Steps

1. **Identify approved vendors for the required lane**
2. **Filter by capability** — Remove any vendors that cannot meet cold chain or other requirements
3. **If multiple vendors qualify**, select based on: lead time, capability match, cost (if available)
4. **If no approved vendor exists for the lane**, flag as a critical gap
5. **Produce vendor selection** — Selected vendor with rationale and alternatives

---

## Output

- Selected vendor for each lane
- Rationale for selection
- Alternative vendors (if available)
- Flags for lanes with no approved vendor

---

## Notes

- Only vendors on the approved list may be selected — never recommend an unapproved vendor
- If no vendor is approved for a required lane, this is a critical gap that must be escalated
