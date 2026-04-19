# Claude Code Configuration for Hermes

## Project Overview
Hermes is a Clinical Supply Chain AI Agent Team for pharmaceutical trial supply chain management. Seven specialised agents collaborate autonomously to ingest data, analyse demand, plan supply, monitor risks, ensure compliance, and generate reports. All agent intelligence lives in markdown files — no coding required to customise behaviour.

## Project Structure
- `/agents/` - 7 specialized agents (each has README.md + system_prompt.md)
- `/skills/` - 76 shared skill definitions (markdown files)
- `/workflows/` - 5 workflow definitions (markdown files)
- `/runner/` - Workflow execution: runner.py (API), run.bat/run.sh (scripts)
- `/workflows/workflows.json` - Machine-readable workflow definitions (agent sequences, routing signals)
- `/studies/{study_id}/` - Per-study data (config/, reference/, data_drops/, outputs/)
- `.claude/` - Claude Code configuration and commands

## Running Workflows from Chat
Use `/run-workflow` to execute workflows directly from the Claude Code chat window.
Example: `/run-workflow WF-04 999999`
The command file is at `.claude/commands/run-workflow.md`.

## Key Design Principles
1. **System Agnostic Data Layer** - Operates on CSV/JSON data drops, not direct ERP/RTSM connections
2. **Portable Study Package** - Framework works identically across studies
3. **Configurable Thresholds** - 10% default demand delta significance, overridable per study
4. **Human in the Loop at Output Only** - Agents run autonomously, humans review outputs
5. **GxP Audit Trail by Default** - All agent actions logged with timestamps
6. **Recommendations vs. Decisions** - Clear distinction in agent outputs

## Agent Team
- **Supervisor** - Orchestrates workflows, routes tasks, validates study packages
- **Demand Analyst** - Analyses enrollment, dispensing, screen failures, and consumption rates
- **Supply Analyst** - Calculates stock positions, safety stock, and reorder points
- **Logistics Specialist** - Plans shipments, manages cold chain, customs, and approved vendors
- **Compliance Manager** - Ensures GxP audit trails, regulatory compliance, and deviation tracking
- **Insights Analyst** - Identifies anomalies, trends, and risk hotspots across all signals
- **Reporting Agent** - Generates executive summaries, deviation reports, and clinical ops updates

## File Conventions
- Documentation: Markdown (.md)
- Configuration: JSON files
- Data: CSV format for data drops
- Audit logs: Structured JSON with timestamps
