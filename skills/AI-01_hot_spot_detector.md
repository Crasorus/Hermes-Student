# AI-01 — Hot Spot Detector

## Purpose

Scan supply chain data for predefined risk patterns that indicate emerging problems — stock-outs, expiry clusters, shipment delays, and consumption anomalies.

---

## Owner

**Primary:** Clinical Data & Insights Analyst

---

## When This Skill Is Used

- During WF-04 (Routine Monitoring) — runs continuously or daily
- After data ingestion to surface risks early

---

## Inputs

1. **Stock position** — From SI-01
2. **Expiry profile** — From SI-03
3. **In-transit status** — From LT-07
4. **Consumption rates** — From DF-01
5. **Safety stock status** — From SI-04

---

## Steps

1. **Scan for stock-out risk** — Sites or countries with stock below safety level
2. **Scan for expiry clusters** — Locations where multiple batches expire in the same window
3. **Scan for shipment delays** — In-transit shipments that are overdue or at risk
4. **Scan for consumption anomalies** — Sites with unusually high or low consumption vs. the group
5. **Flag each hot spot** with location, pattern type, and severity (CRITICAL, HIGH, MEDIUM, LOW)
6. **Rank hot spots** by potential patient impact and operational urgency

---

## Output

- List of hot spots with location, pattern, severity, and supporting data
- Hot spots ranked by urgency
- Recommended actions for each hot spot

---

## Notes

- Hot spots are patterns, not judgments — the skill detects the pattern and flags it for review
- Critical hot spots should trigger the Supervisor to consider a supply plan adjustment
- Feeds into RC-05 (Hot Spot Alert Writer) for stakeholder communication
