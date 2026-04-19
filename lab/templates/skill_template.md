# [SKILL-ID] — [Skill Name]

<!-- ============================================================
     STUDENT INSTRUCTIONS
     Replace [SKILL-ID] and [Skill Name] in the title above.
     Then fill in each section below.

     A skill is a reusable procedure — it describes exactly how
     an agent solves one specific part of its job.

     Choose one skill to write from the list on your Scenario Card,
     or invent your own based on the study you configured.
     ============================================================ -->

## Purpose

<!-- TODO: In 2-3 sentences, describe what this skill does.
     Answer: "This skill exists to..."
     Example: "This skill compares the current demand forecast to the approved
     baseline and quantifies the gap. It answers the question: has demand changed,
     and by how much?" -->

TODO — Write the purpose of your skill here.

---

## Owner

<!-- TODO: Which agent uses this skill primarily? -->

**Primary:** TODO — e.g. Demand & Forecast Analyst

---

## When This Skill Is Used

<!-- TODO: In which workflow(s) is this skill applied? At what point in the process?
     Example: "During WF-01 (Demand Signal Refresh) after consumption analysis,
     when the agent needs to compare current demand to the baseline." -->

- TODO — Which workflow uses this skill (WF-01, WF-02, etc.)?
- TODO — At what point in the workflow is it called?
- TODO — What triggers its use? (e.g. "whenever the Demand Analyst needs to...")

---

## Inputs

<!-- TODO: List everything this skill needs to do its job.
     Include: data files, outputs from other skills, config values.
     Example:
     1. Current consumption rates — output from DF-01
     2. RTSM actuals file (rtsm_actuals.csv)
     3. Demand delta threshold — from study_config.json -->

1. TODO — First input (where does it come from?)
2. TODO — Second input
3. TODO — Third input (add or remove as needed)

---

## Steps

<!-- TODO: Write the step-by-step procedure for this skill.
     Think like a recipe: clear, numbered, sequential.
     Aim for 4-6 steps. Each step should be one clear action.
     Example:
     1. Load the RTSM actuals file and count records by event type
     2. Filter to dispensing events only
     3. Calculate average weekly dispensing rate per site
     4. Flag any sites with zero dispensing in the review period -->

1. TODO — First step

2. TODO — Second step

3. TODO — Third step

4. TODO — Fourth step

5. TODO — Fifth step (optional)

---

## Output

<!-- TODO: Describe what this skill produces. What information does it return?
     Example:
     - Demand delta by country, treatment arm, and item (absolute and %)
     - Direction of change (increase or decrease)
     - Overall study-level delta
     - Reference to source data used -->

- TODO — First output (what data/result does this skill return?)
- TODO — Second output
- TODO — Third output (add or remove as needed)

---

## Notes

<!-- TODO: Optional. Add any important caveats, limitations, or things the agent
     should know when using this skill.
     Example: "This skill calculates the delta but does not judge significance —
     that is done by DF-04 (Threshold Evaluator)." -->

TODO — Add any important notes, or delete this section if not needed.
