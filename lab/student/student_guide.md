# Hermes Lab — Student Guide

**Duration:** 3 hours | **Format:** Individual hands-on build

> Note: At any time you can put this file into preview mode by right clicking the file and selecting `Open Preview`

> **How to read this guide:** `> Tip` = optional shortcut · `> Note` = background · **Checkpoint** = you must be able to do this before moving on. Unfamiliar term? `Hermes_Grimoire.md` in the project root is the canonical reference.

---

### What Hermes Is

Hermes is a **Clinical Supply Chain AI Agent Team** built for pharmaceutical trial supply management. Seven specialised agents collaborate — autonomously where possible, with humans at review points — to ingest operational data, analyse demand, plan supply, monitor risk, enforce compliance, and report out. The intelligence of every agent and every skill is expressed in plain Markdown, not code. A thin Python runner calls the Claude API to execute those prompts in ordered workflows and write auditable outputs. The framework is **system-agnostic** (it reads CSV/JSON data drops rather than talking to ERP/RTSM systems directly) and **portable** (the same study package structure works for any protocol).

> Disclaimer: Hermes is provided solely as an educational and exploratory tool to demonstrate potential AI use cases within clinical supply chain processes. It is not a validated system and must not be used to support decision-making in regulated clinical trial activities, including but not limited to patient safety, drug supply, or compliance-related functions.

> No warranty, express or implied, is provided. Hermes is used entirely at the user’s own risk.

---

## What You Are Building

By the end of this lab you will have built the **Optimization Agent** — a new member of the Hermes Clinical Supply Chain AI Agent Team.

You will configure a study, and then build skills, an agent, and a workflow definition to analyze the supply chain for your study. You will do this entirely in plain English (Markdown). No coding required.

**You will build:**

- 3+ skill definitions (the building blocks of agent capability)
- One complete agent (README + system prompt)
- One workflow definition

**You will be given (pre-loaded in your starter kit):**

- The full skills library (reference only)
- All existing agent system prompts (as reference examples)
- The Python runner code (black box — no coding needed)
- Sample clinical data files
- An agent brief handout that describes what your agent should do
- the Grimoire - an encyclopedia that explains all aspects of Hermes

---

## Pre-requisites

1. Visual Code
2. Extension: Claude Code for VS Code

#### (Optional)

3. Extension: Live Server

## Module 0 · Setup (15 minutes)

### Step 1: Download the Starter Kit

Download `hermes-lab.zip` from the link your instructor provides.
Extract it to a folder on your computer (e.g. `c:/hermes-lab`).

#### The full project is available any time on github here:

https://github.com/Crasorus/Hermes-Student

### Step 2: Open in VS Code

1. Open VS Code
2. Go to **File → Open Folder**
3. Select the `hermes-lab` folder you extracted

### Step 3: Test Claude Code

> TIP: let's use the Haiku model. Hermes tends to run faster (and cheaper) with this model. Click on Show Commands `[/]` (square box with slash). Select `switch model`. Choose `Haiku`.
>
> Note: your instructor should have pre-configured your Anthropic API key. If Claude Code reports "API key not found", ask them to check the `.env` file.

1. Open the Claude Code panel in VS Code (look for the Claude icon in the sidebar, or press `Ctrl+Shift+P` and type "Claude")
2. Type: `What is Hermes?`
3. You should get a response explaining the project. If you do — you are ready!

#### Tips

- Pin the Claude Code panel and open this guide in preview mode side-by-side — you will flip between them constantly.
- Haiku for speed, Sonnet when you want stronger design suggestions. Switch any time with `/model`.
- If Claude Code feels sluggish, confirm you are not accidentally on Opus — slower and pricier for this kind of work.
- Keep one "reference file" open at all times (a skill, an agent, or the Grimoire). Never work from memory.

---

## Module 1 · Architecture Orientation (20 minutes)

Before building anything, take ~20 minutes to get oriented with what is already in the starter kit. The goal here is not to memorise anything — it is to know where things live so that when you build your own agent, the surrounding landscape makes sense.

### The 5 Layers of Hermes

```
Layer 5: RUNNER / COMMANDS — executes workflows (commands and Python code)
Layer 4: WORKFLOWS         — defines which agents run, in what order
Layer 3: AGENTS            — AI specialists, each with their own instructions
Layer 2: SKILLS            — atomic capabilities agents can apply
Layer 1: STUDY PACKAGE     — your study's config + CSV data
```

