# SO-01 — Workflow Router

## Purpose

Determine which workflow(s) to trigger based on the inputs received, the trigger reason, and the current state of the study. This is the Supervisor's core decision-making skill.

---

## Owner

**Primary:** Supervisor Agent

---

## When This Skill Is Used

- At Step 5 of the Supervisor's standard workflow, after data validation is complete
- Whenever the Supervisor needs to decide what to do next

---

## Inputs

1. **Task description** — What has been requested
2. **Trigger reason** — Scheduled, event-driven, on-demand, or chained
3. **Data quality flag** — From DI-10
4. **Study status** — Active, closing, closed

---

## Steps

1. **Interpret the task** — What is being asked? What type of workflow does this require?
2. **Match to workflow** — Map the request to one of the 11 defined workflows
3. **Determine agent sequence** — Which agents need to run and in what order?
4. **Check for chained workflows** — Does the output of this workflow trigger another?
5. **Produce routing decision** — Workflow ID, agent sequence, and rationale

---

## Output

- Workflow to trigger (ID and name)
- Agents to activate and their sequence
- Rationale for the routing decision
- Any chained workflows that may follow

---

## Notes

- The Supervisor is the only agent that routes workflows — no agent self-activates
- If the task is ambiguous and cannot be mapped to a workflow, the Supervisor should halt and request clarification
