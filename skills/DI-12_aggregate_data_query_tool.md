# DI-12 — Aggregate Data Query Tool

## Purpose

Provide agents with 100% accurate, pre-computed aggregate summaries of RTSM, CTMS, and ERP data. This skill prevents data sampling errors, estimation mistakes, and incomplete analysis by computing definitive counts, sums, and aggregations from the full dataset before any agent analysis begins.

This is a **validation tool** — agents call this skill to verify that their calculations are based on accurate source data, not on previews or estimates.

---

## Owner

**Primary:** Supervisor (validation in SO-01: Workflow Router)
**Secondary:** All analytical agents (Demand Analyst, Supply Analyst, Compliance Manager)

---

## When This Skill Is Used

- **Mandatory**: At the start of every workflow, after DI-01 and DI-02 pass (file validation)
- **Optional but recommended**: Whenever an agent needs to produce a count, sum, or rate based on source data
- **Verification step**: Before any agent produces numerical outputs (demand delta, enrollment, stock position, etc.)

---

## Inputs

1. **RTSM actuals file** — `data_drops/{date}/rtsm_actuals.csv`
2. **Site inventory file** — `data_drops/{date}/site_inventory.csv` (NEW — contains current on-hand qty, weekly demand, reorder points)
3. **CTMS plan file** — `data_drops/{date}/ctms_plan.csv`
4. **ERP inventory file** — `data_drops/{date}/erp_inventory.csv`
5. **Study configuration** — `study_config.json` for treatment arms, items, sites, countries

---

## Steps

### Step 1: Read and Validate Files
- Load all four data files (RTSM, Site Inventory, CTMS, ERP)
- Verify non-empty and readable
- Confirm all required columns are present
- If any file is missing or unreadable, halt and report
- **Note:** site_inventory.csv is CRITICAL. If missing, halt immediately.

### Step 2: Compute RTSM Aggregations

**Record Counts by Type:**
```
randomisations_total = COUNT(rtsm WHERE event_type = 'randomisation')
dispensings_total = COUNT(rtsm WHERE event_type = 'dispensing')
screen_failures_total = COUNT(rtsm WHERE event_type = 'screen_failure')
returns_total = COUNT(rtsm WHERE event_type = 'return')
site_inventory_records = COUNT(rtsm WHERE event_type = 'site_inventory')
site_shipment_records = COUNT(rtsm WHERE event_type = 'site_shipment')
```

**Randomisations by Site:**
```
For each unique site in study_config.sites:
  randomisations[site] = COUNT(rtsm WHERE event_type = 'randomisation' AND site_id = site)
  randomisations[site, by_country] = GROUP BY country_code
  randomisations[site, by_arm] = GROUP BY arm_id
```

**Randomisations by Treatment Arm:**
```
For each arm in study_config.treatment_arms:
  randomisations[arm] = COUNT(rtsm WHERE event_type = 'randomisation' AND arm_id = arm)
```

**Dispensings by Item:**
```
For each item in study_config.items:
  dispensings[item] = COUNT(rtsm WHERE event_type = 'dispensing' AND item_id = item)
  dispensings[item, by_site] = GROUP BY site_id
  dispensings[item, by_country] = GROUP BY country_code
```

**Screen Failures by Site:**
```
For each site:
  screen_failures[site] = COUNT(rtsm WHERE event_type = 'screen_failure' AND site_id = site)
screening_rate[site] = (randomisations[site] + screen_failures[site]) / screen_failures[site]
```

**Date Range:**
```
earliest_event = MIN(event_date across all records)
latest_event = MAX(event_date across all records)
date_range_days = days between earliest_event and latest_event
```

### Step 2b: Compute Site Inventory Aggregations (NEW FILE)

**Site Inventory Summary:**
```
Load site_inventory.csv and extract for each site-item combination:
  on_hand_qty[site, item] = On_Hand_Qty
  weekly_demand[site, item] = Weekly_Demand (4-week running average)
  min_reorder_point[site, item] = Min_Reorder_Point
  max_reorder_point[site, item] = Max_Reorder_Point

Calculate derived metrics for each site-item:
  weeks_of_supply[site, item] = on_hand_qty / weekly_demand (if weekly_demand > 0)
  reorder_status[site, item] =
    "BELOW_MIN" if on_hand_qty < Min_Reorder_Point
    "BELOW_MAX" if on_hand_qty >= Min_Reorder_Point AND on_hand_qty < Max_Reorder_Point
    "AT_MAX" if on_hand_qty >= Max_Reorder_Point

Aggregated by site:
  total_on_hand[site] = SUM(On_Hand_Qty across all items)
  total_weekly_demand[site] = SUM(Weekly_Demand across all items)
  sites_below_min[site] = COUNT(items WHERE on_hand_qty < Min_Reorder_Point)
  sites_needing_reorder[site] = COUNT(items WHERE on_hand_qty <= Max_Reorder_Point)
```

