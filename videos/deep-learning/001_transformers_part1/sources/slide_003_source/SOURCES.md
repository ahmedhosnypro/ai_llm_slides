# SOURCES.md — slide 003 "Transformers – Part I" (agenda)

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Researched 2026-10-11 by correction worker
W-A (no image access — frame facts below come from the script-12 vision pass
transcription in `../analysis/slide_003_raw.json`, ground truth for WHAT is shown).

## Slide identity

- New (curated) slide **003** ← old extraction slide **3**, diff 0.031,
  **swapped: true** (`unique_slides/new2old_mapping.json`; the `_meta` records
  `founder_frame_swap: true`, `original_kept_frame: frame_00065.jpg` — the
  founder swapped in a different frame of the same slide during curation).
  Frame `unique_slides/slide_003.jpg` (kept from `frame_00052.jpg`, 46–64 s).
- Frame facts (vision pass): agenda slide — red title "Transformers – Part I"
  top-center; four blue bold agenda lines (no bullet glyphs): "Processing
  Sequential Data" / "Transformer Building Blocks" / "Self Attention Mechanism"
  / "Multi-Head  Attention" (double space in the last); yellow badge "3"
  top-right; red frame; mouse-cursor artifact above line 2; empty lower ~40%.

## Primary source

- **Course-authored** (per `../SOURCES_MAP.md` §2 row "1–5": CONFIRMED
  course-authored, no external source expected). No paper is cited on the slide.
- **Lecture video**: https://www.youtube.com/watch?v=Ff8KU1dyJMA — "[11]
  Transformers - Part I", "Dr. Khaled Mostafa Elsayed", playlist
  "Deep Learning DSAI 308 Fall 2024 - Zewail" (verified live,
  `../SOURCES_MAP.md` §1).

## What the sources CONFIRM (agenda ↔ deck coherence)

- **Item 1 "Processing Sequential Data"** = the title of slide 004 (the very
  next slide) — direct deck-internal confirmation.
- **Item 3 "Self Attention Mechanism"**: three independent lines of evidence:
  1. The raw vision transcription of THIS frame reads "Self Attention Mechanism".
  2. The deck itself covers self-attention as a section (`../SOURCES_MAP.md`
     §2: slides 26–30, 34, 35, 37, 43, 44, 45 = self-attention / scaling /
     multi-head math from arXiv 1706.03762 §3.2).
  3. The lecturer says "self-attention" on the recording (auto-captions,
     ~33:40, fetched 2026-10-11 via yt-dlp); "soft attention" appears nowhere
     in the transcript.
- **Items 2 and 4** map onto the deck's later sections (building blocks →
  slides 6–19 encoder/decoder family; Multi-Head Attention → the multi-head
  section per `../SOURCES_MAP.md` and `../slide_dependencies.json`), consistent
  with a Part-I agenda.
- The lecturer does NOT read the agenda items aloud (checked the 0–170 s
  auto-caption window for this slide's 46–64 s screen time), so no verbatim
  spoken confirmation of the item wording exists.

## Course-authored elements (frame-only; do not "fix" from any web source)

- All four agenda lines' exact wording/spacing, the en dash in the title, the
  double space in "Multi-Head  Attention", and the mouse-cursor artifact are
  the deck's own; keep verbatim.

## [?] Uncertain items

- [x] RESOLVED 2026-10-11 (build worker, slide 003): the frame pixels were re-read
  through the vision gate (analysis, default images route) — transcript banked at
  `../recreated_pptx/qa/slide003/probe_original.txt`. It confirms line 3 reads
  "**Self** Attention Mechanism" (explicitly not "Soft") and confirms the double
  space in "Multi-Head  Attention". The [?] is closed with frame-pixel evidence;
  the spec's verbatim text stands unchanged.
- [?] Founders frame swap: the swap (frame_00065.jpg → frame_00052.jpg) means
  the analyzed frame may show a slightly different capture moment of the same
  static slide; text content is unaffected per the vision pass.

## Corrections

- **No JSON patches** (0). Nothing in the raw transcription was found
  erroneous; the "Soft vs Self" conflict resolves in favor of the existing raw
  transcription (see above) — a patch would change nothing.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). These sources confirm/correct DATA and record
provenance; they never license inventing or "improving" content the slide
doesn't show. If source and slide disagree, record the discrepancy above — the
slide wins for recreation, the source wins for understanding.
