# DF-02 — Enrollment Trajectory Modeller

## Purpose

Project enrollment forward based on the current rate compared to the original plan. This skill answers the question: "At the current pace, when will enrollment be complete, and how does that compare to the plan?"

---

## Owner

**Primary:** Demand & Forecast Analyst

---

## When This Skill Is Used

- During WF-01 (Demand Signal Refresh) after consumption rates are calculated
- Whenever enrollment projections need to be updated

---

## Inputs

1. **Parsed RTSM data** — Output from DI-03 (randomisation events)
2. **Parsed CTMS data** — Output from DI-05 (enrollment plan, site information)
3. **Study configuration** — Target enrollment numbers

---

## Steps

1. **Calculate current enrollment rate** — Actual randomisations per week, by site and country
2. **Compare to planned rate** — How does actual enrollment track against the CTMS plan?
3. **Project forward** — At the current rate, when will enrollment targets be met?
4. **Identify sites ahead or behind plan** — Flag sites that are significantly deviating from their enrollment targets
5. **Produce trajectory summary** — Planned vs. projected completion dates, sites of concern

---

## Output

- Current enrollment rate (actual vs. planned) by site and country
- Projected enrollment completion date at current rate
- Planned completion date from CTMS
- Gap between planned and projected completion
- List of sites significantly ahead or behind plan
- Data source reference — data drop date, files used, and reporting period covered

---

## Notes

- This skill models enrollment trajectory — it does not model demand. Demand impact is calculated by DF-03 and DF-05.
- The enrollment trajectory feeds into scenario modelling (DF-05) and is a key input to the delta calculation (DF-03)
