# Hermes Lab — Student Lab Guide

**Duration:** 3 hours | **Format:** Individual hands-on build

---

## What You Are Building

By the end of this lab you will have your own working version of **Hermes** — a multi-agent AI system that analyses clinical trial supply chains.

You will configure it for a fictional clinical study, write instructions for one AI agent, define a workflow, and run the system end-to-end.

**You will build:**
- A complete study package (JSON config files for your trial)
- One skill definition (the building block of agent capability)
- One agent system prompt (the "instructions" that make an agent smart)
- One workflow (the sequence of agents that run together)

**You will be given (pre-loaded in your starter kit):**
- The full skills library (73 skills)
- All 7 agent system prompts as reference
- The Python runner code (black box — no coding needed)
- Sample clinical data files

---

## Before You Start

### You will need:
1. **VS Code** installed on your machine
2. **Claude Code extension** installed in VS Code
3. **An Anthropic API key** (from console.anthropic.com)
4. The **Hermes Starter Kit** (download link from your instructor)

---

## Module 0 · Setup (15 minutes)

### Step 1: Download the Starter Kit

Download `hermes-lab.zip` from the link your instructor provides.
Extract it to a folder on your computer (e.g. `Desktop/hermes-lab`).

### Step 2: Open in VS Code

1. Open VS Code
2. Go to **File → Open Folder**
3. Select the `hermes-lab` folder you extracted

### Step 3: Set Up Your API Key

1. In the file explorer (left panel), find `.env.template`
2. Right-click → **Rename** → change to `.env`
3. Open `.env` and replace `YOUR_API_KEY_HERE` with your Anthropic API key

```
ANTHROPIC_API_KEY=sk-ant-...your key here...
```

### Step 4: Set Up runner_config.json

1. Find `runner/runner_config.json.template`
2. Rename it to `runner/runner_config.json`
3. Open it and fill in:

```json
{
  "model": "claude-opus-4-7",
  "api_key_env": "ANTHROPIC_API_KEY",
  "agents_path": "agents",
  "workflows_path": "workflows",
  "max_tokens": 8192
}
```

### Step 5: Test Claude Code

1. Open the Claude Code panel in VS Code (look for the Claude icon in the sidebar, or press `Ctrl+Shift+P` and type "Claude")
2. Type: `What is Hermes?`
3. You should get a response explaining the project. If you do — you are ready!

**Checkpoint:** Claude Code is responding in your project. Raise your hand when done.

---

## Module 1 · Architecture Orientation (20 minutes)

Before building anything, spend 10 minutes exploring what's already in the starter kit.

### The 5 Layers of Hermes

```
Layer 5: RUNNER          — executes workflows (Python code — don't touch)
Layer 4: WORKFLOWS       — defines which agents run, in what order
Layer 3: AGENTS          — AI specialists, each with their own instructions
Layer 2: SKILLS          — atomic capabilities agents can apply
Layer 1: STUDY PACKAGE   — your study's config + CSV data
```

> **Note — What Version of Hermes Are You Building?**
>
> The version you are building today is a **prompt-only framework**. Every agent and skill is a Markdown file containing structured English instructions. There is no custom code in the agents or skills themselves. The Python runner calls the Claude API on your behalf, passing those instructions as prompts and returning the output.
>
> This is a deliberate design choice: it keeps the system accessible to non-technical users and easy to inspect, modify, and understand.
>
> A **production implementation** of Hermes would go one step further — using Anthropic's **Agent SDK** to give each agent its own autonomous runtime. Agents would call each other directly, spawn sub-tasks, and run end-to-end without a human in the loop between steps. The Markdown files you write today would become the system prompts fed into those agent instances.
>
> What you are building is the blueprint. The Agent SDK turns that blueprint into a fully autonomous system.

### Explore Activity (10 minutes)

Open and read these two files:

**1. A Skill Definition:**
Open `skills/DF-03_demand_delta_calculator.md`

Read it and answer in your own words:
- What does this skill do?
- What are its inputs?
- What does it output?

**2. An Agent README:**
Open `agents/demand_analyst/README.md`

Read it and answer:
- What is the Demand Analyst responsible for?
- How many skills does it own?
- What data does it need?

**Checkpoint:** Can you explain "agent", "skill", and "workflow" in one sentence each?

---

## Module 2 · Configure Your Study (40 minutes)

Your instructor has given you a **Scenario Card** with details for your fictional clinical trial. Use it to fill in three configuration files.

### 2a. study_config.json (20 minutes)

