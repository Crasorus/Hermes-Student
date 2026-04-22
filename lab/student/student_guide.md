# Hermes Lab — Student Guide

**Duration:** 3 hours | **Format:** Individual hands-on build

> Note: At any time you can put this file into preview mode by right clicking the file and selecting `Open Preview`

---

### What Hermes Is

Hermes is a **Clinical Supply Chain AI Agent Team** built for pharmaceutical trial supply management. Seven specialised agents collaborate — autonomously where possible, with humans at review points — to ingest operational data, analyse demand, plan supply, monitor risk, enforce compliance, and report out. The intelligence of every agent and every skill is expressed in plain Markdown, not code. A thin Python runner calls the Claude API to execute those prompts in ordered workflows and write auditable outputs. The framework is **system-agnostic** (it reads CSV/JSON data drops rather than talking to ERP/RTSM systems directly) and **portable** (the same study package structure works for any protocol).

> Disclaimer: Hermes is provided solely as an educational and exploratory tool to demonstrate potential AI use cases within clinical supply chain processes. It is not a validated system and must not be used to support decision-making in regulated clinical trial activities, including but not limited to patient safety, drug supply, or compliance-related functions.

> No warranty, express or implied, is provided. Hermes is used entirely at the user’s own risk.

---

## What You Are Building

By the end of this lab you will have built the **Optimization Agent** — a new member of the Hermes Clinical Supply Chain AI Agent Team.

You will write skill files, an agent system prompt, and a workflow definition entirely in plain English (Markdown). No coding required.

**You will build:**

- 4–5 skill definitions (the building blocks of agent capability)
- One complete agent (README + system prompt)
- One workflow definition

**You will be given (pre-loaded in your starter kit):**

- The full skills library (reference only)
- All existing agent system prompts (as reference examples)
- The Python runner code (black box — no coding needed)
- Sample clinical data files
- An agent brief handout that describes what your agent should do

---

## Pre-requisites

1. Visual Code
2. Extension: Claude Code for VS Code-

#### -(Optional)

3. Extension: Live Server

## Module 0 · Setup (15 minutes)

### Step 1: Download the Starter Kit

Download `hermes-lab.zip` from the link your instructor provides.
Extract it to a folder on your computer (e.g. `c:/hermes-lab`).

### Step 2: Open in VS Code

1. Open VS Code
2. Go to **File → Open Folder**
3. Select the `hermes-lab` folder you extracted

### Step 3: Test Claude Code

1. Open the Claude Code panel in VS Code (look for the Claude icon in the sidebar, or press `Ctrl+Shift+P` and type "Claude")
2. Type: `What is Hermes?`
3. You should get a response explaining the project. If you do — you are ready!

---

## Module 1 · Architecture Orientation (20 minutes)

Before building anything, spend 10 minutes exploring what's already in the starter kit.

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
> A **production implementation** of Hermes would go one step further — using Anthropic's **Agent SDK** to give each agent its own autonomous runtime. Agents would call each other directly, spawn sub-tasks, and run end-to-end without a human in the loop between steps. Importantly, you could connect them directly to your data sources via an MCP server or other techique (Thus avoiding data drops). The Markdown files you write today would become the system prompts fed into those agent instances.
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

**Checkpoint:** Can you explain "agent", "skill", and "workflow" in one sentence each?

> Note: .md (Markdown) — A lightweight markup format used to create readable, formatted documents using plain text. Designed primarily for human consumption, it supports simple styling such as headings, lists, links, and emphasis.

> Note: .json (JavaScript Object Notation) — A structured data format used to represent information as key–value pairs. Designed for machine readability and data exchange between systems, it is commonly used in APIs, configurations, and data storage.

---

## Module 2 · Configure Your Study with the GUI (40 minutes)

We need a test study for our analsis. You will create one from scratch.

We will prepare Hermes for your study, then create the definition of your study, finally generate some test transactional data for your study.

Your instructor has given you a **Scenario Card** with details for your fictional clinical trial. Instead of hand-editing JSON, you will use the **Study Data Creation** GUI to produce the three configuration files, then drop them into your study folder. When creating the study - you can adjust the values to your taste. You dont have to stick to the values on the scenario card precisely.

Throughout this module, `<STUDY_ID>` means the Study ID printed on your Scenario Card (for example `STUDY-LAB-01`).

### 2a. Initialise the Study Folder (5 minutes)

First, create the folder skeleton that your configuration files will live in.

Lets use a hermes command to do this, all our commands are located in the commands folder.

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

