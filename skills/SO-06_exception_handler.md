# SO-06 — Exception Handler

## Purpose

Manage unexpected errors, missing data, and workflow failures gracefully. This skill ensures the framework fails informatively rather than silently.

---

## Owner

**Primary:** Supervisor Agent

---

## When This Skill Is Used

- When any agent encounters an error or unexpected condition
- When a workflow step fails and the Supervisor must decide how to proceed

---

## Inputs

1. **Error details** — What went wrong, where, and why (if known)
2. **Workflow context** — What step was running, what data was being processed

---

## Steps

1. **Classify the error**:
   - **Recoverable** — The workflow can continue with caveats (e.g., optional data missing)
   - **Non-recoverable** — The workflow must halt (e.g., critical data missing, agent failure)
2. **If recoverable**, note the caveat and continue the workflow
3. **If non-recoverable**, halt the workflow and produce an error report
4. **Log the exception** in the audit trail with full context
5. **Produce error report** — What happened, what was affected, and what is needed to resolve it

---

## Output

- Error classification (recoverable or non-recoverable)
- Error report with details, impact, and recommended resolution
- Audit trail entry

---

## Notes

- The goal is informative failure — never fail silently
- Error reports should be clear enough that a non-technical user can understand what went wrong and what to do about it
