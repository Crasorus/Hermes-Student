# DI-08 — Reference Document Loader

## Purpose

Read and normalise the study's reference documents so that agents can apply country-specific compliance rules and use approved vendor lists. This skill loads shelf life requirements, label requirements, and approved vendors from the study package reference folder.

---

## Owner

**Primary:** GxP Compliance Manager

---

## When This Skill Is Used

- At the start of any workflow that involves compliance checking, shipping, or label validation
- Used by the Compliance Manager to validate shelf life and labelling compliance
- Used by the Logistics Specialist to select approved vendors

---

## Inputs

1. **Shelf life by country file** — `shelf_life_by_country.json` from the study package reference folder
2. **Label requirements file** — `label_requirements.json` from the study package reference folder
3. **Approved vendors file** — `approved_vendors.json` from the study package reference folder

---

## Steps

1. **Read the shelf life by country file**
   - Load `shelf_life_by_country.json`
   - For each country, extract:
     - Country identifier
     - Minimum remaining shelf life at time of shipment (in months or days)
     - Any item-specific overrides (if certain items have different requirements)
   - Flag any countries in the study configuration that do not have a shelf life entry

2. **Read the label requirements file**
   - Load `label_requirements.json`
   - For each country, extract:
     - Country identifier
     - Required label language(s)
     - Required label content elements
     - Required label format or packaging specifications
   - Flag any countries in the study configuration that do not have label requirements defined

3. **Read the approved vendors file**
   - Load `approved_vendors.json`
   - For each vendor, extract:
     - Vendor name or identifier
     - Vendor type (courier, broker, CMO)
     - Approved lanes (which origin-destination routes this vendor is approved for)
     - Capabilities (cold chain, controlled substance, hazardous goods)
   - Flag any shipping lanes in the supply network that do not have at least one approved vendor

4. **Validate the reference documents**
   - Check that all countries in the study have shelf life and label entries
   - Check that all shipping lanes have at least one approved vendor
   - Check for internal consistency (e.g., no duplicate entries, no conflicting rules)
   - Note the version or last-updated date of each document (if available) for change detection by CO-10

5. **Produce the parsed output**
   - A normalised set of reference data ready for use by other agents
   - A validation summary with any gaps or issues found

---

## Output

- **Parsed reference data** — Normalised data covering:
  - Shelf life requirements by country (with any item-specific overrides)
  - Label requirements by country (language, content, format)
  - Approved vendors by lane (with capabilities)
- **Validation summary**:
  - Countries with complete reference data
  - Countries with missing shelf life or label entries
  - Lanes with no approved vendor
  - Document version dates (if available)
  - Any inconsistencies or gaps

---

## Halt Conditions

- Recommend halt if none of the three reference files can be read
- Flag but continue if one or two files are missing — the agent team can still operate with reduced compliance coverage, but compliance checks for the missing area will return "UNABLE TO VERIFY"

---

## Notes

- These are static reference files — they change rarely, typically when a new country is added or a vendor is approved/removed
- This skill does not enforce compliance — it provides the reference data that CO-01 (Protocol Compliance Checker), CO-02 (Label Requirements Validator), CO-03 (Shelf Life Compliance Checker), and LT-05 (Approved Vendor Selector) use
- CO-10 (Regulatory Change Alerter) compares the version dates loaded here against the previous run to detect changes
- Implementations should define their reference documents to match their regulatory and procurement requirements
