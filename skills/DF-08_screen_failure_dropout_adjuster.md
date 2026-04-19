# DF-08 — Screen Failure & Dropout Adjuster

## Purpose

Refine demand estimates by applying screen failure rates and dropout rates. Raw demand calculations assume all screened patients are randomised and complete all visits — this skill adjusts for reality.

---

## Owner

**Primary:** Demand & Forecast Analyst

---

## When This Skill Is Used

- After DF-07 (Visit & Dispensing Calculator) has produced raw demand numbers
- Applied to each scenario in DF-05 and DF-06

---

## Inputs

1. **Raw demand calculation** — Output from DF-07
2. **Parsed RTSM data** — Actual screen failure and dropout rates from DI-03
3. **Study configuration** — Assumed rates if actuals are not yet available

---

## Steps

1. **Determine screen failure rate** — Use actual rate from RTSM data if available, otherwise use the assumed rate from study configuration
2. **Determine dropout rate** — Use actual rate from RTSM data if available, otherwise use assumed rate
3. **Adjust enrollment numbers** — Reduce effective enrollment by the screen failure rate
4. **Adjust demand across visits** — Reduce later-visit demand by the cumulative dropout rate
5. **Flag whether rates are actual or assumed** — Clearly state which rates are based on data and which are assumptions
6. **Produce adjusted demand** — Refined demand numbers with adjustments applied

---

## Output

- Adjusted demand numbers (with screen failure and dropout applied)
- Screen failure rate used (actual or assumed)
- Dropout rate used (actual or assumed)
- Impact of adjustment (how much demand changed vs. raw calculation)
- Data source reference — data drop date, files used, and reporting period covered

---

## Notes

- Always flag whether rates are observed from data or assumed from configuration — this affects confidence in the forecast
- Early in a study, rates will be assumed. As data accumulates, actual rates should replace assumptions.
- This skill refines demand — it does not change enrollment projections (that is DF-02)
