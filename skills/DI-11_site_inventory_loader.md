# DI-11 — Site Inventory Loader

## Purpose

Load and validate the site_inventory.csv file, which contains the current snapshot of inventory status at each site. This file is critical for understanding real-time site supply positions, current demand patterns, and reorder point settings.

---

## Owner

**Primary:** Demand & Forecast Analyst (via DI-12)
**Secondary:** Supply Analyst (for supply planning)

---

## When This Skill Is Used

- Part of the DI-12 (Aggregate Data Query Tool) execution at the start of every workflow
- Whenever current site inventory status is needed for demand or supply analysis
- After data quality checks pass (DI-01 and DI-02)

---

## Inputs

1. **Site inventory file** — `data_drops/{date}/site_inventory.csv`
2. **Study configuration** — `study_config.json` for site list and item list

---

## Steps

1. **Read the site_inventory.csv file**
   - Load the file from the current data drop folder
   - Confirm the file is non-empty and readable
   - Verify all required columns are present: Site, item_id, On_Hand_Qty, Weekly_Demand, Min_Reorder_Point, Max_Reorder_Point

2. **Validate data integrity**
   - Confirm all sites in the file match sites in study_config.json
   - Confirm all items in the file match items in study_config.json
   - Flag any unknown or unmapped sites or items
   - Verify all numeric columns are non-negative
   - Flag any records with missing values

3. **Compute derived metrics for each site-item combination**
   ```
   weeks_of_supply = On_Hand_Qty / Weekly_Demand (if Weekly_Demand > 0)

   reorder_status =
     "BELOW_MIN" if On_Hand_Qty < Min_Reorder_Point
     "BELOW_MAX" if On_Hand_Qty >= Min_Reorder_Point AND On_Hand_Qty < Max_Reorder_Point
     "AT_MAX" if On_Hand_Qty >= Max_Reorder_Point

   estimated_stockout_days = (On_Hand_Qty / Weekly_Demand) * 7 (if Weekly_Demand > 0)
   ```

4. **Aggregate by site**
   - Total on-hand across all items at each site
   - Total weekly demand across all items at each site
   - Count of items below minimum reorder point
   - Count of items needing reorder (below max but above or at min)

5. **Aggregate by item**
   - Total on-hand across all sites for each item
   - Total weekly demand across all sites for each item
   - Count of sites below minimum for each item
   - Count of sites needing reorder for each item

6. **Produce output**
   - Validated, enriched site inventory data with derived metrics
   - By-site and by-item aggregations
   - List of sites/items requiring immediate attention (below min)

---

## Output

- **Validated site inventory dataset** — One record per site-item combination with:
  - Site and item identifiers
  - On-hand quantity, weekly demand, min/max reorder points
  - Weeks of supply (calculated)
  - Reorder status (BELOW_MIN / BELOW_MAX / AT_MAX)
  - Estimated days to stockout (if applicable)

- **Aggregations**:
  - By-site: total on-hand, total weekly demand, items needing attention
  - By-item: total on-hand across sites, total weekly demand, sites needing attention

- **Alerts**:
  - List of site-item combinations requiring immediate reorder (BELOW_MIN)
  - List of site-item combinations needing reorder within normal cycle (BELOW_MAX)
  - Data validation issues (unmapped sites/items, missing values, implausible data)

---

## Halt Conditions

- Recommend halt if the file cannot be read or is fundamentally unparseable
- Recommend halt if more than a configurable percentage of records have critical issues (e.g., missing site, missing item)
- Recommend halt if site_inventory.csv is missing entirely (this is a CRITICAL file as of 2026-03-14)

Flag but continue if:
- A small number of records have minor issues (can be excluded from analysis)
- A site or item is in the file but not in study_config (flag as orphaned data)

---

## Notes

- This skill does not analyse inventory levels — it prepares and validates them. Analysis happens in demand and supply skills (DF-01, DF-03, SI-02, etc.)
- Site_inventory.csv is a snapshot as of the data drop date — it represents current reality, not planned or forecasted levels
- Weekly_Demand in this file is a 4-week running average, which smooths out weekly variation
- Min_Reorder_Point and Max_Reorder_Point are the current operational settings for that site — they may vary by site/item or be standardized across the study
- **Critical difference from RTSM:** Site inventory is no longer in rtsm_actuals.csv. It is now in a dedicated file. This enables more frequent or updated inventory snapshots without requiring full RTSM exports.

---

## Changes (2026-03-14)

**NEW FILE:** Site_inventory.csv is a new data source as of this date.
- Previously, site inventory was sometimes embedded in RTSM actuals or derived from multiple sources
- Now it is a dedicated, authoritative file updated at each data drop
- This change simplifies data handling and ensures inventory status is always current and consistent