1. In the file explorer, navigate to `studies/MY-STUDY-01/config/`
2. Open `study_config.json` (already a template with TODO markers)
3. Fill in every field marked **TODO** using values from your Scenario Card

**Key things to fill in:**
- Study identity (name, protocol, sponsor, phase)
- Treatment arms (ARM-A and ARM-B)
- Items (your two investigational products)
- Countries and sites
- Thresholds (demand delta significance %)
- Assumptions (screen failure rate, dropout rate)

**Tip:** Keep your JSON valid. Each `"key": "value"` pair needs quotes and commas in the right places. If unsure, ask Claude Code: *"Is my study_config.json valid JSON?"*

### 2b. supply_network.json (10 minutes)

Open `supply_network.json` and fill in:
- Your depot (regional warehouse) from the Scenario Card
- Your manufacturing site
- Your shipping lane (from manufacturer to depot)
- Country-depot assignments

### 2c. policies.json (10 minutes)

Open `policies.json` and fill in:
- Safety stock weeks (from Scenario Card)
- Reorder point weeks (from Scenario Card)
- Max stock weeks (from Scenario Card)
- Budget (from Scenario Card)
- Shelf life requirement (from Scenario Card)

**Checkpoint:** Three config files complete, consistent with your Scenario Card. Ask Claude Code: *"Check my study_config.json and policies.json — are the numbers consistent with each other?"*

---

## Module 3 · Write a Skill (15 minutes)

Now you will write one skill from scratch. This teaches you the building block of agent capability.

### Step 1: Choose Your Skill

Pick one skill from this list (or invent your own based on your study):

| Option | Skill Name | What It Does |
|---|---|---|
| A | Expiry Risk Scorer | Flag items whose lot expiry date is within 8 weeks |
| B | Site Consumption Reporter | Summarise kit dispensing totals by site |
| C | Enrollment Gap Detector | Identify sites that are behind their enrollment plan |
| D | Cold Chain Checker | Flag any shipment that violates temperature requirements |
| E | Low Stock Alerter | List all items currently below safety stock threshold |
| F | Your own idea | Define something useful for your study scenario |

### Step 2: Create the Skill File

1. In the `skills/` folder, create a new file
2. Name it using the pattern: `XX-YY_skill_name.md` (e.g. `LA-01_expiry_risk_scorer.md`)
   - `LA` = Lab skill (your custom category)
   - `01` = your first skill
3. Open `lab/templates/skill_template.md` for the template to fill in
4. Copy the template content into your new file and fill in all the TODO sections

**Tip:** Keep it simple — 4-5 steps is plenty. Focus on *what the skill does*, not the code behind it.

**Checkpoint:** Skill file exists in `/skills/` with all 5 sections filled in.

---

## Module 4 · Write an Agent System Prompt (30 minutes)

This is the most important exercise. You are going to write the "instructions" that tell an AI agent how to do its job.

### What Is a System Prompt?

A system prompt is a set of standing orders for an AI specialist. It defines:
- Who the agent is
- What skills they own and when to use them
- What steps they follow
- What signals they emit
- When they stop

**These are NOT code.** They are structured English instructions. The AI reads them and uses them to guide its analysis.

### Your Task

