# SOURCES.md — slide 018 "Adding Position Information"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Vision transcript of record: `transcripts/slide_018_webverify.txt` (2026-10-11,
default `images` route, `--thinking high`, via `scripts/16_vision_gate.sh`).

## Slide identity

- Frame `unique_slides/slide_018.jpg`, badge "18" (timeline: t≈638–644 s, old
  extraction 29). No dependency edge; P2 membership starts at 20 (this slide
  is the two-approach agenda that INTRODUCES the Position-Information block).
- Frame facts (vision transcript, ground truth): title "Adding Position
  Information" (dark red); one white box, lower half, with exactly two lines:
  **"[1] Position Encoding"** ("[2] Position" dark blue, "Encoding" dark red)
  and **"[2] Position Embedding"** ("[2] Position" dark blue, "Embedding"
  magenta/purple). No diagram, no equations — a plain agenda slide.
- Video artifacts (do not recreate): presenter mouse cursor just below the
  title; bottom letterbox bar.

## Primary sources (verified live 2026-10-11)

- **Vaswani et al. 2017** — https://arxiv.org/html/1706.03762v7 §3.5
  (WebFetch-confirmed verbatim this session): "Since our model contains no
  recurrence and no convolution, in order for the model to make use of the
  order of the sequence, we must inject some information about the relative
  or absolute position of the tokens in the input sequence." /
  **"There are many choices of positional encodings, learned and fixed [9]."**
  — this sentence IS the slide's [1]-vs-[2] dichotomy at paper level.
  "positional encodings have the same dimension d_model as the embeddings, so
  that the two can be summed" (the dimension premise the following slides use).
- **[2] Position Embedding = learned/trainable variant** — carried from this
  video's verified slide-021 record (`../slide_021_source/SOURCES.md`, 2026-10-11):
  the trainable alternative is the learned position embeddings of
  BERT (arXiv:1810.04805) / GPT-1 (OpenAI tech report), agy-confirmed there.
  The course's own naming ("Encoding" vs "Embedding") splits exactly along
  the paper's fixed-vs-learned axis.

## Figures used by this slide

**None — course-authored agenda slide** (title + one two-line box; no
published figure is redrawn). Download decision: nothing downloaded into
this dir.

## What the sources CONFIRM

- The two named approaches correspond to the paper's "learned and fixed"
  positional-encoding choices (§3.5, verbatim). CONFIRMED.
- Both must be vectors of d_model added to the word embeddings (§3.5) —
  the premise of slides 019–026 (PE development block). CONFIRMED.
- Course branch naming: [1] Position Encoding → the course then develops the
  FIXED sin/cos PE (slides 019–026, paper §3.5 formula); [2] Position
  Embedding → the LEARNED variant (BERT/GPT-1 style; carried from the 021
  record). CONFIRMED as a faithful dichotomy.

## Course vs paper discrepancies (NOT defects — recreation keeps course form)

- None observed: a two-item agenda with no data content. The [1]/[2] numbering
  and the color coding (blue "Position", red "Encoding", magenta "Embedding")
  are course styling — frame wins.

## Open questions

- none. (Next slide 019 recap + 020 pre-processing + 021 "[1] Position
  Encoding" concept intro already verified — the agenda's [1] branch is
  developed there; a [2]-branch development slide does not appear in the
  curated deck's PE block per the existing verified records.)

## Script-12 raw cross-check (raw-verification worker, 2026-10-11 — raw landed
after this file's research; the record's frame facts were transcript-based)

- `analysis/slide_018_raw.json` read in full (model `images`; old extraction 29;
  kept_frame frame_00645, 7 frames). FULLY CONFIRMS the record with zero deltas:
  title "Adding Position Information"; white box with exactly two lines,
  "[1] Position Encoding" ("[1] Position" dark blue + "Encoding" dark red) and
  "[2] Position Embedding" ("[2] Position" dark blue + "Embedding" magenta);
  bracket-style manual numbering; badge "18"; cursor artifact below the title;
  no diagram/equations. Raw adds only color estimates (#0000A0/#CC0000/#CC00CC)
  — consistent.
- [?]: none (record's verdict unchanged). Corrections: none yet — verify against
  script-13 final when it lands (no final for 018 as of this pass).
