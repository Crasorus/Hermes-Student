# SO-05 — Priority Ranker

## Purpose

Prioritise competing workflow requests when multiple studies or multiple triggers arrive at the same time.

---

## Owner

**Primary:** Supervisor Agent

---

## When This Skill Is Used

- When multiple workflow requests are pending simultaneously
- In multi-study environments where resources must be allocated

---

## Inputs

1. **Pending workflow requests** — List of workflows waiting to run
2. **Study registry** — From SO-02 (study priorities and status)
3. **Trigger urgency** — Scheduled vs. event-driven vs. on-demand

---

## Steps

1. **Assess urgency of each request** — Event-driven and deviation responses generally take priority over scheduled runs
2. **Assess patient impact** — Requests with potential patient impact rank higher
3. **Assess data freshness** — Requests with time-sensitive data rank higher
4. **Rank all pending requests** by priority
5. **Produce priority queue**

---

## Output

- Prioritised list of pending workflow requests
- Rationale for the ranking

---

## Notes

- In a single-study, single-trigger environment this skill is rarely needed
- Patient safety concerns always take highest priority
