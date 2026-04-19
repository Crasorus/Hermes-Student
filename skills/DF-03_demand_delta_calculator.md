# DF-03 — Demand Delta Calculator

## Purpose

Compare the current demand forecast to the approved baseline and quantify the gap. This skill answers the question: "Has demand changed, and by how much?"

---

## Owner

**Primary:** Demand & Forecast Analyst

---

## When This Skill Is Used

- During WF-01 (Demand Signal Refresh) after consumption and enrollment analysis
- The delta result determines whether scenario modelling and supply plan adjustments are needed

---

## Inputs

1. **Current consumption rates** — Output from DF-01
2. **Enrollment trajectory** — Output from DF-02
3. **Approved demand baseline** — The previously approved demand forecast from the study package
4. **Study configuration** — Items, treatment arms, countries
5. **Visit & dispensing parameters** — From study configuration (kits per visit per arm)

---

## Steps

1. **Calculate current demand forecast** — Use DF-01 consumption rates to establish per-site burn rate and DF-02 enrollment trajectory to project remaining patients and visits. Multiply remaining visits by per-visit kit requirements (from study configuration) to get projected remaining demand. This is a rate-based projection — DF-07 and DF-08 are used by DF-05 for scenario modelling, not here
2. **Compare to approved baseline** — For each country, treatment arm, and item
3. **Quantify the delta** — Express as both absolute units and percentage change
4. **Flag direction** — Is demand increasing or decreasing relative to baseline?
5. **Produce delta report** — Deltas by country, arm, and item, ready for threshold evaluation (DF-04)

---

## Output

- Delta by country, treatment arm, and item (absolute and percentage)
- Direction of change (increase or decrease)
- Overall study-level delta
- Summary of where the largest shifts are occurring
- Data source reference — data drop date, files used, and reporting period covered

---

## Notes

- This skill calculates the delta but does not judge significance — that is DF-04 (Threshold Evaluator)
- The delta report is one of the key artifacts of WF-01 and feeds into the Supply Analyst's planning
