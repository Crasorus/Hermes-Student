# CO-10 — Regulatory Change Alerter

## Purpose

Flag when reference documents have been updated since the last workflow run. Changes to shelf life rules, label requirements, or approved vendors may affect the current supply plan.

---

## Owner

**Primary:** GxP Compliance Manager

---

## When This Skill Is Used

- During the compliance validation mode, as part of the reference document loading process
- Runs alongside DI-08 (Reference Document Loader)

---

## Inputs

1. **Current reference documents** — Loaded by DI-08
2. **Previous run metadata** — Version dates or checksums from the last workflow run (if available)

---

## Steps

1. **Compare current reference documents to previous versions** — Check version dates, file modification dates, or checksums
2. **Identify any documents that have changed** since the last run
3. **Assess potential impact** — What areas of the supply plan could be affected by the change?
4. **Produce change alert** — Which documents changed and what the potential implications are

---

## Output

- List of reference documents checked
- Change status for each (changed or unchanged)
- For changed documents: what changed (if detectable) and potential impact
- Recommendation on whether the current plan needs to be re-validated

---

## Notes

- Change detection depends on version dates or file metadata being available — if not available, the result is UNABLE TO VERIFY
- This is an early warning system — it alerts that something has changed, not necessarily what the specific impact is
- Significant changes should trigger the Supervisor to route the plan back through compliance validation
