# Hermes Lab — Instructor Guide

A 3-hour hands-on lab where students build their own working version of Hermes from scratch.

---

## Overview

**Students:** 10 (non-technical: life sciences, supply chain, business analysts)
**Duration:** 3 hours
**Each student gets:** Their own computer, their own API key, their own fictional study scenario
**Platform:** VS Code + Claude Code extension (no Python coding required)

Students build Hermes piece by piece, understanding each layer of the architecture before running the system end-to-end.

---

## What Students BUILD vs GET

| Students BUILD | Students GET (pre-loaded) |
|---|---|
| study_config.json | All 73 skill definitions |
| supply_network.json | All 7 agent system prompts (as reference) |
| policies.json | Python runner code |
| 1 skill definition | /run-workflow command |
| demand_analyst system prompt | CLAUDE.md, README.md |
| 1 workflow in workflows.json | Sample data drop (4 CSV files) |
| runner_config.json (just API key) | workflows.json (WF-01 complete as reference) |

---

## Lab Materials in This Folder

```
lab/
├── README.md                          This file — instructor guide
├── instructor/
│   ├── lab_guide.md                   Step-by-step student instructions (print or share)
│   └── scenario_cards.md              10 unique fictional study scenarios (print and cut)
└── templates/
    ├── study_config.template.json     Annotated config template for students
    ├── supply_network.template.json   Annotated supply network template
    ├── policies.template.json         Annotated policies template
    ├── skill_template.md              Blank skill template with fill-in-the-blank sections
    ├── demand_analyst_system_prompt.template.md   Agent system prompt template
    └── workflows.template.json        WF-01 (reference) + WF-LAB-01 (blank for students)
```

---

## Building the Starter Kit

The "Starter Kit" students download is a prepared copy of Hermes. Build it as follows:

### Step 1: Copy the project
```
cp -r /path/to/Hermes hermes-lab
```

### Step 2: Create the study folder for students
```
mkdir -p hermes-lab/studies/MY-STUDY-01/config
mkdir -p hermes-lab/studies/MY-STUDY-01/data_drops
mkdir -p hermes-lab/studies/MY-STUDY-01/outputs
```

### Step 3: Add template config files
Copy from `lab/templates/` into the study folder:
```
cp lab/templates/study_config.template.json hermes-lab/studies/MY-STUDY-01/config/study_config.json
cp lab/templates/supply_network.template.json hermes-lab/studies/MY-STUDY-01/config/supply_network.json
cp lab/templates/policies.template.json hermes-lab/studies/MY-STUDY-01/config/policies.json
```

### Step 4: Add template agent system prompt
```
cp lab/templates/demand_analyst_system_prompt.template.md hermes-lab/agents/demand_analyst/system_prompt.md
```
(Backs up the original to `demand_analyst/system_prompt.md.reference` first)

### Step 5: Add workflow template
```
cp lab/templates/workflows.template.json hermes-lab/workflows/workflows.json
```

### Step 6: Add .env template
Create `hermes-lab/.env.template`:
```
ANTHROPIC_API_KEY=YOUR_API_KEY_HERE
```

### Step 7: Add runner_config template
Create `hermes-lab/runner/runner_config.json.template` with:
```json
{
  "model": "claude-opus-4-7",
  "api_key_env": "ANTHROPIC_API_KEY",
  "agents_path": "agents",
  "workflows_path": "workflows",
  "max_tokens": 8192
}
```

### Step 8: Add sample data
Copy one data drop from an existing study into:
```
hermes-lab/studies/MY-STUDY-01/data_drops/[today's date]/
```
Include all 4 CSVs: `rtsm_actuals.csv`, `ctms_plan.csv`, `erp_inventory.csv`, `site_inventory.csv`

### Step 9: Zip and distribute
```
zip -r hermes-lab.zip hermes-lab/
```

---

## Pre-Lab Checklist

**1 week before:**
- [ ] Test the full lab end-to-end yourself (start from the zip, follow lab_guide.md)
- [ ] Verify `/run-workflow WF-LAB-01 MY-STUDY-01` produces output
- [ ] Print scenario cards (one per student, no duplicates)
- [ ] Print or digitally share lab_guide.md

**Day before:**
- [ ] Confirm students have VS Code installed
- [ ] Confirm students have Anthropic API keys (or set up a class key)
- [ ] Share hermes-lab.zip download link

**Day of:**
- [ ] Have the lab guide open on a display for reference
- [ ] Have your own Hermes running to demonstrate
- [ ] Prepare to spend 5 min in Module 0 helping with API key setup

---

## Timing Guide

| Module | Topic | Time | Watch For |
|---|---|---|---|
| M0 | Setup | 15 min | API key issues — have backup keys ready |
| M1 | Architecture | 20 min | Keep it moving — exploration, not deep dive |
| M2 | Config files | 40 min | JSON syntax errors — point them to Claude Code for help |
| M3 | Skill writing | 15 min | Choice paralysis — assign Option A if stuck |
| M4 | System prompt | 30 min | Biggest learning — give full time, circulate |
| M5 | Workflow | 15 min | Quick — most students can copy WF-01 pattern |
| M6 | Run + review | 20 min | API errors, missing data — troubleshoot table in lab_guide |
| M7 | Discussion | 10 min | Ask: what was surprising? what would you change? |
| Buffer | Q&A | 15 min | Use for M4 overflow — it always runs long |

---

## Common Issues and Fixes

| Issue | Fix |
|---|---|
| API key not working | Check `.env` file name (no `.txt` extension), key format starts with `sk-ant-` |
| `/run-workflow` not found | Check `.claude/commands/run-workflow.md` exists |
| "Study not found" error | Study ID in command must exactly match `study_id` in study_config.json |
| Output file missing | Check `outputs/` folder has a date subfolder for today |
| JSON parse error | Open the file in VS Code, it highlights syntax errors in red |
| Demand analyst not doing anything | Check system prompt has the procedure steps filled in |

---

## Discussion Questions for Module 7

1. "Two students had similar scenarios but different agent instructions. Who got better output? Why?"
2. "What surprised you about writing the system prompt? Was it harder or easier than expected?"
3. "If you were applying this to a real study, what would you change first?"
4. "What's the most important agent in the system and why?"
5. "What other domains could you apply this multi-agent architecture to?"
