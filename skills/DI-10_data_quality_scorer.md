# DI-10 — Data Quality Scorer

## Purpose

Assess the overall completeness and consistency of the ingested data and produce a quality flag that travels with the data through all downstream processing. This skill gives every agent a clear signal about how much to trust the data they are working with.

---

## Owner

**Primary:** Supervisor Agent

---

## When This Skill Is Used

- After DI-01 (Data Manifest Checker) and DI-02 (Schema Validator) have passed
- Before the Supervisor routes the workflow to any specialist agent
- The quality flag produced here is included in the context passed to every downstream agent

---

## Inputs

1. **Parsing summaries** — The output summaries from whichever data parsers have run (DI-03, DI-04, DI-05, etc.)
2. **Schema validation results** — The output from DI-02
3. **Study configuration** — For context on what data is expected (countries, sites, items)

---

## Steps

1. **Review completeness**
   - What percentage of expected records are present?
   - Are all countries in the study configuration represented in the data?
   - Are all sites represented?
   - Are all treatment arms represented?
   - Are there any gaps in date coverage (e.g., missing weeks)?

2. **Review consistency**
   - Do the data sources agree with each other where they overlap? (e.g., do sites in RTSM data match sites in CTMS data?)
   - Are there any obvious contradictions? (e.g., more kits dispensed than received)
   - Are totals and subtotals internally consistent where checkable?

3. **Review flagged issues**
   - Collect all flags and warnings raised by the parsers and schema validator
   - Count the total number of flagged records across all files
   - Calculate the percentage of records with issues

4. **Assign a quality flag**
   - **CLEAN** — Data is complete, consistent, and has no significant issues. Agents can proceed with confidence.
   - **WARNINGS** — Data is usable but has minor gaps or inconsistencies. Agents should proceed but note caveats in their outputs.
   - **CRITICAL** — Data has significant completeness or consistency problems. The Supervisor should consider halting the workflow.

5. **Produce the quality report**
   - State the overall quality flag
   - Summarise the completeness assessment
   - Summarise the consistency assessment
   - List the most significant issues found
   - Recommend whether to proceed, proceed with caveats, or halt

---

## Output

- **Data quality flag**: `CLEAN` | `WARNINGS` | `CRITICAL`
- **Quality report**:
  - Overall flag with plain English explanation
  - Completeness score (what percentage of expected data is present)
  - Consistency score (how well data sources agree with each other)
  - Total flagged records across all files
  - Top issues (the most significant problems found, ranked by impact)
  - Recommendation (proceed, proceed with caveats, or halt)

---

## Halt Conditions

- Recommend halt if quality flag is CRITICAL
- The Supervisor makes the final call on whether to halt or proceed with caveats

---

## Notes

- The quality flag is not a pass/fail gate — it is information that helps agents and human reviewers understand confidence in the results
- Every downstream agent receives the quality flag as part of its input context and should reference it in its outputs
- This skill aggregates issues already found by the parsers and schema validator — it does not re-read raw files
- Implementations may want to define specific thresholds for what counts as CLEAN vs. WARNINGS vs. CRITICAL based on their risk tolerance
