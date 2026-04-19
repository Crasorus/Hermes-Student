# DF-06 — What-If Scenario Engine

## Purpose

Model specific user-defined scenarios that go beyond the standard three (base, optimistic, pessimistic). Examples include site closures, new country additions, protocol amendments, or changes to treatment arm ratios.

---

## Owner

**Primary:** Demand & Forecast Analyst

---

## When This Skill Is Used

- When specific what-if scenarios are requested by the user or triggered by an event
- During WF-03 (Protocol Amendment Impact) to model the demand impact of amendments

---

## Inputs

1. **Scenario definition** — Plain English description of what to model
2. **Current demand data** — Outputs from DF-01, DF-02, DF-03
3. **Study configuration** — Current study parameters as baseline

---

## Steps

1. **Interpret the scenario** — Understand what is changing (e.g., a site closes, a country is added, a visit is removed)
2. **Adjust the demand model** — Modify the relevant parameters to reflect the scenario
3. **Calculate impact** — Project demand under the adjusted parameters
4. **Compare to base case** — Quantify the difference in total demand, timeline, and distribution
5. **Produce scenario output** — The what-if result with assumptions, impact, and comparison to base case

---

## Output

- Scenario description and assumptions
- Projected demand under the scenario
- Comparison to base case (delta in units and percentage)
- Impact on study timeline
- Any risks or considerations specific to this scenario
- Data source reference — data drop date, files used, and reporting period covered

---

## Notes

- What-if scenarios are compared against the base case from DF-05 if available from the current cycle. If DF-05 has not run (e.g., during WF-03 Protocol Amendment Impact), compare against the approved demand baseline from the study package.
- This skill uses DF-07 and DF-08 internally to calculate demand for the modelled scenario, the same way DF-05 does for standard scenarios.
- Multiple what-if scenarios can be run in a single workflow
- This skill models demand impact only — supply and logistics impacts are assessed by other agents downstream
