# DF-09 — Demand Baseline Updater

## Purpose

Write the approved new demand baseline back to the study package after a demand refresh has been confirmed. This skill updates the reference point that all future delta calculations will compare against.

---

## Owner

**Primary:** Demand & Forecast Analyst

---

## When This Skill Is Used

- After a demand refresh (WF-01) has been reviewed and approved by a human
- This is a post-approval step — it only runs after human sign-off

---

## Inputs

1. **Approved demand forecast** — The demand scenario that has been confirmed as the new baseline
2. **Current baseline** — The existing approved baseline in the study package
3. **Approval context** — Who approved it, when, and why

---

## Steps

1. **Archive the current baseline** — Save the existing baseline with a timestamp so the history is preserved
2. **Write the new baseline** — Replace the current baseline with the approved demand forecast
3. **Log the update** — Record the change with timestamp, approval reference, and reason for update
4. **Confirm the update** — Verify the new baseline was written correctly

---

## Output

- Confirmation that the baseline has been updated
- Reference to the archived previous baseline
- Audit log entry for the update
- Data source reference — data drop date, files used, and reporting period covered

---

## Notes

- This skill only runs after human approval — it is never triggered automatically
- The baseline history should be preserved so that trend analysis can compare across cycles
- This is the only skill that writes back to the study package — all other skills are read-only
- The baseline file location and archive path are defined in `study_config.json`. The baseline is stored as JSON in the study package config directory. Archived baselines are timestamped (e.g., `demand_baseline_2026-03-06.json`) and stored in the archive subdirectory.
- The updated baseline becomes the new reference for DF-03 (Demand Delta Calculator) in the next cycle
