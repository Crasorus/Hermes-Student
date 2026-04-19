# DI-07 — Policy Loader

## Purpose

Read and normalise the supply chain policies so that agents can apply the correct business rules when making decisions. This skill loads safety stock rules, reorder rules, budget constraints, and expiry/destruction rules from the policies configuration.

---

## Owner

**Primary:** Supply & Inventory Analyst, GxP Compliance Manager (shared)

---

## When This Skill Is Used

- At the start of any workflow that involves supply planning, inventory analysis, or compliance checking
- Used by the Supply Analyst to apply safety stock and reorder rules
- Used by the Compliance Manager to enforce expiry and destruction policies

---

## Inputs

1. **Policies file** — `policies.json` from the study package config folder

---

## Steps

1. **Read the policies file**
   - Load `policies.json` from the study package config folder
   - Confirm the file is non-empty and readable

2. **Extract safety stock rules**
   - Minimum weeks of supply thresholds
   - These may be defined at different levels (global default, by depot, by country, or by item)
   - Note the hierarchy — more specific rules override more general ones

3. **Extract reorder rules**
   - Reorder point definitions — the stock level at which replenishment should be triggered
   - Minimum order quantities — the smallest order that can be placed
   - Maximum order quantities — the largest order that should be placed in a single order

4. **Extract budget constraints**
   - Budget envelope — the total spend limit for the study
   - Cost parameters — unit costs, shipping costs, or other cost references (if available)

5. **Extract expiry and destruction rules**
   - Minimum remaining shelf life rules — how much shelf life must remain at time of shipment or receipt
   - Destruction eligibility criteria — the conditions under which stock can be destroyed (expired, study closed, recalled, etc.)

6. **Validate the policies**
   - Check that safety stock thresholds are present and plausible (positive numbers)
   - Check that reorder points are defined
   - Check that budget envelope is present (flag as warning if missing, not an error)
   - Flag any contradictions (e.g., minimum order quantity greater than maximum)

7. **Produce the parsed output**
   - A normalised set of policy rules ready for use by other agents
   - A validation summary with any issues found

---

## Output

- **Parsed policies** — Normalised rules covering:
  - Safety stock thresholds (with any per-depot, per-country, or per-item overrides)
  - Reorder points and order quantity limits
  - Budget envelope and cost parameters
  - Expiry and destruction rules
- **Validation summary**:
  - Policies loaded by category
  - Any missing or incomplete policies
  - Any contradictions or implausible values
  - Warnings (e.g., no budget defined)

---

## Halt Conditions

- Recommend halt if the file cannot be read or is missing
- Recommend halt if no safety stock rules are defined (cannot assess inventory risk without thresholds)
- Flag but continue if budget or destruction rules are missing

---

## Notes

- This is a static configuration file — it changes rarely, typically only when policies are updated by the supply team
- Policies may be defined at multiple levels of specificity. When loading, preserve the hierarchy so that consuming agents can apply the most specific rule available
- This skill does not apply the policies — it provides the rules that SI-04 (Safety Stock Checker), SI-05 (Reorder Trigger Evaluator), and CO-07 (Destruction Eligibility Checker) use
- Implementations should define their policies to match their organisation's supply chain rules and budget processes
