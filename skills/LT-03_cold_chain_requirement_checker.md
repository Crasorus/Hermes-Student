# LT-03 — Cold Chain Requirement Checker

## Purpose

Identify temperature-sensitive items and validate that the shipping lane and selected vendor can maintain the required temperature conditions throughout transit.

---

## Owner

**Primary:** Trade & Logistics Specialist

---

## When This Skill Is Used

- During shipping planning for any shipment containing temperature-sensitive items
- Before vendor selection (LT-05) to filter vendors by cold chain capability

---

## Inputs

1. **Study configuration** — Item details including temperature requirements
2. **Supply network** — Lane capabilities from DI-06
3. **Approved vendors** — Vendor capabilities from DI-08

---

## Steps

1. **Identify which items are temperature-sensitive** and their required storage/transit conditions
2. **For each shipping lane**, check whether the route supports the required temperature conditions
3. **For each approved vendor on the lane**, check whether they have cold chain capability
4. **Flag any gaps** — Items that need cold chain on a lane or with a vendor that cannot provide it
5. **Produce cold chain assessment** — Item-by-lane-by-vendor capability matrix

---

## Output

- Temperature requirements by item
- Lane cold chain capability (confirmed or not)
- Vendor cold chain capability (confirmed or not)
- Flags for any shipments where cold chain cannot be assured

---

## Notes

- Cold chain gaps are serious — a temperature-sensitive item shipped without proper cold chain may be compromised
- This is both a logistics and compliance concern — the Compliance Manager may also review cold chain findings
