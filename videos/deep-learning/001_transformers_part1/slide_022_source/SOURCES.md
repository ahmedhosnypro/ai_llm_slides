# SOURCES.md — slide 022 "Continuous bag-of-words (CBOW)   vs Skip-Gram Models" (architectures)

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via curl of the
ar5iv asset + byte comparison + SVG palette analysis (no image access — frame
facts come from the script-12 raw transcription `analysis/slide_022_raw.json`).

## Slide identity

- New (curated) slide **022** ← old extraction slide **47** (diff 0.0)
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_022.jpg`.
- Frame facts (raw transcription): title = "Continuous bag-of-words (CBOW)   vs
  Skip-Gram Models" (same string as slide 021's subtitle); two side-by-side
  blue-bordered panels each with a three-column network diagram — INPUT /
  PROJECTION / OUTPUT — plus yellow tag boxes "CBOW" (left) and "Skip-gram"
  (right); word labels w(t-2), w(t-1), w(t+1), w(t+2), w(t); SUM label over the
  CBOW projection square; mouse-cursor artifact near w(t-1) in the right panel.

## Primary source

- **URL**: https://arxiv.org/abs/1301.3781 — Mikolov, Chen, Corrado, Dean 2013,
  "Efficient Estimation of Word Representations in Vector Space" (verified live
  2026-10-11 via the ar5iv render https://ar5iv.labs.arxiv.org/html/1301.3781).
- The two diagrams are the paper's **Figure 1** redrawn and recolored.

## Figures used by this slide

- **Figure 1** — caption (verbatim, ar5iv render): "Figure 1: New model
  architectures. The CBOW architecture predicts the current word based on the
  context, and the Skip-gram predicts surrounding words given the current word."
- Original downloaded into this dir as **`efficient-models.svg`** (55,196 bytes,
  sha256 `788cbf471f136fa0b48d4091b1176a7bf15ef62fdbdce68097138d08763d46e4`,
  viewBox 612×432, ar5iv in-page id `S3.F1.g1`, displayed at 510×360 as
  `ltx_img_landscape`):
  https://ar5iv.labs.arxiv.org/html/1301.3781/assets/efficient-models.svg
  — re-fetched and compared byte-for-byte on 2026-10-11: **byte-identical**
  (same sha256). Note: this file landed in the dir during an earlier (aborted)
  worker run with no SOURCES.md; this record establishes its identity. Originals
  as downloaded — never renamed/deleted.
- Text labels in the original figure (readable in the SVG as `<use>` glyph runs;
  topology confirmed from the paper render): CBOW panel — INPUT column w(t-2),
  w(t-1), w(t+1), w(t+2); PROJECTION column with one square, label "SUM" above;
  OUTPUT column w(t). Skip-gram panel — INPUT w(t); PROJECTION one square;
  OUTPUT w(t-2), w(t-1), w(t+1), w(t+2). Panel tags "CBOW" / "Skip-gram".
  The slide reproduces ALL of these exactly.

## What the source CONFIRMS (data behind the slide)

- Figure identity and topology: four context inputs converge into a single
  projection (SUM) in CBOW; a single input fans out to four context outputs in
  skip-gram; the w(t±) label notation and the INPUT/PROJECTION/OUTPUT column
  headers are the paper's own.
- **The original figure is monochrome**: the ar5iv SVG's entire palette is
  strokes `#808080` (12 paths) and `#000000` (10 paths), glyph fill `#3c3c3c`,
  white background — no red/orange/green anywhere. The slide's dark-red INPUT
  containers, orange/peach PROJECTION, green OUTPUT, blue panel borders, and
  yellow tag boxes are therefore the **course's recoloring**, not paper data.
- The definitions on the preceding slide (021) and the paper §3.2/§3.1 text
  anchor the same two architectures this figure depicts.

## Course-authored elements (no paper counterpart — do not "fix" to paper)

- The recoloring listed above, the blue outer panel rectangles, the slide's
  frame/badge chrome, the title (taken from the tutorial-driven slide 021), and
  the two yellow "CBOW"/"Skip-gram" tag boxes as rendered (the paper labels are
  plain text under the panels). The mouse cursor is a recording artifact.

## [?] Uncertain items

- [?] Exact arrow geometry (converging vs fanning angles) is a layout fact only
  the frame can answer; the raw pins it (converge into SUM left / fan out right)
  and it is consistent with the paper figure.
- [?] Whether the projection square in the slide's skip-gram panel is unlabeled —
  the raw says unlabeled, which matches the paper's skip-gram projection square;
  frame-level confirmation stands with the raw.

## Corrections

none — every transcribed label (INPUT, PROJECTION, OUTPUT, SUM, w(t-2), w(t-1),
w(t), w(t+1), w(t+2), CBOW, Skip-gram) matches the paper's Figure 1 verbatim;
nothing to correct.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
