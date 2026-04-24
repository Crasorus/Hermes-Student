# Hermes Lab — Instructor Guide

A teaching companion for the 3-hour Hermes lab. Read this alongside `lab/student/student_guide.md`. The student guide is the recipe; this is your script.

Each module here has three parts:

- **Purpose** — what this module exists to do.
- **Concepts** — the teaching points you deliver at the start of the module and reinforce at the end.
- **Tips / Notes** — what you should watch for and call out while students are working.

---

## Before the Lab

**Lab summary in one breath.** Over three hours, students build the eighth member of the Hermes Clinical Supply Chain AI Agent Team — the *Optimization Agent*. They configure a fictional study, write at least three skills, an agent, and a workflow, then run the whole thing end-to-end. Not a single line of Python. Everything is Markdown and JSON.

**Audience.** Non-technical: life sciences, supply chain, clinical operations, business analysts. Assume no coding background. Do assume professional comfort with VS Code-level tools.

**What each student needs on their machine.**

- VS Code installed.
- The *Claude Code for VS Code* extension installed.
- An Anthropic API key already pre-configured in a `.env` file (you configure this, not them).
- The `hermes-lab.zip` starter kit extracted to a folder.
- A printed Scenario Card with their fictional study details.
- (Optional) The *Live Server* VS Code extension — makes the Study Data Creation GUI step smoother.

**Your prep checklist.**

- API keys distributed and tested on each machine before students arrive.
- `hermes-lab.zip` ready on a share, USB, or download link.
- Scenario Cards printed, one per student, with unique Study IDs (e.g. `STUDY-LAB-01` through `STUDY-LAB-10`).
- Confirm the default model is **Haiku** on every machine. Haiku is fast and cheap enough to survive 10 students for 3 hours; Opus is not.
- A fallback study (`9999999`) is packaged in the starter kit — know where it is so you can point stuck students at it.
- Have a terminal ready to demo `git reset --hard` and the zip-backup restore path.

**Rough timing map (≈180 minutes).**

| Module | Topic | Minutes |
| --- | --- | ---: |
| M0 | Setup | 15 |
| M1 | Architecture orientation | 20 |
| M2 | Configure your study (GUI + data drop + baseline chain run) | 50 |
| M3 | Meet the Optimization Agent | 15 |
| M4 | Write your skills | 40 |
| M5 | Write the agent | 30 |
| M6 | Define your workflow | 15 |
| M7 | Run the workflow chain | 15 |
| M8 | Review & discussion | 10 |

If you are over by M4, cut the skill target to 3 and keep moving. M7 is the payoff — never sacrifice it.

**Teaching philosophy — say this at the top of the class.**

- **Plan top-down, build bottom-up.** Read workflow → agent → skill to understand. Write skill → agent → workflow to build.
- **Markdown is the code.** There is no magic. The agents' intelligence is plain English in `.md` files. If you can write a clear instruction, you can write an agent.
- **Errors are the lesson.** When something fails, don't just re-run it. Read the error. That is where the learning lives.

---

## Module 0 — Setup (15 min)

### Purpose
Get every student's environment working: VS Code open, Claude Code responding, Haiku selected, starter kit in place. Nothing else in the lab works until this does.

### Concepts
- Claude Code is an AI pair-programmer that lives inside VS Code. Today it is also our runtime — it *is* how we run Hermes.
- Three models, three tradeoffs: **Haiku** (fast, cheap, good enough for running), **Sonnet** (best for design suggestions), **Opus** (strongest but slowest and most expensive). We use Haiku today.
- The API key lives in a `.env` file that the instructor pre-configured. Students never touch it.
- The starter kit is a snapshot of a working Hermes project. Students will modify it, not build it from scratch.

### Tips / Notes
- Walk the room and confirm every student has selected Haiku before Module 1 starts. Don't trust self-reports.
- Validate the API key by asking each student to type `What is Hermes?` in the Claude Code panel. A response means they're live. Silence means check the `.env`.
- If someone hits "API key not found", it's always the `.env` — quote marks, spaces, wrong path.
- Show them how to put the student guide into preview mode (right-click → Open Preview) and pin it side-by-side with Claude Code. They will flip between these two views constantly.

---

## Module 1 — Architecture Orientation (20 min)

### Purpose
Give students a mental map of Hermes before they build. They should leave this module able to point at a file and say which layer it belongs to.

