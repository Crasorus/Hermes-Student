# AI-02 — Anomaly Detector

## Purpose

Identify statistical anomalies in consumption, enrollment, or inventory data that may indicate data errors, protocol deviations, or emerging operational issues.

---

## Owner

**Primary:** Clinical Data & Insights Analyst

---

## When This Skill Is Used

- During hot spot surveillance (WF-04)
- During data quality assessment to catch unexpected patterns

---

## Inputs

1. **Parsed RTSM data** — From DI-03
2. **Parsed ERP data** — From DI-04
3. **Parsed CTMS data** — From DI-05
4. **Historical data** — Previous cycle data if available

---

## Steps

1. **Establish expected ranges** for key metrics (consumption rate, enrollment rate, inventory levels) based on historical data or study averages
2. **Compare current data** to expected ranges
3. **Flag values outside expected range** — Sudden spikes, drops, or unexpected patterns
4. **Assess confidence** — How confident is the anomaly detection? (HIGH, MEDIUM, LOW)
5. **Suggest possible cause** — Data error, protocol deviation, operational issue, or natural variation

---

## Output

- List of anomalies with location, metric, expected value, observed value, and deviation
- Confidence level for each anomaly
- Possible causes
- Recommended follow-up actions

---

## Notes

- Not every fluctuation is an anomaly — this skill should distinguish signal from noise
- Low-confidence anomalies should be flagged for monitoring, not immediate action
- Anomalies may indicate data quality issues rather than operational problems
