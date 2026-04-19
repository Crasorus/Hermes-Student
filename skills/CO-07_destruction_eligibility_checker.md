# CO-07 — Destruction Eligibility Checker

## Purpose

Determine which stock is eligible for destruction based on expiry status, study status, and policy rules. This skill is used at study closedown or when stock needs to be disposed of.

---

## Owner

**Primary:** GxP Compliance Manager

---

## When This Skill Is Used

- During future workflow — Study Closedown & Destruction
- When expired or recalled stock needs to be assessed for destruction

---

## Inputs

1. **Stock position** — From SI-01 (batch-level detail)
2. **Expiry profile** — From SI-03
3. **Policies** — Destruction eligibility criteria from DI-07
4. **Study status** — Whether the study is active, closing, or closed

---

## Steps

1. **Identify candidate stock** — Expired batches, stock at closed sites, recalled stock, damaged stock
2. **Check each candidate against destruction criteria** from policies:
   - Is the stock expired beyond any retest period?
   - Is the study closed for this item or site?
   - Has the stock been recalled or quarantined?
3. **Verify no open patients need the stock** — Stock cannot be destroyed if patients still need it
4. **Classify eligibility** — Eligible for destruction, not eligible, or conditional
5. **Produce destruction eligibility report**

---

## Output

- List of stock eligible for destruction (batch, item, location, quantity, reason)
- Stock not eligible with explanation
- Any conditions on destruction (e.g., pending investigation)
- Total quantity eligible for destruction

---

## Notes

- Destruction of clinical supplies is a regulated activity — this skill provides the eligibility assessment, but actual destruction requires human authorisation
- Always verify that no open patients need the stock before approving destruction