### Step 3: Compute CTMS Aggregations

**Enrollment Plan by Site:**
```
For each site in ctms WHERE record_type = 'enrollment_plan':
  planned_enrollment[site] = planned_enrollment (from record)
  total_planned = SUM(planned_enrollment across all sites)
```

**Enrollment Plan by Country:**
```
For each country in study_config.countries:
  planned_enrollment[country] = SUM(planned_enrollment WHERE country_code = country)
```

**Visit Schedules:**
```
For each unique (site, visit_type) in ctms WHERE record_type = 'visit_schedule':
  visits[site, visit_type] = visit_window_days
```

### Step 4: Compute ERP Aggregations

**Stock On Hand by Depot:**
```
For each depot in supply_network.depots:
  For each item in study_config.items:
    stock_on_hand[depot, item] = SUM(quantity WHERE location = depot AND record_type = 'stock_on_hand')
    total_on_hand[depot] = SUM across all items
```

**In-Transit by Lane:**
```
For each shipment in transit:
  in_transit[origin, destination, item] = quantity
  total_in_transit = SUM across all shipments
```

**On-Order by Manufacturing Site:**
```
For each production order:
  on_order[item] = quantity
  total_on_order = SUM across all orders
```

**Batch Expiry Profile:**
```
For each batch (lot_number):
  batch[lot_number] = {item, location, quantity, expiry_date}
  expiry_summary = GROUP BY expiry_date, show oldest to newest
```

### Step 5: Compute Derived Metrics

**Enrollment Delta:**
```
actual_enrollment_total = randomisations_total
planned_enrollment_total = SUM(planned_enrollment from CTMS)
enrollment_delta_pct = (actual_enrollment_total - planned_enrollment_total) / planned_enrollment_total * 100
```

**Demand Rate (Preliminary):**
```
total_dispensings = dispensings_total
days_elapsed = date_range_days
dispensing_rate_per_day = total_dispensings / days_elapsed
dispensing_rate_per_week = dispensing_rate_per_day * 7
```

**Supply Coverage (Weeks):**
```
For each item:
  total_available[item] = stock_on_hand[item] + in_transit[item] + on_order[item]
  weeks_of_supply[item] = total_available[item] / (dispensing_rate_per_week)
```

### Step 6: Data Integrity Checks

Verify consistency across files:

```
CHECK 1: Patient ID Continuity
  Extract all patient_ids from RTSM (PAT-001, PAT-002, ...)
  Flag: Any gaps in sequence (e.g., PAT-001, PAT-002, PAT-004 — missing PAT-003)
  Flag: Duplicate records = same patient + same event type + same date
  Note: Multiple events (e.g., multiple dispensings) on different dates are normal and expected

CHECK 2: Site Consistency
  Extract all sites from RTSM (actual events)
  Extract all sites from CTMS (planned events)
  Extract all sites from study_config (defined sites)
  Flag: Any site in RTSM or CTMS not in study_config
  Flag: Any site in study_config with zero activity (no RTSM records)

CHECK 3: Item Consistency
  Extract all items from RTSM dispensings
  Extract all items from study_config
  Flag: Any item in RTSM not in study_config
  Flag: Any item in study_config with zero dispensings

CHECK 4: Arm Consistency
  Extract all arms from RTSM randomisations
  Extract all arms from study_config
  Flag: Any arm in RTSM not in study_config
  Flag: Any randomisation with invalid arm_id

CHECK 5: Randomisation-Dispensing Balance
  randomisations_count = total from Step 2
  dispensings_count = total from Step 2
  ongoing_patients = randomisations_count - dispensings_count (patients randomized but not yet dispensed)
  Flag: If dispensings_count > randomisations_count (unexpected scenario — verify source data)

CHECK 6: Screen Failure Rates by Site
  For each site:
    screening_attempts = randomisations + screen_failures
    screen_failure_rate = screen_failures / screening_attempts
    Flag: If screen_failure_rate > 50% (unusually high, warrant investigation)
    Flag: If screen_failure_rate = 0% (unusual for real-world sites, warrant investigation)

CHECK 7: Date Consistency
  For each site:
    first_event_date = earliest event date for that site
    last_event_date = latest event date for that site
    Flag: If last_event_date < first_event_date (impossible)
    Flag: If event_dates are in future relative to data_drop_date

CHECK 8: Expiry Date Validation
  For each batch:
    if expiry_date <= data_drop_date:
      Flag: CRITICAL — batch has expired
    if expiry_date - data_drop_date < 6 months:
      Flag: WARNING — batch expires within 6 months
```

