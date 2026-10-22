# FLEET_BRIEF_TEMPLATE.md — build-worker dispatch brief (deck 03)

Assemble each worker's dispatch prompt from this template. Substitute `NNN`,
the per-slide DEPS line, and the per-slide CONTENT LINES (derived from
`analysis/slide_NNN_final.json` + the original frame at dispatch time — never
from memory of another deck). Everything else is verbatim.

---

You are the build worker for slide NNN of
`/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/`.
Work autonomously to a certified single-version deliverable. You are the ONLY
worker on this slide; DB claims enforce that.

READ FIRST, in this order (they are binding law; the deck files OVERRIDE the
generic runbook wherever they differ):
1. `~/.zcode/skills/slide-recreation/SKILL.md` — the skill. Follow
   `references/building.md`, `references/judging.md`,
   `references/dependencies.md` (children only), and `references/patterns/`
   (index.json → the patterns your slide needs).
2. `/home/ahmed/Projects/ai_llm_slides/scripts/17_worker_instructions.md` —
   the worker runbook (DB milestones, render, self-check, judge, verdict law,
   resume rule, final report).
3. `/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md` —
   THIS deck's law (measured chrome, dependency graph, ZOOMED-judge-for-ALL).
4. `/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md` —
   the FROZEN judge templates. Source every `-p` payload byte-for-byte from
   there (substitute only NNN/K/region). Never hand-roll a judge prompt.

STATE:
- Content spec: `videos/machine-learning/03_ridger_regression_gradient_descent/analysis/slide_NNN_final.json`
  (verbatim-text law: text is VERBATIM, `[?]` markers preserved, never invent facts).
- Ground truth frame: `videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_NNN.jpg`
  (960×540, 1px = 1pt = 1/72in). Measure with PIL — geometry from measurement,
  never intuition.
- DB (run from `/home/ahmed/Projects/ai_llm_slides`):
  `VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py <cmd>`
  (claim/heartbeat/release/set/get; `set` takes THREE positionals; verify every
  write with a `get`). **NEVER invoke 15_progress.py without the `VIDEO=` prefix**
  — the default targets the CLOSED ml-intro deck's DB and a stray `set` silently
  corrupts another deck's certified rows (known incident class, 2026-10-19;
  if it ever happens, restore the foreign row from git and report it in your
  worker_report.md).

PROTOCOL:
1. `claim NNN <your-unique-id>` (stand down read-only if a FRESH peer claim
   exists; heartbeat every ~10 min of quiet phases; `release` at the end).
2. DB milestones as you go: `gen_status=building`, `build_script`,
   `pptx_path`, `visual_attempts`, `visual_check`, `visual_transcript`,
   `gen_status`, `last_error` on failure.
3. Build: `node videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_NNN.js`
   producing `recreated_pptx/slide_NNN_recreated.pptx` (plain name, single version).
   - House chrome: `require("../../shared_patterns/house_chrome.js").drawHouseChrome(pptx, slide, {numeral: NNN})`
     — THIS deck has NO top stroke (that is correct; do not add one).
   - hex colors never carry `#` in pptxgenjs; lineSpacing mandatory on multi-line
     text; measured geometry over intuition; never edit a certified component
     in place (copy-then-modify).
   - Equations (if any): matplotlib mathtext → 600dpi transparent PNG →
     `addImage()` at exact px/600 size; bank PNGs + `eq_NNN_*.json` sidecars
     (rel_id, image, mathtext, font_size_pt, color) under `recreated_pptx/build/assets/`
     for the post-certification OMML wrap (`scripts/18_omml_wrapper.py`).
   - Advanced graphs (if any): graphgen venv, topic-correct library, real data.
4. Render 150dpi (private scratch + OWN LibreOffice profile
   `-env:UserInstallation=file:///tmp/lo_slideNNN`; TMPDIR=
   `/home/ahmed/Projects/ai_llm_slides/scratch/tmp`), then run
   `python3 videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/house_chrome_check.py <render.png> NNN`
   — FAIL = fix the build BEFORE spending a vision call.
5. Judge — BOTH legs (founder directive: ALL slides get the zoomed judge):
   a. FULL-SLIDE comparison (Template A of judge_protocol_03.md), attempt K.
   b. ZOOMED CROP-PAIR certificates (Procedure B): ≥1 crop region covering the
      slide's densest content (one per dense region on multi-region slides);
      crop-vs-crop ONLY at matched effective scale (upscale the original crop
      by H_render/540, LANCZOS); bank pairs + transcripts under
      `recreated_pptx/qa/slideNNN/`.
   Bank `judge_prompt_K.txt` + `build_attempt_K.js` per attempt; verdicts only
   from real winner bodies; 3 garbage re-invokes; 6 attempts max then park
   `gen_status=failed` + `last_error` and STOP.
   Adjudication: judge findings are HYPOTHESES — PIL-measure against the
   original frame before fixing; refuted findings become judge context for the
   re-roll (judge variance is sampling). Inherited/cascade zones are
   adjudication inputs, never fix triggers.
6. Certification: full-slide PASS + all crop certificates clean (or
   PIL-adjudicated with banked refutation records) → DB `visual_check=PASS`,
   `visual_transcript=<path>`, `gen_status=passed`. OMML wrap happens
   POST-certification as a separate orchestrator pass (do not wrap yourself
   unless your brief says so).
7. `worker_report.md` in `qa/slideNNN/` + final message: slide id, attempts,
   final verdict, pptx path, transcript paths, one-line judge-flag summary.

DEPS: <"root — no dependencies; build free." | "child of M: import the certified
component `recreated_pptx/build/components/slide_MMM.js` (renderBase + per-block
exports with skip/only); never copy-paste; your parent is certified — its
pixels are law; child-local fixes only (copy-then-modify), never edit the
parent component. Special note for 13: inherit 12's table PATTERN, redraw at
13's measured position with 13's numbers. Special note for 17: chain 12→13→17
composes transitively.">

CONTENT LINES: <3-6 lines from the slide's own final JSON + frame: title,
layout regions, key visual elements (tables/equations/graphs with their
values), any founder/AGENTS.md notes. Workers verify against the spec anyway —
these are orientation, not authority.>

STORM RESILIENCE: on provider/upstream errors sleep 120s and retry up to 3×;
bank per step atomically; keep logs in project scratch (never host /tmp);
never abort the run; never delete banked evidence.

---

Dispatch law (orchestrator): waves are gated on the DB — a child dispatches
only when its parent shows `gen_status='passed' AND visual_check='PASS'`
(`15_progress.py deps` is the oracle; `buildable` is the dispatch list).
Roots: all 47 (pool-saturated batches of ~10-12). Children: 10 after 9;
13 after 12; 17 after 13; 18 after 17.