1. Open `agents/demand_analyst/system_prompt.md` (this is your template — it has TODO markers)
2. Also open `agents/supervisor/system_prompt.md` as a reference (it's complete)
3. Fill in your demand_analyst system prompt

**Work through each section:**

| Section | What to Write | Time |
|---|---|---|
| **Identity** | 2-3 sentences: who is this agent, what are they responsible for? | 3 min |
| **Skills Table** | List 5-6 skills (use DF- and DI- skills from the /skills folder) with when to use each | 7 min |
| **Procedure** | 4-5 numbered steps: what does the agent do when invoked? | 10 min |
| **Routing Signals** | When to emit SIGNIFICANT_DELTA, MINOR_DELTA, or HALT | 3 min |
| **Halt Conditions** | 3-4 conditions that cause the agent to stop | 3 min |
| **Rules** | 3-4 rules about HOW the agent behaves (precision, conservatism, traceability) | 4 min |

**Tip:** Look at the completed `supervisor/system_prompt.md` for examples of tone, structure, and level of detail. Then write in your own words.

**Checkpoint:** `demand_analyst/system_prompt.md` is complete with all sections filled in and at least one routing signal decision rule.

---

## Module 5 · Define a Workflow (15 minutes)

Now you will define the sequence of agents that run when your workflow executes.

### Step 1: Open the Workflow Template

Open `workflows/workflows.json`

You will see WF-01 (complete, as reference) and WF-LAB-01 (your template to fill in).

### Step 2: Fill In Your Workflow

Fill in the `WF-LAB-01` entry:

1. **Name:** Give your workflow a descriptive name
2. **Steps:** Define 3-4 steps. For each step you need:
   - `"agent"` — the name of the agent that runs (must match a folder name in `/agents/`)
   - `"task"` — a plain English description of what this agent should do

**Recommended workflow sequence for your lab:**
```
Step 1: supervisor — always runs first, validates data (copy from WF-01)
Step 2: demand_analyst — analyse demand, calculate delta
Step 3: reporting_agent — write the summary report
```

**Tip:** Step 1 (supervisor data validation) is identical in every workflow — copy it exactly from WF-01.

**Checkpoint:** `workflows/workflows.json` is valid JSON with your WF-LAB-01 workflow defined.

---

## Module 6 · Run the System (20 minutes)

### Step 1: Verify Your Data Drop

Check that sample data files are in place:

Navigate to: `studies/MY-STUDY-01/data_drops/`

You should see a folder with today's date containing 4 CSV files:
- `rtsm_actuals.csv`
- `ctms_plan.csv`
- `erp_inventory.csv`
- `site_inventory.csv`

If the folder is empty or missing, ask your instructor for the sample data files.

### Step 2: Run Your Workflow

In the Claude Code chat panel, type:

```
/run-workflow WF-LAB-01 MY-STUDY-01
```

(Replace `MY-STUDY-01` with your actual Study ID if you changed it.)

Watch the agents execute in the chat. You should see:
1. Supervisor validates data
2. Demand Analyst analyses consumption and enrollment
3. Reporting Agent writes the summary

### Step 3: Find Your Output

Navigate to: `studies/MY-STUDY-01/outputs/[today's date]/`

Open `WF-LAB-01_run_summary.md`

Read through it and find:
- What did the Demand Analyst find?
- Was the demand delta SIGNIFICANT or MINOR?
- What did the Reporting Agent recommend?

**Checkpoint:** `/run-workflow` produced a `_run_summary.md` file. You can identify one recommendation from the output.

---

## Module 7 · Review & Discussion (10 minutes)

Your instructor will ask 2-3 students to share their outputs.

**Think about these questions:**

1. What signal did your demand analyst emit — SIGNIFICANT_DELTA or MINOR_DELTA?
2. If two students have similar scenarios but different agent instructions, did their outputs differ?
3. What would you change about your agent's instructions to make it more useful?
4. Where could you apply this kind of multi-agent system in your own work?

---

## Completion Checklist

Check off each item as you complete it:

- [ ] **M0:** Claude Code is open and responding in the project
- [ ] **M1:** Can explain "agent", "skill", and "workflow" in one sentence each
- [ ] **M2:** Three config files complete (`study_config.json`, `supply_network.json`, `policies.json`)
- [ ] **M3:** New skill file exists in `/skills/` with all 5 sections
- [ ] **M4:** `demand_analyst/system_prompt.md` complete with routing signals and halt conditions
- [ ] **M5:** `WF-LAB-01` workflow defined in `workflows/workflows.json`
- [ ] **M6:** `/run-workflow` ran successfully and produced a `_run_summary.md`
- [ ] **M7:** Can identify one supply chain recommendation from your output

---

## Stretch Exercises (if you finish early)

**Option A — Second Workflow**
Define `WF-LAB-02` in `workflows/workflows.json` for a different scenario (e.g., supply plan generation). Add the `supply_analyst` and `logistics_specialist` agents to the sequence.

**Option B — Supply Analyst System Prompt**
Open `agents/supply_analyst/system_prompt.md` and write a custom version. What skills would it use from the `SI-` category? What decisions would it make?

**Option C — Add Your Custom Skill**
Write a second skill definition in the `/skills/` folder. Reference it from your demand_analyst system prompt.

**Option D — Chain Two Workflows**
In the Claude Code chat, run:
```
/run-workflow-chain WF-LAB-01 WF-LAB-02 MY-STUDY-01
```
Review the chained output — how do the two workflow outputs connect?

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Claude Code says "API key not found" | Check your `.env` file has the key on one line with no spaces |
| `/run-workflow` says "study not found" | Check your Study ID matches exactly in the command and study_config.json |
| JSON errors in config files | Ask Claude Code: *"Is my study_config.json valid? Fix any errors."* |
| "Agent not found" error | Check agent name in workflows.json matches a folder name in /agents/ exactly |
| Output file not created | Run `/run-workflow` again; check the outputs/ folder for the date folder |
