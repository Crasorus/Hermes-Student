# DF-04 — Threshold Evaluator

## Purpose

Apply configurable significance thresholds to demand deltas and classify each delta as significant or minor. This skill is the decision gate that determines whether further action (scenario modelling, supply plan adjustment) is needed.

---

## Owner

**Primary:** Demand & Forecast Analyst, Supervisor (shared)

---

## When This Skill Is Used

- Immediately after DF-03 (Demand Delta Calculator) produces deltas
- The result determines whether the workflow fast-tracks (minor deltas) or continues to scenario modelling (significant deltas)

---

## Inputs

1. **Delta report** — Output from DF-03
2. **Study configuration** — Threshold settings (default 10%, with per-item or per-country overrides)

---

## Steps

1. **Load thresholds** from study configuration — default and any overrides
2. **Apply threshold to each delta** — Compare the percentage delta to the applicable threshold
3. **Classify each delta** as SIGNIFICANT or MINOR
4. **Determine overall significance** — If any delta is significant, the overall result is significant
5. **Produce evaluation result** — Each delta with its classification and the threshold that was applied

---

## Output

- Each delta classified as SIGNIFICANT or MINOR
- The threshold applied to each (noting any overrides)
- Overall significance flag
- Recommendation: proceed to scenario modelling or fast-track to reporting
- Data source reference — data drop date, files used, and reporting period covered

---

## Notes

- The default threshold is 10% but this is fully configurable per study, per item, or per country in `study_config.json`
- A delta in either direction (increase or decrease) can be significant
- This skill is the branching point in WF-01 — significant deltas trigger full analysis, minor deltas trigger fast-track reporting