### Concepts
- **The 5 layers**, top to bottom: *Runner → Workflows → Agents → Skills → Study Package*. Runner orchestrates; workflows sequence; agents specialise; skills do one thing; study package is the data.
- **Skills are a shared library**, not agent-owned. The same skill (e.g. SI-01) can be called by several agents. This is deliberate — it keeps the system small.
- **Every agent has the same shape**: a `README.md` and a `system_prompt.md`. Learn the shape once, apply it seven times.
- **What students are building today is the *prompt-only* version** of Hermes. A production version would use Anthropic's Agent SDK to make each agent autonomous with its own runtime, MCP connections to real data sources, and no human in the loop between steps. The markdown they write today becomes the system prompts in that production system. Say this out loud — it makes the lab feel like real engineering, not a toy.
- **The Grimoire** (`Hermes_Grimoire.md`) is the encyclopedia. It answers "what is X?" faster than Claude can.

### Tips / Notes
- Don't lecture the architecture — let them find it. The Explore Activity (skill → agent → workflow) is doing the work; your job is to answer "where is X?" questions quickly.
- At the end of the module, ask three students to define agent / skill / workflow in one sentence each. If they can't, stay here another five minutes. Don't move on.
- Common confusion: students think each agent "owns" its skills. Correct this immediately — skills live in one shared folder.

---

## Module 2 — Configure Your Study (50 min)

### Purpose
Students create a real, working study package from their Scenario Card, generate test CSV data, and run a baseline end-to-end chain against it. By the end they have a functioning Hermes study and three output files to compare their own agent against later.

### Concepts
- **Hermes is system-agnostic.** It does not talk to ERP or RTSM systems. It reads CSV/JSON "data drops" that any source can produce. This is what makes it portable across studies and sponsors.
- **The study package is three config files** (`study_config.json`, `supply_network.json`, `policies.json`) plus **dated data drops** (`data_drops/YYYY-MM-DD/`). The date format is not decorative — the runner uses it to find the right drop.
- **`/preflight`** is the integrity gate. It catches 90% of problems at their source — missing files, malformed JSON, broken references — before they become confusing agent errors 20 minutes later.
- **`/init-study`** and **`/run-workflow-chain`** are examples of *slash commands* — reusable recipes that live in `.claude/commands/`. They are part of the framework, not magic.
- **Running the baseline chain (WF-01 → WF-02 → WF-05) gives students a reference output.** When their own agent runs in M7, they have something to compare against.

### Tips / Notes
- **The single biggest time sink of the whole lab is ID mismatches.** `ARM-A` vs `ARM_A`. `SITE-01` vs `Site-01`. Item IDs in the CSVs that don't match item IDs in `study_config.json`. Call this out *before* they start, not after they break. Tell them: "If you get a weird error in M7, 90% of the time it's an ID typo in M2."
- Students will try to save browser downloads directly into `studies/<STUDY_ID>/config/`. They can't — the browser always writes to Downloads. Pre-warn them and show the move step once.
- They will close the browser tab and lose their study data. Teach them the **Load Config** buttons in the GUI sidebar before they need them.
- Run `/preflight` after every config change, not just at the end. Make this a reflex.
- When they get to "Run a full workflow chain" — let them watch it. The theatre of agents calling each other is part of the sell. Don't rush it.
- When the runner asks to save outputs, remind them to say **yes**. Saved outputs are the before-picture for M7's after-picture.
- **Fallback:** if a student is hopelessly stuck at M2, use the bundled study `9999999` and skip them ahead to M3. Don't let a student drown in config for 40 minutes.
- Before leaving this module, have every student commit or zip-backup their work. A `git add -A && git commit -m "lab baseline"` here will save someone's skin in M5.

---

## Module 3 — Meet the Optimization Agent (15 min)

### Purpose
Students switch from "configure existing Hermes" to "design a new agent". They read the brief and plan their agent on paper before touching any file.

### Concepts
- **Read the brief, then plan, then build.** In that order. The brief describes *what* the agent should do; the design decisions of *how* are theirs.
- **The one-sentence test.** If a student can't describe their agent's purpose in one sentence, the scope is too wide. Keep cutting until one sentence fits.
- **There is no single correct answer.** Two students will design differently-shaped agents that both work. This is the point of the lab, not a bug.
- **Plan before you type.** Paper or a scratch note is faster than a file and forces brevity.

### Tips / Notes
- Resist the urge to share a "reference design" early. The design decisions *are* the lesson.
- Walk the room during planning. Ask each student: "Say your agent's purpose in one sentence." If they can't, stay with them until they can.
- If someone asks "how many skills should I have?" — answer "three to five, and start with three". Don't give a number beyond that.
- Flag the brief's ambiguity as a feature: clinical problems in real life come in exactly this shape.

---

## Module 4 — Write Your Skills (40 min)

### Purpose
Students write at least three skill files. By the end of this module, each of those skills should (a) read one input, (b) do one analysis, (c) return one kind of finding.

