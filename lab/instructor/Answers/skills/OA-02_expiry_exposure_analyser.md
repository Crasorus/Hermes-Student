# OA-02 — Expiry Exposure Analyser

<!-- ============================================================
     REFERENCE ANSWER — For instructor/student review after the lab.
     This is one possible implementation. Student versions will vary.
     ============================================================ -->

## Purpose

<!-- PURPOSE: What this skill does in 2-3 sentences.
     Focus on the clinical supply risk: wasted medicine = protocol risk + cost. -->

This skill identifies investigational product lots that are at risk of expiring before they can be consumed. It compares each lot's remaining shelf life against the current consumption rate at the holding location, flagging lots where expiry is imminent relative to usage pace. Expiry waste is one of the most common and costly inefficiencies in clinical supply chains.

---

## Owner

<!-- OWNER: Which agent uses this skill? Must match an agent folder name. -->

**Primary:** Optimization Agent

---

## When This Skill Is Used

<!-- WHEN: Where in the workflow sequence does this run?
     Runs second — after OA-01 has already identified excess depots, which are the highest expiry risk. -->

- During WF-OA-01 (Optimization Analysis), as the second analytical step.
- Runs after OA-01 (Excess Inventory Detector) — excess depots are the highest expiry risk.
- Always runs regardless of OA-01 results (expiry risk can exist even within policy limits).

---

## Inputs

<!-- INPUTS: Every data source needed.
     erp_inventory.csv contains batch expiry dates — students often miss this field. -->

1. `erp_inventory.csv` — batch-level data including: lot number, expiry date, quantity on hand, holding location
2. Current date (system date) — to calculate days remaining to expiry
3. Consumption rate per location (from OA-01 or DF-01) — to estimate time to deplete the lot
4. `policies.json` — `shelf_life_requirement_weeks` threshold (minimum acceptable shelf life at time of use)

---

## Steps

<!-- STEPS: Numbered procedure the agent follows.
     Step 3 is the critical calculation — the weeks-to-depletion formula.
     Step 4 defines the two independent flag conditions — both must be checked. -->

1. Load `erp_inventory.csv` and extract all batch records with their expiry dates, quantities, and holding locations.

2. For each batch, calculate **days remaining to expiry**:
   `days_remaining = expiry_date - today`

3. For each batch at each location, calculate **weeks to depletion** at current consumption rate:
   `weeks_to_depletion = quantity_on_hand ÷ weekly_consumption_rate`

4. Flag a batch as **EXPIRY RISK** if either condition is true:
   - `days_remaining < (weeks_to_depletion × 7)` — lot will expire before it is consumed
   - `days_remaining < (shelf_life_requirement_weeks × 7)` — lot is approaching minimum shelf life threshold

5. For each flagged lot, calculate **projected waste units**:
   `waste_units = quantity_on_hand - (consumption_rate × days_remaining ÷ 7)`

6. Rank flagged lots by days remaining (most urgent first). Return ranked list.

---

## Output

<!-- OUTPUT: Fields returned to the agent.
     OA-05 needs lot number, location, and urgency to make a recommendation.
     Risk level bands are fixed thresholds — students should not change them without a policy basis. -->

- Ranked list of expiry risk findings, each containing:
  - Lot number
  - Item name
  - Holding location (depot or site)
  - Expiry date
  - Days remaining to expiry
  - Quantity on hand
  - Projected waste units (if not consumed in time)
  - Risk level: CRITICAL (< 4 weeks), HIGH (4–8 weeks), MODERATE (8–12 weeks)
- Summary count: number of lots flagged by risk level

---

## Notes

<!-- NOTES: Boundaries and caveats.
     Expiry is lot-level; OA-01 is depot-level. These are complementary, not overlapping.
     A depot with healthy overall stock can still contain individual lots nearing expiry. -->

- This skill operates at the **lot/batch level**. A depot can have healthy overall stock (OA-01 passes) but still have specific lots at expiry risk.
- Does not decide which lot to prioritise for consumption — that is OA-05's job.
- If expiry date is missing from the data, flag the batch as "expiry date not available" and exclude from ranking.
