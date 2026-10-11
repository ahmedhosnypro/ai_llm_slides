# SOURCES.md — slide 021 "Word Embedding" (CBOW vs Skip-Gram definitions)

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via agy search
+ WebFetch verification (no image access — frame facts come from the script-12
raw transcription `analysis/slide_021_raw.json`).

## Slide identity

- New (curated) slide **021** ← old extraction slide **46** (diff 0.125,
  **founder frame swap**: kept frame `frame_01467.jpg`, original kept frame
  `frame_01583.jpg`) (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_021.jpg`.
- Frame facts (raw transcription): text-only slide — red title "Word Embedding",
  red subtitle "Continuous bag-of-words (CBOW)   vs Skip-Gram Models" (double
  space before "vs"), one blue-bordered box with two labeled definition
  paragraphs and a comparative summary sentence (blue-highlighted key terms
  "bag-of-words model" / "skip-gram model"); yellow/red badge "21"; mouse-cursor
  artifact over the first paragraph. The body text is **verbatim course
  copy-paste of the TensorFlow word2vec tutorial** (see below).

## Primary source

- **URL**: https://www.tensorflow.org/tutorials/representation/word2vec
  (verified live 2026-10-11 via WebFetch; located via agy exact-phrase search)
- **What it is**: TensorFlow's official word2vec tutorial ("Word embeddings").
- Supporting primary literature (the tutorial's own basis, not quoted on the
  slide): Mikolov, Chen, Corrado, Dean 2013, "Efficient Estimation of Word
  Representations in Vector Space", arXiv:1301.3781 — verified live 2026-10-11
  via the ar5iv render https://ar5iv.labs.arxiv.org/html/1301.3781 .

## Figures used by this slide

- **None** (text-only slide). No figure downloaded into this dir.

## What the source CONFIRMS (data behind the slide)

The slide's body text is **verbatim from the tutorial**, confirmed live 2026-10-11:

- "Continuous bag-of-words model: predicts the middle word based on surrounding
  context words. The context consists of a few words before and after the current
  (middle) word. This architecture is called a bag-of-words model as the order of
  words in the context is not important." — matches the tutorial's CBOW list item
  word-for-word (both its sentences and the "bag-of-words" naming explanation).
- "Continuous skip-gram model: predicts words within a certain range before and
  after the current word in the same sentence." — matches the tutorial's skip-gram
  list item word-for-word (the tutorial continues "A worked example of this is
  given below.", which the slide does not show).
- Summary sentence — tutorial, "Skip-gram and negative sampling" section, starts
  "While a bag-of-words model predicts a word given the neighboring context, a
  skip-gram model predicts the context (or neighbors) of a word, given the word
  itself." The slide's line reads the same **minus the leading "While"** (a
  fragment join; see [?] below).
- Consistency with the underlying paper: the skip-gram definition matches
  arXiv:1301.3781 §3.2 ("predict words within a certain range before and after
  the current word… based on another word in the same sentence"); the paper's
  Figure 1 caption gives the same contrast ("The CBOW architecture predicts the
  current word based on the context, and the Skip-gram predicts surrounding words
  given the current word"). The paper does NOT contain the "middle word" /
  "order of words" sentences — those are the tutorial's wording.

## Course-authored elements (no source counterpart)

- Title "Word Embedding", subtitle wording/spacing, the blue body-box border, the
  red paragraph-header styling, the blue inline highlight of the two key terms,
  badge "21", and the choice to splice the tutorial's list items + comparison
  sentence into one box. The mouse cursor is a recording artifact (omit in a
  clean recreation).

## [?] Uncertain items

- [?] Whether the frame's summary line really omits the tutorial's leading
  "While" (raw transcribes it starting lowercase "a bag-of-words…"), or whether
  the transcription just dropped it — only the frame can answer; recreation must
  follow the frame as transcribed.
- [?] Exact line breaks of each paragraph inside the box (raw gives paragraph
  text, not line-wrap).

## Corrections

none — transcription checked sentence-by-sentence against the tutorial (verified
live): the body text matches verbatim; nothing to correct.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
