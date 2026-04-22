# Hermes Grimoire

> The encyclopaedic reference for every moving part of the Hermes Clinical Supply Chain AI Agent Team. Where [README.md](README.md) is the quickstart and [CLAUDE.md](CLAUDE.md) is the IDE configuration, this Grimoire is the deep reference: every command, agent, skill, workflow, tool, template, config file, reference file, data drop, and output folder — plus a dedicated section on the Python runner that sits underneath the prompt layer.

---

## Table of Contents

- [Part I — Overview](#part-i--overview)
- [Part II — Slash Commands](#part-ii--slash-commands)
- [Part III — The Agent Team](#part-iii--the-agent-team)
- [Part IV — The Skills Library](#part-iv--the-skills-library)
- [Part V — Workflows](#part-v--workflows)
- [Part VI — The Study Package](#part-vi--the-study-package)
- [Part VII — Templates and Study Initialisation](#part-vii--templates-and-study-initialisation)
- [Part VIII — The StudyDataCreation HTML Tool](#part-viii--the-studydatacreation-html-tool)
- [Part IX — The Lab (Training Kit)](#part-ix--the-lab-training-kit)
- [Part X — Two Ways to Run Hermes](#part-x--two-ways-to-run-hermes)
- [Part XI — Python in Depth](#part-xi--python-in-depth)
- [Part XII — Environment and Settings](#part-xii--environment-and-settings)
- [Part XIII — Glossary and Cross-Reference Index](#part-xiii--glossary-and-cross-reference-index)

---

## Part I — Overview

### What Hermes Is

Hermes is a **Clinical Supply Chain AI Agent Team** built for pharmaceutical trial supply management. Seven specialised agents collaborate — autonomously where possible, with humans at review points — to ingest operational data, analyse demand, plan supply, monitor risk, enforce compliance, and report out. The intelligence of every agent and every skill is expressed in plain Markdown, not code. A thin Python runner calls the Claude API to execute those prompts in ordered workflows and write auditable outputs. The framework is **system-agnostic** (it reads CSV/JSON data drops rather than talking to ERP/RTSM systems directly) and **portable** (the same study package structure works for any protocol).

> Disclaimer: Hermes is provided solely as an educational and exploratory tool to demonstrate potential AI use cases within clinical supply chain processes. It is not a validated system and must not be used to support decision-making in regulated clinical trial activities, including but not limited to patient safety, drug supply, or compliance-related functions.

> No warranty, express or implied, is provided. Hermes is used entirely at the user’s own risk.

### Design Principles

1. **System-Agnostic Data Layer** — Hermes operates on CSV/JSON data drops, not live ERP/RTSM connections. Any source can feed it as long as the files match the schema.
2. **Portable Study Package** — the folder layout inside `studies/{study_id}/` is identical across protocols; only the content changes.
3. **Configurable Thresholds** — defaults (e.g. 10% demand-delta significance) are overridable per study via `study_config.json`.
4. **Human-in-the-Loop at Output Only** — agents run end-to-end without interruption; humans review outputs and approve supply plans before execution.
5. **GxP Audit Trail by Default** — every agent action is logged with timestamp, study ID, workflow ID, and input references.
6. **Recommendations vs Decisions** — agents never make regulated decisions. They produce recommendations; humans accept or reject.

### Top-Level Folder Map

```
d:\Hermes\
├── README.md                   User-facing quickstart
├── CLAUDE.md                   Claude Code IDE configuration
├── Hermes_Grimoire.md          This document
├── .env.example                API-key template
├── run.bat / run.sh            Interactive CLI launchers
│
├── agents/                     7 specialised agents (Markdown only)
├── skills/                     76 shared skill definitions
├── workflows/                  5 workflow markdowns + workflows.json
├── runner/                     Python execution engine
├── studies/                    Per-study packages + templates
├── StudyDataCreation/          Browser-based test-data generator
├── lab/                        3-hour workshop kit
├── docs/                       Artifacts and training material
└── .claude/                    Commands, settings, memories
```

### How Everything Fits Together

A user (or cron job) triggers a **workflow** by ID against a **study**. The workflow names a sequence of **agents**. Each agent follows its system prompt and invokes the **skills** it owns, reading from the study's **data drop** and **config/reference** files. The runner (or chat session) relays signals between steps, gates conditional steps, and writes the final outputs to `studies/{study_id}/outputs/{date}/`. The agents reason in Markdown; the runner does the plumbing.

---

## Part II — Slash Commands

Four Claude Code chat commands live in [.claude/commands/](.claude/commands/). Each is a Markdown file that the IDE loads when you type its name. They are thin wrappers around workflow execution and study setup.

| Command                 | Syntax                                                 | Purpose                                                                                                                                                                                                                 |
| ----------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **/run-workflow**       | `/run-workflow <WF-ID> <STUDY_ID> [YYYY-MM-DD]`        | Execute a single workflow against a study, optionally pinning the data-drop date (defaults to latest). Runs the agents in conversation.                                                                                 |
| **/run-workflow-chain** | `/run-workflow-chain <STUDY_ID> <WF-ID_1> [WF-ID_2] …` | Run multiple workflows sequentially in one chat session so context carries forward (e.g. WF-01 → WF-02).                                                                                                                |
| **/init-study**         | `/init-study <STUDY_ID>`                               | Create a new study folder from [studies/templates/](studies/templates/). Creates `config/`, `reference/`, `data_drops/`, `outputs/`, substitutes the study ID, and leaves `TODO` markers where human input is required. |
| **/preflight**          | `/preflight <STUDY_ID>`                                | Quick pre-flight check: invokes SO-00 → DI-12 against the latest data drop and reports PASS / WARNING / FAIL before you commit to a full workflow run.                                                                  |

Command source files:

- [.claude/commands/run-workflow.md](.claude/commands/run-workflow.md)
- [.claude/commands/run-workflow-chain.md](.claude/commands/run-workflow-chain.md)
- [.claude/commands/init-study.md](.claude/commands/init-study.md)
- [.claude/commands/preflight.md](.claude/commands/preflight.md)

---

## Part III — The Agent Team

Each agent lives in its own folder under [agents/](agents/) with exactly two files: `README.md` (human-readable role card) and `system_prompt.md` (the actual instructions Claude follows). Agents are stateless — they receive a user message assembled by the runner (or by Claude in chat mode) and produce a Markdown response.

| #   | Agent                                | Folder                                                       | Role                                                                                                                                                                   |
| --- | ------------------------------------ | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Supervisor**                       | [agents/supervisor/](agents/supervisor/)                     | Entry point for every workflow. Validates study packages, routes work, coordinates agents, emits control signals (SIGNIFICANT_DELTA, HALT, …), writes the run summary. |
| 2   | **Demand & Forecast Analyst**        | [agents/demand_analyst/](agents/demand_analyst/)             | Calculates consumption rates, enrollment trajectories, demand deltas; generates base/optimistic/pessimistic scenarios; updates baselines.                              |
| 3   | **Supply & Inventory Analyst**       | [agents/supply_analyst/](agents/supply_analyst/)             | Computes stock positions, weeks-of-supply, safety-stock checks, reorder points, order quantities.                                                                      |
| 4   | **Trade & Logistics Specialist**     | [agents/logistics_specialist/](agents/logistics_specialist/) | Plans shipping windows, validates cold-chain and customs requirements, selects approved vendors, generates shipping requests.                                          |
| 5   | **GxP Compliance Manager**           | [agents/compliance_manager/](agents/compliance_manager/)     | Cross-cutting guardrail. Protocol/label/shelf-life compliance, deviation impact, SOP cross-checks, maintains the audit trail via CO-08.                                |
| 6   | **Clinical Data & Insights Analyst** | [agents/insights_analyst/](agents/insights_analyst/)         | Risk intelligence — hot-spot detection, anomaly detection, KPI calculation, shortage probability modelling.                                                            |
| 7   | **Communications & Reporting Agent** | [agents/reporting_agent/](agents/reporting_agent/)           | Converts structured agent outputs into stakeholder-ready reports: demand refresh summaries, executive reports, hot-spot alerts, deviation reports, dashboard feeds.    |

Open any agent's `README.md` for its owned-skills list and input/output shape, and `system_prompt.md` for the actual directive Claude executes.

---

## Part IV — The Skills Library

76 skills live as individual Markdown files in [skills/](skills/). Skills are **shared**: any agent can invoke any skill. They are identified by a two-letter category prefix and a two-digit number (e.g. `DI-12`). The agent's README names the skills it owns; the skill file itself documents Purpose, Owner, Inputs, Steps, and Output Format.

### DI — Data Ingestion (12)

| ID    | Title                     | Purpose                                                                                            |
| ----- | ------------------------- | -------------------------------------------------------------------------------------------------- |
| DI-01 | Data Manifest Checker     | Verify all expected files are present before a workflow begins                                     |
| DI-02 | Schema Validator          | Validate CSV column structure and field types                                                      |
| DI-03 | RTSM Data Parser          | Parse dispensing, randomisations, screen failures, returns                                         |
| DI-04 | ERP Inventory Parser      | Parse stock-on-hand, batches, orders, shipments-in-transit                                         |
| DI-05 | CTMS Plan Parser          | Parse enrollment plan, site activation, visit schedules                                            |
| DI-06 | Supply Network Loader     | Load depots, lanes, lead times, manufacturing sites                                                |
| DI-07 | Policy Loader             | Load safety-stock rules, reorder points, budget envelope, SOPs                                     |
| DI-08 | Reference Document Loader | Load shelf life, label requirements, approved vendors                                              |
| DI-09 | Study Config Loader       | Load protocol parameters, arms, pack sizes, thresholds                                             |
| DI-10 | Data Quality Scorer       | Completeness, accuracy, timeliness scores                                                          |
| DI-11 | Site Inventory Loader     | Load site-level inventory positions and batch details                                              |
| DI-12 | Aggregate Data Query Tool | Compute verified aggregations and integrity checks across all data files — the pre-flight backbone |

### DF — Demand & Forecasting (9)

| ID    | Title                             | Purpose                                               |
| ----- | --------------------------------- | ----------------------------------------------------- |
| DF-01 | Consumption Rate Calculator       | Actual kit consumption by site, country, arm          |
| DF-02 | Enrollment Trajectory Modeller    | Current rate vs plan; projected completion            |
| DF-03 | Demand Delta Calculator           | Delta by country/site/arm/item with significance flag |
| DF-04 | Threshold Evaluator               | Compare deltas to configured thresholds               |
| DF-05 | Scenario Modeller                 | Base / optimistic / pessimistic forecasts             |
| DF-06 | What-If Scenario Engine           | Alternative-parameter demand modelling                |
| DF-07 | Visit & Dispensing Calculator     | Visit and dispensing-driven demand impacts            |
| DF-08 | Screen Failure & Dropout Adjuster | Adjust demand for SF and dropouts                     |
| DF-09 | Demand Baseline Updater           | Update approved baseline when delta accepted          |

### SI — Supply & Inventory (10)

| ID    | Title                      | Purpose                                              |
| ----- | -------------------------- | ---------------------------------------------------- |
| SI-01 | Stock Position Calculator  | Current stock by depot/country/arm/item with WOS     |
| SI-02 | Weeks of Supply Calculator | Weeks of supply at current consumption               |
| SI-03 | Expiry Profile Analyser    | Map batch expiry against projected consumption       |
| SI-04 | Safety Stock Checker       | Flag locations at/below safety-stock threshold       |
| SI-05 | Reorder Trigger Evaluator  | Evaluate reorder triggers against policy             |
| SI-06 | Order Quantity Calculator  | Recommended replenishment quantities                 |
| SI-07 | Supply Gap Identifier      | Where projected demand exceeds available supply      |
| SI-08 | Overage & Waste Estimator  | Project study-end overage and waste                  |
| SI-09 | Supply Plan Scorer         | Score plan on efficiency, risk, cost, complexity     |
| SI-10 | Batch Selection Advisor    | Which batches to ship/use based on expiry & location |

### LT — Logistics & Trade (8)

| ID    | Title                          | Purpose                                             |
| ----- | ------------------------------ | --------------------------------------------------- |
| LT-01 | Lead Time Calculator           | End-to-end lead time per lane                       |
| LT-02 | Shipping Window Planner        | Latest-ship-date vs required-by-date                |
| LT-03 | Cold Chain Requirement Checker | Temperature control requirements vs lane capability |
| LT-04 | Import Requirement Checker     | Country-specific permits and documentation          |
| LT-05 | Approved Vendor Selector       | Courier/broker selection with rationale             |
| LT-06 | Shipping Request Generator     | Structured shipment document ready for execution    |
| LT-07 | In-Transit Tracker             | Status of shipments in flight                       |
| LT-08 | Customs Documentation Checker  | Customs and trade compliance                        |

### CO — Compliance & Regulatory (10)

| ID    | Title                           | Purpose                                               |
| ----- | ------------------------------- | ----------------------------------------------------- |
| CO-01 | Protocol Compliance Checker     | Validate decisions against approved protocol          |
| CO-02 | Label Requirements Validator    | Confirm label requirements met per country            |
| CO-03 | Shelf Life Compliance Checker   | Minimum shelf life for destination                    |
| CO-04 | Expiry Date Rule Enforcer       | Enforce study expiry-dating rules                     |
| CO-05 | Protocol Change Impact Assessor | Full supply-chain impact of amendments                |
| CO-06 | Deviation Impact Assessor       | Supply-chain impact of reported deviations            |
| CO-07 | Destruction Eligibility Checker | What stock is eligible for destruction, why           |
| CO-08 | Audit Trail Logger              | Timestamped log of every agent action (cross-cutting) |
| CO-09 | SOP Reference Checker           | Validate against documented SOPs                      |
| CO-10 | Regulatory Change Alerter       | Flag when reference docs changed since last run       |

### AI — Analytics & Insights (9)

| ID    | Title                         | Purpose                                                   |
| ----- | ----------------------------- | --------------------------------------------------------- |
| AI-01 | Hot Spot Detector             | Find stock-outs, expiry clusters, delays, anomalies       |
| AI-02 | Anomaly Detector              | Statistical anomalies in consumption/enrollment/inventory |
| AI-03 | Risk Scorer                   | Risk scores by site/country/depot with factors            |
| AI-04 | Trend Analyser                | Directional trends over time                              |
| AI-05 | KPI Calculator                | Service level, waste %, on-time delivery, cost/patient    |
| AI-06 | Shortage Probability Modeller | Stock-out probability by site/country within horizon      |
| AI-07 | Budget Variance Analyser      | Actual spend vs budget with variance explanations         |
| AI-08 | Comparator Analysis Engine    | Compare metrics across scenarios                          |
| AI-09 | Waste Root Cause Analyser     | Overage/waste pattern analysis with root causes           |

### RC — Reporting & Communication (10)

| ID    | Title                                | Purpose                                          |
| ----- | ------------------------------------ | ------------------------------------------------ |
| RC-01 | Demand Refresh Summary Writer        | Structured WF-01 output for demand changes       |
| RC-02 | Executive Report Writer              | Monthly high-level report for management/sponsor |
| RC-03 | ClinOps Report Writer                | Detailed operational report for Clinical Ops     |
| RC-04 | Budget Review Report Writer          | Quarterly spend vs budget analysis               |
| RC-05 | Hot Spot Alert Writer                | Structured risk alert with recommended actions   |
| RC-06 | Protocol Change Impact Report Writer | Impact assessment following amendment            |
| RC-07 | Study Start-Up Report Writer         | Baseline report for new study or country         |
| RC-08 | Deviation Report Writer              | Impact and remediation for a reported deviation  |
| RC-09 | Dashboard Data Publisher             | Key metrics formatted for dashboard consumption  |
| RC-10 | Narrative Summariser                 | Plain-English summary of any structured output   |

### SO — Supervision & Orchestration (8)

| ID    | Title                         | Purpose                                                                               |
| ----- | ----------------------------- | ------------------------------------------------------------------------------------- |
| SO-00 | Workflow Pre-Flight Verifier  | **Mandatory step 0 of every workflow** — invokes DI-12 and gates on PASS/WARNING/FAIL |
| SO-01 | Workflow Router               | Route workflows to appropriate agents based on context                                |
| SO-02 | Study Registry Manager        | Study registration and metadata management                                            |
| SO-03 | Inter-Agent Conflict Resolver | Resolve conflicting agent outputs                                                     |
| SO-04 | Workflow Status Tracker       | Progress and status across workflow execution                                         |
| SO-05 | Priority Ranker               | Rank priorities and escalation paths                                                  |
| SO-06 | Exception Handler             | Handle exceptions and errors mid-workflow                                             |
| SO-07 | Run Summary Generator         | Concise end-of-workflow summary                                                       |

**Total: 76 skills.** DI(12) + DF(9) + SI(10) + LT(8) + CO(10) + AI(9) + RC(10) + SO(8).

---

## Part V — Workflows

Five workflows live in [workflows/](workflows/). Each has two representations that serve different audiences:

- **Markdown file** (e.g. `WF-01_demand_signal_refresh.md`) — human-readable design reference: purpose, trigger, agents, phases, outputs. Not executed.
- **[workflows/workflows.json](workflows/workflows.json)** — machine-readable runtime definition. This is what the Python runner (and the `/run-workflow` command) actually reads. It contains:
  - `routing_signals` — the whitelist of control tokens agents may emit
  - `workflows.{WF-ID}.steps[]` — ordered array of `{ agent, task, condition? }` objects
  - `condition.requires_signal` — gate that skips a step unless a prior step emitted the named signal

### The Five Workflows

| ID        | Name                      | Trigger                                                                        | Primary Agents                                                                                                          | Typical Output                                                                 |
| --------- | ------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **WF-01** | Demand Signal Refresh     | New data drop arrives                                                          | Supervisor → Demand Analyst → Reporting                                                                                 | Demand Refresh Summary; emits SIGNIFICANT_DELTA or MINOR_DELTA                 |
| **WF-02** | Supply Plan Generation    | After WF-01 with SIGNIFICANT_DELTA, or ad hoc (new inventory, protocol change) | Supervisor → Supply Analyst → Logistics Specialist → Compliance Manager → Reporting                                     | Draft supply plan with order qtys and shipment routing                         |
| **WF-03** | Protocol Amendment Impact | Protocol amendment received                                                    | Supervisor → Compliance Manager → Demand Analyst → Supply Analyst → Reporting                                           | Impact assessment; may emit DEMAND_CHANGE / INVENTORY_CHANGE / MATERIAL_CHANGE |
| **WF-04** | Routine Monitoring        | Scheduled (daily/weekly) or ad-hoc risk check                                  | Supervisor → Supply Analyst → Logistics Specialist → Demand Analyst → Insights Analyst → Compliance Manager → Reporting | Hot-spot alert digest; emits CRITICAL_HOTSPOT when applicable                  |
| **WF-05** | Supply Plan Execution     | Human approval of a plan from WF-02                                            | Supervisor → Supply Analyst → Compliance Manager → Logistics Specialist → Reporting                                     | Shipping requests, final compliance sign-off; emits NON_COMPLIANT on failure   |

### Routing Signals

Defined once in `workflows.json` under `routing_signals`. Agents include these tokens in their output text; the runner scans for them via whole-word regex and uses them to gate later steps or halt the workflow.

| Signal              | Meaning                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| `SIGNIFICANT_DELTA` | Demand delta meets/exceeds configured threshold — run scenario analysis, consider triggering WF-02 |
| `MINOR_DELTA`       | Below threshold — acknowledge but don't replan                                                     |
| `HALT`              | Stop the workflow immediately (validation failure, data integrity fail)                            |
| `DEMAND_CHANGE`     | Amendment affects demand — recalculate                                                             |
| `INVENTORY_CHANGE`  | Amendment affects inventory — recheck stock                                                        |
| `CRITICAL_HOTSPOT`  | Risk severe enough to escalate                                                                     |
| `MATERIAL_CHANGE`   | Amendment materially changes the study package                                                     |
| `NON_COMPLIANT`     | Compliance gate failed — cannot proceed to execution                                               |

### Chaining

- WF-01 → WF-02 (automatic if SIGNIFICANT_DELTA)
- WF-02 → WF-05 (manual, after human approval)
- WF-03 → WF-02 (if amendment impact confirmed)
- WF-04 runs independently and can trigger ad-hoc follow-ups

---

## Part VI — The Study Package

Every study is a self-contained folder under [studies/](studies/) with four subfolders. Framework code does not change between studies; only the contents of this package do. This is what "portable" means in practice.

```
studies/{study_id}/
├── config/
│   ├── study_config.json          Identity, arms, items, sites, thresholds, schemas
│   ├── supply_network.json        Depots, manufacturing sites, lanes, lead times
│   └── policies.json              Safety stock, reorder rules, budget, expiry, SOPs
├── reference/
│   ├── shelf_life_by_country.json Minimum remaining shelf life at ship time, per country
│   ├── approved_vendors.json      Couriers, brokers, CMOs with approved lanes & capabilities
│   ├── label_requirements.json    Languages, required content, format per country
│   └── reorder_policies.json      Reorder-point parameters (review period, service level, MOQ)
├── data_drops/
│   └── {YYYY-MM-DD}/              One folder per data drop
│       ├── rtsm_actuals.csv       Patient-level supply events
│       ├── erp_inventory.csv      Stock movements, shipments, production orders
│       ├── ctms_plan.csv          Enrollment plan and visit schedule
│       └── site_inventory.csv     Clinical site on-hand snapshot
└── outputs/
    └── {YYYY-MM-DD}/              Written by the runner, one folder per data drop
        ├── {WF-ID}_{timestamp}_run_summary.md
        ├── {WF-ID}_{timestamp}_outputs.json
        └── {WF-ID}_{timestamp}_audit_log.json
```

### config/ — set once, edit rarely

- **study_config.json** is the **single source of truth** for the study. It contains: `study_identity` (study_id, protocol_number, phase, sponsor), `treatment_arms`, `randomisation_ratio`, `items` (pack size, units per pack, temperature requirement), `thresholds.demand_delta_significance_pct` (default 10%), `countries`, `sites`, `required_files` (the manifest DI-01 checks), `schemas` (column types and date formats for every CSV), and `assumptions` (screen failure rate, dropout rate, review period). The runner enforces that `protocol_number` matches the `--study` argument — a mismatch aborts the run.
- **supply_network.json** describes the physical world: `depots`, `manufacturing_sites`, `shipping_lanes` (origin/destination/lead_time_days/lane_type), and `country_depot_assignments`.
- **policies.json** encodes business rules: `safety_stock.default_minimum_weeks`, `reorder_rules` (reorder_point_weeks, MOQ), `maximum_stock_levels`, `budget.budget_envelope`, `expiry_rules.minimum_remaining_shelf_life_months`, `destruction_eligibility`, `sop_references`.

### reference/ — regulatory and vendor truth

Slow-changing reference files. When they change, CO-10 (Regulatory Change Alerter) flags the drift at the next run. Vendor selection (LT-05), label compliance (CO-02), and shelf-life gates (CO-03) all consult these files.

### data_drops/{date}/ — the input

Each subfolder name is a date (`YYYY-MM-DD`). Four CSV files per drop:

| File                 | Key columns                                                                                                                                             | Represents                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `rtsm_actuals.csv`   | site_id, country_code, event_type (screen_failure / randomisation / dispensing / return), item_id, arm_id, event_date, quantity, patient_id, lot_number | Patient-level supply events from RTSM |
| `erp_inventory.csv`  | item_id, location, record_type (stock_on_hand / production_order / shipment_in_transit), quantity, lot_number, expiry_date, origin, destination, status | Physical stock and movements          |
| `ctms_plan.csv`      | site_id, country_code, record_type, record_date, planned_enrollment, actual_enrollment, site_status, visit_type, visit_window_days                      | Enrollment plan and visit schedule    |
| `site_inventory.csv` | Site, item_id, On_Hand_Qty, Weekly_Demand, Min_Reorder_Point, Max_Reorder_Point                                                                         | Clinical site on-hand snapshot        |

### outputs/{date}/ — the result

Every workflow run writes three files, prefixed with the workflow ID and a run timestamp:

| File              | Purpose                                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------ |
| `_run_summary.md` | Human-readable executive summary (last reporting agent's output)                                                   |
| `_outputs.json`   | Structured array of every agent's full output text, in order                                                       |
| `_audit_log.json` | GxP audit trail — timestamp per step, agent, status (completed / skipped / halted), detected signals, error detail |

### File Formats — Config and Reference

Every JSON file in `config/` and `reference/` follows a fixed shape. The schemas below are the canonical reference. **Working examples** of every file are in the sample study [studies/999999/](studies/999999/). **Blank scaffolds** with `TODO` placeholders are in [studies/templates/](studies/templates/) — copy these (via `/init-study`) rather than authoring from scratch.

#### `config/study_config.json`

The single source of truth for study identity, trial design, file manifest, and CSV schemas. The runner enforces that `study_identity.protocol_number` matches the `--study` argument at launch.

```json
{
  "study_identity": {
    "study_id": "string",
    "study_name": "string",
    "protocol_number": "string",
    "phase": "Phase 1 | Phase 2 | Phase 3 | Phase 4",
    "sponsor": "string"
  },
  "treatment_arms": [
    { "arm_id": "string", "arm_name": "string", "description": "string" }
  ],
  "randomisation_ratio": "1:1 | 2:1 | …",
  "items": [
    {
      "item_id": "string",
      "item_name": "string",
      "arm": "arm_id",
      "pack_size": 1,
      "units_per_pack": 28,
      "temperature_requirement": "ambient | cold_chain | frozen",
      "description": "string"
    }
  ],
  "thresholds": {
    "demand_delta_significance_pct": 10,
    "overrides": []
  },
  "countries": [
    { "country_code": "ISO-2", "country_name": "string" }
  ],
  "sites": [
    { "site_id": "string", "site_name": "string", "country_code": "ISO-2" }
  ],
  "required_files": {
    "files": [
      {
        "file_name": "rtsm_actuals.csv",
        "location": "data_drops/{data_drop_date}/",
        "criticality": "critical | optional"
      }
    ]
  },
  "schemas": {
    "rtsm_actuals":  { "required_columns": [], "optional_columns": [], "column_types": {} },
    "erp_inventory": { "required_columns": [], "optional_columns": [], "column_types": {} },
    "ctms_plan":     { "required_columns": [], "optional_columns": [], "column_types": {} }
  },
  "assumptions": {
    "screen_failure_rate_pct": 16,
    "dropout_rate_pct": 10,
    "review_period_weeks": 4
  }
}
```

`column_types` values are one of `text | number | date`. DI-02 (Schema Validator) uses this block to validate every incoming CSV.

#### `config/supply_network.json`

The physical world: depots, manufacturing sites, shipping lanes, and the mapping from each country to its serving depot.

```json
{
  "depots": [
    {
      "depot_id": "string",
      "depot_name": "string",
      "country": "ISO-2",
      "capabilities": ["ambient", "cold_chain", "frozen", "controlled_substance"],
      "description": "string"
    }
  ],
  "manufacturing_sites": [
    {
      "site_id": "string",
      "site_name": "string",
      "country": "ISO-2",
      "produces": ["item_id", "item_id"],
      "description": "string"
    }
  ],
  "shipping_lanes": [
    {
      "lane_id": "string",
      "origin": "depot_id | mfg_site_id",
      "destination": "depot_id | site_id",
      "lead_time_days": 5,
      "lane_type": "air | road | sea",
      "description": "string"
    }
  ],
  "country_depot_assignments": [
    { "country_code": "ISO-2", "depot_id": "depot_id" }
  ]
}
```

#### `config/policies.json`

Business rules for safety stock, reorder behaviour, stock ceilings, budget envelope, and expiry.

```json
{
  "safety_stock": {
    "default_minimum_weeks": 2,
    "overrides": []
  },
  "reorder_rules": {
    "reorder_point_weeks": 4,
    "minimum_order_quantity": 4,
    "maximum_order_quantity": 5
  },
  "maximum_stock_levels": {
    "default_maximum_weeks": 9,
    "overrides": []
  },
  "budget": {
    "budget_envelope": 2500000,
    "currency": "USD | EUR | GBP | …"
  },
  "expiry_rules": {
    "minimum_remaining_shelf_life_months": 6,
    "destruction_eligibility": {
      "expired_stock": true,
      "study_closed_stock": true,
      "recalled_stock": false,
      "damaged_stock": true
    }
  },
  "sop_references": []
}
```

`overrides[]` entries in `safety_stock` and `maximum_stock_levels` accept per-country or per-item objects; leave empty to use the default.

#### `reference/shelf_life_by_country.json`

Minimum remaining shelf life required at shipment time, per destination country. Consulted by CO-03 (Shelf Life Compliance Checker).

```json
{
  "_instructions": "Define minimum remaining shelf life (months) required at shipment time per destination country.",
  "countries": [
    {
      "country_code": "ISO-2",
      "country_name": "string",
      "minimum_remaining_shelf_life_months": "18",
      "item_overrides": [
        { "item_id": "string", "minimum_remaining_shelf_life_months": "12" }
      ]
    }
  ]
}
```

#### `reference/approved_vendors.json`

Couriers, brokers, and CMOs approved for the study. Each vendor lists the `lane_id`s (from `supply_network.json`) it is approved to service. Used by LT-05 (Approved Vendor Selector).

```json
{
  "_instructions": "List couriers, brokers, and CMOs approved for use. Each must link to lane IDs in supply_network.json.",
  "vendors": [
    {
      "vendor_id": "string",
      "vendor_name": "string",
      "vendor_type": "Courier | Broker | CMO",
      "approved_lanes": ["lane_id"],
      "capabilities": ["ambient", "cold_chain", "controlled_substance", "customs_clearance"],
      "contact_info": "string"
    }
  ]
}
```

#### `reference/label_requirements.json`

Label language, content, and format requirements per country. Used by CO-02 (Label Requirements Validator).

```json
{
  "_instructions": "Define label language, content, and format requirements for each country.",
  "countries": [
    {
      "country_code": "ISO-2",
      "country_name": "string",
      "required_languages": ["English", "French", "…"],
      "required_content": [
        "study_number",
        "item_description",
        "storage_conditions",
        "sponsor_name",
        "lot_number",
        "expiry_date",
        "caution_statement"
      ],
      "format_notes": "string — regulator-specific guidance"
    }
  ]
}
```

#### `reference/reorder_policies.json`

Reorder-point parameters per site/item, with a default policy and optional overrides. Used by SI-05 / SI-06 and [runner/reorder_calculator.py](runner/reorder_calculator.py).

```json
{
  "_instructions": "Default policy applies unless overridden. Site and item overrides allow fine-grained control.",
  "_math_reference": "s = NORM.INV(CSL, mean_LT, sqrt(mean_LT)); S = MAX(NORM.INV(CSL, mean_LT+review, sqrt(...)), s + MOQ)",
  "default_policy": {
    "review_period_days": 7,
    "cycle_service_level": 0.95,
    "moq": 1,
    "pack_multiple": 1,
    "description": "string"
  },
  "site_policies": [
    {
      "site_id": "string",
      "site_name": "string",
      "review_period_days": "3",
      "cycle_service_level": ".90",
      "moq": "1",
      "pack_multiple": 1,
      "description": "string"
    }
  ],
  "item_overrides": [],
  "parameter_definitions": {
    "review_period_days": "Days between stock reviews.",
    "cycle_service_level": "Target probability of meeting demand without stockout (0.70–0.99).",
    "moq": "Minimum Order Quantity.",
    "pack_multiple": "Packaging multiplier (reserved for future use).",
    "lead_time_days": "Sourced from supply_network.json shipping_lanes."
  }
}
```

> **Where to find examples:** Every file above has a fully populated working copy in [studies/999999/](studies/999999/) (the sample study) and a blank `TODO`-marked scaffold in [studies/templates/](studies/templates/). Use `/init-study <STUDY_ID>` to copy the scaffolds into a new study folder rather than authoring from scratch.

---

## Part VII — Templates and Study Initialisation

[studies/templates/](studies/templates/) is the blueprint for new studies. It mirrors the per-study structure but every editable field contains a `TODO:` marker. **Templates are never edited directly** — they are the reference copy.

### Template contents

- `config/study_config.json` — study identity, arms, items, thresholds, schemas with `TODO` placeholders
- `config/supply_network.json` — depots/lanes/manufacturing scaffolding
- `config/policies.json` — safety stock, reorder rules, budget, expiry defaults
- `reference/shelf_life_by_country.json` — country-keyed shelf-life requirements
- `reference/approved_vendors.json` — vendor registry scaffold
- `reference/label_requirements.json` — labelling compliance scaffold
- `reference/reorder_policies.json` — reorder-point parameter scaffold
- `README.md` — template usage rules and the TODO workflow

### The `/init-study` lifecycle

1. Run `/init-study <STUDY_ID>` in the Claude Code chat.
2. The command copies the template tree into `studies/{STUDY_ID}/`.
3. `__STUDY_ID__` placeholders are substituted automatically.
4. The human fills in the remaining `TODO:` fields (items, sites, thresholds, vendors, shelf life).
5. The study is now ready to receive a data drop in `data_drops/{date}/`.
6. Run `/preflight <STUDY_ID>` to validate before invoking a full workflow.

---

## Part VIII — The StudyDataCreation HTML Tool

Location: [StudyDataCreation/](StudyDataCreation/). Self-contained, browser-only, no server required.

| File                    | Purpose                                                                                                                      |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `index.html`            | Step-by-step wizard for generating synthetic study data. Produces all four data-drop CSVs plus a seeded `study_config.json`. |
| `data_drop_viewer.html` | Inspection UI — load generated CSVs, view as sortable/searchable tables, validate before running Hermes.                     |
| `readme.txt`            | User instructions.                                                                                                           |

### How a user flows through it

1. Open `index.html` in any browser (no install, no server).
2. Define study metadata — study ID, protocol number, sponsor, phase.
3. Configure items and treatment arms (pack sizes, randomisation ratio).
4. Add sites and countries.
5. Simulate enrollment — screen-failure rate, dropout rate, randomisation events over time.
6. Simulate supply events — dispensings, returns, lot definitions, expiry profiles.
7. Configure logistics — depots, manufacturing origins, lead times.
8. Download the generated CSVs.
9. Save them to `studies/{study_id}/data_drops/{YYYY-MM-DD}/`.
10. Open `data_drop_viewer.html` to spot-check the generated files before running `/preflight`.

The tool exists because hand-crafting plausible RTSM/ERP/CTMS datasets in spreadsheets is error-prone and slow. It gives instructors, labs, and new-study owners a realistic package in minutes.

---

## Part IX — The Lab (Training Kit)

[lab/](lab/) is a complete 3-hour hands-on workshop where non-technical learners build their own Hermes agent from scratch. It is not used at runtime — it is a pedagogical artefact.

### What students build vs. receive

| Students BUILD                                                             | Students RECEIVE pre-loaded                          |
| -------------------------------------------------------------------------- | ---------------------------------------------------- |
| `study_config.json`, `supply_network.json`, `policies.json` for a scenario | All 76 skill definitions                             |
| One new skill definition (e.g. OA-01 Excess Inventory Detector)            | All 7 production agent system prompts (as reference) |
| One new agent system prompt (Optimization Agent)                           | Python runner + `/run-workflow` command              |
| One new workflow (WF-LAB-01) in workflows.json                             | Sample data drop                                     |

### Structure

```
lab/
├── README.md                         Instructor guide (prep, timing, troubleshooting)
├── instructor/
│   ├── scenario_cards.md             10 fictional study scenarios, one per student
│   ├── hermes_intro_presentation.html Optional slides
│   └── Answers/
│       ├── optimization_agent/       Reference README.md + system_prompt.md
│       ├── skills/                   Reference OA-01 … OA-05
│       └── workflows/                Reference WF-OA-01 + workflows.json
├── student/
│   ├── student_guide.md              7 modules, 20 pages
│   ├── optimization_agent_brief.md   Spec for the agent to build
│   └── references.md                 Glossary and links
└── templates/
    ├── study_config.template.json
    ├── supply_network.template.json
    ├── policies.template.json
    ├── skill_template.md             Blank skill scaffold
    ├── demand_analyst_system_prompt.template.md
    └── workflows.template.json       WF-01 intact + blank WF-LAB-01
```

### The seven modules

| Module | Duration | Focus                                                                                         |
| ------ | -------- | --------------------------------------------------------------------------------------------- |
| M0     | 15 min   | Setup — unzip kit, open VS Code, configure `.env`, smoke-test Claude Code                     |
| M1     | 20 min   | Architecture orientation — the five layers (runner, workflows, agents, skills, study package) |
| M2     | 40 min   | Config files — fill in the three JSON files from the scenario card                            |
| M3     | 15 min   | Skill writing — write one skill definition against the template                               |
| M4     | 30 min   | System prompt — write the Optimization Agent's system prompt                                  |
| M5     | 15 min   | Workflow — add WF-LAB-01 to workflows.json                                                    |
| M6     | 20 min   | Run & review — execute `/run-workflow WF-LAB-01 STUDY-LAB-XX`, debug                          |
| M7     | 10 min   | Discussion — meta-reflection on agent design                                                  |

---

## Part X — Two Ways to Run Hermes

Hermes has two execution paths. They share everything below the surface — the same agents, skills, workflows, and study packages — but they differ in how steps are orchestrated, how context is passed, and how outputs are logged.

### Chat mode: `/run-workflow`

You invoke the command in Claude Code. Claude itself plays the role of the runner: it reads `workflows.json`, loads each agent's system prompt, and executes the steps in conversation. Context flows naturally through conversation history. There is no streaming mode distinct from chat output, and no enforced pre-flight — the supervisor agent's first step _asks_ DI-12 to run.

### CLI mode: `python runner/runner.py`

You invoke the Python runner (directly or via [run.bat](run.bat) / [run.sh](run.sh)). It makes explicit Claude API calls per step, passes prior outputs as explicit context, streams responses to stdout, runs DI-12 as a forced step-0 gate, and writes structured JSON audit logs to disk.

### Side-by-side

| Aspect             | `/run-workflow` (chat)                         | `runner.py` (CLI)                                                             |
| ------------------ | ---------------------------------------------- | ----------------------------------------------------------------------------- |
| Entry point        | Claude Code chat                               | Terminal                                                                      |
| Context passing    | Conversation history (implicit)                | Explicit user-message construction                                            |
| Streaming          | No distinct stream — chat output               | Real-time to stdout via `messages.stream()`                                   |
| DI-12 validation   | Inline when the supervisor asks for it         | Forced pre-flight at step 0, PASS/WARNING/FAIL gate                           |
| Signal detection   | Claude reads prior text and reasons            | Regex whole-word match on each agent's output                                 |
| Conditional steps  | Handled by Claude's judgement                  | Framework logic: `condition.requires_signal` checked against `active_signals` |
| HALT behaviour     | Claude stops when asked                        | Framework hard-stops, no further API calls                                    |
| Audit trail        | Conversation log (lossy)                       | `_audit_log.json` with ISO-8601 timestamps                                    |
| Output persistence | Optional, on user request                      | Mandatory three-file write                                                    |
| Best for           | Exploration, demos, lab sessions, quick triage | Production, automation, scheduled runs, auditable evidence                    |

The prompt layer doesn't care which one runs it — the system prompts are identical in both paths.

---

## Part XI — Python in Depth

This is the section the project owner asked for explicitly. Hermes is marketed (accurately) as zero-code: all agent intelligence is Markdown. So why is there Python at all?

### 1. Why Python is here

Because _something_ has to call the Claude API, feed each agent the right system prompt, carry the previous step's output forward as context, scan responses for routing signals, enforce conditional gates, halt on failure, and write auditable output files to disk. That's plumbing — and the plumbing is the runner. The runner contains **no business logic**. It knows nothing about demand, supply, compliance, or reporting. It knows how to sequence agent turns and honour the grammar of `workflows.json`. Every decision that matters clinically or commercially lives in a Markdown file under [agents/](agents/) or [skills/](skills/).

Python is also needed one you need to be absolutely sure that the AI is using deterministic methods to process data. Functions as simple as counting records or summing values across large data sets are almost ALWAYS better performed with a python script. Using code will dramatically increase performance. Python code will never halucinate.

### 2. The runner module — [runner/runner.py](runner/runner.py)

A single ~560-line Python file that does the following, in order:

**Initialisation**

- Loads `.env` (via `python-dotenv` if present) so `ANTHROPIC_API_KEY` is available
- Loads [runner/runner_config.json](runner/runner_config.json) for model name, paths, and token limits
- Resolves project-relative paths to `agents/`, `workflows/workflows.json`, and `studies/{study_id}/`
- CLI: `python runner/runner.py --workflow WF-01 --study PULSE-01 [--data-drop 2026-03-15]`

**`load_workflows()`**

- Reads [workflows/workflows.json](workflows/workflows.json)
- Validates presence of `workflows` and `routing_signals` sections
- Validates each step has `agent` and `task` fields
- Exits with a helpful message on malformed JSON

**`validate_study_package()`**

- Verifies `studies/{study_id}/config/` contains `study_config.json`, `supply_network.json`, `policies.json`
- Opens `study_config.json` and confirms `protocol_number` matches the `--study` argument (a cross-study safety check)
- If `--data-drop` is not supplied, finds the latest `YYYY-MM-DD` folder in `data_drops/`
- Confirms `rtsm_actuals.csv`, `erp_inventory.csv`, `ctms_plan.csv` exist in that folder
- Returns a context dict with all resolved paths and the study's metadata

**Step 0 — pre-flight (hard-coded before any workflow step)**

- Imports and runs [runner/di_12_aggregate_data_query.py](runner/di_12_aggregate_data_query.py) directly
- Computes aggregations and integrity checks (see §4 below)
- Reads `overall_data_integrity` from the DI-12 result:
  - `FAIL` → halt immediately, log the error, write the audit log, exit
  - `WARNING` → continue with a caution flag embedded in accumulated outputs
  - `PASS` → continue
- DI-12's result becomes the first entry in `accumulated_outputs` so every downstream agent can reference verified numbers

**Step loop (steps 1..N)**

For each step in `workflows.{WF-ID}.steps`:

1. **Condition check.** If the step has `"condition": { "requires_signal": "X" }` and `X` is not in `active_signals`, skip it and log the skip.
2. **Load agent prompt.** Read `agents/{step.agent}/system_prompt.md` as the system message.
3. **Build user message.** Inline: workflow context (workflow_id, study_id, data_drop_date, trigger), absolute paths to every study-package file, the `task` text from the workflow step, and the full concatenated text of every previous step's output.
4. **Call the API.** `client.messages.stream(model, max_tokens, system, messages)` — streams the response to the terminal in real time.
5. **Capture output.** Append the full response text to `accumulated_outputs`.
6. **Detect signals.** Scan the response with a case-insensitive whole-word regex against each token in `routing_signals`. Add any matches to `active_signals`.
7. **Check for HALT.** If `HALT` is in `active_signals`, stop the loop — no further steps, no further API calls.

**`write_outputs()`**

- Creates `studies/{study_id}/outputs/{data_drop_date}/` if missing
- Writes three files with prefix `{WF-ID}_{run_timestamp}`:
  - `_run_summary.md` — text of the final agent's output (typically Reporting Agent)
  - `_outputs.json` — ordered array of every agent's full output, with step index and agent name
  - `_audit_log.json` — step-by-step log: start/end timestamps, status (`completed` / `skipped` / `halted` / `error`), signals detected, any error detail

### 3. [runner/runner_config.json](runner/runner_config.json)

```json
{
  "model": "claude-opus-4-6",
  "api_key_env": "ANTHROPIC_API_KEY",
  "agents_path": "agents",
  "workflows_path": "workflows",
  "max_tokens": 8192
}
```

Five fields, all self-explanatory. Change `model` to upgrade the engine; change `max_tokens` to raise/lower the per-step output budget.

### 4. [runner/di_12_aggregate_data_query.py](runner/di_12_aggregate_data_query.py)

DI-12 is the only skill that has a Python implementation _in addition to_ its Markdown definition. That is deliberate: the numbers this skill produces (patient counts, dispensing totals, batch quantities, expiry profiles) must be exact and reproducible, and arithmetic is the one thing you do not want an LLM improvising. The Python module parses the four CSVs, rolls up aggregations, and returns a structured report the supervisor can trust.

**Outputs:**

- `rtsm_aggregations` — counts by event type, site, arm, item
- `ctms_aggregations` — planned vs actual enrollment
- `erp_aggregations` — stock levels, in-transit, production orders, batch expiry profiles
- `site_inventory_aggregations` — on-hand vs weekly demand vs reorder thresholds
- `derived_metrics` — enrollment delta, demand rate, supply coverage
- `data_integrity_checks` — 8 cross-file validations (patient-ID uniqueness, site consistency, item consistency, arm consistency, randomisation-vs-dispensing balance, screen-failure rates, date consistency, expiry validation)
- `overall_data_integrity` — `PASS` | `WARNING` | `FAIL`
- `recommendations` — array of `{ severity, issue, action }` objects

### 5. [runner/reorder_calculator.py](runner/reorder_calculator.py)

Companion utility used by SI-05/SI-06 when precise reorder points are required. Computes minimum and maximum reorder quantities under a Poisson-approximated Normal distribution for a given review period, demand rate, service level, and MOQ. Same rationale as DI-12: arithmetic must be exact, so it lives in Python.

> This is a classic example of why python would be used. Its a deterministic application when needed.

### 6. [run.bat](run.bat) and [run.sh](run.sh)

Convenience wrappers at the project root. Both display a numbered menu of the five workflows, prompt for `study_id` and optional `data_drop` date, load `ANTHROPIC_API_KEY` from `.env`, and call `python runner/runner.py` with the assembled arguments. They exist for operators who do not want to remember the CLI syntax.

### 7. The signal protocol

Signals are the only way Python control flow interacts with LLM output. They are:

| Signal              | Trigger                         | Consequence                       |
| ------------------- | ------------------------------- | --------------------------------- |
| `SIGNIFICANT_DELTA` | Demand delta ≥ threshold        | Enables downstream scenario steps |
| `MINOR_DELTA`       | Demand delta < threshold        | Acknowledges without replanning   |
| `HALT`              | Validation or integrity failure | Hard-stops the workflow           |
| `DEMAND_CHANGE`     | Amendment affects demand        | Enables demand-recalc step        |
| `INVENTORY_CHANGE`  | Amendment affects inventory     | Enables stock-recheck step        |
| `CRITICAL_HOTSPOT`  | Severe risk detected            | Escalates to alert-writing step   |
| `MATERIAL_CHANGE`   | Material amendment              | Gates protocol-impact steps       |
| `NON_COMPLIANT`     | Compliance gate failed          | Blocks execution step             |

The runner's regex check is deliberately strict — whole-word, case-insensitive. Agents must emit these tokens _verbatim_ for the runner to react. This makes the control protocol auditable: search the audit log for a signal and you can always find the step that emitted it.

### 8. What Python does NOT do

- **No demand logic.** Consumption rates, trajectories, deltas — all computed by Claude following skill instructions.
- **No supply logic.** Safety stock, reorder points, order quantities — all computed by Claude.
- **No compliance logic.** Protocol checks, shelf-life checks, label checks — all computed by Claude.
- **No reporting logic.** Every narrative, summary, table is generated by Claude.

Python sequences the turns and writes the logs. Markdown thinks.

---

## Part XII — Environment and Settings

| File                                                       | Role                                                                                                                        |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [.env.example](.env.example)                               | Template for `.env`. Copy to `.env`, paste an `ANTHROPIC_API_KEY`. `.env` is gitignored.                                    |
| `.env`                                                     | Not committed. Contains the actual API key. Read by the runner at startup.                                                  |
| [.claude/settings.json](.claude/settings.json)             | Minimal Claude Code settings — enabled plugins only.                                                                        |
| [.claude/settings.local.json](.claude/settings.local.json) | Local permissions allow-list (grants for git, Read, Python execution of DI-12, etc.). Not shared.                           |
| [CLAUDE.md](CLAUDE.md)                                     | Auto-loaded by Claude Code at session start — project overview, structure, design principles, agent team, file conventions. |

---

## Part XIII — Glossary and Cross-Reference Index

### Agents

- [compliance_manager](agents/compliance_manager/) — cross-cutting GxP guardrail
- [demand_analyst](agents/demand_analyst/) — consumption, enrollment, scenarios
- [insights_analyst](agents/insights_analyst/) — hot spots, anomalies, KPIs
- [logistics_specialist](agents/logistics_specialist/) — shipping, cold chain, customs
- [reporting_agent](agents/reporting_agent/) — stakeholder reports
- [supervisor](agents/supervisor/) — orchestration and routing
- [supply_analyst](agents/supply_analyst/) — stock, safety stock, reorder

### Workflows

- [WF-01 Demand Signal Refresh](workflows/) — weekly data ingestion and demand recalculation
- [WF-02 Supply Plan Generation](workflows/) — stock and shipment planning
- [WF-03 Protocol Amendment Impact](workflows/) — amendment impact assessment
- [WF-04 Routine Monitoring](workflows/) — continuous risk scanning
- [WF-05 Supply Plan Execution](workflows/) — approved-plan execution

### Signals

`SIGNIFICANT_DELTA`, `MINOR_DELTA`, `HALT`, `DEMAND_CHANGE`, `INVENTORY_CHANGE`, `CRITICAL_HOTSPOT`, `MATERIAL_CHANGE`, `NON_COMPLIANT` — all defined in [workflows/workflows.json](workflows/workflows.json).

### Commands

- [/init-study](.claude/commands/init-study.md)
- [/preflight](.claude/commands/preflight.md)
- [/run-workflow](.claude/commands/run-workflow.md)
- [/run-workflow-chain](.claude/commands/run-workflow-chain.md)

### Key config and data files (per study)

- `studies/{id}/config/study_config.json` — single source of truth
- `studies/{id}/config/supply_network.json` — physical network
- `studies/{id}/config/policies.json` — business rules
- `studies/{id}/reference/*.json` — regulatory and vendor reference
- `studies/{id}/data_drops/{date}/*.csv` — input data
- `studies/{id}/outputs/{date}/*` — workflow outputs

### Skills — all 76

See [Part IV](#part-iv--the-skills-library) for the category-by-category tables. Skill files: [skills/](skills/).

---

_End of Grimoire._
