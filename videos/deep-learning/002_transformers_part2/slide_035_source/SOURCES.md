# SOURCES.md — slide 035 "Building Transformer Block" (transition/agenda: what gets added next)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_035_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner) cross-checked against `analysis/slide_035_raw.json` (raw
agrees: same three component lines + "Adding"). Web evidence from the
already-live banked paper fetch (`scratch/webverify/paper_v7.html`, quoted
verbatim below). No new agy query spent — this is a course-authored
transition slide whose three items are named constructs of the banked,
live-verified paper (same treatment as the verified dividers 003/050).

## Slide identity

- New (curated) slide **035** ← old extraction **102** —
  `unique_slides/new2old_mapping.json`, frame `unique_slides/slide_035.jpg`.
- Frame facts (vision transcript): title "Building Transformer Block" (red,
  bold); badge "35". Body is a four-line indented list only — "Adding" /
  "Residual Connections" / "Layer Normalization" / "Feed Forward Network"
  (all blue bold). NO diagram, no equations, no figures (explicit in the
  transcript). Artifacts: mouse cursor at the left edge of "Layer
  Normalization"; bottom letterbox bar.

## Slide role

Course-authored transition/agenda slide announcing the components to be
added around the Multi-Head Self-Attention block in the next slides (36 =
MHSA block input/output semantics, 38 = "Residual Connections and
Normalization" building the full composition). It precedes — and its three
items enumerate — the paper's sub-layer wrapping constructs.

## Primary sources (for the three named constructs)

**arXiv 1706.03762v7 §3.1 / §3.3** (live curl 2026-10-11, banked) — verbatim:
- "We employ a **residual connection** [11] around each of the two
  sub-layers, followed by **layer normalization** [1]. That is, the output of
  each sub-layer is LayerNorm(x + Sublayer(x)), where Sublayer(x) is the
  function implemented by the sub-layer itself." — items 1 and 2.
- "…the Transformer instead uses a **position-wise fully connected
  feed-forward network**." (§3.3 opening; full FFN equation on the video-2
  045 record) — item 3.
- Reference [1] = Ba, Kiros, Hoffer? — no: [1] = Lei Ba et al., "Layer
  Normalization" (arXiv:1607.06450); reference [11] = He et al., "Deep
  Residual Learning" (both verified in the paper's reference list within the
  same banked fetch and on the video-2 041/044 records).

## What the sources CONFIRM

- The three component NAMES are exactly the paper's sub-layer constructs in
  the order they wrap the attention block (residual → layer-norm around each
  sub-layer; FFN as the second sub-layer). The slide adds nothing beyond the
  names — nothing to correct.

## Figures used by this slide

- **None.** Text-only transition slide (vision-verified: no nodes, boxes,
  arrows, or insets).

## Course-authored elements

- Title, the "Adding" lead-in line, the three-item list, layout — all
  course-authored; keep verbatim for recreation; badge "35".

## [?] Uncertain items

- none.

## Corrections

- none.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. Sources
confirm/correct DATA and record provenance; they never license inventing or
"improving" content the slide doesn't show.
