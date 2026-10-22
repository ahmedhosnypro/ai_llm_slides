# SOURCES.md — slide 007 "Parallelization / Implementation Issues" (section header)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Written 2026-10-11 by the Part II web-verification
worker.

## Slide identity

- Frame `unique_slides/slide_007.jpg`, badge numeral **7** (matches file id).
- Old extraction: slide 7 ← old 6 (`unique_slides/new2old_mapping.json`).

## Vision transcript of record

- `transcripts/slide007_vision_2026-10-11.txt` — ONE default-route (`images`) probe,
  `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`; winner
  `images (round 1, attempt 1)`, degenerate events 0. Cross-checked against the
  pre-existing script-12 raw `analysis/slide_007_raw.json` — consistent (raw also
  found nothing beyond title/badge/cursor).

## Frame facts (vision, ground truth)

- Title on two centered dark-red bold lines: "Parallelization" / "Implementation
  Issues"; badge "7" (yellow ellipse, purple/blue outline); otherwise EMPTY
  light-gray body in a thin dark-red border; black bottom letterbox; mouse-cursor
  artifact below "Parallelization". No diagrams, no equations, no bullets.

## Primary source

- **None on the slide — course-authored section header.** (agy 2026-10-11,
  `../scratch/agy_s007.txt`: the slide carries no figure; nothing to source.)
- **Section-content background (for the slides that follow, not shown here)** —
  Vaswani et al. 2017, arXiv:1706.03762, §3.2 + Table 1, verified live in the
  fleet map and re-confirmed by agy same day:
  - recurrent layers "generate a sequence of hidden states h_t as a function of
    the previous hidden state h_{t−1} … This inherently sequential nature
    precludes parallelization within training examples";
  - "a self-attention layer connects all positions with a constant number of
    sequentially executed operations" (Table 1: Self-Attention O(n²·d) per layer,
    O(1) sequential ops, O(1) max path length; Recurrent O(n·d²), O(n), O(n));
  - URL: https://arxiv.org/html/1706.03762v7 (PDF:
    https://arxiv.org/pdf/1706.03762.pdf).

## Figures used

- None. Nothing downloaded.

## What the source CONFIRMS / CORRECTS

- CONFIRMS: header wording is the course's section name for the parallelization
  topic; the topic's canonical data source is the paper's §3.2/Table 1 (recorded
  above so the follow-up slides can cite it).
- CORRECTS: nothing. No `[?]` items.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. House slide;
no web data enters the recreation.

## Script-12 raw cross-check (raw-verification worker, 2026-10-11)

- `analysis/slide_007_raw.json` re-read in full (model `images`; old extraction 6;
  kept_frame frame_00095, 4 frames). Fully consistent with this record: two-line
  red title "Parallelization" / "Implementation Issues", badge "7", otherwise
  empty body, cursor artifact below the first title line. Raw confirms there is
  NO other content (no bullets/diagrams/equations) — the §3.2/Table 1 background
  recorded above remains context for the FOLLOWING slides only.
- [?]: none. Corrections: none yet — verify against script-13 final when it lands
  (no final for 007 as of this pass).
