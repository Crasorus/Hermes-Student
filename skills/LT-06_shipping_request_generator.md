# LT-06 — Shipping Request Generator

## Purpose

Produce a structured shipping request document that contains everything needed to execute a shipment. This is the primary action-oriented output of the logistics workflow.

---

## Owner

**Primary:** Trade & Logistics Specialist

---

## When This Skill Is Used

- After all logistics checks are complete (lead times, cold chain, vendors, documentation)
- Produces the Shipping Request artifact (O-07)

---

## Inputs

1. **Order recommendations** — From SI-06
2. **Batch selection** — From SI-10
3. **Shipping windows** — From LT-02
4. **Vendor selection** — From LT-05
5. **Cold chain assessment** — From LT-03
6. **Import requirements** — From LT-04

---

## Steps

1. **For each approved shipment**, assemble:
   - Origin and destination
   - Item details and quantities
   - Selected batch(es) with lot numbers
   - Selected vendor
   - Recommended ship date and required-by date
   - Temperature requirements
   - Documentation checklist (what paperwork must accompany the shipment)
2. **Validate completeness** — Ensure all required fields are populated
3. **Flag any incomplete requests** — Missing vendor, missing documentation, closed shipping window
4. **Produce shipping request documents** — One per shipment, structured and ready for execution

---

## Output

- Structured shipping request for each shipment containing all execution details
- Documentation checklist status (ready or gaps)
- Flags for any requests that are incomplete or have issues

---

## Notes

- The shipping request is a RECOMMENDATION — it requires human approval before execution
- This is the handoff point from the agent team to the operational team
- Feeds into the Reporting Agent for inclusion in operational reports
