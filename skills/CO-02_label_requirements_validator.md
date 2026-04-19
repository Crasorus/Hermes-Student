# CO-02 — Label Requirements Validator

## Purpose

Check that label content, language, and format meet country-specific requirements for each country in the supply plan.

---

## Owner

**Primary:** GxP Compliance Manager

---

## When This Skill Is Used

- During compliance validation of a supply plan or shipping request
- Before shipments are approved for countries with specific label requirements

---

## Inputs

1. **Label requirements** — From DI-08 (country-specific label rules)
2. **Supply plan or shipping request** — Items and destination countries to validate

---

## Steps

1. **For each country in the plan**, look up label requirements (language, content elements, format)
2. **Check whether the items being shipped have labels that meet the destination country's requirements**
3. **Flag any countries where label compliance cannot be confirmed**
4. **Classify** — COMPLIANT, NON-COMPLIANT, or UNABLE TO VERIFY

---

## Output

- Label compliance status by country
- Details of any label gaps (wrong language, missing content, format issues)
- Severity of each finding
- Recommended actions for non-compliant labels

---

## Notes

- Label issues can prevent shipments from clearing customs or being used at sites
- If label requirements data is missing for a country, the result is UNABLE TO VERIFY, not COMPLIANT
