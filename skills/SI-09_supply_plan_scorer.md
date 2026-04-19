# SI-09 — Supply Plan Scorer

## Purpose

Score the supply plan across four dimensions — efficiency, risk, cost, and complexity — to give planners and reviewers a quick assessment of plan quality.

---

## Owner

**Primary:** Supply & Inventory Analyst, Clinical Data & Insights Analyst (shared)

---

## When This Skill Is Used

- After the supply plan is complete (WF-02, Phase 5 — Plan Scoring)
- Produces the Supply Plan Score Card artifact

---

## Inputs

1. **Supply plan** — Order recommendations from SI-06
2. **Waste estimate** — Output from SI-08
3. **Supply gaps** — Output from SI-07
4. **Safety stock status** — Output from SI-04
5. **Budget data** — From policies (DI-07)

---

## Steps

1. **Score Efficiency (0-100)** — How right-sized is the plan? Low waste = high score. High overage = low score.
2. **Score Risk (0-100)** — Are safety stocks adequate? Are gaps closed? Low risk = high score.
3. **Score Cost (0-100)** — Is the plan within budget? Lower cost relative to budget = higher score.
4. **Score Complexity (0-100)** — How many shipments, vendors, and lanes are involved? Simpler = higher score.
5. **Calculate composite score** — Weighted average of the four dimensions
6. **Produce commentary** — Plain English assessment of the plan's strengths and weaknesses

---

## Output

- Scores for each dimension (efficiency, risk, cost, complexity) on a 0-100 scale
- Composite score
- Plain English commentary on plan quality
- Key strengths and weaknesses

---

## Notes

- The scoring is relative, not absolute — a score of 80 means the plan is good across the dimensions, not that it is 80% optimal
- The commentary should help non-technical reviewers understand what the scores mean
- This is the final analytical step before the plan goes to human review
