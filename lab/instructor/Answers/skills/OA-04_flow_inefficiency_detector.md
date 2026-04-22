# OA-04 — Flow Inefficiency Detector

<!-- ============================================================
     REFERENCE ANSWER — For instructor/student review after the lab.
     This is one possible implementation. Student versions will vary.
     ============================================================ -->

## Purpose

<!-- PURPOSE: This skill is different — it looks at patterns over time, not point-in-time stock.
     Emergency shipments and repeat resupply are symptoms of a broken replenishment process.
     Contrast with OA-01/OA-02/OA-03, which are all snapshot-based. -->

This skill detects inefficiencies in the supply flow — patterns that indicate the supply chain is reacting to problems rather than running smoothly. It looks for emergency shipments, repeated unplanned resupply events, and significant shipping delays. These patterns are evidence of upstream planning failures, not just inventory problems.

---

## Owner

<!-- OWNER: Which agent uses this skill? Must match an agent folder name. -->

**Primary:** Optimization Agent

---

## When This Skill Is Used

<!-- WHEN: This is a pattern-detection skill — it needs shipment history, not just a current snapshot.
     The 30-day review window is the default; study config can override it. -->

- During WF-OA-01 (Optimization Analysis), as the fourth analytical step.
- Reads shipment history from `erp_inventory.csv` (shipment records section).
- Runs after OA-01/OA-02/OA-03 to provide a complementary "flow" perspective alongside the "stock" perspective.

---

## Inputs

<!-- INPUTS: erp_inventory.csv contains shipment records — students need to know which columns to look for.
     supply_network.json holds standard lane lead times — the baseline for delay detection. -->

1. `erp_inventory.csv` — shipment records including: shipment type (planned/emergency), origin, destination, dispatch date, arrival date, quantity
2. Current date — to calculate shipping delays
3. `config/supply_network.json` — standard lead times per lane (to identify delays)
4. Review window: last 30 days of shipment history (configurable)

---

## Steps

<!-- STEPS: Three distinct pattern checks — emergency shipments, repeat resupply, and delays.
     Each check is independent; all three must always run.
     The 20% delay threshold and 2-event emergency pattern threshold are policy defaults. -->

1. Load shipment records from `erp_inventory.csv`. Filter to shipments dispatched within the last 30 days.

2. **Check 1 — Emergency Shipments:**
   Flag any shipment marked as type `emergency` or `unplanned`.
   Count emergency shipments per lane over the review window.
   Flag lanes with 2 or more emergency shipments in 30 days as PATTERN (not isolated incident).

3. **Check 2 — Repeated Resupply:**
   Identify any site or depot that received more than 2 shipments in 30 days for the same item.
   Flag as a repeated resupply pattern (indicates the replenishment trigger is too low or demand is volatile).

4. **Check 3 — Shipping Delays:**
   For each completed shipment, calculate actual lead time: `arrival_date - dispatch_date`.
   Compare to standard lead time from `supply_network.json` for that lane.
   Flag shipments where actual lead time exceeded standard lead time by more than 20%.

5. Aggregate findings: emergency count, repeat resupply count, delay count. Return all flagged events.

---

## Output

<!-- OUTPUT: Three categories of flow findings — keep them separate so OA-05 can triage them independently.
     A high emergency count is a different severity than a shipping delay. -->

- Emergency shipment findings: list of emergency shipments, grouped by lane, with count and dates
- Repeat resupply findings: list of sites/depots with repeated same-item shipments in the window
- Shipping delay findings: list of delayed shipments with actual vs. expected lead times
- Summary: total flow inefficiency events detected

---

## Notes

<!-- NOTES: This is pattern detection — a single emergency shipment is not a finding.
     The threshold (2 events in 30 days) is a default — study may configure differently.
     Delays need human review; the skill flags, it does not diagnose root cause. -->

- A **single** emergency shipment is not a pattern — only flag when it recurs.
- This skill reads historical patterns, not current stock levels. It complements OA-01/OA-02/OA-03, it does not overlap them.
- Shipping delays may have legitimate causes (customs, cold chain holds). Flag them but note they require human review.
