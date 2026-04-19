# SO-03 — Inter-Agent Conflict Resolver

## Purpose

Detect and resolve contradictions between agent outputs. When two agents produce conflicting recommendations, the Supervisor uses this skill to determine the resolution.

---

## Owner

**Primary:** Supervisor Agent

---

## When This Skill Is Used

- When the Supervisor collects outputs from multiple agents and detects inconsistencies
- During Step 6 of the Supervisor's standard workflow

---

## Inputs

1. **Agent outputs** — Outputs from two or more agents that appear to conflict
2. **Study configuration** — For reference and context

---

## Steps

1. **Identify the conflict** — What specifically contradicts between the agent outputs?
2. **Assess which agent has stronger data support** — Which output is backed by more reliable or more recent data?
3. **Apply design principles** — When in doubt, defer to compliance (DP-05), be conservative (DP-04), and favour patient safety
4. **Produce resolution** — State the conflict, the resolution, and the rationale
5. **Log the conflict and resolution** in the audit trail

---

## Output

- Description of the conflict
- Resolution and rationale
- Which agent output was favoured and why
- Audit trail entry

---

## Notes

- Conflicts should be rare if agents are working from the same data — a conflict may indicate a data quality issue
- The resolution should always be logged for traceability
