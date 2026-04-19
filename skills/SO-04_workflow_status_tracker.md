# SO-04 — Workflow Status Tracker

## Purpose

Track progress of each workflow run, log completion status, and flag stalls or failures.

---

## Owner

**Primary:** Supervisor Agent

---

## When This Skill Is Used

- Throughout every workflow run to track progress
- At workflow completion to log the final status

---

## Inputs

1. **Workflow definition** — Which workflow is running and what steps are expected
2. **Agent responses** — Status and outputs from each agent as they complete

---

## Steps

1. **Track each step** of the workflow — Started, in progress, completed, or failed
2. **Log agent completion** — When each agent returns its output, record the status
3. **Detect stalls** — If an agent does not respond or takes unexpectedly long, flag it
4. **Record final status** — Workflow completed successfully, completed with warnings, or failed
5. **Produce status summary**

---

## Output

- Step-by-step status of the workflow run
- Agent completion status
- Overall workflow status (SUCCESS, COMPLETED WITH WARNINGS, FAILED)
- Any stalls or failures flagged

---

## Notes

- The status tracker provides the backbone for the audit trail and run summary
