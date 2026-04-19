# DI-02 — Schema Validator

## Purpose

Validate that each data file conforms to its expected structure — correct columns, expected data types, and required fields present. This skill catches structural problems before any analysis begins.

---

## Owner

**Primary:** Supervisor Agent

---

## When This Skill Is Used

- Immediately after DI-01 (Data Manifest Checker) passes
- Runs on every file that was confirmed present in the manifest check
- The Supervisor executes this skill as Step 3 of its standard workflow

---

## Inputs

1. **Study configuration** — The `study_config.json` file, which contains a `schemas` section defining the expected structure for each data file
2. **Data files** — The files confirmed present by DI-01

---

## Steps

1. **Read the schema definitions from study configuration**
   - Open `study_config.json`
   - Locate the `schemas` section
   - Each entry defines an expected file and its structure:
     - Expected columns or keys
     - Which columns or keys are required vs. optional
     - Expected data types (text, number, date, boolean)

2. **Validate each file against its schema**
   - For CSV files:
     - Check that all required columns are present in the header row
     - Check that no unexpected columns exist (flag as warning, not error)
     - Spot-check a sample of rows to confirm data types are plausible (e.g., a date column contains date-like values, a number column contains numeric values)
   - For JSON files:
     - Check that all required keys are present at the expected level
     - Check that values are the expected data types

3. **Classify each file**
   - **VALID** — All required columns/keys present, data types plausible
   - **VALID WITH WARNINGS** — Required structure is present but unexpected columns found or minor type mismatches detected
   - **INVALID** — Required columns/keys missing or data types fundamentally wrong

4. **Produce the validation report**
   - List every file validated, its schema status, and any specific issues found
   - If any file is INVALID, recommend the Supervisor halt the workflow

---

## Output

A schema validation report with the following structure:

- **Overall status**: `VALID` | `VALID WITH WARNINGS` | `INVALID`
- **Files validated**: A list showing each file, its schema status, and any issues
- **Warnings**: Any non-critical issues (unexpected columns, minor type concerns)
- **Errors**: Any critical issues (missing required columns/keys, wrong data types)
- **Recommendation**: Whether the workflow should proceed, proceed with caveats, or halt

---

## Halt Conditions

- Recommend HALT if any file is classified as INVALID — the Supervisor makes the final call
- This skill recommends but does not halt directly — only the Supervisor halts workflows

---

## Notes

- Schema definitions live in `study_config.json`, keeping everything in one place per study
- This skill validates structure only — it does not assess data quality or completeness (that is DI-10)
- Type checking should be pragmatic, not strict — a date formatted as "2026-03-06" and "06-Mar-2026" are both acceptable if they are recognisably dates
- Implementations may need to adjust schema definitions as their data sources evolve
