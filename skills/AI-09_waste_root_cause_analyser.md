# AI-09 — Waste Root Cause Analyser

## Purpose

Identify patterns in overage and waste to surface the root causes. This goes beyond SI-08 (which estimates waste) to explain why waste is occurring and how to reduce it.

---

## Owner

**Primary:** Clinical Data & Insights Analyst

---

## When This Skill Is Used

- During reporting workflows when waste analysis is needed
- When waste levels exceed acceptable thresholds

---

## Inputs

1. **Waste estimate** — From SI-08
2. **Expiry profile** — From SI-03
3. **Order history** — From DI-04
4. **Consumption rates** — From DF-01
5. **Protocol change history** — If available

---

## Steps

1. **Categorise waste by source**:
   - Expiry — Stock expired before it could be used
   - Over-ordering — More stock ordered than needed
   - Protocol change — Demand changed due to amendments, making existing stock unnecessary
   - Other — Damage, recalls, or other causes
2. **Identify the top contributor** to waste
3. **Analyse patterns** — Is waste concentrated at specific locations, items, or time periods?
4. **Identify root causes** — Why is this waste occurring? (e.g., overly conservative ordering, long lead times, poor demand forecasting)
5. **Recommend mitigations** — Actionable steps to reduce waste

---

## Output

- Waste breakdown by source (expiry, over-ordering, protocol change, other)
- Contribution percentage for each source
- Root causes identified
- Recommendations to reduce waste

---

## Notes

- Some waste is inevitable in clinical trials — the goal is to minimise avoidable waste
- Root cause analysis requires data from multiple cycles to be most effective
- Feeds into reporting and budget analysis
