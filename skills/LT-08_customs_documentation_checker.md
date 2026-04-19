# LT-08 — Customs Documentation Checker

## Purpose

Validate that all required customs and import documentation is in place for a specific shipment before it is dispatched.

---

## Owner

**Primary:** Trade & Logistics Specialist, GxP Compliance Manager (shared)

---

## When This Skill Is Used

- Before a shipping request is finalised (LT-06)
- As a compliance check on outbound shipments

---

## Inputs

1. **Import requirements** — Output from LT-04
2. **Shipment details** — Origin, destination, item type, quantities
3. **Reference documents** — From DI-08

---

## Steps

1. **Identify all required documentation** for the shipment based on destination country and item type
2. **Check each document** — Is it available, current, and valid?
3. **Flag any missing or expired documents**
4. **Classify documentation status**:
   - **READY** — All documentation in place
   - **GAPS** — One or more documents missing or expired
5. **Produce documentation checklist** — Each required document with its status

---

## Output

- Documentation checklist for the shipment (document name, status, expiry if applicable)
- Overall documentation status (READY or GAPS)
- List of any missing or expired documents with recommended action

---

## Notes

- A shipment with documentation gaps should not be dispatched until the gaps are resolved
- This skill is shared between Logistics and Compliance — both agents may review the output
- Documentation gaps are a common cause of shipment delays and should be flagged as early as possible in the planning process
