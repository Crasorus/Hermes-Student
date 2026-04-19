# Pre-Flight Verifier — Quick Reference

## What is the Pre-Flight Step?

**SO-00: Workflow Pre-Flight Verifier** is the mandatory Step 0 of every workflow. It runs **DI-12: Aggregate Data Query Tool** to load all study data, compute verified aggregations, and validate data integrity before any agent begins analysis.

The pre-flight step exists to prevent counting errors — all agents draw numbers from the DI-12 output, never from raw CSV files.

## When to Use

- **Always** at the start of any workflow (Supervisor runs this automatically)
- **Manually** when you want to check data integrity on a data drop
- **Before** producing any numerical analysis or report

## How to Invoke DI-12

### Chat mode (no Python required)
Read the study's data files directly and perform the pre-flight analysis as Claude, following the steps in `skills/SO-00_workflow_preflight_verifier.md`. This is the default path for `/run-workflow` and the lab.

### Python runner (if installed)
```bash
python runner/di_12_aggregate_data_query.py \
  studies/{study_id}/data_drops/{date}/rtsm_actuals.csv \
  studies/{study_id}/data_drops/{date}/ctms_plan.csv \
  studies/{study_id}/data_drops/{date}/erp_inventory.csv \
  studies/{study_id}/config/study_config.json
```

## What You Get Back

A JSON object with:

### `rtsm_aggregations`
- `record_counts`: Total counts by event type
- `randomisations_by_site`: Count breakdown by site
- `randomisations_by_arm`: Count by treatment arm
- `dispensings_by_item`: Count by item
- `screen_failures_by_site`: Screening rates
- `date_range`: Earliest/latest event dates
- `site_inventory`: Stock on hand at each site

### `ctms_aggregations`
- `enrollment_plan_by_site`: Planned enrollment per site
- `enrollment_plan_total`: Total planned enrollment
- `enrollment_plan_by_country`: Plan by country
- `visit_schedules`: Visit windows by site

### `erp_aggregations`
- `stock_on_hand_by_depot`: Current stock levels
- `in_transit`: Active shipments
- `on_order`: Production orders
- `batch_expiry_profile`: Expiry dates and quantities

### `derived_metrics` (Pre-Computed)
- `enrollment_delta`: Actual vs planned, % change
- `demand_rate`: Dispensing rate per week
- `supply_coverage`: Weeks of supply by item

### `data_integrity_checks`
Eight validation checks:
1. Patient ID continuity (gaps, duplicates)
2. Site consistency (data vs config)
3. Item consistency (data vs config)
4. Arm consistency (data vs config)
5. Randomisation-dispensing balance
6. Screen failure rates (flag if unusual)
7. Date consistency
8. Expiry validation

### `overall_data_integrity`
- **PASS**: All checks passed, safe to proceed
- **WARNING**: Some issues, proceed with caution
- **FAIL**: Critical issues, halt workflow

## Pre-Flight Decision Rules

| Status | Action |
|--------|--------|
| PASS | Log and continue |
| WARNING | Log all warnings, flag outputs, continue |
| FAIL | HALT — report issues, do not proceed |

## Key Rules for Agents

1. **Always use DI-12 counts** — Never estimate or count rows manually
2. **Check integrity first** — If `overall_data_integrity` is FAIL, halt and report
3. **Reference DI-12 in audit trail** — Format: `"DI-12 verified: [count] [metric]"`
4. **Never sample data** — DI-12 reads 100% of files, use its output
5. **Halt if missing** — If `context.di12_output` is absent, request it from Supervisor

## Example Output

From the 2026-03-09 data drop:

```json
{
  "rtsm_aggregations": {
    "record_counts": {
      "randomisations_total": 60,
      "dispensings_total": 60,
      "screen_failures_total": 15
    }
  },
  "derived_metrics": {
    "enrollment_delta": {
      "actual_enrollment": 60,
      "planned_enrollment": 435,
      "delta_pct": -86.2,
      "delta_direction": "DECREASE"
    },
    "supply_coverage": {
      "ITEM-E": {
        "total_available": 106,
        "weeks_of_supply": 1.8
      }
    }
  },
  "overall_data_integrity": "WARNING",
  "recommendations": [
    {
      "severity": "CRITICAL",
      "message": "Patient ID gaps or duplicates detected"
    }
  ]
}
```

## Troubleshooting

**"File not found"**
- Check that data_drop_date is correct (use folder name in data_drops/)

**`overall_data_integrity: "FAIL"`**
- Check `recommendations` array for what to fix
- Common issues: missing sites, duplicate patient IDs, inconsistent arms
- Halt workflow until resolved

**"Unusual screen failure rates"**
- This is a WARNING, not a FAIL
- Proceed but flag for investigation

## See Also

- `skills/SO-00_workflow_preflight_verifier.md` — Pre-flight enforcement policy
- `skills/DI-12_aggregate_data_query_tool.md` — DI-12 full specification
- `runner/di_12_aggregate_data_query.py` — Python implementation
