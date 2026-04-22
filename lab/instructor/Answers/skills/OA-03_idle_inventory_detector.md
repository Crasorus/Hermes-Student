# OA-03 — Idle Inventory Detector

<!-- ============================================================
     REFERENCE ANSWER — For instructor/student review after the lab.
     This is one possible implementation. Student versions will vary.
     ============================================================ -->

## Purpose

<!-- PURPOSE: Distinguish OA-03 from OA-01.
     OA-01 = depot vs. policy max (quantity threshold).
     OA-03 = site consumption velocity vs. stock held (consumption rate problem).
     These are different inefficiencies with different root causes. -->

This skill detects sites where investigational product is sitting unused despite being available. It compares site-level stock on hand against the site's current consumption rate, flagging sites where stock far exceeds what the site is actually using. Unlike OA-01 (which flags depots exceeding policy thresholds), this skill focuses on **site-level consumption velocity** — stock that is present but not moving.

---

## Owner

<!-- OWNER: Which agent uses this skill? Must match an agent folder name. -->

**Primary:** Optimization Agent

---

## When This Skill Is Used

<!-- WHEN: Site data comes from site_inventory.csv — a different file than OA-01/OA-02.
     This distinction matters: depot data and site data are separate sources. -->

- During WF-OA-01 (Optimization Analysis), as the third analytical step.
- Reads from `site_inventory.csv` — this is separate from the depot-level ERP data.
- Particularly relevant when enrollment is low at a site (stock delivered but not dispensed).

---

## Inputs

<!-- INPUTS: site_inventory.csv is the key source here — not erp_inventory.csv.
     Make this distinction explicit so students learn the two data sources.
     study_config.json provides enrollment context to distinguish expected vs. unexpected low consumption. -->

1. `site_inventory.csv` (from current data drop) — site-level: site name, item, on-hand quantity, weekly demand, reorder points
2. `erp_inventory.csv` — to cross-reference any recent shipments to these sites
3. `study_config.json` — enrollment plan by site (to contextualise low consumption)

---

## Steps

<!-- STEPS: The idle calculation is weeks_of_supply at the site level.
     High weeks_of_supply at a site with low enrollment = idle inventory.
     Step 4 adds the enrollment context check — do not skip this; it avoids false positives. -->

1. Load `site_inventory.csv` and extract on-hand quantity and weekly demand for each site-item combination.

2. Calculate **weeks of supply at each site**:
   `weeks_of_supply = on_hand_qty ÷ weekly_demand`

3. Flag a site-item as **IDLE** if either condition is true:
   - `weeks_of_supply > 12` — more than 3 months of stock at current consumption rate
   - `weekly_demand == 0` — site has stock but zero recorded consumption

4. Cross-reference flagged sites against enrollment data from `study_config.json`. Confirm whether low consumption is explained by low enrollment (expected) or is unexpected (a genuine inefficiency signal).

5. For flagged idle sites, check `erp_inventory.csv` for recent inbound shipments. If a shipment arrived in the last 4 weeks, note it as a contributing factor.

6. Return ranked list of idle inventory findings, sorted by weeks of supply (highest first).

---

## Output

<!-- OUTPUT: Distinguish from OA-01 output — this is site-level, not depot-level.
     The enrollment context field is what makes OA-03 output actionable vs. OA-01. -->

- Ranked list of idle inventory findings, each containing:
  - Site name
  - Item name
  - On-hand quantity
  - Weekly demand (current rate)
  - Weeks of supply (calculated)
  - Enrollment context (is low consumption explained by low enrollment?)
  - Recent shipment flag (was stock recently topped up despite low demand?)
- Summary count: number of site-item combinations flagged

---

## Notes

<!-- NOTES: Explain the OA-01 vs OA-03 boundary clearly for students.
     The two skills can fire independently — passing one does not mean passing the other. -->

- **OA-01 vs OA-03:** OA-01 compares depot stock to a policy maximum (quantity threshold). OA-03 compares site stock to actual consumption velocity (usage rate). A site can pass OA-03 while its depot fails OA-01, and vice versa.
- Sites with zero enrollment are expected to have zero consumption — flag but do not escalate if enrollment explains it.
- Does not recommend whether to recall or redistribute the stock — that is OA-05's job.
