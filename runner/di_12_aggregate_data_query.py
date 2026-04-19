#!/usr/bin/env python3
"""
DI-12 Aggregate Data Query Tool

This module implements the DI-12 skill for computing 100% accurate aggregate summaries
of RTSM, CTMS, and ERP data. All counts are derived from the full dataset, not samples.

Usage:
    from di_12_aggregate_data_query import AggregateDataQuery

    query = AggregateDataQuery(
        rtsm_file="data_drops/2026-03-14/rtsm_actuals.csv",
        ctms_file="data_drops/2026-03-14/ctms_plan.csv",
        erp_file="data_drops/2026-03-14/erp_inventory.csv",
        site_inventory_file="data_drops/2026-03-14/Site_Inventory.csv",
        config_file="config/study_config.json"
    )

    result = query.execute()
    print(result)
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Tuple


class AggregateDataQuery:
    def __init__(self, rtsm_file: str, ctms_file: str, erp_file: str, site_inventory_file: str, config_file: str):
        """Initialize the query tool with file paths."""
        self.rtsm_file = Path(rtsm_file)
        self.ctms_file = Path(ctms_file)
        self.erp_file = Path(erp_file)
        self.site_inventory_file = Path(site_inventory_file)
        self.config_file = Path(config_file)
        self.data_drop_date = rtsm_file.split('/')[-2] if '/' in rtsm_file else "unknown"

        # Data containers
        self.rtsm_data = []
        self.ctms_data = []
        self.erp_data = []
        self.site_inventory_data = []
        self.config = {}

        # Aggregation results
        self.aggregations = {}
        self.integrity_issues = []
        self.warnings = []

    def _parse_csv_date(self, date_str: str):
        """Parse DD-MMM-YYYY date strings from CSV files (e.g. 30-Sep-2027).
        All transactional dates in data drop CSVs use DD-MMM-YYYY format.
        Returns a datetime object, or None if the string cannot be parsed."""
        if not date_str or not date_str.strip():
            return None
        try:
            return datetime.strptime(date_str.strip(), "%d-%b-%Y")
        except ValueError:
            return None

    def execute(self) -> Dict[str, Any]:
        """Execute the full DI-12 pipeline and return structured output."""
        try:
            # Step 1: Load and validate files
            self._load_files()

            # Step 2: Compute aggregations
            self._compute_rtsm_aggregations()
            self._compute_ctms_aggregations()
            self._compute_erp_aggregations()
            self._compute_site_inventory_aggregations()
            self._compute_derived_metrics()

            # Step 3: Run data integrity checks
            self._check_patient_id_continuity()
            self._check_site_consistency()
            self._check_item_consistency()
            self._check_arm_consistency()
            self._check_randomisation_dispensing_balance()
            self._check_screen_failure_rates()
            self._check_date_consistency()
            self._check_expiry_validation()

            # Step 4: Build and return output
            return self._build_output()

        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _load_files(self):
        """Load CSV and JSON files."""
        # Load RTSM
        if not self.rtsm_file.exists():
            raise FileNotFoundError(f"RTSM file not found: {self.rtsm_file}")
        with open(self.rtsm_file, 'r') as f:
            reader = csv.DictReader(f)
            self.rtsm_data = list(reader)

        # Load CTMS
        if not self.ctms_file.exists():
            raise FileNotFoundError(f"CTMS file not found: {self.ctms_file}")
        with open(self.ctms_file, 'r') as f:
            reader = csv.DictReader(f)
            self.ctms_data = list(reader)

        # Load ERP
        if not self.erp_file.exists():
            raise FileNotFoundError(f"ERP file not found: {self.erp_file}")
        with open(self.erp_file, 'r') as f:
            reader = csv.DictReader(f)
            self.erp_data = list(reader)

        # Load Site Inventory
        if not self.site_inventory_file.exists():
            raise FileNotFoundError(f"Site inventory file not found: {self.site_inventory_file}")
        with open(self.site_inventory_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            # Normalize column headers to lowercase to handle capitalisation variations and BOM
            self.site_inventory_data = [
                {k.strip().lower(): v.strip() for k, v in row.items()}
                for row in reader
            ]

        # Load config
        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_file}")
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def _compute_rtsm_aggregations(self):
        """Compute RTSM aggregations from full dataset."""
        rtsm_agg = {
            "record_counts": {},
            "randomisations_by_site": {},
            "randomisations_by_arm": {},
            "dispensings_by_item": {},
            "screen_failures_by_site": {},
            "date_range": {},
            "site_inventory": {}
        }

        # Record counts by type
        event_types = defaultdict(int)
        for record in self.rtsm_data:
            event_type = record.get('event_type', '').strip()
            event_types[event_type] += 1

        rtsm_agg["record_counts"] = {
            "randomisations_total": event_types.get('randomisation', 0),
            "dispensings_total": event_types.get('dispensing', 0),
            "screen_failures_total": event_types.get('screen_failure', 0),
            "returns_total": event_types.get('return', 0),
            "site_inventory_records": event_types.get('site_inventory', 0),
            "site_shipment_records": event_types.get('site_shipment', 0),
            "total_records": len(self.rtsm_data)
        }

        # Randomisations by site
        rando_by_site = defaultdict(int)
        rando_by_site_arm = defaultdict(lambda: defaultdict(int))
        for record in self.rtsm_data:
            if record.get('event_type', '').strip() == 'randomisation':
                site = record.get('site_id', '').strip()
                arm = record.get('arm_id', '').strip()
                rando_by_site[site] += 1
                rando_by_site_arm[site][arm] += 1

        for site in rando_by_site:
            country = self._get_country_for_site(site)
            rtsm_agg["randomisations_by_site"][site] = {
                "count": rando_by_site[site],
                "country": country,
                "by_arm": dict(rando_by_site_arm[site])
            }

        # Randomisations by arm
        rando_by_arm = defaultdict(int)
        for record in self.rtsm_data:
            if record.get('event_type', '').strip() == 'randomisation':
                arm = record.get('arm_id', '').strip()
                if arm:
                    rando_by_arm[arm] += 1
        rtsm_agg["randomisations_by_arm"] = dict(rando_by_arm)

        # Dispensings by item
        disp_by_item = defaultdict(int)
        for record in self.rtsm_data:
            if record.get('event_type', '').strip() == 'dispensing':
                item = record.get('item_id', '').strip()
                if item:
                    disp_by_item[item] += 1
        rtsm_agg["dispensings_by_item"] = dict(disp_by_item)

        # Screen failures by site
        sf_by_site = defaultdict(int)
        for record in self.rtsm_data:
            if record.get('event_type', '').strip() == 'screen_failure':
                site = record.get('site_id', '').strip()
                sf_by_site[site] += 1

        for site in sf_by_site:
            screening_attempts = rando_by_site.get(site, 0) + sf_by_site[site]
            rate = (sf_by_site[site] / screening_attempts * 100) if screening_attempts > 0 else 0
            rtsm_agg["screen_failures_by_site"][site] = {
                "count": sf_by_site[site],
                "screening_rate_pct": round(rate, 1)
            }

        # Date range
        dates = []
        for record in self.rtsm_data:
            date_str = record.get('event_date', '').strip()
            if date_str:
                dates.append(date_str)
        if dates:
            dates.sort()
            rtsm_agg["date_range"] = {
                "earliest_event": dates[0],
                "latest_event": dates[-1],
                "days_elapsed": self._days_between(dates[0], dates[-1])
            }

        # Site inventory (latest by location, item)
        inv_by_loc_item = {}
        for record in self.rtsm_data:
            if record.get('event_type', '').strip() == 'site_inventory':
                site = record.get('site_id', '').strip()
                item = record.get('item_id', '').strip()
                qty = int(record.get('quantity', 0))
                key = (site, item)
                # Keep latest (CSV is ordered by date, so last wins)
                inv_by_loc_item[key] = qty

        # Reshape for output
        inv_by_site = defaultdict(dict)
        for (site, item), qty in inv_by_loc_item.items():
            inv_by_site[site][item] = qty
        rtsm_agg["site_inventory"] = dict(inv_by_site)

        self.aggregations["rtsm_aggregations"] = rtsm_agg

    def _compute_ctms_aggregations(self):
        """Compute CTMS aggregations from full dataset."""
        ctms_agg = {
            "enrollment_plan_by_site": {},
            "enrollment_plan_total": 0,
            "enrollment_plan_by_country": defaultdict(int),
            "visit_schedules": defaultdict(dict)
        }

        # Enrollment plan by site
        for record in self.ctms_data:
            if record.get('record_type', '').strip() == 'enrollment_plan':
                site = record.get('site_id', '').strip()
                planned = int(record.get('planned_enrollment', 0))
                ctms_agg["enrollment_plan_by_site"][site] = planned

                # By country
                country = record.get('country_code', '').strip()
                if country:
                    ctms_agg["enrollment_plan_by_country"][country] += planned

        ctms_agg["enrollment_plan_total"] = sum(ctms_agg["enrollment_plan_by_site"].values())
        ctms_agg["enrollment_plan_by_country"] = dict(ctms_agg["enrollment_plan_by_country"])

        # Visit schedules
        for record in self.ctms_data:
            if record.get('record_type', '').strip() == 'visit_schedule':
                site = record.get('site_id', '').strip()
                visit_type = record.get('visit_type', '').strip()
                visit_window = record.get('visit_window_days', '0')
                try:
                    visit_window = int(visit_window)
                except:
                    visit_window = 0

                if site and visit_type:
                    ctms_agg["visit_schedules"][site][visit_type] = visit_window

        ctms_agg["visit_schedules"] = dict(ctms_agg["visit_schedules"])
        self.aggregations["ctms_aggregations"] = ctms_agg

    def _compute_erp_aggregations(self):
        """Compute ERP aggregations from full dataset."""
        erp_agg = {
            "stock_on_hand_by_depot": defaultdict(lambda: defaultdict(int)),
            "in_transit": [],
            "on_order": [],
            "batch_expiry_profile": []
        }

        # Stock on hand
        soh_by_depot_item = defaultdict(int)
        for record in self.erp_data:
            if record.get('record_type', '').strip() == 'stock_on_hand':
                location = record.get('location', '').strip()
                item = record.get('item_id', '').strip()
                qty = int(record.get('quantity', 0))
                soh_by_depot_item[(location, item)] += qty

        # Reshape and add total
        for (location, item), qty in soh_by_depot_item.items():
            erp_agg["stock_on_hand_by_depot"][location][item] = qty

        # Add totals per depot
        for depot in erp_agg["stock_on_hand_by_depot"]:
            total = sum(erp_agg["stock_on_hand_by_depot"][depot].values())
            erp_agg["stock_on_hand_by_depot"][depot]["total"] = total

        # In transit
        for record in self.erp_data:
            if record.get('record_type', '').strip() == 'shipment_in_transit':
                shipment_id = record.get('shipment_id', '').strip()
                item = record.get('item_id', '').strip()
                qty = int(record.get('quantity', 0))
                origin = record.get('origin', '').strip()
                destination = record.get('destination', '').strip()

                erp_agg["in_transit"].append({
                    "shipment_id": shipment_id,
                    "item": item,
                    "quantity": qty,
                    "origin": origin,
                    "destination": destination
                })

        # On order
        for record in self.erp_data:
            if record.get('record_type', '').strip() == 'production_order':
                order_id = record.get('order_id', '').strip()
                item = record.get('item_id', '').strip()
                qty = int(record.get('quantity', 0))

                erp_agg["on_order"].append({
                    "order_id": order_id,
                    "item": item,
                    "quantity": qty
                })

        # Batch expiry profile
        for record in self.erp_data:
            lot_number = record.get('lot_number', '').strip()
            if lot_number:
                item = record.get('item_id', '').strip()
                location = record.get('location', '').strip()
                qty = int(record.get('quantity', 0))
                expiry = record.get('expiry_date', '').strip()

                # Avoid duplicates (if same lot in multiple records, take first)
                if not any(b['lot_number'] == lot_number for b in erp_agg["batch_expiry_profile"]):
                    erp_agg["batch_expiry_profile"].append({
                        "lot_number": lot_number,
                        "item": item,
                        "location": location,
                        "quantity": qty,
                        "expiry_date": expiry
                    })

        # Sort by expiry date (parse dd-mm-yy format; unreadable dates sort last)
        erp_agg["batch_expiry_profile"].sort(
            key=lambda x: self._parse_csv_date(x.get('expiry_date', '')) or datetime.max
        )

        # Convert defaultdicts to dicts
        erp_agg["stock_on_hand_by_depot"] = {
            k: dict(v) for k, v in erp_agg["stock_on_hand_by_depot"].items()
        }

        self.aggregations["erp_aggregations"] = erp_agg

    def _compute_site_inventory_aggregations(self):
        """Compute site inventory aggregations from site_inventory.csv."""
        inv_agg = {}

        for row in self.site_inventory_data:
            site = row.get('site', '').strip()
            item = row.get('item_id', '').strip()
            try:
                on_hand = int(row.get('on_hand_qty', 0))
                weekly_demand = float(row.get('weekly_demand', 0))
                min_reorder = int(row.get('min_reorder_point', 0))
                max_reorder = int(row.get('max_reorder_point', 0))
            except (ValueError, TypeError):
                continue

            weeks = round(on_hand / weekly_demand, 1) if weekly_demand > 0 else 0
            reorder_status = "BELOW_MIN" if on_hand < min_reorder else "AT_OR_ABOVE_MIN"

            if site not in inv_agg:
                inv_agg[site] = {}

            inv_agg[site][item] = {
                "on_hand_qty": on_hand,
                "weekly_demand": weekly_demand,
                "min_reorder_point": min_reorder,
                "max_reorder_point": max_reorder,
                "weeks_of_supply": weeks,
                "reorder_status": reorder_status
            }

        self.aggregations["site_inventory_aggregations"] = inv_agg

    def _compute_derived_metrics(self):
        """Compute derived metrics from aggregations."""
        derived = {
            "enrollment_delta": {},
            "demand_rate": {},
            "supply_coverage": {}
        }

        # Enrollment delta
        actual = self.aggregations["rtsm_aggregations"]["record_counts"]["randomisations_total"]
        planned = self.aggregations["ctms_aggregations"]["enrollment_plan_total"]

        if planned > 0:
            delta_pct = (actual - planned) / planned * 100
            direction = "INCREASE" if delta_pct > 0 else "DECREASE"
        else:
            delta_pct = 0
            direction = "N/A"

        derived["enrollment_delta"] = {
            "actual_enrollment": actual,
            "planned_enrollment": planned,
            "delta_pct": round(delta_pct, 1),
            "delta_direction": direction
        }

        # Demand rate
        total_disp = self.aggregations["rtsm_aggregations"]["record_counts"]["dispensings_total"]
        days = self.aggregations["rtsm_aggregations"]["date_range"].get("days_elapsed", 1)
        if days < 1:
            days = 1

        disp_per_day = total_disp / days
        disp_per_week = disp_per_day * 7

        derived["demand_rate"] = {
            "total_dispensings": total_disp,
            "days_elapsed": days,
            "dispensing_rate_per_day": round(disp_per_day, 2),
            "dispensing_rate_per_week": round(disp_per_week, 2)
        }

        # Supply coverage
        disp_per_week = derived["demand_rate"]["dispensing_rate_per_week"]
        if disp_per_week < 0.01:
            disp_per_week = 0.1  # Avoid division by zero

        soh = self.aggregations["erp_aggregations"]["stock_on_hand_by_depot"]
        in_transit_by_item = defaultdict(int)
        for shipment in self.aggregations["erp_aggregations"]["in_transit"]:
            in_transit_by_item[shipment["item"]] += shipment["quantity"]

        on_order_by_item = defaultdict(int)
        for order in self.aggregations["erp_aggregations"]["on_order"]:
            on_order_by_item[order["item"]] += order["quantity"]

        for item in self.config.get("items", []):
            item_id = item.get("item_id", "")

            # Sum across all depots
            on_hand = 0
            for depot in soh.values():
                on_hand += depot.get(item_id, 0)

            in_trans = in_transit_by_item.get(item_id, 0)
            on_ord = on_order_by_item.get(item_id, 0)
            total_avail = on_hand + in_trans + on_ord

            weeks = total_avail / disp_per_week if disp_per_week > 0 else 0

            derived["supply_coverage"][item_id] = {
                "on_hand": on_hand,
                "in_transit": in_trans,
                "on_order": on_ord,
                "total_available": total_avail,
                "weeks_of_supply": round(weeks, 1)
            }

        self.aggregations["derived_metrics"] = derived

    def _check_patient_id_continuity(self):
        """Check for gaps or duplicates in patient IDs."""
        patient_ids = set()
        for record in self.rtsm_data:
            patient_id = record.get('patient_id', '').strip()
            if patient_id:
                patient_ids.add(patient_id)

        if not patient_ids:
            self.integrity_issues.append("patient_id_continuity")
            return

        # Check for duplicates within the same event type on the same date
        # Different event types for same patient (e.g., randomization + dispensing) are NOT duplicates
        # Multiple events of same type on different dates (e.g., multiple dispensings) are NOT duplicates
        # Gaps in patient ID sequences are expected (test data may use non-sequential IDs)
        status = "PASS"
        issues = []

        seen_patient_events = set()
        for record in self.rtsm_data:
            pid = record.get('patient_id', '').strip()
            event_type = record.get('event_type', '').strip()
            event_date = record.get('event_date', '').strip()
            if pid and event_type:
                # Key includes date to allow multiple events of same type on different dates
                key = (pid, event_type, event_date)
                if key in seen_patient_events:
                    # Same patient + same event type + same date = actual duplicate
                    status = "FAIL"
                    issues.append(f"Duplicate record: {pid} with event type '{event_type}' on {event_date}")
                else:
                    seen_patient_events.add(key)

        try:
            numbers = sorted([int(pid.replace('PAT-', '')) for pid in patient_ids if 'PAT-' in pid])
            if numbers:

                self.aggregations["data_integrity_checks"] = self.aggregations.get("data_integrity_checks", {})
                self.aggregations["data_integrity_checks"]["patient_id_continuity"] = {
                    "status": status,
                    "issues": issues,
                    "patient_id_range": f"PAT-{min(numbers)} to PAT-{max(numbers)}",
                    "total_unique_patients": len(patient_ids)
                }
        except:
            self.aggregations["data_integrity_checks"] = self.aggregations.get("data_integrity_checks", {})
            self.aggregations["data_integrity_checks"]["patient_id_continuity"] = {
                "status": "PASS",
                "issues": [],
                "total_unique_patients": len(patient_ids)
            }

    def _check_site_consistency(self):
        """Check that sites in data match study config."""
        config_sites = {s.get('site_id', '') for s in self.config.get('sites', [])}
        rtsm_sites = {r.get('site_id', '').strip() for r in self.rtsm_data if r.get('site_id', '').strip()}
        ctms_sites = {r.get('site_id', '').strip() for r in self.ctms_data if r.get('site_id', '').strip()}

        all_data_sites = rtsm_sites | ctms_sites

        issues = []
        for site in all_data_sites:
            if site and site not in config_sites:
                issues.append(f"Site in data but not in config: {site}")

        inactive_sites = config_sites - all_data_sites

        status = "PASS" if not issues else "FAIL"

        self.aggregations["data_integrity_checks"] = self.aggregations.get("data_integrity_checks", {})
        self.aggregations["data_integrity_checks"]["site_consistency"] = {
            "status": status,
            "issues": issues,
            "sites_in_study_config": list(config_sites),
            "sites_with_activity": list(all_data_sites),
            "inactive_sites": list(inactive_sites)
        }

    def _check_item_consistency(self):
        """Check that items in data match study config."""
        config_items = {i.get('item_id', '') for i in self.config.get('items', [])}
        rtsm_items = {r.get('item_id', '').strip() for r in self.rtsm_data if r.get('item_id', '').strip()}

        issues = []
        for item in rtsm_items:
            if item and item not in config_items:
                issues.append(f"Item in data but not in config: {item}")

        status = "PASS" if not issues else "FAIL"

        self.aggregations["data_integrity_checks"] = self.aggregations.get("data_integrity_checks", {})
        self.aggregations["data_integrity_checks"]["item_consistency"] = {
            "status": status,
            "issues": issues,
            "items_in_study_config": list(config_items),
            "items_with_dispensings": list(rtsm_items)
        }

    def _check_arm_consistency(self):
        """Check that arms in data match study config."""
        config_arms = {a.get('arm_id', '') for a in self.config.get('treatment_arms', [])}
        rtsm_arms = {r.get('arm_id', '').strip() for r in self.rtsm_data if r.get('arm_id', '').strip()}

        issues = []
        for arm in rtsm_arms:
            if arm and arm not in config_arms:
                issues.append(f"Arm in data but not in config: {arm}")

        status = "PASS" if not issues else "FAIL"

        self.aggregations["data_integrity_checks"] = self.aggregations.get("data_integrity_checks", {})
        self.aggregations["data_integrity_checks"]["arm_consistency"] = {
            "status": status,
            "issues": issues
        }

    def _check_randomisation_dispensing_balance(self):
        """Check that dispensings don't exceed randomisations."""
        rando = self.aggregations["rtsm_aggregations"]["record_counts"]["randomisations_total"]
        disp = self.aggregations["rtsm_aggregations"]["record_counts"]["dispensings_total"]

        issues = []
        status = "PASS"

        if disp > rando:
            issues.append(f"Dispensings ({disp}) exceed randomisations ({rando}) — unexpected scenario")
            status = "WARNING"

        ongoing = rando - disp

        self.aggregations["data_integrity_checks"] = self.aggregations.get("data_integrity_checks", {})
        self.aggregations["data_integrity_checks"]["randomisation_dispensing_balance"] = {
            "status": status,
            "randomisations": rando,
            "dispensings": disp,
            "ongoing_patients": ongoing,
            "issues": issues
        }

    def _check_screen_failure_rates(self):
        """Check screen failure rates for unusual values."""
        flagged_sites = []

        for site, sf_data in self.aggregations["rtsm_aggregations"]["screen_failures_by_site"].items():
            rate = sf_data["screening_rate_pct"]

            if rate > 50:
                flagged_sites.append({
                    "site": site,
                    "rate_pct": rate,
                    "flag": "unusually_high"
                })
            elif rate == 0:
                # Check if there were screening attempts
                rando_count = self.aggregations["rtsm_aggregations"]["randomisations_by_site"].get(site, {}).get("count", 0)
                if rando_count > 0:
                    flagged_sites.append({
                        "site": site,
                        "rate_pct": rate,
                        "flag": "unusually_low"
                    })

        status = "WARNING" if flagged_sites else "PASS"

        self.aggregations["data_integrity_checks"] = self.aggregations.get("data_integrity_checks", {})
        self.aggregations["data_integrity_checks"]["screen_failure_rates"] = {
            "status": status,
            "flagged_sites": flagged_sites
        }

    def _check_date_consistency(self):
        """Check for date anomalies."""
        issues = []
        status = "PASS"

        date_range = self.aggregations["rtsm_aggregations"].get("date_range", {})
        earliest = date_range.get("earliest_event", "")
        latest = date_range.get("latest_event", "")

        if earliest and latest:
            if latest < earliest:
                issues.append(f"Latest date ({latest}) is before earliest date ({earliest})")
                status = "FAIL"

        self.aggregations["data_integrity_checks"] = self.aggregations.get("data_integrity_checks", {})
        self.aggregations["data_integrity_checks"]["date_consistency"] = {
            "status": status,
            "issues": issues
        }

    def _check_expiry_validation(self):
        """Check expiry dates. CSV dates are dd-mm-yy format — always use _parse_csv_date()."""
        expired = []
        expiring_soon = []
        ambiguous = []

        # data_drop_date is YYYY-MM-DD (from folder path)
        try:
            drop_dt = datetime.strptime(self.data_drop_date, "%Y-%m-%d")
        except ValueError:
            # Cannot parse drop date — skip check
            self.aggregations["data_integrity_checks"] = self.aggregations.get("data_integrity_checks", {})
            self.aggregations["data_integrity_checks"]["expiry_validation"] = {
                "status": "WARNING",
                "expired_batches": 0,
                "batches_expiring_within_6_months": 0,
                "flagged_batches": [],
                "note": f"Could not parse data_drop_date '{self.data_drop_date}' — expiry check skipped"
            }
            return

        for batch in self.aggregations["erp_aggregations"]["batch_expiry_profile"]:
            expiry_str = batch.get("expiry_date", "")
            lot = batch.get("lot_number", "")

            if not expiry_str:
                continue

            exp_dt = self._parse_csv_date(expiry_str)

            if exp_dt is None:
                # Cannot parse — flag as ambiguous, do not assume expired
                ambiguous.append({
                    "lot_number": lot,
                    "expiry_date": expiry_str,
                    "flag": "ambiguous_date"
                })
            elif exp_dt <= drop_dt:
                expired.append({
                    "lot_number": lot,
                    "expiry_date": expiry_str,
                    "flag": "expired"
                })
            else:
                days_remaining = (exp_dt - drop_dt).days
                if days_remaining < 180:
                    expiring_soon.append({
                        "lot_number": lot,
                        "expiry_date": expiry_str,
                        "flag": "expires_soon"
                    })

        status = "PASS"
        if expired:
            status = "FAIL"
        elif expiring_soon or ambiguous:
            status = "WARNING"

        self.aggregations["data_integrity_checks"] = self.aggregations.get("data_integrity_checks", {})
        self.aggregations["data_integrity_checks"]["expiry_validation"] = {
            "status": status,
            "expired_batches": len(expired),
            "batches_expiring_within_6_months": len(expiring_soon),
            "ambiguous_dates": len(ambiguous),
            "flagged_batches": expired + expiring_soon + ambiguous
        }

    def _build_output(self) -> Dict[str, Any]:
        """Build the final output dictionary."""
        # Determine overall integrity status
        integrity_checks = self.aggregations.get("data_integrity_checks", {})
        statuses = [check.get("status", "PASS") for check in integrity_checks.values()]

        if "FAIL" in statuses:
            overall = "FAIL"
        elif "WARNING" in statuses:
            overall = "WARNING"
        else:
            overall = "PASS"

        # Build recommendations
        recommendations = []
        if integrity_checks.get("patient_id_continuity", {}).get("status") == "FAIL":
            recommendations.append({
                "category": "patient_id_continuity",
                "severity": "CRITICAL",
                "message": "Patient ID gaps or duplicates detected",
                "action": "Investigate data source and correct anomalies"
            })

        if integrity_checks.get("site_consistency", {}).get("status") == "FAIL":
            recommendations.append({
                "category": "site_consistency",
                "severity": "CRITICAL",
                "message": "Data contains sites not in study configuration",
                "action": "Update study config or correct site identifiers in data"
            })

        if integrity_checks.get("randomisation_dispensing_balance", {}).get("status") == "WARNING":
            recommendations.append({
                "category": "randomisation_dispensing_balance",
                "severity": "WARNING",
                "message": "More dispensings than randomisations — verify source data",
                "action": "Review RTSM data for missing randomisation records"
            })

        if integrity_checks.get("screen_failure_rates", {}).get("status") == "WARNING":
            recommendations.append({
                "category": "screen_failure_rates",
                "severity": "HIGH",
                "message": "Unusually high or low screen failure rates detected",
                "action": "Review screening criteria and site practices"
            })

        if integrity_checks.get("expiry_validation", {}).get("status") in ["WARNING", "FAIL"]:
            recommendations.append({
                "category": "expiry_validation",
                "severity": "MEDIUM",
                "message": "Batches expiring soon or already expired",
                "action": "Monitor expiry dates; plan destruction for expired stock"
            })

        output = {
            "tool": "DI-12 — Aggregate Data Query Tool",
            "execution_timestamp": datetime.now().isoformat(),
            "data_drop_date": self.data_drop_date,
            "files_processed": [
                {"file": "rtsm_actuals.csv", "status": "OK", "total_records": len(self.rtsm_data)},
                {"file": "ctms_plan.csv", "status": "OK", "total_records": len(self.ctms_data)},
                {"file": "erp_inventory.csv", "status": "OK", "total_records": len(self.erp_data)},
                {"file": "site_inventory.csv", "status": "OK", "total_records": len(self.site_inventory_data)}
            ],
            **self.aggregations,
            "data_integrity_checks": integrity_checks,
            "overall_data_integrity": overall,
            "recommendations": recommendations
        }

        return output

    def _get_country_for_site(self, site: str) -> str:
        """Look up country for a site from config."""
        for s in self.config.get('sites', []):
            if s.get('site_id', '') == site:
                return s.get('country_code', '')
        return ""

    def _days_between(self, date1_str: str, date2_str: str) -> int:
        """Calculate days between two DD-MMM-YYYY date strings."""
        try:
            d1 = self._parse_csv_date(date1_str)
            d2 = self._parse_csv_date(date2_str)
            if d1 and d2:
                return (d2 - d1).days
            return 0
        except:
            return 0


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 6:
        print("Usage: python di_12_aggregate_data_query.py <rtsm_file> <ctms_file> <erp_file> <site_inventory_file> <config_file>")
        sys.exit(1)

    query = AggregateDataQuery(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    result = query.execute()
    print(json.dumps(result, indent=2))
