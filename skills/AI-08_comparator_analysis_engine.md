# AI-08 — Comparator Analysis Engine

## Purpose

Analyse comparator drug supply patterns separately from investigational product. Comparator drugs often have different supply chains, lead times, and constraints that require dedicated analysis.

---

## Owner

**Primary:** Clinical Data & Insights Analyst

---

## When This Skill Is Used

- When the study includes comparator drugs
- During supply planning and reporting to ensure comparator supply is tracked separately

---

## Inputs

1. **Study configuration** — Which items are comparator drugs
2. **Stock position** — From SI-01 (filtered to comparator items)
3. **Consumption rates** — From DF-01 (filtered to comparator items)
4. **Supply network** — Comparator-specific supply lanes (if different)

---

## Steps

1. **Identify comparator items** from the study configuration
2. **Analyse comparator supply separately** — Stock position, consumption rate, weeks of supply
3. **Identify comparator-specific risks** — Different lead times, single-source supply, limited availability
4. **Compare comparator supply health to investigational product** — Are there any asymmetric risks?
5. **Produce comparator analysis** — Dedicated view of comparator supply status

---

## Output

- Comparator supply position (stock, consumption, weeks of supply)
- Comparator-specific risks
- Comparison to investigational product supply health
- Recommendations for comparator supply management

---

## Notes

- Not all studies have comparator drugs — this skill is only applicable when comparators are defined in the study configuration
- Comparator supply chains often have less flexibility than investigational product — risks should be flagged early
