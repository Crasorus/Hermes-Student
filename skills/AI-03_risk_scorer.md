# AI-03 — Risk Scorer

## Purpose

Assign a composite risk score to each site, country, and depot based on multiple supply chain signals. This gives planners a single number to prioritise attention.

---

## Owner

**Primary:** Clinical Data & Insights Analyst

---

## When This Skill Is Used

- During hot spot surveillance (WF-04)
- During plan scoring (WF-02 (Plan Scoring phase)) to assess the risk dimension

---

## Inputs

1. **Safety stock status** — From SI-04
2. **Expiry profile** — From SI-03
3. **Consumption rates** — From DF-01
4. **Enrollment trajectory** — From DF-02
5. **In-transit status** — From LT-07
6. **Hot spots** — From AI-01

---

## Steps

1. **For each location** (site, country, depot), assess risk across multiple factors:
   - Stock level relative to safety stock
   - Expiry exposure
   - Consumption trend (stable, increasing, decreasing)
   - Enrollment trajectory (on plan, behind, ahead)
   - Shipment reliability (any delays?)
   - Hot spot count
2. **Weight each factor** and calculate a composite risk score (0-100, higher = more risk)
3. **Classify into risk tiers** — CRITICAL, HIGH, MEDIUM, LOW
4. **Rank all locations** by risk score

---

## Output

- Risk score for each location (0-100)
- Contributing factors with individual scores
- Risk tier classification
- Locations ranked by risk (highest first)

---

## Notes

- The risk score is a summary tool — reviewers should look at the contributing factors for detail
- Risk scores are relative, not absolute — they help prioritise attention across locations