### Concepts
- **A skill is a reusable procedure.** It answers four questions: what do I analyse, what do I read, what steps do I follow, what do I return.
- **Seven sections, always.** Purpose, Owner, When Used, Inputs, Steps, Output, Notes. The template in `lab/templates/skill_template.md` is the shape — don't freelance it.
- **Single responsibility.** One skill, one job. If a skill name contains "and", it's two skills.
- **Name skills with verbs.** `detect_`, `flag_`, `calculate_`, `identify_`. Verbs force single responsibility. Nouns let you hide multiple jobs behind one name.
- **Build one, then test it.** Write OA-01, ask Claude to summarise it, fix the issues, *then* write OA-02. Don't write five skills and debug a wall.
- **What good looks like.** A skill's output should be phraseable in one human-actionable sentence: *"Depot APAC-01 holds 14 weeks of ARM-A stock against an 8-week target — flag as OPTIMIZATION_OPPORTUNITY."* If it can't be phrased that crisply, scope is too broad.

### Tips / Notes
- Push back when a skill does two things. If a student writes "detect near-expiry lots **and** recommend action", split it into two skills (detection, then recommendation). This is the single most important correction you'll make in this module.
- When a student shows you a bullet-salad skill, read it back to them and ask "what does this skill *return*?" If they hesitate, the skill isn't done.
- Claude will happily rewrite a skill into something more "comprehensive". Teach students to push back: *terse beats comprehensive*.
- If a student is wrestling with syntax, have them copy an existing skill (`SI-01`, `AI-01`) and adapt. A blank page is the hardest place to start.
- **Pacing check.** If the room is behind at the 20-minute mark, drop the target to three skills and move on. M7 is the payoff.

---

## Module 5 — Write the Agent (30 min)

### Purpose
Students assemble their skills into an agent with a clear identity, a procedure, and a routing vocabulary. By the end the agent folder exists with both `README.md` and `system_prompt.md` complete.

### Concepts
- **An agent is six things**: identity, skills table, procedure, output format, halt conditions, rules. Miss any of these and the agent feels broken.
- **An agent only "knows" the skills listed in its Skills Table.** A skill file existing on disk is not enough. This is the single most common silent failure.
- **Routing signals are the agent's vocabulary to the next step.** Today we use `OPTIMIZATION_OPPORTUNITY`, `CRITICAL_WASTE_RISK`, and `NO_ACTION`. Each must be emitted deliberately — `NO_ACTION` is an answer, not an error.
- **The system prompt is prose, not a spec sheet.** Write instructions to a smart colleague, not a compliance document.
- **Halt conditions keep the agent safe.** Be generous with them. A halt is cheap; a bad output isn't.

### Tips / Notes
- Have each student read their Skills Table aloud to you. If they listed OA-05 but didn't write OA-05, catch it now. If they wrote OA-05 but didn't list it, catch that too.
- Recommend starting from `agents/demand_analyst/system_prompt.md` as a copy-edit source. Blank pages kill momentum.
- Check that the agent folder is named **exactly** `optimization_agent`. Not `Optimization_Agent`, not `optimisation_agent`. M6 will fail loudly if it's wrong.
- When a procedure step says "analyse stock" without naming a skill, push back — every procedure step should name the OA-0X skill it runs.
- Ask: "When does your agent emit `CRITICAL_WASTE_RISK`?" If the student can't point to a rule in their system prompt, it won't happen.

---

## Module 6 — Define Your Workflow (15 min)

### Purpose
Students wire their agent into the runner by registering it in `workflows/workflows.json`. By the end, `WF-OA-01` is defined and the three new routing signals are registered globally.

### Concepts
- **The workflow is the orchestration layer.** It says *which agent runs, in what order, with what task*. It does not contain the intelligence — that lives in the agent and its skills.
- **Signals live in two places.** The global `routing_signals` array (so the system recognises them) and the agent's system prompt (so the agent knows when to emit them). Miss either and signals vanish silently.
- **JSON is unforgiving.** One missing comma, one stray bracket, and the whole file is broken.
- **The `"agent"` field must match the folder name exactly.** Case-sensitive, character-for-character.
- **The `"task"` field is a concrete instruction**, not a mission statement. "Analyse depot network for optimisation opportunities and emit OPTIMIZATION_OPPORTUNITY when excess stock exceeds the max-weeks policy" beats "do optimisation".

### Tips / Notes
- Teach them to trust VS Code's red squiggles. A squiggle on save is cheaper than a cryptic runner error five minutes later.
- When a student says "it won't run", the first thing to check is always JSON validity — not their agent, not their skills.
- Show the "add signals to the global array" step twice. Students consistently forget this half.
- If Claude Code rewrites `workflows.json` and accidentally removes an existing workflow, catch it before save. Ask Claude to "add" not "rewrite".

