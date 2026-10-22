# SOURCES.md — slide 011 "Multi Head Self Attention of Word X₂" (five-head cascaded recap, Wide architecture)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Written 2026-10-11 by the Part II web-verification
worker.

## Slide identity

- Frame `unique_slides/slide_011.jpg`, badge numeral **11** (matches file id).
- Old extraction: slide 11 ← old 16 (`unique_slides/new2old_mapping.json`).
- **Cross-video child: 11 ← 001:43** (`slide_dependencies.json`) — recap of Part I's
  "Multi Head Self Attention of Word X2 'Wide' Architecture" slide. Per the
  cross-video recap rule, primary provenance = 001's record
  `../001_transformers_part1/slide_043_source/SOURCES.md`; only NEW visual
  differences were re-verified here. No script-12 raw existed for 011 at research
  time — the vision probe below is the frame-facts record of first instance.

## Vision transcript of record

- `transcripts/slide011_vision_2026-10-11.txt` — ONE default-route (`images`) probe,
  `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`; winner
  `images (round 1, attempt 1)`, degenerate events 0. Many micro-labels flagged
  [?] by the probe itself (tiny two-digit W codes, arc label, bottom-strip tail).

## Primary sources

- **Paper**: https://arxiv.org/html/1706.03762v7 — "Attention Is All You Need"
  (Vaswani et al., 2017), §3.2.2 "Multi-Head Attention" (verified live in 001's
  records and the fleet map, 2026-10-11).
- **Course "Wide/Narrow" vocabulary origin**: Peter Bloem, "Transformers from
  scratch" — https://peterbloem.nl/blog/transformers (verified live, per 001:43's
  record: Bloem's 2019 update added the wide/narrow section).
- **agy 2026-10-11** (`../scratch/agy_s011.txt`): the slide's two-digit superscript
  weight codes (W^01, W^11, W^12, W^21…) match NO published convention — ad-hoc/
  course-specific; the paper's standard is W_i^Q, W_i^K, W_i^V (subscript = head
  index, superscript = role).

## Figures used by this slide

**None — course-original "cascaded heads" composition** (same verdict as the
parent: 001:43's five-head diagram is course-original; the probe notes the STYLE
is reminiscent of Jay Alammar's annotated diagrams, but no published figure is
redrawn). Download decision: nothing downloaded.

## Composition match vs 001:43 (parent)