### Step 7: Produce Output

Generate a structured JSON output containing all aggregations, integrity checks, and warnings.

---

## Output Format

```json
{
  "tool": "DI-12 — Aggregate Data Query Tool",
  "execution_timestamp": "<ISO 8601>",
  "data_drop_date": "<YYYY-MM-DD>",
  "files_processed": [
    {"file": "rtsm_actuals.csv", "status": "OK", "total_records": <count>},
    {"file": "site_inventory.csv", "status": "OK", "total_records": <count>},
    {"file": "ctms_plan.csv", "status": "OK", "total_records": <count>},
    {"file": "erp_inventory.csv", "status": "OK", "total_records": <count>}
  ],
  "rtsm_aggregations": {
    "record_counts": {
      "randomisations_total": <count>,
      "dispensings_total": <count>,
      "screen_failures_total": <count>,
      "returns_total": <count>,
      "site_shipment_records": <count>,
      "total_records": <count>
    },
    "randomisations_by_site": {
      "S42": {"count": <n>, "by_country": "US", "by_arm": {...}},
      "S43": {"count": <n>, "by_country": "US", "by_arm": {...}},
      ...
    },
    "randomisations_by_arm": {
      "ARM-01": <count>,
      "ARM-02": <count>,
      "ARM-03": <count>
    },
    "dispensings_by_item": {
      "ITEM-E": <count>,
      "ITEM-O": <count>,
      "ITEM-G": <count>
    },
    "screen_failures_by_site": {
      "S42": {"count": <n>, "screening_rate": <rate>},
      ...
    },
    "date_range": {
      "earliest_event": "<YYYY-MM-DD>",
      "latest_event": "<YYYY-MM-DD>",
      "days_elapsed": <days>
    },
  },
  "site_inventory_aggregations": {
    "site_inventory_records": <count>,
    "by_site": {
      "S42": {
        "total_on_hand": <qty>,
        "total_weekly_demand": <qty/week>,
        "items": {
          "ITEM-E": {
            "on_hand_qty": <qty>,
            "weekly_demand": <qty/week>,
            "min_reorder_point": <qty>,
            "max_reorder_point": <qty>,
            "weeks_of_supply": <weeks>,
            "reorder_status": "BELOW_MIN | BELOW_MAX | AT_MAX"
          },
          ...
        },
        "items_below_min": <count>,
        "items_needing_reorder": <count>
      },
      ...
    },
    "by_item": {
      "ITEM-E": {
        "total_on_hand_across_sites": <qty>,
        "total_weekly_demand_across_sites": <qty/week>,
        "sites_below_min": <count>,
        "sites_needing_reorder": <count>,
        "site_details": [
          {"site": "S42", "on_hand": <qty>, "weekly_demand": <qty>, "reorder_status": "..."},
          ...
        ]
      },
      ...
    }
  },
  "ctms_aggregations": {
    "enrollment_plan_by_site": {
      "S42": <planned>,
      "S43": <planned>,
      ...
    },
    "enrollment_plan_total": <total_planned>,
    "enrollment_plan_by_country": {
      "US": <total>,
      "CA": <total>
    },
    "visit_schedules": {
      "S42": {"screening": 0, "baseline": 7, "week_4": 35, ...},
      ...
    }
  },
  "erp_aggregations": {
    "stock_on_hand_by_depot": {
      "DP-CARY-05": {
        "ITEM-E": <qty>,
        "ITEM-O": <qty>,
        "ITEM-G": <qty>,
        "total": <total>
      }
    },
    "in_transit": {
      "SHIP-001": {"item": "ITEM-E", "quantity": <qty>, "origin": "PLANT-DUB-06", "destination": "DP-CARY-05"},
      ...
    },
    "on_order": {
      "ORD-001": {"item": "ITEM-G", "quantity": <qty>}
    },
    "batch_expiry_profile": [
      {"lot_number": "LOT-001", "item": "ITEM-E", "location": "DP-CARY-05", "quantity": <qty>, "expiry_date": "2027-09-11"},
      ...
    ]
  },
  "derived_metrics": {
    "enrollment_delta": {
      "actual_enrollment": <count>,
      "planned_enrollment": <count>,
      "delta_pct": <pct>,
      "delta_direction": "INCREASE | DECREASE"
    },
    "demand_rate": {
      "total_dispensings": <count>,
      "days_elapsed": <days>,
      "dispensing_rate_per_day": <rate>,
      "dispensing_rate_per_week": <rate>
    },
    "supply_coverage": {
      "ITEM-E": {
        "on_hand": <qty>,
        "in_transit": <qty>,
        "on_order": <qty>,
        "total_available": <qty>,
        "weeks_of_supply": <weeks>
      },
      ...
    }
  },
  "data_integrity_checks": {
    "patient_id_continuity": {
      "status": "PASS | FAIL",
      "issues": ["<issue 1>", "<issue 2>"],
      "patient_id_range": "PAT-001 to PAT-XXX",
      "total_unique_patients": <count>
    },
    "site_consistency": {
      "status": "PASS | FAIL",
      "issues": ["<issue 1>"],
      "sites_in_study_config": <list>,
      "sites_with_activity": <list>,
      "inactive_sites": <list>
    },
    "item_consistency": {
      "status": "PASS | FAIL",
      "issues": ["<issue 1>"],
      "items_in_study_config": <list>,
      "items_with_dispensings": <list>
    },
    "arm_consistency": {
      "status": "PASS | FAIL",
      "issues": ["<issue 1>"]
    },
    "randomisation_dispensing_balance": {
      "status": "PASS | FAIL",
      "randomisations": <count>,
      "dispensings": <count>,
      "ongoing_patients": <count>,
      "issues": ["<issue 1>"]
    },
    "screen_failure_rates": {
      "status": "PASS | WARNING",
      "flagged_sites": [
        {"site": "S42", "rate_pct": <pct>, "flag": "unusually_high | unusually_low"}
      ]
    },
    "date_consistency": {
      "status": "PASS | FAIL",
      "issues": ["<issue 1>"]
    },
    "expiry_validation": {
      "status": "PASS | WARNING | FAIL",
      "expired_batches": <count>,
      "batches_expiring_within_6_months": <count>,
      "flagged_batches": [
        {"lot_number": "LOT-001", "expiry_date": "2027-09-11", "flag": "expires_soon"}
      ]
    }
  },
  "overall_data_integrity": "PASS | WARNING | FAIL",
  "recommendations": [
    {
      "category": "<integrity_check>",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "message": "<explanation>",
      "action": "<what to do>"
    }
  ]
}
```