---

## Module 7 — Run the Workflow Chain (15 min)

### Purpose
The payoff. Students run their own agent end-to-end against their own study and read the output critically. By the end, every student has a file in `outputs/` with at least one finding that came from a skill they wrote.

### Concepts
- **End-to-end matters.** Running WF-01 followed by WF-OA-01 proves the whole chain works — from study config, through the Supervisor's validation, into the student's own agent.
- **"Completed" does not mean "correct".** A workflow can complete with empty findings. Always open the output and read it.
- **The follow-up-question step is where the real insight lives.** Ask the agents things like "what happens if we close site X?" or "what's the impact of quarantining lot Y?". This is the demo moment — don't skip it.
- **Design with Sonnet, run with Haiku.** Save tokens during execution; use the smarter model when you want better design suggestions.

### Tips / Notes
- **The first run will fail for at least one student.** Make this public. Triage the error aloud so the whole room learns.
- Most failures at this stage are ID mismatches from M2, a skill file not listed in the agent's Skills Table from M5, or JSON errors in M6. Walk that list.
- When the output is empty (agent emits `NO_ACTION`), check the thresholds in the skills before "fixing" it. Sometimes the data really is fine.
- Each run creates a new dated output folder, so students can re-run freely and diff their results. Encourage this.
- Spend real time on the BONUS questions. This is where students feel what an agentic system is actually good for.

---

## Module 8 — Review & Discussion (10 min)

### Purpose
Surface the diversity of student designs, compare to the reference, and extract at least one takeaway each student could apply at work.

### Concepts
- **Comparison is the point**, not ranking. Two valid designs will disagree. Which one is "right" is often a question of judgement, not correctness.
- **`NO_ACTION` is a valid result.** An agent that says "nothing to flag" after reading the data correctly is doing its job.
- **One takeaway you would apply at work > a flawless implementation.** The goal of the lab is not a perfect Optimization Agent. It's a working mental model of how agentic systems get built.

### Tips / Notes
- Have **two or three** students share their output — not all ten. Pick ones with visibly different designs so the contrast is instructive.
- Good debrief prompts to pose:
  1. "If you started over, what would your first skill be instead?"
  2. "Where in your day-to-day work could this kind of agent live?"
  3. "What's one thing Claude did *for* you that you should probably do yourself next time?"
  4. "If you had another 30 minutes, which halt condition would you add?"
  5. "What surprised you about the output — good or bad?"
- Close with the production-vs-prompt-only distinction again. What they built today becomes the system prompts for an Agent-SDK system tomorrow.

---

## Common Failure Modes (and where they surface)

| Symptom | Usually caused by | Surfaces in |
| --- | --- | --- |
| "Study not found" | Study ID typo in command vs `study_config.json` | M2 / M7 |
| "Data drop not found" | Folder date not in `YYYY-MM-DD` format, or wrong date passed | M2 / M7 |
| Agent completes with empty output | A skill wasn't listed in the Skills Table (silently ignored) | M7 |
| "Agent not found" | Agent folder name ≠ `"agent"` value in `workflows.json` | M7 |
| JSON parse error on run | Missing comma or bracket in `workflows.json` | M6 / M7 |
| `NO_ACTION` unexpectedly | Missing CSV in data drop, or thresholds too forgiving | M7 |
| Weird analysis results in M7 | ID mismatch between config and CSVs | M2 (root) / M7 (visible) |
| API key not found | `.env` has quotes, spaces, or is in the wrong folder | M0 |

## If You Fall Behind

- **Drop stretch exercises.** They're optional for a reason.
- **Cut the skill target from "3–5" to exactly 3.** Quality of three beats rushed five.
- **Use study `9999999` as a fallback** for anyone stuck in M2. Skip them ahead; their agent will still run.
- **Shorten M8 to 5 minutes.** One student shares, everyone takes one lesson home.

## Restore Path for a Broken Repo

If a student has wrecked their lab kit by M5 and can't recover:

1. If they committed at the end of M2 (they should have): `git reset --hard <commit-sha>` then re-do M3–M5. Faster than it sounds.
2. If they didn't commit: unzip the backup copy of `hermes-lab.zip` into a fresh folder and re-open in VS Code. They'll lose their config work but keep the Scenario Card — the GUI will rebuild in 10 minutes using **Load Config**.
3. As a last resort, give them a paired partner for M5–M7 and make them the "tester" role. They'll learn the lab from the other side.

---

## One Last Thing

The best version of this class is one where students leave slightly dangerous. They should be able to go back to their real job on Monday and say: *"We could build one of these for our team."* Calibrate toward confidence, not completeness.