> **Note — What Version of Hermes Are You Building?**
>
> The version you are building today is a **prompt-only framework**. Every agent and skill is a Markdown file containing structured English instructions. There is no custom code in the agents or skills themselves. We will not use The Python code today. But it is there for you to explore later on your own. The Grimoire fully explains the python extensions available to Hermes.
>
> This is a deliberate design choice: it keeps the system accessible to non-technical users and easy to inspect, modify, and understand.
>
> A **production implementation** of Hermes would go one step further — using Anthropic's **Agent SDK** to give each agent its own autonomous runtime. Agents would call each other directly, spawn sub-tasks, and run end-to-end without a human in the loop between steps. Importantly, you could connect them directly to your data sources via an MCP server or other technique (thus avoiding data drops). The Markdown files you write today would become the system prompts fed into those agent instances.
>
> So.. What you are building is the blueprint. The Agent SDK turns that blueprint into a fully autonomous system.

### Explore Activity (10 minutes)

Here is the folder structure for Hermes:

##### Top-Level Folder Map

```
c:\Hermes\
├── README.md                   Quickstart Guide
├── CLAUDE.md                   Claude Code IDE configuration
├── Hermes_Grimoire.md          The full encyclopedia for Hermes
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

Open and read these files:

**1. A Skill Definition:**

> Note: .md (Markdown) — A lightweight markup format used to create readable, formatted documents using plain text. Designed primarily for human consumption, it supports simple styling such as headings, lists, links, and emphasis.

> Note: .json (JavaScript Object Notation) — A structured data format used to represent information as key–value pairs. Designed for machine readability and data exchange between systems, it is commonly used in APIs, configurations, and data storage.

Open `skills/SI-01_stock_position_calculator.md`

Read it and understand:

- What does this skill do?
- What are its inputs?
- What does it output?

**2. An Agent README:**
Open `agents/supply_analyst/README.md`

Read it and answer:

- What is the Supply Analyst responsible for?
- How many skills does it own?
- What data does it need?

**3. The workflows**
Open `workflows\workflows.json`

Read it and answer:

- What is a hermes workflow?
- how many steps does the WF-02 have?

**Checkpoint:** Can you explain "agent", "skill", and "workflow" in one sentence each? If stuck, the Grimoire (`Hermes_Grimoire.md`) has a glossary — or just ask Claude Code: _"Explain agent, skill, and workflow in Hermes, one sentence each."_

#### Tips

- Read top-down: **Workflow → Agent → Skill**. The "why" lives at the top; the "how" at the bottom.
- Skills are a _shared library_, not agent-owned. The same skill can be called by several agents.
- Every agent has the same two-file shape (README + system_prompt). Learn the shape once, apply it seven times.
- Open three files in a split view — a skill, an agent README, and `workflows.json` — so you can see how they reference each other.
- The Grimoire usually answers "what is X?" faster than asking Claude.

---

## Module 2 · Configure Your Study with the GUI (50 minutes)

We need a test study for our analysis. You will create one from scratch.

We will prepare Hermes for your study, then create the definition of your study, finally generate some test transactional data for your study.

Your instructor has given you a **Scenario Card** with details for your fictional clinical trial. Instead of hand-editing JSON, you will use the **Study Data Creation** GUI to produce the three configuration files, then drop them into your study folder. When creating the study - you can adjust the values to your taste. You dont have to stick to the values on the scenario card precisely.

Throughout this module, `<STUDY_ID>` means the Study ID printed on your Scenario Card (for example `STUDY-LAB-01`).

### 2a. Initialise the Study Folder (5 minutes)

First, create the folder skeleton that your configuration files will live in.

Let's use a Hermes command to do this. All our commands live in the `.claude/commands/` folder.

To invoke a command, you can call them directly In the Claude Code chat panel, run:

```
/init-study <STUDY_ID>
```

When Claude asks _"Do you want to copy over templates?"_, answer **yes**. This places placeholder `study_config.json`, `supply_network.json`, and `policies.json` under `studies/<STUDY_ID>/config/` — These are just placeholders, you will overwrite them later with your own study definitions in step 2f.

Confirm in the file explorer that `studies/<STUDY_ID>/` now exists with `config/`, `reference/`, `data_drops/`, and `outputs/` subfolders.

### 2b. Open the Study Data Creation Tool (2 minutes)

#### Option I - live server

if 'LiveServer' extension is installed in your visual code environment you can right click on the html file and select
`Open with live server`

#### Option II - file explorer

Otherwise...In the file explorer, navigate to [StudyDataCreation/index.html](../../StudyDataCreation/index.html).

Right-click → **Open in Browser** (or double-click — it opens directly, no server required). If this doesn't work, you can locate the file on your disk via `Reveal in File Explorer` and double-click it from there.

Take a moment to orient yourself. The left sidebar has three numbered steps — **Study Config**, **Supply Network**, **Policies** — plus a **Load Config** section you will use later to re-import files.

### 2c. Step 1 — Study Config (15 minutes)

Click **1. Study Config** in the sidebar. Expand each section and fill it in using your Scenario Card:

- **Study Identity** — Study ID, Study Name, Protocol Number, Phase, Sponsor.
- **Treatment Arms** — click **+ Add Arm** once for each arm on your card (typically ARM-A and ARM-B); fill Arm ID, Name, Description.
- **Randomisation** — enter the ratio (e.g. `1:1` or `2:1`).
- **Items (Drugs / Kits)** — click **+ Add Item** for each investigational product. The **Arm** dropdown will list the arms you just created. Fill Item ID, Name, Pack Size, Units per Pack, Temperature.
- **Countries** — **+ Add Country** for each country on the card (code and name).
- **Clinical Sites** — **+ Add Site** for each site; the **Country** dropdown is populated from the countries above.
- **Thresholds** — Demand Delta % from the card.
- **Assumptions** — screen failure rate, dropout rate, review period weeks.

When finished, click **↓ Download study_config.json**. The file lands in your browser's Downloads folder.

### 2d. Step 2 — Supply Network (8 minutes)

Click **2. Supply Network** in the sidebar. Fill in:

- **Depots** — Depot ID, name, country, capabilities (ambient / cold chain).
- **Manufacturing Sites** — Site ID, name, country, and the Item IDs it produces (comma-separated — these must match the Item IDs you used in Step 1).
- **Shipping Lanes** — Lane ID, Origin (manufacturer ID), Destination (depot ID), Lead Time Days, Lane Type.
- **Country–Depot Assignments** — map each country to its serving depot. Both fields are dropdowns populated from what you entered above.

Click **↓ Download supply_network.json**.

### 2e. Step 3 — Policies (7 minutes)

Click **3. Policies** in the sidebar. Fill in:

- **Safety Stock** — default minimum weeks (from card).
- **Reorder Rules** — reorder point weeks, min / max order quantities.
- **Maximum Stock Levels** — default maximum weeks.
- **Budget** — budget envelope and currency from the card.
- **Expiry Rules** — minimum remaining shelf life months. Leave the destruction-eligibility checkboxes at their defaults.

Click **↓ Download policies.json**.

### 2f. Move the Files into Your Study (3 minutes)

You now have three JSON files in your `Downloads folder`. Move all three into:

```
studies/<STUDY_ID>/config/
```

When the OS prompts you, choose **Replace** to overwrite the template files that `/init-study` put there previously.

### 2g. Inspect Your Files (≈3 minutes)

Find & Open each file in VS Code and skim it to confirm it captures your study correctly:

- `study_config.json` — arms, items, countries, and sites are all present.
- `supply_network.json` — your lane's origin and destination match your manufacturer and depot IDs.
- `policies.json` — budget and safety stock match your card.

> **How this html tool works**
>
> - **There is no database.** The GUI writes to files in your browser's Downloads folder. It does not "save" anywhere you can reach later unless you move the files into your study folder yourself.
> - **Re-import anytime.** The sidebar has **Load Study Config**, **Load Supply Network**, and **Load Policies** buttons. Point them at the files in your `config/` folder to re-open and keep editing.
> - **Download overwrites.** Each time you click Download, the browser creates a fresh file with the same name. Drop it back into `config/` and choose **Replace** to update your study.
> - **Plain JSON.** These are ordinary JSON files — if you prefer, you can edit them directly in VS Code. The GUI is a convenience, not a requirement.

**Checkpoint:** Three config files sit in `studies/<STUDY_ID>/config/`, generated from the GUI and consistent with your Scenario Card.

> Note: We are using this technique, it is basic, but effective, can be modified any time, and is easy to replicate for any data source. Just watch out for the file format. The file format spec is fully described in the Grimoire.

### 2h. Generate Your Test Data (≈5 minutes)

While your study data is still loaded in the GUI, you will generate three CSV files that simulate your trial's first data drop.

> **Important:** The GUI must show your study data to generate files that match your study's site IDs, arm IDs, and item IDs. If the browser has been closed or the fields are empty, use the **Load Config** buttons in the sidebar — **Load Study Config**, **Load Supply Network**, and **Load Policies** — to reload your three JSON files from `studies/<STUDY_ID>/config/` before continuing.

In the **Create Actuals** section of the sidebar, download all three files:

- **↓ Download ctms_plan.csv** — planned enrollment by site and period
- **↓ Download erp_inventory.csv** — depot stock levels and batch data
- **↓ Download rtsm_actuals.csv** — randomisation and dispensing events

Each file lands in your browser's Downloads folder.

**Create a dated folder** inside your study's data drop folder. Use today's date in `YYYY-MM-DD` format — for example `2026-04-22`:

Move all three CSV files into that folder. (This date format is what the runner expects — sticking to it avoids "data drop not found" errors later.)

You should now have:

```
studies/<STUDY_ID>/data_drops/<today>/
  ├── rtsm_actuals.csv
  ├── ctms_plan.csv
  ├── erp_inventory.csv
  └── site_inventory.csv
