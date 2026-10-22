# SOURCES.md — slide 006 "Traditional RNN  Seq2Seq model"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
ar5iv HTML (no vision calls run; no image access — frame facts below come from the
verified vision pass description of 2026-10-11 and the script-12 raw JSON).

## Slide identity

- New (curated) slide **006** ← old extraction slide **10** (diff 0.0)
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_006.jpg`
  (kept frame `frame_00282.jpg`).
- Frame facts (raw JSON, ground truth for WHAT is shown): title "Traditional RNN
  Seq2Seq model" (red, double space); yellow DECODER panel upper-right with
  "Decoder (RNN)" caption, three steps (o₁/o₂/o₃, softmax, green softmax bars,
  orange hidden bars, s₁/s₂/s₃, recurrent loops); peach ENCODER panel lower-left
  with "Encoder  (RNN)" caption (pink hidden bars, h₁/h₂, tan input bars,
  "embedding x₁/x₂/x₃", x₁/x₂/x₃); red curved context-vector arrow
  encoder-red-dot → decoder-red-dot; pink callout "Context Vector (of Whole
  Inputs)" tied to the encoder by a leader line. Mouse cursor below the title =
  recording artifact, omit on recreation.

## Primary source

- **URL**: https://ar5iv.labs.arxiv.org/html/1406.1078 (verified live 2026-10-11);
  paper: https://arxiv.org/abs/1406.1078
- **Paper**: "Learning Phrase Representations using RNN Encoder–Decoder for
  Statistical Machine Translation" — Cho, van Merriënboer, Gulcehre, Bahdanau,
  Bougares, Schwenk, Bengio (EMNLP 2014), arXiv:1406.1078.

## Figures used by this slide

- **Figure 1** — caption (verbatim, ar5iv): "An illustration of the proposed RNN
  Encoder–Decoder."
- **Downloaded into this dir**: `rnn_encdec.svg`
  (https://ar5iv.labs.arxiv.org/html/1406.1078/assets/rnn_encdec.svg,
  27,612 bytes, fetched 2026-10-11) — the paper's original Figure 1. Reference
  for topology/labels only; the course REDRAWS it in its own style (orange/yellow
  blocks, callouts). No pixel match is expected.
- This slide is the DEPENDENCY PARENT of slides 7, 8, 9 (`slide_dependencies.json`:
  7←6, 8←6, 9←6) and grandparent via its diagram of 10; those slides reuse this
  composition with deltas and reference this figure bank.

## What the source CONFIRMS (data behind the slide)

- **The topology**: paper Figure 1 = encoder RNN chain (x₁…x_T) → single context
  vector c → decoder RNN chain producing y₁…y_T′. The slide shows exactly this
  with a 3-step toy length.
- **The context vector**: abstract — one RNN "encodes a sequence of symbols into
  a fixed-length vector representation". §2.2 — the encoder "maps a variable-length
  source sequence to a fixed-length vector" and after reading the sequence "the
  hidden state of the RNN is a summary **c** of the whole input sequence" (Sec 4.4
  also calls c "the representation (c in Fig. 1)"). This confirms the slide's
  "Context Vector (of Whole Inputs)" callout is the paper's c, not an instructor
  invention.
- **State-arrow notation**: paper encoder hidden states are h⟨t⟩ and inputs x_t
  (matches the slide's h₁/h₂ and x₁/x₂/x₃); the paper's DECODER hidden state is
  h′⟨t⟩ and its outputs are y_t — see "Course-authored elements" for the s/o
  substitution.

## Course-authored elements (no paper counterpart — frame is ground truth)

- The symbol substitution: decoder states drawn as **s** (paper: h′) and decoder
  outputs as **o** (paper: y). Common textbook convention (e.g. d2l.ai); the slide
  wins for recreation.
- The color coding (yellow decoder panel, peach encoder panel, green/orange
  segmented cell bars), the red dots/curved arrow, the pink "Context Vector (of
  Whole Inputs)" callout box, and the caption placement ("Decoder (RNN)" above,
  "Encoder  (RNN)" below) are the course's redrawing, not paper pixels.
- Title wording "Traditional RNN  Seq2Seq model" (with the double space) and the
  numbered-badge chrome are course-level.

## [?] Uncertain items

- [?] Whether the paper figure itself (vs the text) labels the context vector "c"
  at the arrow position between the two chains — ar5iv HTML did not expose the
  figure's internal label text; `rnn_encdec.svg` (banked here) carries it for the
  build worker to inspect if ever needed. The slide does not print a "c" anyway;
  it speaks in words via the callout.
- [?] Exact handedness/shape of the recurrent feedback loops in the decoder (the
  frame pins them; the paper's figure is a different drawing style and cannot
  adjudicate).

## Corrections

none — raw transcription matches the source's data; no patch applied to
`analysis/slide_006_raw.json`.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
