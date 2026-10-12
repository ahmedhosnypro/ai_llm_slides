---
name: slide-recreation
description: >-
  Recreate lecture/course slides (from video frames or slide images) as high-fidelity
  PPTX files — full pipeline: frame extraction, phash dedup, vision analysis, text
  validation, pptxgenjs build, render-vs-original visual judging, professional 2D math
  equations, AI-algorithm-generated graphs, and progress tracking. Use whenever the task
  involves generating, recreating, or batch-producing PowerPoint slides from existing
  slide images or video — even if the user just says "make slides from this video" or
  "fix the equations/charts on this slide". Also covers judging/validating rendered
  slides against originals and embedding matplotlib equations or sklearn/matplotlib
  graphs into pptx builds.
---

# Slide Recreation — video frames to judge-certified PPTX

End-to-end pipeline for turning a lecture video (or a folder of slide images) into
individually-certified PowerPoint recreations. Built and battle-tested on a 64-slide
ML course deck; every rule below was paid for by a real failure.

**This skill is self-learning.** Before starting any task in this domain:

1. Read `memory/lessons.md` and `memory/incidents.md` (in this skill's dir) — they hold
   mistakes and fixes newer than this document.
2. When you finish a task (or hit a novel failure), APPEND what you learned to those
   files per the protocol in `memory/README.md`. Never edit SKILL.md or references/*
   during a task — new knowledge goes into `memory/` only. That is how the skill evolves.

## Reference map (read on demand, not upfront)

| Read this | When |
|---|---|
| `patterns/index.json` + `references/patterns.md` | **FIRST, before every build** — the reusable example-script library (`../patterns/`, one runnable script per pattern; laws in the comments). Read the index, use the applicable patterns, run their companion checkers. `references/patterns.md` is the pointer doc. Each recreation MUST also run the pre-judge checks in `scripts/17_worker_instructions.md` |
| `references/pipeline.md` | Extracting frames, deduping slides, analyzing + validating specs |
| `references/dependencies.md` | Decks whose slides build on each other (founder dependency graph): build gating on parent certification, shared component imports (u-components model), DB `depends_on` tracking |
| `references/building.md` | Writing the pptxgenjs build, rendering, house template law |
| `references/judging.md` | The visual judge — verdict law, walls, ground rules |
| `references/equations.md` | Any slide containing math — 2D format rule + alignment law + OMML |
| `references/graphs.md` | Slides with charts/plots — generated-graph two-version rule |
| `references/operations.md` | Model endpoint quirks, retry patterns, coordination traps |

## The pipeline at a glance

```
video ──fps 1──▶ frames ──phash dedup──▶ unique_slides ──vision analysis──▶ raw specs
      ──text validation──▶ final specs ──content gate (score≥8)──▶ build (pptxgenjs)
      ──render (LO headless→pdftoppm 150dpi)──▶ closed-loop PIL checks
      ──visual judge (render vs original)──▶ PASS = done | FAIL = fix loop
      ──post-passes──▶ equations (2D + OMML) / graphs (generated images)
      ──all slides PASS──▶ final-deck merge (byte-verbatim OPC) ──0/N pixel gate──▶ deck closed
```

Non-negotiable laws (each is expanded in its reference file):

- **HARD STOP after unique-frame extraction: a HUMAN must review the extracted unique
  frames before ANY later processing.** After `11_unique_slides.py` produces
  `unique_slides/`, STOP — no analysis (script 12), no validation, no builds, no
  subagent dispatch on those frames until the founder (or the human reviewer) has
  reviewed and approved the set. This is non-negotiable (founder directive
  2026-10-10): curation decisions (duplicate/non-valid frames, numbering, badges) are
  human-owned. The machine may prepare a review packet (contact sheet, index,
  new2old mapping) but must never mark the set approved itself.
- **Dependent slides gate builds on parent certification and share components**
  (founder directive 2026-10-11, `references/dependencies.md`). When a deck's
  founder-supplied dependency graph says slide B builds on slide A, B's BUILD is
  blocked until A is judge-certified (analysis/validation stay unblocked, and
  siblings unblock together). B's build must IMPORT A's certified composition as a
  shared component module (`build/components/`, u-components model) and draw only
  its own delta — never copy-paste the parent. Components are certified
  single-source-of-truth: editing one re-opens its whole descendant subtree.
- **A slide is done ONLY with a real comparison-transcript PASS from the vision model.**
  Timeouts, empty streams, and programmatic checks count as FAIL. A "looks fine" from
  yourself or a peer is not a verdict.
- **Never invent content.** Spec text is verbatim; uncertain content keeps its `[?]`
  marker. Fidelity of content and visualization is the whole point.
- **Match the original's measured geometry, not your intuition.** The original frame is
  960×540 px and 1px = 1pt in the build. PIL-measure ink edges in the original and
  closed-loop-verify your render against them (~4px tolerance at 150dpi) BEFORE judging.
  A judge PASS does not waive geometric checks — founder feedback overrides judges on
  placement defects.
- **Never delete banked evidence** — per-attempt builds, transcripts, renders, pre-fix
  backups, archived runs. Overwrite nothing certified; copy-then-modify.
- **Every deck closes with a combined all-in-one deck** (founder directive 2026-10-12).
  When the last slide certifies, merge the certified per-slide decks via
  `patterns/final-deck-merge/` (byte-verbatim OPC merge — never re-encode certified
  content), gate it at 0/N mismatched pages (merged render vs every source render, one
  LO session), and deliver `<video>_final.pptx` + md5 + banked gate report. The
  per-slide certifications are NOT the end of the program: a deck is closed only when
  the combined deck passes the merge gate. Certified working precedent:
  `videos/deep-learning/002_transformers_part2/scratch/merge_final_002_RUNBOOK.md`.
- **Always stream** vision-model requests; non-streaming dies at the upstream gateway's
  ~60s cut.

## Model routing (this project's concrete setup)

- Vision model `images` via local router `http://localhost:17844/v1`, key in
  `.analyze-image-key` (mode 600), all calls through the flock gate
  `scripts/16_vision_gate.sh` (never a raw curl), default route — no `--models` flag.
- Text validation model `glm-5.3`. If it returns empty content: re-run. If it burns the
  whole token budget reasoning (`finish_reason=length`, `content=null`): raise
  `IR_MAX_TOKENS` env (32000–65536 proven).
- Web research via the agy CLI: `agy -p "<query>"`; on 401/403 run `agy -p "hi"` once
  to refresh the token, then retry.

## Worker protocol for batch recreation

One slide = one worker, end to end. Per-slide instructions live in
`scripts/17_worker_instructions.md` (the binding contract — build pattern, judge
template, alignment law, DB updates). The DB (`scripts/15_progress.py`, `VIDEO=<id>`)
tracks every milestone; update it after every step, and a watchdog re-reads it to
recover dead workers. Workers MUST use the claim/heartbeat liveness contract
(`claim`/`heartbeat`/`release` on 15_progress.py; liveness is read via `sweep` — never
inferred from file mtimes; see `references/operations.md`). Copy that worker-instruction
pattern when applying this skill to a new project rather than re-deriving it.

## After every task

Append to `memory/` (see `memory/README.md` for format):
- What failed and the measured fix (lessons.md)
- Coordination/incident notes if a trap repeated (incidents.md)

That append is part of the task's definition of done — the next session's accuracy
depends on it.