---

## Halt Conditions

Halt and raise an error if:

1. **Any data file missing or unreadable** — Cannot proceed without complete data (CRITICAL: site_inventory.csv is required)
2. **site_inventory.csv missing or unparseable** — Cannot proceed. This is the source of truth for current site inventory status
3. **Overall data integrity status is FAIL** — Critical issues prevent safe analysis
4. **Patient ID continuity fails with gaps** — Cannot trust patient records
5. **Site consistency fails** — Sites in data don't match study configuration

**Note:** Randomisation-dispensing balance mismatch (dispensings > randomisations) is flagged as WARNING, not halt.

Flag but continue if:

1. **Data integrity status is WARNING** — Issues exist but analysis can proceed with caution
2. **Screen failure rates are unusual** — Flag for investigation but don't halt
3. **Expiry dates are flagged** — Monitor but don't halt current analysis

---

## How Agents Use This Skill

**Pattern:**
```
1. Agent receives task from Supervisor
2. Agent calls: DI-12 Aggregate Data Query Tool
3. Receives JSON output with all counts and aggregations
4. Uses numbers from DI-12 output DIRECTLY in analysis (not from CSV preview)
5. References DI-12 output in audit trail: "Randomisations: 60 (verified by DI-12)"
6. Never estimates or samples data
```

**Example in Demand Analyst workflow:**
```
Task: Calculate enrollment delta
Step 1: Call DI-12
Output: {"rtsm_aggregations": {"record_counts": {"randomisations_total": 60}},
         "ctms_aggregations": {"enrollment_plan_total": 435}}
Step 2: Calculate: delta = (60 - 435) / 435 = -86.2%
Step 3: Log: "Enrollment delta calculated from DI-12 verified counts: 60 actual vs 435 planned"
Step 4: Output: No estimation or uncertainty
```

---

## Notes

- **DI-12 is a validation tool first, data processing tool second** — Its primary purpose is to catch errors and verify accuracy before agents proceed
- **Every count in DI-12 output is derived from 100% of the source data** — No sampling, no preview-based estimates
- **DI-12 output should be run once per workflow at the start** — Agents can reference it throughout the workflow
- **DI-12 is a "single source of truth" for data counts** — If an agent's manual count differs from DI-12, the agent's manual count is wrong
- **Data integrity checks are non-negotiable** — All seven checks must pass or warning-level issues must be explicitly acknowledged