- MATCHES: five heads h=1..h=5 (course illustrates with h=5; paper uses h=8 —
  illustration choice, kept verbatim per the parent's record); per-head pipeline
  Dot Product → **Scaling by √d** (present here, as in the parent — the scaling
  ABSENT on slide 008 is by then introduced) → Soft max → ⊗ with V → Σ weighted
  sum; stage ovals "Similarity" / "Probabilities" / "Weighted SUM"; per-row
  K₁..K₄ / V₁..V₄ with the query word X₂ emphasized; "Wide" architecture
  (per-head projections of the full embedding, heads combined at the end).
- NEW/different on THIS frame (vs the parent record):
  - **Cascaded-panel rendering**: heads drawn as five overlapping rounded panels
    fanned back-right (h=1 front, fully detailed; h=2..h=5 successively
    simplified/occluded), joined by a large red curved arc — the parent drew the
    heads side-by-side. Course rendering choice; frame wins.
  - **k_i·q and the fraction k_i·q/√d** annotated on the arrows into Dot Product /
    Scaling (tiny, read consistently by the probe; the parent record had no such
    inline annotations) — visually confirms score = kᵢ·q scaled by 1/√d,
    i.e. paper §3.2.1 with d_k → d (course's d×d bookkeeping).
  - **W-matrix boxes with two-digit codes** (W_v^01 ×3 on inputs; W_0^11 ×3 and
    W_1^11/12/13 after Σ on h=1; W_0^2x/W_1^2x … per back panel): course-specific
    ad-hoc coding (agy: not a published convention). Role of each code
    (which is Q/K/V, whether first digit = head) NOT decodable at this
    resolution — **build-time zoom re-check required**; recreation reproduces the
    codes verbatim once read.
  - **No "Concatenated Vector 1×dH" / "Linear Transformation [T] dH×d" labels
    seen** by the probe (the parent frame carried them per 001:43's record). The
    post-Σ small boxes (W_0^11 …) likely embody concat→linear, but the labels are
    either absent or unreadable here — [?] build-time zoom re-check.
  - **Bottom sentence strip** (dashed container, tokens X₁..X₄ trailing right)
    with a small box read as "W^v" beneath X₂, four large translucent colored
    ellipses fanned around X₂, and a yellow translucent "beam" overlay sweeping
    to the last head's output (dashed red rectangle) — presenter-style emphasis
    overlays; the magnifier-cursor artifact over X₂ is a recording artifact.
  - **Red arc label** reads "1st Heads" [?] (could be "h Heads") — tiny italic;
    build-time re-check.

## What the sources CONFIRM (semantics)

- Wide multi-head attention: per-head projections of the (full-dimension)
  embeddings → per-head attention with scaling by √d → softmax → weighted sums →
  heads combined (concat then linear in the parent's explicit labels; the paper:
  MultiHead = Concat(head₁..head_h)W^O). Confirmed by §3.2.2 and Bloem's wide
  description (both in the parent record).
- h=5 on the slide vs h=8 in the paper — illustration choice (parent precedent,
  kept verbatim).
- No numeric data on the slide (d symbolic under √d; no values to recompute).

## Course-authored elements (do not "fix" to a source)

- Cascaded fanned-panel rendering, stage ovals, two-digit W codes, red arc,
  colored ellipses/beam overlays, colored token strips — all instructor's own.

## [?] Uncertain items (build-time zoom re-checks; no patches)

- [?] Exact two-digit codes on every W box (incl. whether "W_v^01" subscript is
  really "v", and the h=2..h=5 back-panel codes).
- [?] Arc label: "1st Heads" vs "h Heads".
- [?] Whether concat/linear stage labels exist on this frame (parent had them).
- [?] Bottom-strip trailing tokens beyond X₄ (blurred/occluded).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows; 001:43's record,
the paper, and Bloem confirm semantics/provenance. Micro-label disagreements are
recorded, never silently resolved.

## Script-12 raw cross-check (raw-verification worker, 2026-10-11 — raw landed
after this file's research; the record's frame facts were probe-based)

- `analysis/slide_011_raw.json` read in full (model `glm-5.3-flash`; old
  extraction 16; kept_frame frame_00387, 23 frames). Composition fully confirmed
  (five cascaded heads h=1..h=5 with per-head pipeline, red arc, beam, bottom
  input row with X₂ emphasized).
- [?] RESOLVED (arc label): raw reads "*h* Heads" — italic "h Heads" in blue
  (the asterisks are the raw's italics markup). The probe's "1st Heads" was a
  misread; resolved toward "h Heads" (matches the parent's label family).
- [?] NARROWED (W codes): raw reads the h=1 pipeline boxes as W_v^0..W_v^3
  [possibly W_k] and, on the diagonal band, five per-head triplets
  W_q^{<h>} / W_k^{<h>} / W_v^{<h>} for h=1..5 — i.e. the probe's "two-digit
  codes" are per-head W boxes with angle-bracket head superscripts plus small
  digit superscripts. agy's verdict (ad-hoc course codes, no published
  convention) stands; exact per-glyph states remain build-time zoom [?] with
  both reads now recorded.
- [?] RESOLVED (concat/linear labels): raw also sees NO "Concatenated Vector" /
  "Linear Transformation" labels on THIS frame — they are absent/occluded here
  (sibling 017 shows them explicitly). The record's finding is confirmed by a
  second independent read.
- [?] RESOLVED (bottom-strip trailing tokens): raw reads the bottom row as
  exactly X₁ X₂ X₃ X₄ (X₂ red, black dashed ellipse) — no trailing tokens
  beyond X₄ on this frame.
- Raw additions for the build: title sits at the BOTTOM of the slide (~89% y;
  bold serif; "Multi Head" red / "Self Attention of Word" black / X₂ red);
  head colors #F28B8B/#B9AEE3/#EDE87E/#8FE0A0/#F5B8B8; "Probabilities" oval on
  h=1 only; fraction K·q/√d annotated above the Scaling box and "K·q" at the
  Dot Product top-right; four ⊗ nodes (supports the topology count); dashed
  Y₁..Y₄ output boxes under the beam [?tiny].
- Script-13 final: NOT YET LANDED for 011. Corrections: none yet — verify against
  script-13 final when it lands.
