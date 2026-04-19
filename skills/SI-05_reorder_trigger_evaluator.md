# SI-05 — Reorder Point Policy Evaluator

## Purpose

Evaluate current reorder point settings against dynamically calculated optimal values based on current demand, and recommend policy adjustments when thresholds are misaligned. Ensures reorder points remain effective as demand patterns change.

---

## Owner

**Primary:** Supply & Inventory Analyst

---

## When This Skill Is Used

- After SI-04 (Safety Stock Checker) has identified locations at or below threshold
- Determines which locations need orders placed

---

## Inputs

1. **Current weekly demand by item and location** — From demand analyst or DF-* skills (recent actuals or forecast)
2. **Current reorder point settings** — From `reference/reorder_policies.json`:
   - Stored `min_reorder_point` and `max_reorder_point` values per site/item (or derived from stored policy params)
3. **Policy parameters** — From `reference/reorder_policies.json`:
   - `review_period_days`, `cycle_service_level`, `moq`, `pack_multiple`
4. **Lead times** — From `supply_network.json` (shipping_lanes) or DI-06
5. **Current inventory levels** — From DF-* demand skills or inventory system
6. **Historical reorder point adequacy** — From SI-04 (Safety Stock Checker) or event logs

---

## Steps

1. **Calculate optimal reorder points** for each item-location pair using current demand:
   - For each item and location, retrieve:
     - Current weekly demand (from demand analyst or DF-* skills)
     - Lead time (from supply_network.json or DI-06)
     - Policy parameters: `review_period_days`, `cycle_service_level`, `moq` (from reorder_policies.json with item-level overrides)
   - Call `runner/reorder_calculator.py:calculate_reorder_points()` with:
     - `weekly_demand`, `lead_time_days`, `review_period_days`, `cycle_service_level`, `moq`
   - Output: **`calculated_min_s`** and **`calculated_max_S`** — optimal thresholds for current demand

2. **Compare calculated vs. stored reorder points**:
   - Retrieve currently stored `stored_min_s` and `stored_max_S` from reorder_policies.json or inventory system
   - Calculate **delta (variance)**:
     - `min_delta = calculated_min_s - stored_min_s`
     - `max_delta = calculated_max_S - stored_max_S`
   - Determine **adjustment category**:
     - `|min_delta| > 10%` or `|max_delta| > 10%` → **RECOMMEND ADJUSTMENT** (variance exceeds threshold)
     - `|min_delta| <= 10%` and `|max_delta| <= 10%` → **ALIGNED** (within acceptable tolerance)

3. **Diagnose misalignment root cause**:
   - **If calculated_min > stored_min:** Demand has increased; current threshold insufficient for new demand level
   - **If calculated_min < stored_min:** Demand has decreased; current threshold is overly conservative
   - **If calculated_max > stored_max:** Order quantities may be too small; risk of stock depletion between orders
   - **If calculated_max < stored_max:** Over-ordering; excess inventory and holding costs

4. **Generate policy adjustment recommendations**:
   - **For HIGH-DELTA items** (>10% variance):
     - Recommend updating policy parameters in reorder_policies.json
     - Suggest new values: `calculated_min_s` and `calculated_max_S`
     - Flag the reason: demand shift, policy obsolescence, lead time change
     - Indicate impact: "Increasing min point to {new_s} will reduce stockout risk by X%"
   - **For LOW-DELTA items** (within tolerance):
     - Report as "ALIGNED" — no action needed
     - Flag if pattern is trending (e.g., "min point has drifted +15% over last 3 reviews")

5. **Assess inventory currently trapped in old thresholds**:
   - Compare current_stock to both stored and calculated thresholds
   - If `current_stock > calculated_max_S`, identify excess inventory tied to outdated high thresholds
   - If `current_stock < calculated_min_s`, flag as immediate risk under new demand scenario

6. **Produce reorder point policy adjustment report**:
   - Items requiring policy updates, ranked by variance magnitude
   - Recommended changes with business impact summary
   - Audit trail: old values → new values, reason, demand basis date

---

## Output

**Policy Alignment Report:**
- Item-location pairs with policy status (ALIGNED, RECOMMEND ADJUSTMENT)
- Variance analysis: delta between calculated and stored reorder points (as % and absolute units)
- Root cause diagnosis: demand increase, demand decrease, lead time change, policy drift
- Recommended adjustments with new min/max values and business impact
- Inventory implications: excess stock tied to outdated thresholds, risk exposure under new demand
- Audit trail: timestamp, demand basis, old values, proposed new values, change justification
- Ranked by urgency: HIGH-DELTA (>10%) → TRENDING (5-10%) → ALIGNED (<5%)

---

## Notes

- **Continuous policy tuning**: This skill acts as a "thermostat" for reorder policies. As demand patterns change, calculated vs. stored deltas trigger recommended adjustments.
- **Tolerance zone (±10%)**: Small variances (<10%) are acceptable and account for normal demand fluctuations. Only larger deviations trigger adjustment recommendations, avoiding over-reactivity.
- **Poisson approximation**: For low-count demand scenarios (typical in clinical trials), std dev = sqrt(mean) is appropriate and eliminates need for historical variability data.
- **Lead time baked in**: Calculated reorder points fully account for replenishment lead time. The threshold already includes safety stock to cover expected demand during lead time.
- **Policy-driven flexibility**: Item-level overrides in `reorder_policies.json` enable fine-grained control. High-demand items get frequent reviews (3-7 days) and strict CSL; low-demand items relax constraints (longer review, lower CSL).
- **Demand Analyst integration**: The Demand Analyst uses this skill output to recommend policy updates to SI-05 via `reorder_policies.json` changes. Updates are committed with audit trail.
- **Feeds into policy update workflow**: Recommendations from this skill → Demand Analyst review → Policy adjustment PR → reorder_policies.json update
- **Dependency**: Requires `runner/reorder_calculator.py` (Python function callable from agent environment)