Right-click → **Open in Browser** (or double-click — it opens directly, no server required). If this doesnt work, you can locate the file on your disk `reveal in file explorer` and double click it from there.

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

#### Finally

if you get stuck, you can use the Sample study included with the Hermes package. This is study `9999999`

---

## Module 3 · Meet the Optimization Agent (15 minutes)

Before writing anything, read the brief that describes your task.

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

---

## Module 4 · Write Your Skills (40 minutes)

Now write your skill files. These are the building blocks of your agent.

### What Is a Skill?

A skill is a reusable procedure — it describes exactly how an agent solves one part of its job. A skill answers:

- What do I analyse?
- What data do I read?
- What steps do I follow?
- What do I return?

### Step 1: Create Your First Skill File

1. In the `/skills/` folder, create a new file
2. Name it: `OA-01_your_skill_name.md`
   - `OA` = Optimization Agent (your custom category)
   - `01` = your first skill
3. Open `lab/templates/skill_template.md` for the template
4. Copy the template into your new file and fill in all sections

**Target: 3+ skills.** Repeat for OA-02, OA-03, OA-04, OA-05 etcc.

### Suggested Skill Types (pick your own names)

| #     | Type of Analysis                      | Data File               |
| ----- | ------------------------------------- | ----------------------- |
| OA-01 | Something about depot stock levels    | erp_inventory.csv       |
| OA-02 | Something about batch expiry dates    | erp_inventory.csv       |
| OA-03 | Something about site consumption      | site_inventory.csv      |
| OA-04 | Something about shipment patterns     | erp_inventory.csv       |
| OA-05 | Turning findings into recommendations | Outputs of other skills |

> **Tip:** Keep each skill focused on one type of analysis. If a skill tries to do too much, split it.

> **Tip:** Claude will help you. Ask Claude Code: _"Is my skill file complete? Does it have all 6 sections?"_

**Checkpoint:** 3+ skill files in `/skills/` with all sections filled in, no TODO markers remaining.

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

**Checkpoint:** `agents/optimization_agent/system_prompt.md` is complete with all sections filled in and at least one routing signal decision rule.

---

## Module 6 · Define Your Workflow (15 minutes)

<!-- ============================================================
     MODULE 6: Students add WF-OA-01 to workflows.json.
     Key things to explain:
     1. The JSON schema (model on WF-01)
     2. Adding routing signals to the global array
     3. The agent name must match the folder name exactly
     ============================================================ -->

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

> **Tip:** Ask Claude Code: _"Is my workflows.json valid JSON? Check for missing commas or brackets."_

**Checkpoint:** `workflows/workflows.json` is valid JSON with your WF-OA-01 workflow defined.

---

## Module 7 · Run the Workflow Chain (15 minutes)

### Step 1: Verify Your Data Drop

Use the Study ID from your Scenario Card wherever `<STUDY_ID>` appears below.

Check that sample data files are in place. Navigate to: `studies/<STUDY_ID>/data_drops/`

You should see a folder with today's date containing these CSV files:

- `rtsm_actuals.csv`
- `ctms_plan.csv`
- `erp_inventory.csv`
- `site_inventory.csv`

If any file is missing, ask your instructor for the sample data files.

### Step 2: Run the Workflow Chain

> Tip: Hermes runs well with the `Haiku` model. Use it to save tokens. Design with sonnnet, run with haiku
> In the Claude Code chat panel, type:

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

### BONUS: Ask your agents questions about your study

Ask anything. Guage for yourself the quality of the results.

Some example questions:

1. What happens if the study start date is dealyed by 3 months.
2. What happens if the study dispensing is paused for 8 weeks
3. What happens if we close down site 'X'?
4. What might be the impact on sites and future dispensing if i have to a qurantine lot 'Y'?
5. Clinical wish to determine impact on supply chain if they add a new country, and try and use existing supplies. Give me a check list of questions to ask clinical at an upcoming 'discovery' meeting.

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

---

## Completion Checklist

Check off each item as you complete it:

- [ ] **M0:** Claude Code is open and responding in the project
- [ ] **M1:** Can explain "agent", "skill", and "workflow" in one sentence each
- [ ] **M2:** Study folder initialised via `/init-study`, and three config files generated from the Study Data Creation GUI and placed in `studies/<STUDY_ID>/config/`
- [ ] **M3:** Can describe in one sentence what each of your planned skills does
- [ ] **M4:** 4–5 skill files in `/skills/` with prefix `OA-`, all sections filled in
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
