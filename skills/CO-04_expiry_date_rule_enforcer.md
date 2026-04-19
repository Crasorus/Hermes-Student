# CO-04 — Expiry Date Rule Enforcer

## Purpose

Apply country-specific and sponsor-specific rules for expiry dating, retesting, and use-by periods that go beyond standard shelf life requirements.

---

## Owner

**Primary:** GxP Compliance Manager

---

## When This Skill Is Used

- During compliance validation alongside CO-03 (Shelf Life Compliance Checker)
- When expiry-related decisions need to account for specific regulatory rules

---

## Inputs

1. **Policies** — Expiry rules from DI-07
2. **Reference documents** — Country-specific rules from DI-08
3. **Batch details** — Expiry dates and retest dates from DI-04

---

## Steps

1. **Identify applicable expiry rules** — Sponsor rules, country rules, and any item-specific rules
2. **Apply rules to each batch** — Check retest dates, use-by periods, and any special conditions
3. **Flag any batches that violate expiry rules** — Even if they pass standard shelf life checks
4. **Classify** — COMPLIANT or NON-COMPLIANT with explanation

---

## Output

- Expiry rule compliance status for each batch
- Rules applied (citing which policy or regulation)
- Non-compliant batches with details
- Recommended actions

---

## Notes

- Expiry rules can be more restrictive than standard shelf life — a batch may have shelf life remaining but still violate a sponsor or country rule
- This skill complements CO-03 — both should run during compliance validation
