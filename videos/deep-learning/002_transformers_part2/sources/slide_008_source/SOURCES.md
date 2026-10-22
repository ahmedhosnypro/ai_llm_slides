# SOURCES.md — slide 008 "Self Attention Mechanism (Linear Transformation of Inputs) — Self Attention of word X₂ w.r.t All words in Sentence (X₁, X₂, X₃, X₄)"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Written 2026-10-11 by the Part II web-verification
worker.

## Slide identity

- Frame `unique_slides/slide_008.jpg`, badge numeral **8** (matches file id).
- Old extraction: slide 8 ← old 8, **founder frame swap** ("kept frame_00097.jpg,
  mid-group state") — this frame is a mid-group state of the same slide family.
- **Cross-video child: 8 ← 001:33** (`slide_dependencies.json`) — recap of Part I's
  full self-attention dataflow slide. Per the cross-video recap rule, primary
  provenance = 001's record
  `../001_transformers_part1/slide_033_source/SOURCES.md`; only NEW visual
  differences were re-verified here.

## Vision transcript of record

- `transcripts/slide008_vision_2026-10-11.txt` — ONE default-route (`images`) probe,
  `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`; winner
  `images (round 1, attempt 1)`, degenerate events 0. Cross-checked against the
  pre-existing script-12 raw `analysis/slide_008_raw.json` — consistent on
  composition; micro-label disagreements recorded below.

## Primary sources

- **Paper**: https://arxiv.org/html/1706.03762v7 — "Attention Is All You Need"
  (Vaswani et al., 2017), §3.2 / §3.2.1 (verified live 2026-10-11; carried from
  001's slide-33 record and the fleet map).
- **Course notation source**: Peter Bloem, "Transformers from scratch" —
  https://peterbloem.nl/blog/transformers (verified live, carried from 001's
  record). The probe notes the diagram's *style* resembles Bloem's walkthrough,
  but the composition is course-authored (001:33 verdict: no published figure is
  redrawn).

## Figures used by this slide

**None — course-authored diagram** (hand-drawn lecture style). Download decision:
nothing downloaded (same as 001:33; no published figure is redrawn).

## Composition match vs 001:33 (parent)

- MATCHES: end-to-end dataflow for the queried word X₂ — left column of four
  embedding rows → W_k boxes → K₄..K₁ strips → tall gray "Dot Product" box →
  rotated-text "Soft max" bar → ⊗ multiply nodes fed by V₄..V₁ (right column via
  W_v boxes) → "Σ" box → green "Y" output strip; stage chips "Similarity" /
  "Probabilities" / "Weighted SUM"; bottom sentence row X₁..X₄ with X₂
  magenta-highlighted feeding both columns via green dashed curves; legend
  "(1×d) · W(d×d) = (1×d)", "d: Embedding Length"; emphasis overlays (large
  translucent blue circle around q/W_q; red block arrow at X₂; green arrow Σ→Y).
- Scaling (√d) is NOT on this slide — matches 001:33's deliberate course order
  (scaling introduced later at 001's 34–37).

## NEW vs the parent frame (001:33) / frame-level findings

- **Row alignment RESOLVED on this frame**: input rows read X₄,X₃,X₂,X₁
  top→bottom in BOTH the left (K) and right (V) columns, paired row-wise with
  K₄..K₁ / V₄..V₁ top→bottom (raw AND probe agree) — so each row pairs its own
  word with its own key/value. This resolves the ordering tension 001:33's
  SOURCES.md left open for ITS frame (input rows read X₁→X₄ there); 002's frame
  reads consistently.
- **W superscript [?]**: three independent reads disagree — 001:33 raw "^(1) [?]",
  002:008 raw "^(0)", this probe "^(1)". Best-supported reading on THIS frame is
  (1) (probe + 001's record), but the glyphs are tiny: **build-time zoom
  re-check required; frame wins.**
- **Query label [?]**: 002:008 raw reads "q₂", probe reads "q1"; semantics (title:
  "of word X₂"; X₂ highlighted) imply q₂. Build-time zoom re-check; frame wins.
- **Dot-product corner label [?]**: raw "K.q", probe "K..q", 001:33 "K₂q [?]" —
  almost certainly "K·q" with a middle dot; exact subscript state needs a
  build-time zoom re-check.
- **Output label**: this frame reads "Y" (raw + probe agree); 001:33 read "Y₂".
  If the build clones the parent component, adjust the label to the frame.
- **⊗ node count [?]**: raw says four ⊗ circles; probe clearly sees three with
  the fourth (V₄ row) partially obscured. Four expected by topology; build-time
  re-check.
- Cursor artifacts (white arrow over the second dot; red pointer near X₂) are
  recording artifacts, not slide content.

## What the sources CONFIRM (semantics behind the slide)

- Three-stage pipeline = paper §3.2.1 minus (not-yet-introduced) scaling:
  Similarity = Kᵢ·q dot products; Probabilities = softmax; Weighted SUM =
  Σᵢ pᵢ·Vᵢ (paper: output "computed as a weighted sum of the values"; Bloem:
  y_i = Σ_j w_ij·v_j).
- K and V from every word, q from the queried word (paper §3.2.2 projections
  W^Q/W^K/W^V; Bloem: every x_i produces k_i, v_i; q_i compared against all).
- Legend (1×d)·W(d×d)=(1×d) — row-vector times matrix yields row vector;
  dimension-verified numerically in 001:33's record (numpy check, 2026-10-11).
- No numeric data transcribed on the slide; no heatmap values to recompute.

## Course-authored elements (do not "fix" to a source)

- Clip-art colored-bar vector rendering, dashed green containers, yellow W boxes,
  gray Dot Product box, rotated "Soft max" bar, stage-pill wording, emphasis
  overlays, the legend box — all instructor's own.

## [?] Uncertain items (build-time zoom re-checks; no patches)

- [?] W superscript: (0) vs (1).
- [?] Query label: q₂ vs q1.
- [?] Dot-product corner label: K.q / K..q / K₂q.
- [?] Fourth ⊗ node visibility (V₄ row).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows; 001:33's record
and the paper confirm semantics/provenance. Micro-label disagreements are recorded,
never silently resolved.

## Script-12 raw cross-check (raw-verification worker, 2026-10-11)

- `analysis/slide_008_raw.json` re-read in full on disk (model `images`; old
  extraction 8; kept_frame frame_00097, 32 frames; meta carries
  `founder_frame_swap: true` — frame_00097 kept over the group's final frame,
  confirming this record's "mid-group state" note). The record above was already
  written against this raw; re-verification finds no drift. Raw sides exactly as
  recorded on the contested micro-labels: superscript "(0)" (possibly (1)),
  query "q₂", corner label "K.q", FOUR ⊗ multiply nodes, output strip "Y".
- [?] items unchanged (build-time zoom re-checks): W superscript (0) vs (1);
  q₂ vs q1; K.q / K..q / K₂q; 4th ⊗ node visibility.
- Script-13 final: NOT YET LANDED for 008. Corrections: none yet — verify against
  script-13 final when it lands.
