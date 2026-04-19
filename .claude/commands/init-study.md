# Initialise Study Folder

Set up a new study folder under `studies/` with the correct structure and template config files, ready to edit.

## Arguments

The user provides: `$ARGUMENTS`

Parse as: `<study_id>`

- **study_id** (required): the protocol number — this becomes the folder name and must match `protocol_number` in `study_config.json`. Examples: `106100`, `ATLAS-03`, `CARDIO-P2`.

If no study_id is provided, ask the user for it. Do not guess.

---

## Procedure

Follow these steps exactly, in order.

### Step 1: Validate

Check whether `studies/<study_id>/` already exists.

- If it **does exist**, stop and ask: _"A folder for `<study_id>` already exists. Do you want to overwrite it?"_ Do not proceed unless confirmed.
- If it **does not exist**, continue.

### Step 2: Create folder structure

Create the following empty folders:

```
studies/<study_id>/
  config/
  reference/
  data_drops/
  outputs/
```

Use the Write tool to create a `.keep` placeholder file in `data_drops/` and `outputs/` so the empty folders are visible in the file explorer:

- `studies/<study_id>/data_drops/.keep` — content: `# Place dated data drop folders here, e.g. 2026-04-18/`
- `studies/<study_id>/outputs/.keep` — content: `# Workflow run outputs are written here automatically`

### Step 3: Copy and personalise config files

ask the user if they want to copy over templates. If they say yes, then perform the following:

For each of the six template files below, read the template, replace `__STUDY_ID__` with `<study_id>`, then write to the destination.

| Template                                                 | Destination                                               |
| -------------------------------------------------------- | --------------------------------------------------------- |
| `studies/templates/config/study_config.json`             | `studies/<study_id>/config/study_config.json`             |
| `studies/templates/config/supply_network.json`           | `studies/<study_id>/config/supply_network.json`           |
| `studies/templates/config/policies.json`                 | `studies/<study_id>/config/policies.json`                 |
| `studies/templates/reference/approved_vendors.json`      | `studies/<study_id>/reference/approved_vendors.json`      |
| `studies/templates/reference/shelf_life_by_country.json` | `studies/<study_id>/reference/shelf_life_by_country.json` |
| `studies/templates/reference/label_requirements.json`    | `studies/<study_id>/reference/label_requirements.json`    |
| `studies/templates/reference/reorder_policies.json`      | `studies/<study_id>/reference/reorder_policies.json`      |

### Step 4: Report

Print a confirmation and setup checklist:

```
Study <study_id> initialised
================================
Folder: studies/<study_id>/

Folders created:
  ✓ config/
  ✓ reference/
  ✓ data_drops/
  ✓ outputs/

Config files ready to edit:
  ✓ config/study_config.json
  ✓ config/supply_network.json
  ✓ config/policies.json

Reference files ready to edit:
  ✓ reference/approved_vendors.json
  ✓ reference/shelf_life_by_country.json
  ✓ reference/label_requirements.json
  ✓ reference/reorder_policies.json

================================
Next steps — fill in all TODO fields:

  config/study_config.json
    □ study_identity (study_id, study_name, phase, sponsor)
    □ treatment_arms (arm names and descriptions)
    □ items (item IDs, pack sizes, temperature requirements)
    □ countries (country codes and names)
    □ sites (site IDs, names, country assignments)
    □ assumptions (screen failure rate, dropout rate)

  config/supply_network.json
    □ depots (locations, capabilities)
    □ manufacturing_sites (where IMP is produced)
    □ shipping_lanes (routes and lead times)
    □ country_depot_assignments

  config/policies.json
    □ budget (envelope and currency)
    □ sop_references (your organisation's SOPs)
    □ Review safety stock and reorder defaults

  reference/approved_vendors.json
    □ Couriers, brokers, and CMOs with lane assignments

  reference/shelf_life_by_country.json
    □ Minimum shelf life requirement per country

  reference/label_requirements.json
    □ Required languages and content per country

  reference/reorder_policies.json
    □ Site-level overrides if non-default review periods needed

Once all TODO fields are complete, place your first data drop in:
  data_drops/YYYY-MM-DD/
    rtsm_actuals.csv
    erp_inventory.csv
    ctms_plan.csv
    site_inventory.csv


================================
```

---

## Rules

- Do not invent values for TODO fields — leave them as-is for the user to fill in.
- The only substitution you make is replacing `__STUDY_ID__` with the actual study_id.
- Do not create data drop subfolders — those are created when data arrives.
- Do not run any workflows — this command only sets up the folder structure.
