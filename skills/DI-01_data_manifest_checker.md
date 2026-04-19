# DI-01 — Data Manifest Checker

## Purpose

Verify that all expected files are present in the study package before any workflow begins. If critical files are missing, halt the workflow and report what is missing. If optional files are missing, proceed but flag a caveat.

---

## Owner

**Primary:** Supervisor Agent

---

## When This Skill Is Used

- At the start of every workflow run, before any other agent is invoked
- The Supervisor executes this skill as Step 2 of its standard workflow

---

## Inputs

1. **Study configuration** — The `study_config.json` file, which contains a `required_files` section listing the files expected for this study
2. **Study package path** — The root path to the study package folder
3. **Data drop date** — The date of the current data drop (used to locate the correct data drop folder)

---

## Steps

1. **Read the file manifest from study configuration**
   - Open `study_config.json`
   - Locate the `required_files` section
   - This section lists each expected file with:
     - File name or pattern
     - File location (relative to study package root)
     - Criticality: `critical` or `optional`

2. **Check each file**
   - For each file in the manifest:
     - Check whether the file exists at the expected location
     - Check whether the file is non-empty (a zero-byte file counts as missing)
     - Record the result: `FOUND`, `MISSING`, or `EMPTY`

3. **Classify the result**
   - If any file marked `critical` is `MISSING` or `EMPTY` → overall status is **HALT**
   - If all critical files are `FOUND` but some optional files are `MISSING` → overall status is **PASS WITH CAVEATS**
   - If all files are `FOUND` → overall status is **PASS**

4. **Produce the manifest report**
   - List every file checked, its expected location, its criticality, and its status
   - If HALT: clearly state which critical files are missing and that the workflow cannot proceed
   - If PASS WITH CAVEATS: clearly state which optional files are missing and what impact this may have

---

## Output

A manifest report with the following structure:

- **Overall status**: `PASS` | `PASS WITH CAVEATS` | `HALT`
- **Files checked**: A list showing each file, its location, criticality, and status
- **Missing files**: A list of any files not found or empty
- **Halt reason**: If halted, a plain English explanation of what is missing and what is needed to proceed
- **Caveats**: If passing with caveats, a plain English explanation of what is missing and what downstream impact it may have

---

## Halt Conditions

- **HALT** if any file marked `critical` in the manifest is missing or empty
- The Supervisor must stop the workflow and report the manifest error — no other agent should run

---

## Notes

- The file manifest is defined in `study_config.json`, making it fully configurable per study
- This skill does not validate file content or schema — that is DI-02 (Schema Validator)
- This skill does not assess data quality — that is DI-10 (Data Quality Scorer)
- Implementations should define their own file lists and criticality levels in the study configuration
