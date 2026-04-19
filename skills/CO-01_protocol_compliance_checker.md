# CO-01 — Protocol Compliance Checker

## Purpose

Validate that demand assumptions and supply decisions are consistent with the approved study protocol — treatment arms, visit schedules, dose levels, and pack configurations.

---

## Owner

**Primary:** GxP Compliance Manager

---

## When This Skill Is Used

- After the Demand Analyst produces demand forecasts (WF-01)
- After the Supply Analyst produces a supply plan (WF-02)
- Any time agent outputs need protocol validation

---

## Inputs

1. **Agent output to validate** — Demand forecast or supply plan
2. **Study configuration** — Protocol parameters (treatment arms, visit schedules, pack sizes)

---

## Steps

1. **Check treatment arms** — Do the demand or supply outputs reference only treatment arms defined in the protocol?
2. **Check items and pack sizes** — Are the items and pack configurations consistent with the protocol?
3. **Check visit assumptions** — Do dispensing calculations match the protocol visit schedule?
4. **Check dose levels** — Are dose assumptions consistent with the approved protocol?
5. **Flag any discrepancies** — Identify where agent outputs deviate from protocol parameters
6. **Classify each finding** — COMPLIANT, NON-COMPLIANT, or UNABLE TO VERIFY

---

## Output

- Compliance status for each check (COMPLIANT, NON-COMPLIANT, UNABLE TO VERIFY)
- Details of any discrepancies found
- Severity of each finding (CRITICAL, MAJOR, MINOR, OBSERVATION)
- Recommended remediation for non-compliant findings

---

## Notes

- This skill validates against the protocol as defined in `study_config.json` — it does not interpret the protocol itself
- Non-compliance findings are returned to the Supervisor, who may route the originating agent to revise its output
