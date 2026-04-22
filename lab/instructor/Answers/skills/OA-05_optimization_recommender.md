# OA-05 — Optimization Recommender

<!-- ============================================================
     REFERENCE ANSWER — For instructor/student review after the lab.
     This is one possible implementation. Student versions will vary.
     ============================================================ -->

## Purpose

<!-- PURPOSE: This is the synthesis skill — it reads outputs from OA-01 to OA-04
     and turns them into concrete, evidence-backed actions.
     The critical design principle: always cite the specific evidence.
     Students commonly write vague recommendations — this skill's rules prevent that. -->

This skill synthesises all findings from OA-01 through OA-04 into 1–3 concrete, actionable recommendations. It does not generate new analysis — it reads what the other skills found and decides what to do about it. Every recommendation must cite the specific finding that supports it. Vague recommendations are not acceptable.

---

## Owner

<!-- OWNER: Which agent uses this skill? Must match an agent folder name. -->

**Primary:** Optimization Agent

---

## When This Skill Is Used

<!-- WHEN: Always the LAST skill to run — it depends on all four evidence skills.
     Students commonly run this too early. Make the dependency explicit.
     If no findings exist from OA-01 through OA-04, this skill still runs — it just emits NO_ACTION. -->

- During WF-OA-01, as the **final** step — always after OA-01, OA-02, OA-03, and OA-04 have all run.
- If no findings were returned by any of the four evidence skills, this skill emits NO_ACTION.
- If findings exist, it always produces at least one recommendation.

---

## Inputs

<!-- INPUTS: The outputs of the four preceding skills — not raw data files.
     This teaches the important pattern: skills chain together, not just data files.
     OA-05 never reads erp_inventory.csv or site_inventory.csv directly. -->

1. OA-01 output — excess inventory findings (list, may be empty)
2. OA-02 output — expiry risk findings (ranked list, may be empty)
3. OA-03 output — idle inventory findings (ranked list, may be empty)
4. OA-04 output — flow inefficiency findings (list, may be empty)

---

## Steps

<!-- STEPS: Prioritisation logic is key here.
     CRITICAL_WASTE_RISK triggers when both OA-02 has critical lots AND OA-01 has excess.
     The combination of excess stock + imminent expiry is the worst-case scenario.
     Step 3's "one sentence" rule enforces precision — students will want to write paragraphs. -->

1. Review all findings from OA-01 through OA-04. If all four lists are empty, output NO_ACTION and stop.

2. **Prioritise by urgency:**
   - CRITICAL (act now): OA-02 lots with < 4 weeks to expiry + high waste units
   - HIGH (act this week): OA-01 depots with > 150% of policy max, or OA-04 emergency patterns
   - MEDIUM (plan soon): OA-03 idle sites, OA-02 HIGH risk lots, OA-04 repeat resupply
   - LOW (monitor): OA-02 MODERATE risk lots, minor shipping delays

3. **Draft 1–3 recommendations**, in priority order. Each recommendation must:
   - Name the specific depot, site, or lot involved (never generic)
   - State the specific evidence (cite the OA-0X finding)
   - State the specific action (rebalance, slow production, prioritise usage, review trigger)
   - Be expressed in one sentence

4. **Determine routing signal:**
   - Emit `CRITICAL_WASTE_RISK` if: any OA-02 lot is CRITICAL risk AND OA-01 also shows excess at same location
   - Emit `OPTIMIZATION_OPPORTUNITY` if: any findings exist (not all empty)
   - Emit `NO_ACTION` if: all four evidence lists are empty

5. Package recommendations and signal into the agent's output format. Return to the Optimization Agent.

---

## Output

<!-- OUTPUT: The recommendations + the routing signal.
     Both are required — the signal tells the workflow runner what to do next.
     The evidence source field is what distinguishes a quality recommendation from a vague one. -->

- Routing signal: `OPTIMIZATION_OPPORTUNITY`, `NO_ACTION`, or `CRITICAL_WASTE_RISK`
- Recommendations list (1–3 items), each containing:
  - Priority (CRITICAL / HIGH / MEDIUM / LOW)
  - Evidence source (which OA-0X skill flagged this)
  - Specific finding (depot/site/lot name + numbers)
  - Recommended action (one sentence)

---

## Notes

<!-- NOTES: The "cite specific evidence" rule is the most important quality gate.
     Students will tend to write vague recommendations — this note prevents that.
     The 3-recommendation cap forces triage — not every finding needs an action. -->

- **Always cite specific evidence.** A recommendation that says "review inventory levels" without naming a depot and a number is not acceptable output from this skill.
- Maximum 3 recommendations. If more than 3 findings exist, prioritise by urgency and focus on the highest impact actions.
- This skill does not forecast. It does not predict future demand. It only acts on what the evidence skills found in the current data.
