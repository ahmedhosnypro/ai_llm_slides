# image-analysis — harness protocol (round-1 rules generalized; the audit-prompt-template.md in this directory is the canonical prompt artifact)

# Round-1 Analysis Protocol — harness/lane rules (NOT passed to vision models)

Companion to `ANALYSIS-PROMPT.md` (v2). Everything here is for the lane agents and the
orchestrator. The vision models must never see this file.

## Invocation
- Per capture, build the `-p` payload by injecting the VIEW/CAPTURE lines per the recipe
  at the top of ANALYSIS-PROMPT.md, then `cat`ing the model-facing portion.
- Record in each transcript's filename/header: view, story/context, width, model id,
  prompt version (currently **v2**).

## Multi-model runs
- Three script invocations per image, ONE model each, run as parallel background
  processes (`&` + `wait`), transcripts to separate files:
  1. default (no `--models`)
  2. `--models agy/gemini-3.8-flash-high`; on total failure retry ONCE with
     `--models gemini/gemini-3.8-flash` (note the fallback in the transcript header)
  3. `--models kr/claude-sonnet-4.5`
- A model that fails on an image after its fallback is recorded as failed for that
  image — never stall the lane on it.
- Degenerate/garbage bodies (all-bangs, off-topic chat) count as that model's failure
  on that image.

## Vocabulary evolution (the ONLY shared-file mutation)
- Lanes append to the "Issue vocabulary" section of ANALYSIS-PROMPT.md ONLY —
  append-only, never reorder/rewrite, `- [r1-<lane>] <name>: <rule>` format,
  dedup against existing entries AND categories (a)–(o) first (a near-duplicate is
  recorded as "confirms <tag>" in the lane's results file, not appended).
- Two sources of new entries: (1) the lane's own differential (a finding one model
  caught and others missed, DOM-verified), (2) the models' §9 VOCABULARY PROPOSALS —
  harvest them from transcripts, dedup, then append.
- Concurrency: re-read the file immediately before appending; prefer
  `echo '- [r1-…] …' >> <file>` (near-atomic). If the Edit tool reports the file
  changed underneath you, re-read and retry.

## Results files
- Per screen: `ai/plans/view-audit/round1/<screen>-results.md` — per image per model:
  verdict scores + defect register; merged consensus register (findings ≥2 models);
  unique findings with finder-model + DOM-verified REAL/HALLUCINATED classification;
  merged structural proposals; §9 proposals harvested; model reliability notes;
  the 3 worst problems.

## Round 2 preview (per the user's plan)
- After round 1 lands: the orchestrator reviews the prompt deltas + model catch rates,
  improves the analysis script, creates the `image-analysis` skill via skill-creator
  (self-improving, validated, with template md prompt files seeded from this round's
  artifacts), then freezes the prompt and runs round 2 analysis-only with NO model
  params (default model), including verification of round-1 findings against
  re-captures (the precision pass round 1 deliberately lacks).

## Standing constraints
- RAM lock for ALL agent-browser commands (`scripts/agent-browser-lock.py run --`).
- Ports: 5173 (app) and 6055 (storybook) live — never restart them; 6006 is SUR's —
  never touch. No code fixes in round 1. No git. No installs.
