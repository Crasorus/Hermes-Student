# DF-01 — Consumption Rate Calculator

## Purpose

Calculate the actual kit consumption rate from RTSM dispensing data, broken down by site, country, and treatment arm. This provides the factual baseline of how quickly supply is being used.

---

## Owner

**Primary:** Demand & Forecast Analyst

---

## When This Skill Is Used

- During WF-01 (Demand Signal Refresh) as the first analytical step after data parsing
- Whenever an updated consumption rate is needed for planning

---

## Inputs

1. **Parsed RTSM data** — Output from DI-03 (dispensing events)
2. **Study configuration** — Treatment arms, items, pack sizes

---

## Steps

1. **Group dispensing events** by site, country, and treatment arm
2. **Calculate consumption rate** for each grouping:
   - Total units dispensed over the reporting period
   - Rate expressed as units per site per week and units per patient per visit
3. **Identify outliers** — Flag sites where consumption rate deviates from the country or study median beyond the configured threshold. Default method: sites outside 1.5x IQR from the median are flagged. The method and threshold can be overridden in `study_config.json`
4. **Produce summary** — Overall consumption rate and breakdowns by each dimension

---

## Output

- Consumption rates by site, country, and treatment arm
- Overall study-wide consumption rate
- Outlier flags for sites with unusual consumption patterns
- Data source reference — data drop date, files used, and reporting period covered

---

## Validation Against Site Inventory (NEW)

After calculating consumption rates, **cross-reference with site_inventory.csv Weekly_Demand field:**
- Site_inventory.csv contains the 4-week running average weekly demand at each site
- Compare calculated consumption rate vs. site_inventory Weekly_Demand
- Flag any variance > 20% as a potential data quality issue or site activity change
- Log the comparison in the output for audit trail

## Notes

- This skill calculates what has happened — it does not forecast. Forecasting is DF-02 and DF-05.
- The consumption rate from this skill feeds into SI-02 (Weeks of Supply Calculator) and DF-03 (Demand Delta Calculator)
- **As of 2026-03-14:** Site inventory data is now in site_inventory.csv (separate file, not in RTSM). Use DI-12 site_inventory_aggregations for validated data.
