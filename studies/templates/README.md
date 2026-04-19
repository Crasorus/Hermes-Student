# Study Templates

This folder contains the template files used when initialising a new study. Templates are copied into a new study folder and personalised — they are never edited directly.

---

## Initialising a New Study

Run the `/init-study` command from the Claude Code chat window:

```
/init-study <study_id>
```

**Example:**
```
/init-study 106100
```

The `study_id` must match the folder name exactly. It also becomes the `protocol_number` in `study_config.json`, which the runner uses to verify the correct study is loaded.

### What the command does

1. **Checks** whether `studies/<study_id>/` already exists — asks before overwriting
2. **Creates** the folder structure:
   ```
   studies/<study_id>/
     config/       ← static configuration, edit once at study setup
     reference/    ← reference documents, update when regulations change
     data_drops/   ← one dated subfolder per data delivery
     outputs/      ← workflow run outputs, written automatically by the runner
   ```
3. **Copies** all seven template files into the new study folder
4. **Substitutes** `__STUDY_ID__` with the actual study ID in `study_config.json`
5. **Prints a checklist** of every `TODO` field that still needs filling in

### After running the command

Work through the checklist. Every field marked `TODO:` needs a real value before any workflow can run. The checklist groups the fields by file and tells you what each one is for.

Once all `TODO` fields are complete, place the first data drop:
```
studies/<study_id>/data_drops/YYYY-MM-DD/
  rtsm_actuals.csv
  erp_inventory.csv
  ctms_plan.csv
  site_inventory.csv
```

Then run the first workflow:
```
/run-workflow WF-01 <study_id>
```

---

## The Templates

Each template matches the schema expected by the agent team. Structure and field names must not be changed — only the `TODO:` values need replacing.

### `config/study_config.json`

The master configuration file. Defines the study identity, treatment arms, investigational items, countries, sites, and the data schemas that agents use to validate incoming files.

**Key fields to fill in:**
- `study_identity` — study name, phase, sponsor
- `treatment_arms` — arm IDs, names, and descriptions
- `items` — item IDs, pack sizes, temperature requirements
- `countries` and `sites` — all locations the study runs in
- `assumptions` — screen failure and dropout rates for demand modelling

The `protocol_number` field is auto-filled from the study ID you provide. All other values are `TODO`.

---

### `config/supply_network.json`

Defines the physical supply chain: where stock is held, where it is made, and how it moves between locations.

**Key fields to fill in:**
- `depots` — distribution centres with their capabilities (ambient, cold chain)
- `manufacturing_sites` — where IMP is produced, and which items each site makes
- `shipping_lanes` — routes between locations with lead times in business days
- `country_depot_assignments` — which depot serves each country

Lane IDs defined here are referenced by `approved_vendors.json`.

---

### `config/policies.json`

Business rules that govern supply planning. Default values are conservative and suitable for most studies — review and adjust where needed.

**Key fields to review:**
- `budget` — set the budget envelope and currency (or set to `null` if not tracked)
- `sop_references` — list the organisation's relevant SOPs
- `safety_stock.default_minimum_weeks` — adjust for study risk profile and lead times
- `reorder_rules.reorder_point_weeks` — must be greater than safety stock to cover lead time

---

### `reference/approved_vendors.json`

Lists every courier, customs broker, and CMO approved for use in this study. Used by the Logistics Specialist (LT-05) to select vendors for each shipment.

**Key fields to fill in:**
- `vendor_name` and `vendor_type` — courier, broker, or CMO
- `approved_lanes` — the lane IDs from `supply_network.json` this vendor can serve
- `capabilities` — ambient, cold_chain, controlled_substance, customs_clearance

---

### `reference/shelf_life_by_country.json`

Minimum remaining shelf life (in months) required at the time of shipment for each destination country. Used by the Compliance Manager (CO-03) to flag batches that cannot be shipped.

Add one entry per country. If a country has different requirements per item, use `item_overrides`.

---

### `reference/label_requirements.json`

Language, content, and format requirements for clinical supply labels in each country. Used by the Compliance Manager (CO-02) to validate shipments.

Add one entry per country. Check the local regulatory authority's IMP labelling guidance for the required content list.

---

### `reference/reorder_policies.json`

Parameters used by the reorder point calculator to compute optimal min/max stock thresholds for each site and item. The `default_policy` applies to all sites unless overridden.

The defaults (weekly review, 95% service level) are appropriate for most sites. Add entries to `site_policies` for depots that need stricter or more relaxed settings.

---

## Rules

- **Never edit templates directly** to fix a study-specific issue — edit the file in the study's own folder
- **Templates are the starting point**, not the finished product — every `TODO` field must be replaced
- **Do not change field names or structure** — agents expect the exact schema defined here
- If the template structure needs updating (new field, changed schema), update the template here so all future studies benefit
