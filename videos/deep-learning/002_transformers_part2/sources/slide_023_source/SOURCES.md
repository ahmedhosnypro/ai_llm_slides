# SOURCES.md — slide 023 "Suggested Positional Encoders (Normalize Seq. Length to "1")"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_023_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner round 1) + live curl of two tutorial sources + one agy search.

## Slide identity

- New (curated) slide **023** ← old extraction **45** (old group split with new
  slide 022; kept frame `frame_01233.jpg`, the group's final state; shown
  t≈984–1232 s) (`unique_slides/slides_index.json`), frame
  `unique_slides/slide_023.jpg`.
- Frame facts (vision transcript): same three-row family as slide 022 — Word
  0…Word N-1 / Pos 0…Pos N-1 / third row now **0, δ, 2δ, 3δ, 4δ, 5δ, …, 1-δ,
  1** with red "+δ" curved arrows; badge "23". Bottom cyan panel: "Use
  δ=1/Seq. Length  First position Encoding=0, Last Position Encoding=1
  (Independent of Seq. Length)"; "Problems:" + three bullets:
  1. "δ Value depends on Seq. Length ( δ is small for long seq and large for
     short sequence )"
  2. "In other words, Encoding value of position # 4 in short seq will differ
     from position #4 in long seq (though they are same position)"
  3. "Position Encoding is scalar and Word embedding is vector (how to Combine
     them ?)"
  Mouse-cursor artifact over the third "+δ" arrow (recording artifact).

## Primary sources

1. **Kazemnejad, "Positional Encoding in Transformers"** —
   https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
   (live curl 2026-10-11, `scratch/webverify/kazemnejad_pe.html`). The blog
   explicitly poses this exact variant — "Another idea is to assign a number
   to each time-step … within the [0, 1] range" (agy-retrieved quote from the
   same page: "One of the problems it will introduce is that you can't figure
   out how many words are present within a specific range. In other words,
   time-step delta doesn't have consistent meaning across different
   sentences.") — the [0,1]-normalized index with length-dependent δ.
2. **Machine Learning Mastery positional-encoding tutorial** —
   https://machinelearningmastery.com/a-gentle-introduction-to-positional-encoding-in-transformer-models-part-1/
   (live curl 2026-10-11, `scratch/webverify/mlm_pe.html`). Verbatim: "If you
   **normalize the index value to lie between 0 and 1, it can create problems
   for variable length sequences as they would be normalized differently**."
3. **arXiv 1706.03762v7 §3.5** (same live-verified fetch as slides 021/022) —
   the d_model-vector resolution of Problem 3, unchanged from slide 022.
- agy search (2026-10-11) confirms the [0,1]-normalization variant and its
  length-inconsistency problem are a standard pedagogical step (Kazemnejad's
  own text; Alammar mentioned in the blog's references). agy's local file-path
  citations are its retrieval artifacts, not URLs — the page itself was
  fetched and is banked.

## What the source CONFIRMS

- The scheme (δ = 1/Seq.Length, first=0, last=1, "(Independent of Seq.
  Length)" as the design goal): Kazemnejad's [0,1]-range idea, MLM's
  "normalize the index value to lie between 0 and 1".
- Problem 1+2 (δ depends on length → same position #4 encodes differently in
  short vs long sequences): MLM verbatim ("normalized differently" for
  variable lengths); Kazemnejad verbatim ("time-step delta doesn't have
  consistent meaning across different sentences").
- Problem 3 (scalar vs vector): identical to slide 022's problem 3 — MLM
  ("a single number … is not used … each position/index is mapped to a
  vector"); resolution per §3.5 (same d_model).

## Figures used by this slide

- **None.** Course-original strawman diagram, sibling of slide 022's (row 3
  values differ). Nothing downloaded.

## Course-authored elements

- δ-notation ("Use δ=1/Seq. Length", "+δ" arrows, 1-δ penultimate box), the
  position-#4 short-vs-long example, the cyan Problems panel, badge "23".

## [?] Uncertain items

- none beyond slide 022's wording-level [?] (same status here): the three
  problems and the scheme are confirmed, exact slide wording is course-
  authored.

## Corrections

- none.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. This source
confirms/corrects DATA and records provenance; it never licenses inventing or
"improving" content the slide doesn't show.
