# CO-08 — Audit Trail Logger

## Purpose

Record every agent action, decision, and data reference with a timestamp. This skill is the backbone of the GxP audit trail and is implicitly active in every workflow.

---

## Owner

**Primary:** GxP Compliance Manager, Supervisor (shared)

---

## When This Skill Is Used

- Always. This skill is active in every workflow, for every agent action.
- It is not invoked explicitly — it operates as a cross-cutting requirement embedded in every agent's output format.

---

## Inputs

1. **Agent actions** — Every action taken by any agent during the workflow
2. **Data references** — Every file or data point used
3. **Decisions** — Every routing decision, recommendation, or classification

---

## Steps

1. **For each agent action**, record:
   - Timestamp (ISO 8601 format)
   - Agent name
   - Action taken (plain English description)
   - Data referenced (which file, table, or data point was used)
   - Decision or result (what the agent concluded or produced)
2. **Maintain chronological order** — The audit trail is a time-ordered log
3. **Include in every output** — Every agent output must contain an audit trail section
4. **The Supervisor aggregates** all agent audit trails into the run-level audit trail

---

## Output

- Chronological log of all actions, references, and decisions across the workflow
- Each entry includes: timestamp, agent, action, data reference, result

---

## Notes

- The audit trail is not optional — it is a GxP requirement
- If it is not logged, it did not happen — this is the governing principle
- Every agent's output format includes an audit_trail section by design
- The Supervisor collects and aggregates all agent audit trails into the final run output
