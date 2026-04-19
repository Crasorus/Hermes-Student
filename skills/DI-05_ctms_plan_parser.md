# DI-05 — CTMS Plan Parser

## Purpose

Read and normalise the CTMS plan data into a consistent structure that the Demand Analyst can work with. This skill extracts enrollment plans, site information, and visit schedules from the raw CTMS data drop.

---

## Owner

**Primary:** Demand & Forecast Analyst

---

## When This Skill Is Used

- At the start of any workflow that requires demand analysis (e.g., WF-01 — Demand Signal Refresh)
- After the Supervisor has confirmed the CTMS data file is present and structurally valid (DI-01 and DI-02 passed)

---

## Inputs

1. **CTMS plan file** — The raw data drop containing clinical trial management plan data
2. **Study configuration** — `study_config.json` for context on treatment arms, sites, and countries

---

## Steps

1. **Read the CTMS data file**
   - Load the file from the current data drop folder
   - Confirm the file is non-empty and readable

2. **Extract and categorise records**
   - Identify and separate records into the following categories:
     - **Enrollment plan** — Planned enrollment numbers by site and country, target enrollment dates, and milestones
     - **Site information** — Site activation dates (planned and actual), site status (planned, active, closed, on hold)
     - **Visit schedules** — Planned visit types and timing per patient, visit windows
   - For each record, extract the key dimensions:
     - Site identifier
     - Country
     - Treatment arm (where applicable)
     - Date or date range
     - Quantity or count (e.g., planned patients, planned visits)
     - Status (where applicable)

3. **Normalise the data**
   - Ensure all dates are in a consistent format
   - Ensure all site and country identifiers match the study configuration
   - Flag any records with unknown sites or countries
   - Flag any records with missing or implausible values (e.g., activation date after enrollment target date)

4. **Summarise the parsed data**
   - Count the total records parsed, broken down by category
   - Note the date range covered by the plan
   - Summarise total planned enrollment by country
   - Count sites by status (planned, active, closed, on hold)
   - List any flagged records or data issues

5. **Produce the parsed output**
   - A normalised, categorised dataset ready for consumption by other Demand Analyst skills (DF-01, DF-02, etc.)
   - A parsing summary with record counts, totals, and any issues

---

## Output

- **Parsed CTMS dataset** — Normalised records categorised as enrollment plan, site information, or visit schedule entries, each with site, country, dates, quantities, and status
- **Parsing summary**:
  - Total records parsed
  - Records by category (enrollment plan, site information, visit schedules)
  - Date range of the plan
  - Total planned enrollment by country
  - Site status counts (planned, active, closed, on hold)
  - Flagged records (unknown identifiers, missing values, implausible data)
  - Data issues or warnings

---

## Halt Conditions

- Recommend halt if the file cannot be read or is fundamentally unparseable
- Recommend halt if enrollment plan records are entirely missing (cannot model demand without a plan baseline)
- Flag but continue if site information or visit schedule records have minor issues

---

## Notes

- This skill does not analyse the data — it prepares it. Analysis happens in the DF skills (DF-01 through DF-09)
- Column names and file formats will vary by implementation. This skill describes what data to extract, not which columns to read
- Implementations should map their specific CTMS export format to the categories described here
- The normalised output from this skill becomes the input for DF-02 (Enrollment Trajectory Modeller) and DF-07 (Visit & Dispensing Calculator)
