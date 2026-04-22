# OA-01 — Excess Inventory Detector

<!-- ============================================================
     REFERENCE ANSWER — For instructor/student review after the lab.
     This is one possible implementation. Student versions will vary.
     ============================================================ -->

## Purpose

<!-- PURPOSE: What this skill does in 2-3 sentences.
     Answer "this skill exists to..."
     Keep it grounded in the clinical supply chain context. -->

This skill compares current depot stock levels against the maximum stock weeks policy defined in `policies.json`. It flags any depot where holdings exceed the policy maximum, quantifying the excess in weeks of supply and units. It is the first evidence-gathering step in identifying supply waste.

---

## Owner

<!-- OWNER: Which agent uses this skill? Must match an agent folder name. -->

**Primary:** Optimization Agent

---

## When This Skill Is Used

<!-- WHEN: In which workflow and at what point is this skill called?
     Be specific — this helps the agent know when to apply it. -->

- During WF-OA-01 (Optimization Analysis), as the first analytical step.
- Called immediately after data is loaded, before any other OA- skills run.
- Triggered every time the Optimization Agent is invoked.

---

## Inputs

<!-- INPUTS: List every data source this skill reads.
     Include the file name, where it lives, and what field is needed.
     Students often forget policies.json — make it explicit. -->

1. `erp_inventory.csv` (from current data drop) — stock on hand by depot, item, and batch
2. `policies.json` (from study config) — `max_stock_weeks` threshold per item
3. Consumption rate (from OA-03 or DF-01 if available) — used to calculate weeks of supply

---

## Steps

<!-- STEPS: The numbered procedure the agent follows.
     Write each step as a clear, single action.
     Aim for 5-6 steps. Include what to do if data is missing. -->

1. Load `erp_inventory.csv` and extract total stock on hand per depot per item (sum across all batches).

2. Load `policies.json` and extract the `max_stock_weeks` value for each item. If not item-specific, use the study-level default.

3. Calculate **weeks of supply** for each depot-item combination:
   `weeks_of_supply = stock_on_hand ÷ weekly_consumption_rate`

4. Compare each depot-item weeks of supply to the `max_stock_weeks` policy threshold.

5. Flag any depot-item where `weeks_of_supply > max_stock_weeks` as **EXCESS**.
   Calculate: `excess_weeks = weeks_of_supply - max_stock_weeks`
   Calculate: `excess_units = excess_weeks × weekly_consumption_rate`

6. Return a list of excess inventory findings. If no depot exceeds the threshold, return an empty list (no excess found).

---

## Output

<!-- OUTPUT: What this skill returns to the agent.
     Be specific — name the fields so the agent can reference them.
     OA-05 (Optimization Recommender) will read these fields. -->

- List of excess inventory findings, each containing:
  - Depot name
  - Item name
  - Current weeks of supply (calculated)
  - Policy max stock weeks (from config)
  - Excess weeks (difference)
  - Excess units (quantified)
- Summary count: number of depots flagged

---

## Notes

<!-- NOTES: Important caveats. What this skill does NOT do.
     This helps students understand skill boundaries. -->

- This skill detects excess at the **depot level**. Site-level idle stock is handled by OA-03.
- It does not recommend what to do with the excess — that is OA-05's job.
- If weekly consumption rate is not available, flag the depot as "unable to calculate" rather than skipping it.
