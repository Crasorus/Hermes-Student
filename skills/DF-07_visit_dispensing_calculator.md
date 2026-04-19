# DF-07 — Visit & Dispensing Calculator

## Purpose

Calculate expected kit demand from visit schedules, treatment arms, and pack configurations. This skill translates the clinical protocol into concrete supply numbers — how many kits are needed per patient per visit.

---

## Owner

**Primary:** Demand & Forecast Analyst

---

## When This Skill Is Used

- During demand modelling to convert enrollment numbers into kit quantities
- Used by DF-05 and DF-06 when building demand scenarios

---

## Inputs

1. **Visit schedules** — From parsed CTMS data (DI-05)
2. **Study configuration** — Treatment arms, pack sizes, items per visit

---

## Steps

1. **Map visit schedule to dispensing events** — For each visit type, determine what items are dispensed and in what quantity
2. **Calculate per-patient demand** — Total kits needed per patient across all visits in their treatment journey
3. **Scale by enrollment** — Multiply per-patient demand by projected enrollment to get total demand
4. **Break down by treatment arm** — Account for randomisation ratios
5. **Produce demand calculation** — Total kit demand by item, arm, and visit

---

## Output

- Kits per patient per visit by treatment arm
- Total per-patient demand across the study
- Total projected demand scaled by enrollment
- Breakdown by item and treatment arm
- Data source reference — data drop date, files used, and reporting period covered

---

## Notes

- This is a calculation skill, not a forecasting skill — it converts protocol parameters into supply numbers
- The output feeds into DF-05 (Scenario Modeller) and DF-08 (Screen Failure & Dropout Adjuster) for refinement
