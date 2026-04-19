# DI-09 — Study Config Loader

## Purpose

Read and normalise the study configuration file, which is the central definition of the study. This skill loads study identity, treatment arms, items, thresholds, file manifests, schemas, and country/site lists that are used by almost every other skill and agent.

---

## Owner

**Primary:** Supervisor Agent

---

## When This Skill Is Used

- At the very start of every workflow — this is the first skill the Supervisor executes
- The study configuration is the foundation that all other agents and skills depend on

---

## Inputs

1. **Study configuration file** — `study_config.json` from the study package config folder

---

## Steps

1. **Read the study configuration file**
   - Load `study_config.json` from the study package config folder
   - Confirm the file is non-empty and readable

2. **Extract study identity**
   - Study ID
   - Study name
   - Protocol number
   - Study phase

3. **Extract treatment arms**
   - Arm names and descriptions
   - Randomisation ratios (e.g., 2:1 active to placebo)

4. **Extract items and pack sizes**
   - Kit types or item identifiers
   - Pack configurations (units per pack, packs per case)
   - Mapping of items to treatment arms

5. **Extract thresholds**
   - Demand delta significance threshold (default 10%)
   - Any per-item or per-country overrides
   - Any other configurable thresholds used by the framework

6. **Extract required files manifest**
   - The list of expected files used by DI-01 (Data Manifest Checker)
   - Each entry includes file name, location, and criticality (critical or optional)

7. **Extract schema definitions**
   - The expected structure for each data file, used by DI-02 (Schema Validator)
   - Each entry includes expected columns or keys, required vs. optional, and expected data types

8. **Extract countries and sites**
   - List of participating countries
   - List of sites with their country assignments

9. **Validate the configuration**
   - Check that study identity fields are present
   - Check that at least one treatment arm is defined
   - Check that at least one item is defined
   - Check that the required files manifest is present
   - Check that at least one country and site are defined
   - Flag any missing or incomplete sections

10. **Produce the parsed output**
    - A normalised study configuration ready for use by all agents
    - A validation summary with any issues found

---

## Output

- **Parsed study configuration** — Normalised data covering:
  - Study identity (ID, name, protocol, phase)
  - Treatment arms and randomisation ratios
  - Items, pack sizes, and arm mappings
  - Thresholds (with any overrides)
  - Required files manifest
  - Schema definitions
  - Countries and sites
- **Validation summary**:
  - Sections loaded successfully
  - Any missing or incomplete sections
  - Any warnings or issues

---

## Halt Conditions

- Recommend halt if the file cannot be read or is missing — the study configuration is required for every workflow
- Recommend halt if study identity is missing (cannot log or audit without a study ID)
- Recommend halt if no treatment arms or items are defined (cannot analyse demand or supply)
- Flag but continue if thresholds are missing (the framework will apply the default 10%)

---

## Notes

- This is the most critical configuration file in the framework — without it, no workflow can run
- This skill is always the first step in the Supervisor's workflow, before DI-01 and DI-02
- The required files manifest and schema definitions in this file drive DI-01 and DI-02 respectively, making `study_config.json` the single source of truth for what data the framework expects
- Implementations should populate this file carefully during study setup — it defines the entire operating context for the agent team
