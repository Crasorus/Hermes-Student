# Hermes

Hermes is a Clinical Supply Chain AI Agent Team for pharmaceutical trial supply chain management.

Seven specialised agents work together to analyse demand signals, plan supply, monitor risks, ensure compliance, and generate reports. All agent intelligence lives in markdown files — no coding required to customise agent behaviour.

---

## Your First Workflow

The easiest way to run Hermes is directly from the Claude Code chat window using a slash command:

```
/run-workflow WF-04 999999
```

This runs **Routine Monitoring** on the sample study. You'll see the agents work through the data and produce a report in `studies/999999/outputs/`.

---

## All Workflows

| ID    | Name                      | What it does                          | When      |
| ----- | ------------------------- | ------------------------------------- | --------- |
| WF-01 | Demand Signal Refresh     | Analyses enrollment and consumption   | Weekly    |
| WF-02 | Supply Plan Generation    | Calculates stock needs and requests   | As needed |
| WF-03 | Protocol Amendment Impact | Assesses impact of protocol changes   | Ad hoc    |
| WF-04 | Routine Monitoring        | Daily health check across all signals | Daily     |
| WF-05 | Supply Plan Execution     | Executes an approved supply plan      | As needed |

---

## Slash Commands

| Command                                  | What it does                             |
| ---------------------------------------- | ---------------------------------------- |
| `/run-workflow WF-01 999999`             | Run a workflow against a study           |
| `/run-workflow-chain WF-01,WF-02 999999` | Run multiple workflows in sequence       |
| `/init-study MY-STUDY`                   | Create a new study folder from templates |
| `/preflight 999999`                      | Verify a study is ready to run           |

---

## Setting Up a New Study

1. Run `/init-study YOUR-STUDY-ID` — creates the folder structure from templates
2. Edit the config files in `studies/YOUR-STUDY-ID/config/` or use `StudyDataCreation` to create the config files using a User Interface.
3. Use `StudyDataCreation` html app to create some test data for your study
4. Add save the csv files to your data drops to `studies/YOUR-STUDY-ID/data_drops/YYYY-MM-DD/`
5. Run `/preflight YOUR-STUDY-ID` to verify everything is in order
6. Run your first workflow

See `studies/templates/` for blank config files with instructions.

---

## Project Structure

```
agents/              7 specialised agents (README.md + system_prompt.md each)
skills/              76 shared skill definitions (markdown)
workflows/           5 workflow definitions + workflows.json
runner/              Execution engine and configuration
studies/             Per-study folders: config/, reference/, data_drops/, outputs/
  999999/            Sample study — start here
  templates/         Blank templates for creating your own study
StudyDataCreation/   Browser tools for generating synthetic test data
lab/                 Lab exercises and templates
run.bat / run.sh     Interactive launcher (alternative to chat commands)
```

---

## Running with the Interactive Launcher

If you prefer a menu-driven approach, double-click **run.bat** (Windows) or run **./run.sh** (Mac/Linux). The script walks you through choosing a workflow, study, and data-drop date.

**Prerequisites for the launcher:**

1. Python 3.9+ — https://www.python.org/downloads/
2. Anthropic SDK — `pip install anthropic`
3. API key in a `.env` file at the project root (copy `.env.example` and add your key)

---

## What Hermes Produces

Each workflow run writes three files to `studies/{study_id}/outputs/YYYY-MM-DD/`:

| File                   | Purpose                                                |
| ---------------------- | ------------------------------------------------------ |
| `WF-XX_run_summary.md` | Human-readable summary of findings and recommendations |
| `WF-XX_outputs.json`   | Structured agent outputs                               |
| `WF-XX_audit_log.json` | GxP audit trail with timestamps                        |

See `studies/999999/outputs/` for an example of completed output.

> Disclaimer: Hermes is provided solely as an educational and exploratory tool to demonstrate potential AI use cases within clinical supply chain processes. It is not a validated system and must not be used to support decision-making in regulated clinical trial activities, including but not limited to patient safety, drug supply, or compliance-related functions.

> No warranty, express or implied, is provided. Hermes is used entirely at the user’s own risk.
