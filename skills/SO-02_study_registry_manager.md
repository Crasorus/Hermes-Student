# SO-02 — Study Registry Manager

## Purpose

Maintain the list of active studies, their data drop schedules, and current status. This skill helps the Supervisor manage multi-study environments.

---

## Owner

**Primary:** Supervisor Agent

---

## When This Skill Is Used

- When managing multiple studies simultaneously
- When a new study is onboarded or an existing study changes status

---

## Inputs

1. **Study configurations** — From all active study packages
2. **Study status updates** — From workflow outputs or user input

---

## Steps

1. **List all active studies** with their IDs, status, and data drop schedule
2. **Track study lifecycle stage** — Setup, active, closing, closed
3. **Note upcoming data drops** — What is expected and when
4. **Flag overdue data drops** — Studies where expected data has not arrived
5. **Produce registry summary**

---

## Output

- List of active studies with status and schedule
- Overdue data drop flags
- Studies approaching lifecycle transitions

---

## Notes

- In a single-study deployment this skill is simple — it becomes important when the framework manages multiple studies
