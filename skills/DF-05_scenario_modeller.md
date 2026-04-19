# DF-05 — Scenario Modeller

## Purpose

Generate three standard demand scenarios — base case, optimistic, and pessimistic — to give planners a range of possible outcomes for supply planning.

---

## Owner

**Primary:** Demand & Forecast Analyst

---

## When This Skill Is Used

- During WF-01 when significant deltas are detected (after DF-04 flags significance)
- Whenever scenario-based planning is requested

---

## Inputs

1. **Current consumption rates** — Output from DF-01
2. **Enrollment trajectory** — Output from DF-02
3. **Delta report** — Output from DF-03
4. **Study configuration** — Treatment arms, items, pack sizes

---

## Steps

1. **Generate Base Case** — Current trajectory continues unchanged. Use actual consumption rate and enrollment pace as-is.
2. **Generate Optimistic Case** — Enrollment accelerates back to the original plan. Consumption rate adjusts proportionally.
3. **Generate Pessimistic Case** — Enrollment slows further or dropout rate increases. Demand adjusts accordingly.
4. **For each scenario**, calculate:
   - Total projected demand (units) across the remaining study horizon
   - Projected study completion date
   - Demand by country, treatment arm, and item
5. **Produce scenario matrix** — All three scenarios side by side for comparison
6. **Flag recommended scenario** — Based on the data, indicate which scenario is recommended for supply planning purposes. Label this as a RECOMMENDATION, not a DECISION. State the reasoning (e.g., "Base case recommended — enrollment pace stable, no significant deviation from plan")

---

## Scenario Parameter Guidance

- **Base Case**: Current actual rates from DF-01 (consumption) and DF-02 (enrollment) — no adjustments
- **Optimistic**: Enrollment returns to the planned rate from CTMS. Consumption rate stays at actual. Dropout rate uses the lower of actual or assumed.
- **Pessimistic**: Current enrollment trend continues or worsens. Apply a pessimistic multiplier (configurable in `study_config.json`, default 1.5x) to the observed dropout rate. Use actual consumption rate.
- All assumptions must be stated explicitly in the output so reviewers can challenge them.

---

## Output

- Three scenarios (base, optimistic, pessimistic) each with total demand, completion date, and breakdowns
- Scenario comparison matrix
- Key assumptions stated for each scenario
- Recommended scenario for supply planning (labelled RECOMMENDATION)
- Data source reference — data drop date, files used, and reporting period covered

---

## Notes

- Scenarios should clearly state their assumptions so that reviewers can judge plausibility
- This skill uses DF-07 (Visit & Dispensing Calculator) and DF-08 (Screen Failure & Dropout Adjuster) to build demand numbers for each scenario. Those skills provide the per-patient kit calculations and attrition adjustments that feed into the scenario projections.
- The scenario matrix feeds into the Supply Analyst for supply plan adjustment and into the Reporting Agent for the demand refresh summary
- For user-defined what-if scenarios, see DF-06