```

**Run the pre-flight check** to confirm your study package and data drop are valid:

```
/preflight
```

Hermes will read your config files and data drop, run integrity checks, and report back. A `PASS` or `WARNING` status means you are ready to proceed. If it reports `FAIL`, read the recommendations and fix any critical issues before moving on.

**Checkpoint:** `/preflight` reports `PASS` or `WARNING` and three CSV files sit in `studies/<STUDY_ID>/data_drops/2026-04-22/` (today's date).

> **If you get stuck:** a fully-populated sample study is included with Hermes as study `9999999`. You can substitute it anywhere `<STUDY_ID>` appears below and still complete the lab.

---

### 2i. Run a Full Workflow Chain (≈5 minutes)

With your data drop in place and pre-flight passed, run the standard end-to-end chain against your new study. This gives you a **working baseline** before you start building — you will see how the existing agents behave so your own agent has something to compare to. It executes three workflows in sequence — demand analysis, supply planning, and execution — using the config and CSV files you just created.

In the Claude Code chat panel, run:

```
/run-workflow-chain <STUDY_ID> WF-01 WF-02 WF-05
```

Replace `<STUDY_ID>` with your Study ID (for example `STUDY-LAB-01`). The runner will automatically pick up the data drop folder you created in step 2h.

Watch the agents execute. You will see each workflow step complete in order, with its findings, any routing signals emitted, and a summary banner at the end.

> **Tip:** If the runner cannot find your data drop folder, pass the date explicitly as the last argument in `YYYY-MM-DD` format — for example `/run-workflow-chain STUDY-LAB-01 WF-01 WF-02 WF-05 2026-04-22`.

### 2j. Review and Save the Outputs (≈3 minutes)

When all three workflows complete, the runner will display a final summary banner and then ask:

> **"Would you like me to save the outputs to `studies/<STUDY_ID>/outputs/`?"**

Type **yes**. The runner will write two files into `studies/<STUDY_ID>/outputs/<date>/`:

| File                                     | Contents                                        |
| ---------------------------------------- | ----------------------------------------------- |
| `chain_WF-01_WF-02_WF-05_run_summary.md` | Full narrative output from every agent step     |
| `chain_WF-01_WF-02_WF-05_outputs.json`   | Structured JSON with workflow and step metadata |

Once saved, open `chain_WF-01_WF-02_WF-05_run_summary.md` in VS Code and review it:

- **What signals were emitted?** Look for keywords like `DEMAND_DEVIATION`, `REORDER_REQUIRED`, or `HALT` in the findings sections.
- **Did all three workflows complete?** The final summary banner lists how many steps ran and how many were skipped.
- **What did the Supply Analyst recommend?** Find the WF-02 section and read its key findings.
- **Were any integrity warnings carried forward?** Check whether the pre-flight `WARNING` status (if you got one) is referenced in later agent outputs.

**Checkpoint:** Two output files exist in `studies/<STUDY_ID>/outputs/<date>/` and you can identify at least one finding from the chain.

> **Before you move on — save your progress.** You are about to modify `/skills/`, `/agents/`, and `workflows.json`. If you break something later, it is easier to restore if you snapshot now. Either run `git add -A && git commit -m "lab baseline"` in a terminal, or just zip your `hermes-lab` folder as a backup.

#### Tips

- The Scenario Card is a starting point, not a contract — adjust values that feel unrealistic.
- Use short, memorable IDs (`SITE-01`, not `CLINICAL-SITE-BOSTON-MASS-001`). You will type them a lot.
- IDs must match **exactly** across the three JSONs and the CSVs — one typo in `ARM-A` vs `ARM_A` costs 20 minutes later.
- Don't try to save directly into `config/` — the browser drops files in Downloads; move them manually.
- To edit a study, use the **Load** buttons in the GUI sidebar. Never re-type from scratch.
- Run `/preflight` **before and after** any change to the data drop — it catches 90% of problems at their source.

---

## Module 3 · Meet the Optimization Agent (15 minutes)

We are going to simply design the agent. Not build it. We build it later in Module 5. Before writing anything, read the brief that describes your task. Before writing anything, read the brief that describes your task.

### Step 1: Open the Agent Brief

Open `lab/optimization_agent_brief.md`

Read it carefully. It tells you:

- What the Optimization Agent should do
- What kinds of findings it should produce
- What signals it should emit
- What data it has access to

### Step 2: Plan Your Agent (on paper or in a note)

Before you open any files, answer these questions in your own words:

1. How many skills do you think this agent needs?
2. What should each skill analyse? (name each one in one sentence)
3. What data file does each skill read?
4. What signal will your agent emit if it finds a problem?

**Tip:** There is no single correct answer. The brief gives you ideas, but you decide the design.

**Checkpoint:** You can explain what each of your planned skills does.

#### Tips

- Plan on paper or in a scratch note — it is faster than typing and forces brevity.
- Resist reading the reference answer. The design decisions _are_ the lab.
- If the brief feels ambiguous, that is normal — it is _your_ design.
- Name your agent's purpose in one sentence before you name any skill. If you can't, the scope is too wide.

---

## Module 4 · Write Your Skills (40 minutes)

Now write your skill files. These are the building blocks of your agent.

### What Is a Skill?

A skill is a reusable procedure — it describes exactly how an agent solves one part of its job. A skill answers:

- What do I analyse?
- What data do I read?
- What steps do I follow?
- What do I return?

**A skill file has seven sections** (see `lab/templates/skill_template.md`):

1. **Purpose** — what the skill does, in 2–3 sentences
2. **Owner** — which agent uses this skill
3. **When This Skill Is Used** — the workflow and trigger
4. **Inputs** — data files, config values, outputs from other skills
5. **Steps** — the numbered procedure (4–6 steps)
6. **Output** — what the skill returns
7. **Notes** — caveats and limitations (optional)

### Step 1: Create Your First Skill File

1. In the `/skills/` folder, create a new file
2. Name it: `OA-01_your_skill_name.md`
   - `OA` = Optimization Agent (your custom category)
   - `01` = your first skill
3. Open `lab/templates/skill_template.md` for the template
4. Copy the template into your new file and fill in all sections

**Target: at least 3 skills** (3–5 is a good range). Repeat for OA-02, OA-03, and so on.

> **Tip — build one at a time.** Write OA-01, then jump ahead briefly and check that Claude can read and summarise it (_"Read skills/OA-01 and tell me what it does"_). Fix issues there, **then** write OA-02. It is much easier than writing all five first and debugging a wall of errors later.

### Suggested Skill Types (pick your own names)

| #     | Example focus                                                     | Data file                             |
| ----- | ----------------------------------------------------------------- | ------------------------------------- |
| OA-01 | Detect depots holding stock above the max-weeks policy            | `erp_inventory.csv` + `policies.json` |
| OA-02 | Flag lots likely to expire before they can be consumed            | `erp_inventory.csv`                   |
| OA-03 | Spot sites with stock but zero recent dispensing                  | `site_inventory.csv`                  |
| OA-04 | Identify lanes with repeated emergency or over-frequent shipments | `erp_inventory.csv`                   |
| OA-05 | Convert findings from OA-01..04 into 1–3 concrete recommendations | outputs of other skills               |

_These are starting points, not a rubric — rename, reshape, or replace any of them._

> **Tip:** Keep each skill focused on one type of analysis. If a skill tries to do too much, split it.

> **Tip:** Claude will help you. Ask Claude Code: _"Is my skill file complete? Does it have all 6 sections?"_

> **What good looks like.** A well-written skill produces a finding a human can act on in one sentence. Example:
> _"Depot APAC-01 holds 14 weeks of ARM-A kit stock against an 8-week target — 6 weeks excess, flag as `OPTIMIZATION_OPPORTUNITY`."_
> If your skill's output cannot be phrased this crisply, its scope is probably too broad.

**Checkpoint:** 3+ skill files in `/skills/` with all sections filled in, no TODO markers remaining.

#### Tips

- Name every skill with a **verb** (`calculate_`, `detect_`, `flag_`). Verbs force single responsibility.
- One skill, one CSV input — crossing files is usually a sign the skill is two skills.
- Stub _all_ your skills first as one-line descriptions, then flesh each out. You see the whole map before committing to detail.
- Reference other skills by ID (`see OA-02`), never by copy-paste.
- If Claude rewrites your skill and it now does too much, push back — terse beats comprehensive.

---

## Module 5 · Write the Agent (30 minutes)

Now create the agent folder and write its instructions.

### Step 1: Create the Agent Folder

In the `/agents/` folder, create a new folder called `optimization_agent`.

Inside it, create two files:

- `README.md`
- `system_prompt.md`

### Step 2: Write README.md

Open `agents/supervisor/README.md` as a reference (it is complete).

Your README should explain:

- What your agent does (2–3 sentences)
- What it does NOT do (scope boundaries)
- Which skills it owns (table with skill IDs)
- What data files it needs
- What it produces

### Step 3: Write system_prompt.md

Open `agents/supervisor/system_prompt.md` as a reference (it is complete).

> **Optional:** If you want extra scaffolding, a fill-in-the-blank template is available at `lab/templates/optimization_agent_system_prompt.template.md`. Copy it into your new `system_prompt.md` and fill in the TODOs. Skip it entirely if you would rather write from scratch.

Work through each section:

| Section             | What to Write                                                    | Time   |
| ------------------- | ---------------------------------------------------------------- | ------ |
| **Identity**        | 2–3 sentences: who is this agent, what are they responsible for? | 3 min  |
| **Skills Table**    | List your OA- skills with when to use each                       | 5 min  |
| **Procedure**       | 4–5 numbered steps: what does the agent do when invoked?         | 12 min |
| **Output Format**   | What does the agent's output look like?                          | 5 min  |
| **Halt Conditions** | 3–4 conditions that cause the agent to stop                      | 3 min  |
| **Rules**           | 3–4 rules about HOW the agent behaves                            | 2 min  |

> **Tip:** The Procedure section should reference your skills by ID. Each step should say which OA-0X skill to run.

> **Tip:** Look at the existing `demand_analyst/system_prompt.md` for tone and level of detail.

> **Signals your agent should emit.** Your workflow will declare three routing signals in Module 6. Use them consistently in your system prompt:
>
> - **`OPTIMIZATION_OPPORTUNITY`** — excess stock, avoidable waste, a cheaper or faster alternative exists.
> - **`CRITICAL_WASTE_RISK`** — near-term expiry, stranded stock, or an imminent loss if nobody acts.
> - **`NO_ACTION`** — the agent ran cleanly and found nothing worth flagging. (Not the same as an error — emit this deliberately when the data is fine.)

**Checkpoint:** `agents/optimization_agent/system_prompt.md` is complete with all sections filled in and at least one routing signal decision rule.

> **Common pitfalls — check before you move on:**
>
> - Your Skills Table lists a skill that does not exist as a file in `/skills/` → the agent will fail silently.
> - Your agent folder is named something other than `optimization_agent` → the workflow in Module 6 will not resolve it.
> - Your Procedure never says "emit signal X when Y" → the agent will finish without emitting anything.

#### Tips

- Write the system prompt as prose, not bullet salad — instructions to a smart colleague, not a spec sheet.
- The Procedure section should read like a runbook — someone could follow it without knowing the domain.
- Halt conditions are how you stay safe — be generous. A halt is cheap; a bad output isn't.
- Start by copy-pasting `demand_analyst/system_prompt.md`, then edit. A blank page is the hardest place to start.
- An agent only "knows about" skills you list in its Skills Table. If you wrote OA-05 but forgot to list it, it will never run.

---

## Module 6 · Define Your Workflow (15 minutes)

Now define the workflow that runs your agent.

### Step 1: Open workflows.json

Open `workflows/workflows.json`.

You will see the existing workflows (WF-01 through WF-05). Study the structure of WF-01 — your new workflow follows the same pattern.

### Step 2: Add Your New Routing Signals

Before adding your workflow, add your agent's signals to the global `routing_signals` array at the top of the file.

Add these three signals:

```json
"OPTIMIZATION_OPPORTUNITY",
"NO_ACTION",
"CRITICAL_WASTE_RISK"
```

### Step 3: Add WF-OA-01

Add a new entry to the `workflows` object:

```json
"WF-OA-01": {
  "name": "Optimization Analysis",
  "steps": [
    {
      "agent": "optimization_agent",
      "task": "YOUR TASK DESCRIPTION HERE — describe in plain English what the agent should analyse and what signals it should emit"
    }
  ]
}
```

**Important:** The `"agent"` value must exactly match your folder name in `/agents/`.

> **Tip:** Ask Claude Code: _"Is my workflows.json valid JSON? Check for missing commas or brackets."_ VS Code will also underline JSON errors in red the moment you save the file — if you see a red squiggle, hover it for the exact problem.

**Checkpoint:** `workflows/workflows.json` is valid JSON (no red squiggles in VS Code) with your WF-OA-01 workflow defined and its three signals added to the global `routing_signals` array.

#### Tips

- One missing comma breaks the whole file. Save and glance for red squiggles after every edit.
- The `"agent"` value must match the folder name in `/agents/` **exactly** — case-sensitive, spelling-sensitive.
- Signals must appear in **two** places: the global `routing_signals` array **and** the agent's system prompt.
- Write the `"task"` field as a concrete instruction, not a vague mission. _"Analyse optimisation opportunities in the depot network"_ beats _"do optimisation"_.

---

## Module 7 · Run the Workflow Chain (15 minutes)

### Step 1: Verify Your Data Drop

Use the Study ID from your Scenario Card wherever `<STUDY_ID>` appears below.

Check that sample data files are in place. Navigate to: `studies/<STUDY_ID>/data_drops/`

You should see a folder with today's date containing these CSV files:

- `rtsm_actuals.csv`
- `ctms_plan.csv`
- `erp_inventory.csv`
- `site_inventory.csv` _(optional — only required if one of your skills reads it; generate it from the GUI or ask your instructor if missing)_

If a file your agent relies on is missing, either regenerate it from the Study Data Creation GUI or ask your instructor for the sample file.

### Step 2: Run the Workflow Chain

> **Tip:** Hermes runs well with the `Haiku` model. Use it to save tokens. **Design with Sonnet, run with Haiku.**

In the Claude Code chat panel, type:

```
/run-workflow-chain <STUDY_ID> WF-01 WF-OA-01
```

Substitute `<STUDY_ID>` with the Study ID from your Scenario Card (for example `STUDY-LAB-01`).

Watch the agents execute in the chat. You should see:

1. Supervisor validates data (WF-01)
2. Your Optimization Agent runs its analysis (WF-OA-01)

### Step 3: Find Your Output

Navigate to: `studies/<STUDY_ID>/outputs/[today's date]/`

Open the chain output file. Read through it and find:

- What inefficiencies did your agent detect?
- What signal did it emit?
- What actions did it recommend?

**Checkpoint:** `/run-workflow-chain` produced an output file. You can identify at least one finding from your agent.

#### Tips

- First run often fails. Read the error message; don't just re-run.
- Design with Sonnet, run with Haiku — saves tokens and time without much quality loss.
- Each run creates a dated output folder, so you can re-run freely and compare side-by-side.
- Don't trust a "completed" banner on its own. Open the output and read at least one finding — a workflow can complete with empty results.
- After the run, ask the agent follow-up questions in chat — that is where the real insight usually surfaces.

### BONUS: Ask your agents questions about your study

Once the chain has run, try interrogating your agents in natural language. Gauge the quality of the answers for yourself.

Some example questions:

1. What happens if the study start date is delayed by 3 months?
2. What happens if study dispensing is paused for 8 weeks?
3. What happens if we close down site 'X'?
4. What might be the impact on sites and future dispensing if I have to quarantine lot 'Y'?
5. Clinical wish to determine impact on the supply chain if they add a new country and try to use existing supplies. Give me a checklist of questions to ask clinical at an upcoming 'discovery' meeting.

---

## Module 8 · Review & Discussion (10 minutes)

Your instructor will ask 2–3 students to share their outputs.

**Compare your output to the reference answer:**

After the lab, the reference implementation will be available at:

- `agents/optimization_agent/` (reference system prompt and README)
- `skills/OA-01` through `OA-05` (reference skill definitions)

**Think about these questions:**

1. What signal did your agent emit — `OPTIMIZATION_OPPORTUNITY`, `NO_ACTION`, or `CRITICAL_WASTE_RISK`?
2. How many skills did you write? How does that compare to a classmate's design?
3. If two students have different skill structures, did their recommendations differ?
4. What would you change about your agent's instructions to make it more useful?
5. Where could you apply this kind of optimization agent in your own work?

#### Tips

- Comparison > perfection. Two valid designs will disagree — that is the interesting part.
- An agent that emits `NO_ACTION` is a valid result, not a failure. Check the thresholds before "fixing" it.
- One takeaway you would actually apply at work is worth more than a flawless implementation.

---

## Completion Checklist

Check off each item as you complete it:

- [ ] **M0:** Claude Code is open and responding in the project
- [ ] **M1:** Can explain "agent", "skill", and "workflow" in one sentence each
- [ ] **M2:** Study folder initialised via `/init-study`, and three config files generated from the Study Data Creation GUI and placed in `studies/<STUDY_ID>/config/`
- [ ] **M3:** Can describe in one sentence what each of your planned skills does
- [ ] **M4:** At least 3 skill files in `/skills/` with prefix `OA-`, all sections filled in
- [ ] **M5:** `agents/optimization_agent/system_prompt.md` complete with routing signals and halt conditions
- [ ] **M6:** `WF-OA-01` defined in `workflows/workflows.json` with new signals added
- [ ] **M7:** `/run-workflow-chain <STUDY_ID> WF-01 WF-OA-01` ran and produced output
- [ ] **M8:** Can identify one optimization finding from your agent's output

---

## Troubleshooting

| Problem                                      | Solution                                                                                                                                                      |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Code says "API key not found"         | Check your `.env` file has the key on one line with no spaces                                                                                                 |
| Config files missing from `config/`          | Re-download from the Study Data Creation GUI and move them into `studies/<STUDY_ID>/config/`, choosing **Replace** when prompted                              |
| Want to edit a study after downloading       | In the GUI sidebar, click **Load Study Config / Supply Network / Policies** and pick the JSON from your `config/` folder — edit, then re-download and replace |
| `/run-workflow-chain` says "study not found" | Check your Study ID matches exactly in the command and `study_config.json`                                                                                    |
| "Agent not found" error                      | Check the agent name in `workflows.json` matches the folder name in `/agents/` exactly                                                                        |
| JSON errors in `workflows.json`              | Ask Claude Code: _"Is my workflows.json valid? Fix any errors."_                                                                                              |
| Output file not created                      | Run again; check the `outputs/` folder for the date folder                                                                                                    |
| Agent emits NO_ACTION unexpectedly           | Check that `site_inventory.csv` and `erp_inventory.csv` are present in the data drop                                                                          |

---

## Stretch Exercises (if you finish early)

**Option A — Improve a Skill**
Go back to one of your skill files and add a **Notes** section explaining one limitation or edge case. For example: what happens if consumption rate is zero?

**Option B — Add a Second Workflow**
Define `WF-OA-02` that chains your Optimization Agent after the Supply Analyst: run `/run-workflow-chain MY-STUDY-01 WF-01 WF-02 WF-OA-01`.

**Option C — Compare to the Reference Answer**
Open `agents/optimization_agent/system_prompt.md` (the reference). Compare your Procedure section to the reference. What did you include that the reference missed? What did the reference include that you missed?

**Option D — Write a Sixth Skill**
Add a skill `OA-06` that does something new — for example, a Budget Impact Estimator that estimates the cost of the waste your agent found.

## Ideas for other skills:

1. Financial Advisor - reviews cost of decisions. Would be data heavy. Would work well with the Optimization Agent
2. Capacity Agent - Reviews and make recommendations on capacity questions across your factory, and even depots
3. Site Experience Agent - Train an agent to appear like a clinical site. How are decisions you are making in the supply network impacting the site. Guage their satisfication by asking the Site Experience Analyst to review your decisions.
