# DI-06 — Supply Network Loader

## Purpose

Read and normalise the supply network configuration so that agents understand the physical infrastructure of the clinical supply chain — where stock is held, where it is manufactured, how it moves between locations, and which depots serve which countries.

---

## Owner

**Primary:** Supply & Inventory Analyst, Trade & Logistics Specialist (shared)

---

## When This Skill Is Used

- At the start of any workflow that involves inventory analysis, supply planning, or shipping
- Used by the Supply Analyst to understand depot locations and country assignments
- Used by the Logistics Specialist to determine shipping lanes and lead times

---

## Inputs

1. **Supply network file** — `supply_network.json` from the study package config folder

---

## Steps

1. **Read the supply network file**
   - Load `supply_network.json` from the study package config folder
   - Confirm the file is non-empty and readable

2. **Extract locations**
   - **Depots and warehouses** — For each location, extract:
     - Name or identifier
     - Country
     - Storage capabilities (e.g., ambient, cold chain, controlled substance)
   - **Manufacturing sites** — For each site, extract:
     - Name or identifier
     - Country
     - What items they produce or package

3. **Extract shipping lanes**
   - For each lane, extract:
     - Origin location
     - Destination location
     - Lead time in business days
     - Lane type (ground, air, sea)

4. **Extract country assignments**
   - For each country in the study:
     - Which depot(s) serve that country
     - Which sites are supplied from which depot(s)

5. **Validate the network**
   - Check that every country in the study configuration has at least one assigned depot
   - Check that every shipping lane has a valid origin and destination
   - Check that lead times are present and plausible (positive numbers)
   - Flag any orphaned locations (locations defined but not connected to any lane)
   - Flag any countries without a depot assignment

6. **Produce the parsed output**
   - A normalised supply network dataset listing all locations, lanes, and country assignments
   - A validation summary with any issues found

---

## Output

- **Parsed supply network** — Normalised data covering:
  - All depot and warehouse locations with their capabilities
  - All manufacturing sites with their production scope
  - All shipping lanes with origin, destination, lead time, and type
  - Country-to-depot assignments
- **Validation summary**:
  - Total locations (depots, manufacturing sites)
  - Total shipping lanes
  - Countries with assigned depots
  - Flagged issues (orphaned locations, missing assignments, implausible lead times)

---

## Halt Conditions

- Recommend halt if the file cannot be read or is missing
- Recommend halt if no depot locations are defined (cannot plan supply without depots)
- Recommend halt if no shipping lanes are defined (cannot plan logistics without lanes)
- Flag but continue if some countries lack depot assignments or some lanes have missing lead times

---

## Notes

- This is a static configuration file — it changes rarely, typically only when a new country or depot is added to the study
- This skill does not calculate lead times or plan shipments — it provides the network data that LT-01 (Lead Time Calculator) and LT-02 (Shipping Window Planner) use
- Implementations should define their supply network to match their actual depot and logistics infrastructure
