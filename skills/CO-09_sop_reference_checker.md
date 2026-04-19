# CO-09 — SOP Reference Checker

## Purpose

Cross-reference a proposed action against known SOPs to flag potential violations or deviations from standard operating procedures.

---

## Owner

**Primary:** GxP Compliance Manager

---

## When This Skill Is Used

- During compliance validation of supply plans, shipping requests, or other agent outputs
- When proposed actions need to be checked against organisational SOPs

---

## Inputs

1. **Proposed action** — The agent output or recommendation to check
2. **Policies** — SOP references from DI-07

---

## Steps

1. **Identify which SOPs are relevant** to the proposed action (ordering, shipping, destruction, etc.)
2. **Check the proposed action against the SOP requirements**
3. **Flag any potential violations or deviations**
4. **Classify** — COMPLIANT, POTENTIAL DEVIATION, or UNABLE TO VERIFY

---

## Output

- SOP compliance status for each proposed action
- SOPs referenced
- Any potential deviations with explanation
- Recommended actions to resolve deviations

---

## Notes

- SOP references in `policies.json` may be high-level — this skill checks what it can and flags uncertainty as UNABLE TO VERIFY
- This is a best-effort check — detailed SOP compliance may require human review
