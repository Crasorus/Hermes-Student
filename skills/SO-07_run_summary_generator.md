# SO-07 — Run Summary Generator

## Purpose

Produce a concise summary of what ran, what was found, and what was actioned at the end of every workflow. This is the final step of every Supervisor workflow.

---

## Owner

**Primary:** Supervisor Agent

---

## When This Skill Is Used

- At Step 7 of the Supervisor's standard workflow — the final step of every run

---

## Inputs

1. **Workflow status** — From SO-04
2. **All agent outputs** — Collected during the workflow
3. **Audit trail** — From CO-08

---

## Steps

1. **Summarise what ran** — Which workflow, which agents, how many steps
2. **Summarise what was found** — Key findings and deltas detected
3. **Summarise what was actioned** — Decisions taken, recommendations produced, artifacts generated
4. **Note risks and caveats** — Any data quality issues, missing data, or unresolved conflicts
5. **State next steps** — What happens next, who needs to act, what is pending
6. **Package the complete run output** — Including all agent outputs and the aggregated audit trail

---

## Output

- Run summary with: what ran, what was found, what was actioned, risks, next steps
- Complete audit trail
- All agent outputs packaged together
- Final execution status (SUCCESS, HALTED, COMPLETED WITH WARNINGS)

---

## Notes

- The run summary is the top-level output of every workflow — it should give a complete picture in one document
- This is the primary artifact for human review and audit purposes
