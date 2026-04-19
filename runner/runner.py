#!/usr/bin/env python3
"""
Hermes Runner — executes Hermes workflows via the Claude API.

Usage:
    python runner/runner.py --workflow WF-01 --study STUDY-001
    python runner/runner.py --workflow WF-01 --study STUDY-001 --data-drop 2026-03-06
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic

# Load .env file if it exists
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                value = value.strip('"\'')
                if key not in os.environ:
                    os.environ[key] = value

# ── Paths ──────────────────────────────────────────────────────────────────────
RUNNER_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = RUNNER_DIR.parent.resolve()
CONFIG_PATH = RUNNER_DIR / "runner_config.json"

WORKFLOWS_PATH = RUNNER_DIR.parent / "workflows" / "workflows.json"


def load_workflows() -> dict:
    """Load workflows.json. Exit with helpful message if missing or invalid."""
    if not WORKFLOWS_PATH.exists():
        sys.exit(
            f"ERROR: workflows.json not found at {WORKFLOWS_PATH}\n"
            f"This file defines the workflow steps. See runner/readme.txt."
        )
    with open(WORKFLOWS_PATH) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            sys.exit(f"ERROR: workflows.json contains invalid JSON: {e}")

    if "workflows" not in data:
        sys.exit("ERROR: workflows.json is missing the 'workflows' section.")
    if "routing_signals" not in data:
        sys.exit("ERROR: workflows.json is missing the 'routing_signals' list.")

    for wf_id, wf in data["workflows"].items():
        if "steps" not in wf:
            sys.exit(f"ERROR: workflows.json — workflow {wf_id} is missing 'steps'.")
        for i, step in enumerate(wf["steps"], 1):
            if "agent" not in step or "task" not in step:
                sys.exit(
                    f"ERROR: workflows.json — {wf_id}, step {i}: "
                    f"each step must have 'agent' and 'task' fields."
                )

    return data


def load_config() -> dict:
    """Load runner_config.json. Exit with helpful message if missing."""
    if not CONFIG_PATH.exists():
        sys.exit(
            f"ERROR: runner_config.json not found at {CONFIG_PATH}\n"
            f"Copy runner/runner_config.json.example and fill in your settings."
        )
    with open(CONFIG_PATH) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            sys.exit(f"ERROR: runner_config.json contains invalid JSON: {e}")


def resolve_paths(config: dict, study_id: str) -> dict:
    """Resolve paths. study_path is derived from study_id (protocol_number)."""
    study_path = (PROJECT_ROOT / "studies" / study_id).resolve()

    if not study_path.exists():
        sys.exit(
            f"ERROR: Study folder not found: {study_path}\n"
            f"Expected: studies/{study_id}\n"
            f"Create the folder or check that the protocol number is correct."
        )

    study_config_path = study_path / "config" / "study_config.json"
    if not study_config_path.exists():
        sys.exit(f"ERROR: study_config.json not found at {study_config_path}")

    with open(study_config_path) as f:
        try:
            study_config = json.load(f)
        except json.JSONDecodeError as e:
            sys.exit(f"ERROR: study_config.json contains invalid JSON: {e}")

    config_protocol = study_config.get("study_identity", {}).get("protocol_number", "")
    if config_protocol != study_id:
        sys.exit(
            f"ERROR: Study folder mismatch — safety check failed.\n"
            f"  --study argument:           {study_id}\n"
            f"  protocol_number in config:  {config_protocol!r}\n"
            f"  These must match exactly. Wrong study data would be loaded."
        )

    return {
        "study": study_path,
        "agents": (PROJECT_ROOT / config["agents_path"]).resolve(),
        "workflows": (PROJECT_ROOT / config["workflows_path"]).resolve(),
    }


def parse_args(workflow_ids: list) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Hermes Runner — execute a Hermes workflow via the Claude API"
    )
    parser.add_argument(
        "--workflow",
        required=True,
        choices=workflow_ids,
        help="Workflow to execute",
    )
    parser.add_argument(
        "--study",
        required=True,
        help="Protocol number — must match the folder name and study_config.json protocol_number field",
    )
    parser.add_argument(
        "--data-drop",
        help="Data drop folder date in YYYY-MM-DD format (defaults to latest in data_drops/). Note: dates inside CSV files must use DD-MMM-YYYY format (e.g. 30-Sep-2027).",
    )
    return parser.parse_args()


def validate_study_package(paths: dict, study_id: str, data_drop_date: str) -> dict:
    """
    Validate the study folder exists and all critical files are present.
    Returns a context dict with validated paths.
    Exits with clear error if anything is missing.
    """
    sp = paths["study"]

    # study_config.json
    study_config_path = sp / "config" / "study_config.json"
    if not study_config_path.exists():
        sys.exit(f"ERROR: study_config.json not found at {study_config_path}")

    with open(study_config_path) as f:
        try:
            study_config = json.load(f)
        except json.JSONDecodeError as e:
            sys.exit(f"ERROR: study_config.json contains invalid JSON: {e}")

    # data_drop folder
    data_drops_root = sp / "data_drops"
    if data_drop_date:
        drop_path = data_drops_root / data_drop_date
        if not drop_path.exists():
            sys.exit(f"ERROR: Data drop folder not found: {drop_path}")
        print(f"  data_drop     : {data_drop_date}")
    else:
        # Find latest dated subfolder
        dated_folders = sorted(
            [d for d in data_drops_root.iterdir() if d.is_dir()],
            reverse=True,
        )
        if not dated_folders:
            sys.exit(f"ERROR: No data drop folders found in {data_drops_root}")
        drop_path = dated_folders[0]
        data_drop_date = drop_path.name
        print(f"  data_drop     : {data_drop_date} (latest, auto-detected)")

    # Critical files from manifest
    critical_files = [
        sp / "config" / "study_config.json",
        sp / "config" / "supply_network.json",
        sp / "config" / "policies.json",
        drop_path / "rtsm_actuals.csv",
        drop_path / "erp_inventory.csv",
        drop_path / "ctms_plan.csv",
    ]
    missing = [str(f) for f in critical_files if not f.exists()]
    if missing:
        sys.exit("ERROR: Missing critical files:\n" + "\n".join(f"  {m}" for m in missing))

    print("  study package : OK (all critical files present)")

    return {
        "study_id": study_id,
        "data_drop_date": data_drop_date,
        "drop_path": drop_path,
        "study_config": study_config,
        "study_config_path": str(study_config_path),
    }


def load_agent_prompt(agents_path: Path, agent_name: str) -> str:
    """Load an agent's system_prompt.md. Exit if not found."""
    prompt_path = agents_path / agent_name / "system_prompt.md"
    if not prompt_path.exists():
        sys.exit(f"ERROR: Agent system prompt not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def detect_signals(text: str, routing_signals: list) -> set:
    """Extract routing signal keywords from agent output text (whole-word match)."""
    found = set()
    for signal in routing_signals:
        if re.search(rf'\b{signal}\b', text, re.IGNORECASE):
            found.add(signal)
    return found


def build_user_message(
    workflow_id: str,
    study_context: dict,
    task_description: str,
    accumulated_outputs: list,
) -> str:
    """
    Build the user message for an agent call.
    Includes workflow context, file paths, task, and all prior agent outputs.
    """
    sp = study_context["drop_path"]
    config_path = study_context["study_config_path"]

    lines = [
        "## Workflow Context",
        "",
        f"- Workflow: {workflow_id}",
        f"- Study ID: {study_context['study_id']}",
        f"- Data Drop Date: {study_context['data_drop_date']}",
        "- Trigger: command-line invocation",
        "",
        "## Study Package File Paths",
        "",
        f"- study_config.json: {config_path}",
        f"- rtsm_actuals.csv: {sp / 'rtsm_actuals.csv'}",
        f"- erp_inventory.csv: {sp / 'erp_inventory.csv'}",
        f"- ctms_plan.csv: {sp / 'ctms_plan.csv'}",
        "",
        "## Your Task",
        "",
        task_description,
    ]

    if accumulated_outputs:
        lines += ["", "## Prior Agent Outputs", ""]
        for entry in accumulated_outputs:
            lines += [
                f"### {entry['agent']} output",
                "",
                entry["output"],
                "",
            ]

    return "\n".join(lines)


def call_agent(
    client,
    config: dict,
    system_prompt: str,
    user_message: str,
    step_label: str,
) -> str:
    """
    Call the Claude API with streaming. Print each chunk to terminal.
    Returns the full response text.
    """
    print(f"\n{step_label}")
    print()

    chunks = []
    with client.messages.stream(
        model=config["model"],
        max_tokens=config["max_tokens"],
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            chunks.append(text)

    full_response = "".join(chunks)
    print()  # newline after streaming ends
    return full_response


def run_workflow(
    client,
    config: dict,
    paths: dict,
    workflow_id: str,
    study_context: dict,
    workflow_data: dict,
) -> tuple:
    """
    Execute all steps in a workflow.
    Returns (accumulated_outputs, active_signals, run_log).
    """
    steps = workflow_data["workflows"][workflow_id]["steps"]
    routing_signals = workflow_data["routing_signals"]
    accumulated_outputs = []
    active_signals = set()
    run_log = []

    total = len(steps)

    # ── STEP 0: Run DI-12 Data Validation (NEW) ──────────────────────────────────
    # Execute DI-12 before any workflow steps to verify data integrity
    print("\nStep 0/DI-12 — Data Validation")
    print()

    from di_12_aggregate_data_query import AggregateDataQuery

    sp = paths["study"] / "data_drops" / study_context["data_drop_date"]
    rtsm_file = sp / "rtsm_actuals.csv"
    ctms_file = sp / "ctms_plan.csv"
    erp_file = sp / "erp_inventory.csv"
    config_file = paths["study"] / "config" / "study_config.json"

    # Handle case-insensitive filename (Site_Inventory.csv vs site_inventory.csv)
    site_inventory_file = sp / "site_inventory.csv"
    if not site_inventory_file.exists():
        site_inventory_file = sp / "Site_Inventory.csv"

    try:
        di12_query = AggregateDataQuery(
            str(rtsm_file), str(ctms_file), str(erp_file),
            str(site_inventory_file), str(config_file)
        )
        di12_output = di12_query.execute()

        # Check overall data integrity status
        integrity_status = di12_output.get("overall_data_integrity", "UNKNOWN")
        print(f"Data Integrity Status: {integrity_status}")

        if integrity_status == "FAIL":
            print("\n⚠️  CRITICAL DATA ISSUES DETECTED — Halting workflow")
            print("\nIssues:")
            for rec in di12_output.get("recommendations", []):
                print(f"  - [{rec['severity']}] {rec['message']}")
                print(f"    Action: {rec['action']}")

            run_log.append({
                "step": 0,
                "agent": "DI-12",
                "status": "halt",
                "reason": "Data integrity FAIL",
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            })

            return accumulated_outputs, active_signals, run_log

        if integrity_status == "WARNING":
            print("\n⚠️  WARNING: Data issues flagged (proceeding with caution)")
            for rec in di12_output.get("recommendations", []):
                if rec.get("severity") in ["HIGH", "CRITICAL"]:
                    print(f"  - [{rec['severity']}] {rec['message']}")

        # Add DI-12 output to accumulated outputs so agents can reference it
        accumulated_outputs.append({
            "agent": "DI-12",
            "output": json.dumps(di12_output, indent=2),
        })

        run_log.append({
            "step": 0,
            "agent": "DI-12",
            "status": "complete",
            "integrity_status": integrity_status,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        })

        print("✓ Data validation complete. Proceeding with workflow steps.")

    except Exception as e:
        print(f"ERROR running DI-12: {e}")
        run_log.append({
            "step": 0,
            "agent": "DI-12",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        })
        return accumulated_outputs, active_signals, run_log

    for i, step in enumerate(steps, 1):
        agent_name = step["agent"]
        task_description = step["task"]

        # Check if this step is conditional
        condition = step.get("condition")
        condition_signal = condition.get("requires_signal") if condition else None
        if condition_signal and condition_signal not in active_signals:
            print(f"\n[Step {i}/{total}] {agent_name} — SKIPPED (signal {condition_signal} not present)")
            run_log.append({
                "step": i,
                "agent": agent_name,
                "status": "skipped",
                "reason": f"Signal {condition_signal} not present",
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            })
            continue

        step_label = f"[Step {i}/{total}] {agent_name}"
        system_prompt = load_agent_prompt(paths["agents"], agent_name)
        user_message = build_user_message(
            workflow_id, study_context, task_description, accumulated_outputs
        )

        started_at = datetime.now(timezone.utc).isoformat() + "Z"
        try:
            output = call_agent(client, config, system_prompt, user_message, step_label)
        except anthropic.APIError as e:
            print(f"\nAPI ERROR on step {i} ({agent_name}): {e}")
            run_log.append({
                "step": i,
                "agent": agent_name,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            })
            break
        finished_at = datetime.now(timezone.utc).isoformat() + "Z"

        # Accumulate for next agents
        accumulated_outputs.append({"agent": agent_name, "output": output})

        # Detect routing signals
        new_signals = detect_signals(output, routing_signals)
        active_signals |= new_signals

        run_log.append({
            "step": i,
            "agent": agent_name,
            "status": "complete",
            "signals_detected": list(new_signals),
            "started_at": started_at,
            "finished_at": finished_at,
        })

        # Hard halt
        if "HALT" in new_signals:
            print(f"\nHALT signalled by {agent_name}. Stopping workflow.")
            break

    return accumulated_outputs, active_signals, run_log


def write_outputs(
    paths: dict,
    workflow_id: str,
    study_context: dict,
    accumulated_outputs: list,
    run_log: list,
) -> Path:
    """Write run outputs to outputs/YYYY-MM-DD/ under the study folder."""
    date_str = study_context["data_drop_date"]
    out_dir = paths["study"] / "outputs" / date_str
    out_dir.mkdir(parents=True, exist_ok=True)

    run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    prefix = f"{workflow_id}_{run_ts}"

    run_at = datetime.now(timezone.utc).isoformat() + "Z"

    # run_summary.md — last agent output (reporting agent)
    last_output = accumulated_outputs[-1]["output"] if accumulated_outputs else "(no output)"
    summary_path = out_dir / f"{prefix}_run_summary.md"
    summary_path.write_text(
        f"# {workflow_id} Run Summary — {date_str}\n\n{last_output}",
        encoding="utf-8",
    )

    # outputs.json — all agent outputs
    outputs_path = out_dir / f"{prefix}_outputs.json"
    outputs_path.write_text(
        json.dumps(
            {
                "workflow": workflow_id,
                "study_id": study_context["study_id"],
                "data_drop_date": date_str,
                "run_at": run_at,
                "steps": accumulated_outputs,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # audit_log.json — timestamped step log
    audit_path = out_dir / f"{prefix}_audit_log.json"
    audit_path.write_text(
        json.dumps(
            {
                "workflow": workflow_id,
                "study_id": study_context["study_id"],
                "data_drop_date": date_str,
                "run_at": run_at,
                "steps": run_log,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return out_dir, summary_path, outputs_path, audit_path


def main():
    workflow_data = load_workflows()
    args = parse_args(list(workflow_data["workflows"].keys()))
    config = load_config()

    api_key = os.environ.get(config["api_key_env"])
    if not api_key:
        sys.exit(
            f"ERROR: Environment variable {config['api_key_env']} is not set.\n"
            f"Run: export {config['api_key_env']}=sk-ant-..."
        )
    client = anthropic.Anthropic(api_key=api_key)

    paths = resolve_paths(config, args.study)

    print(f"\n[{args.workflow}] Hermes Runner — {args.study}")
    print("─" * 53)

    context = validate_study_package(paths, args.study, args.data_drop)

    steps = workflow_data["workflows"][args.workflow]["steps"]
    print(f"\nRunning {args.workflow} — {len(steps)} steps")
    print("─" * 53)

    accumulated_outputs, signals, run_log = run_workflow(
        client, config, paths, args.workflow, context, workflow_data
    )

    out_dir, summary_path, outputs_path, audit_path = write_outputs(
        paths, args.workflow, context, accumulated_outputs, run_log
    )

    print("\n" + "─" * 53)
    print("Run complete. Outputs written to:")
    print(f"  {summary_path}")
    print(f"  {outputs_path}")
    print(f"  {audit_path}")
    print()


if __name__ == "__main__":
    main()
