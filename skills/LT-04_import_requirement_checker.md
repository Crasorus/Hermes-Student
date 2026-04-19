# LT-04 — Import Requirement Checker

## Purpose

Look up country-specific import requirements for clinical supplies — licences, permits, and documentation that must be in place before a shipment can enter the country.

---

## Owner

**Primary:** Trade & Logistics Specialist

---

## When This Skill Is Used

- During shipping planning for any international shipment
- Before shipping requests are generated (LT-06) to ensure documentation is ready

---

## Inputs

1. **Reference documents** — From DI-08 (label requirements, approved vendors)
2. **Supply network** — Country information from DI-06
3. **Shipment details** — Destination country, item type

---

## Steps

1. **Look up destination country import requirements** — Licences, permits, controlled substance documentation, language requirements for paperwork
2. **Check documentation status** — Is the required documentation in place?
3. **Flag any gaps** — Missing or expired documentation that would delay the shipment
4. **Produce import requirements summary** — Requirements and status by country

---

## Output

- Import requirements by destination country
- Documentation status (complete or gaps identified)
- List of any missing or expired documentation
- Estimated delay if documentation is not in place

---

## Notes

- Missing import documentation can delay shipments by weeks — this should be flagged as early as possible
- Feeds into LT-08 (Customs Documentation Checker) for more detailed validation
