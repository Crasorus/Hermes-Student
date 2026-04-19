# DI-03 — RTSM Data Parser

## Purpose

Read and normalise the RTSM actuals data into a consistent structure that the Demand Analyst can work with. This skill extracts dispensing events, randomisation records, screen failures, returns, and site shipments from the raw RTSM data drop.

**NOTE (2026-03-14):** Site inventory has been moved to a separate file (`site_inventory.csv`). DI-03 no longer parses site inventory — that is now handled by the Site Inventory Reader (separate skill, TBD).

---

## Owner

**Primary:** Demand & Forecast Analyst

---

## When This Skill Is Used

- At the start of any workflow that requires demand analysis (e.g., WF-01 — Demand Signal Refresh)
- After the Supervisor has confirmed the RTSM data file is present and structurally valid (DI-01 and DI-02 passed)

---

## Inputs

1. **RTSM actuals file** — The raw data drop containing RTSM transaction data
2. **Study configuration** — `study_config.json` for context on treatment arms, items, and site list

---

## Steps

1. **Read the RTSM data file**
   - Load the file from the current data drop folder
   - Confirm the file is non-empty and readable

2. **Extract and categorise records**
   - Identify and separate records into the following categories:
     - **Dispensing events** — When a kit or pack was dispensed to a patient at a site
     - **Randomisation events** — When a patient was randomised into a treatment arm
     - **Screen failure events** — When a screened patient did not proceed to randomisation
     - **Return events** — When dispensed stock was returned (unused, damaged, or expired)
     - **Site shipment events** — Shipments received at or in transit to a site
   - **Skip site inventory events** — These are now in site_inventory.csv (separate file)
   - For each record, extract the key dimensions:
     - Site identifier
     - Country
     - Treatment arm (where applicable)
     - Item or kit type
     - Date of the event
     - Quantity

3. **Normalise the data**
   - Ensure all dates are in a consistent format
   - Ensure all site and country identifiers match the study configuration
   - Flag any records with unknown sites, countries, or treatment arms
   - Flag any records with missing or implausible values (e.g., negative quantities, future dates)

4. **Summarise the parsed data**
   - Count the total records parsed, broken down by category
   - Note the date range covered by the data
   - List any flagged records or data issues
   - **Note:** If site_inventory records are found in RTSM file, flag them with a message: "Site inventory records found in rtsm_actuals.csv — these should be in site_inventory.csv instead. Please verify data structure."

5. **Produce the parsed output**
   - A normalised, categorised dataset ready for consumption by other Demand Analyst skills (DF-01, DF-02, etc.)
   - A parsing summary with record counts, date range, and any issues

---

## Output

- **Parsed RTSM dataset** — Normalised records categorised as dispensing, randomisation, screen failure, return, or site shipment events (site inventory excluded), each with site, country, arm, item, date, and quantity
- **Parsing summary**:
  - Total records parsed
  - Records by category (dispensing, randomisation, screen failure, return, site shipment)
  - Date range of the data
  - Flagged records (unknown identifiers, missing values, implausible data)
  - Data issues or warnings
  - **Alert if site_inventory records found:** "Site inventory data found in rtsm_actuals.csv but should be in site_inventory.csv"

---

## Halt Conditions

- Recommend halt if the file cannot be read or is fundamentally unparseable
- Recommend halt if more than a configurable percentage of records have critical issues (e.g., missing site, missing date)
- Flag but continue if a small number of records have minor issues

---

## Notes

- This skill does not analyse the data — it prepares it. Analysis happens in the DF skills (DF-01 through DF-09)
- Column names and file formats will vary by implementation. This skill describes what data to extract, not which columns to read
- Implementations should map their specific RTSM export format to the categories described here
- The normalised output from this skill becomes the input for DF-01 (Consumption Rate Calculator) and DF-02 (Enrollment Trajectory Modeller)
