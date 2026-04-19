# DI-04 — ERP Inventory Parser

## Purpose

Read and normalise the ERP inventory data into a consistent structure that the Supply Analyst can work with. This skill extracts stock positions, batch details, orders, and shipment records from the raw ERP data drop.

---

## Owner

**Primary:** Supply & Inventory Analyst

---

## When This Skill Is Used

- At the start of any workflow that requires inventory analysis (e.g., WF-02 — Supply Plan Generation)
- After the Supervisor has confirmed the ERP data file is present and structurally valid (DI-01 and DI-02 passed)

---

## Inputs

1. **ERP inventory file** — The raw data drop containing ERP inventory and order data
2. **Study configuration** — `study_config.json` for context on items, treatment arms, and pack sizes

---

## Steps

1. **Read the ERP data file**
   - Load the file from the current data drop folder
   - Confirm the file is non-empty and readable

2. **Extract and categorise records**
   - Identify and separate records into the following categories:
     - **Stock on hand** — Current quantity of each item held at each depot or warehouse location
     - **Batch/lot details** — Individual batch records including lot number, manufacturing date, expiry date, quantity, and stock status (available, quarantined, released, rejected, on hold)
     - **Purchase orders** — Orders placed with manufacturers or CMOs, including quantities, expected delivery dates, and order status (open, confirmed, in production, shipped, closed)
     - **Production orders** — Manufacturing orders in progress, including expected completion dates and quantities
     - **Shipments in transit** — Stock that has been shipped but not yet received, including origin, destination, expected arrival date, and current status
     - **Shipment history** — Completed shipments for reference and trend analysis
   - For each record, extract the key dimensions:
     - Item or kit type
     - Location (depot, warehouse, or manufacturing site)
     - Country (where applicable)
     - Treatment arm (where applicable)
     - Quantity
     - Date (transaction date, expiry date, expected date — as applicable)
     - Status

3. **Normalise the data**
   - Ensure all dates are in a consistent format
   - Ensure all location and item identifiers match the study configuration and supply network
   - Flag any records with unknown locations, items, or statuses
   - Flag any records with missing or implausible values (e.g., negative stock, expiry dates in the past for available stock)

4. **Summarise the parsed data**
   - Count the total records parsed, broken down by category
   - Note the date range covered by the data
   - Summarise total stock on hand across all locations
   - Count open orders and shipments in transit
   - List any flagged records or data issues

5. **Produce the parsed output**
   - A normalised, categorised dataset ready for consumption by other Supply Analyst skills (SI-01, SI-02, etc.)
   - A parsing summary with record counts, totals, and any issues

---

## Output

- **Parsed ERP dataset** — Normalised records categorised as stock on hand, batch details, purchase orders, production orders, shipments in transit, or shipment history, each with item, location, country, quantity, date, and status
- **Parsing summary**:
  - Total records parsed
  - Records by category (stock on hand, batch/lot, purchase orders, production orders, in-transit shipments, shipment history)
  - Date range of the data
  - Total stock on hand (units across all locations)
  - Open orders count and total quantity
  - In-transit shipments count
  - Flagged records (unknown identifiers, missing values, implausible data)
  - Data issues or warnings

---

## Halt Conditions

- Recommend halt if the file cannot be read or is fundamentally unparseable
- Recommend halt if stock on hand records are entirely missing (cannot assess inventory without stock data)
- Flag but continue if order or shipment records have minor issues

---

## Notes

- This skill does not analyse the data — it prepares it. Analysis happens in the SI skills (SI-01 through SI-10)
- Column names and file formats will vary by implementation. This skill describes what data to extract, not which columns to read
- Implementations should map their specific ERP export format to the categories described here
- The normalised output from this skill becomes the input for SI-01 (Stock Position Calculator), SI-02 (Weeks of Supply Calculator), and SI-03 (Expiry Profile Analyser)
