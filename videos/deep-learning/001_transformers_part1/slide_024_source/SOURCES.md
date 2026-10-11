# SOURCES.md — slide 024 "Objective of Self attention"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via agy search
(no image access — frame facts come from the script-12 raw transcription
`analysis/slide_024_raw.json`).

## Slide identity

- New (curated) slide **024** ← old extraction slide **49** (diff 0.0)
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_024.jpg`.
- Frame facts (raw transcription): a course-drawn pedagogical diagram — title
  "Objective of Self attention"; dashed-blue example-sentence box "The boy
  climbs the tree in the garden" (word "boy" bold); one huge dashed pale-cyan
  circle containing a six-node word graph (in, garden, the, Boy, tree, climbs —
  "Boy" the only green node) with red attention arrows of varying thickness and
  five blue embedding-vector icons; a pink hatched block arrow pointing to the
  result: a green "Boy" node with an ORANGE vector icon (new contextual
  embedding) linked by a red dashed line to a second green "Boy" node with a
  BLUE vector icon (original input embedding); badge "24"; a presenter pen icon
  artifact on the garden<->tree arrow.

## Primary source

- **No published figure or text matches this slide — it is course-authored.**
  agy exact-phrase search (2026-10-11) found no verifiable published source for
  the sentence "The boy climbs the tree in the garden" paired with an
  attention/word-graph diagram; the sentence circulates only as a generic
  teaching example, and neither "Attention Is All You Need", nor Jay Alammar's
  "The Illustrated Transformer", nor the Hugging Face/TensorFlow/PyTorch
  tutorials use it.
- The CONCEPT the diagram teaches is the paper's: Vaswani et al. 2017,
  "Attention Is All You Need", arXiv 1706.03762 (verified live 2026-10-11 via
  the figure-family records in `slide_018_source/SOURCES.md`), §3.2: "Self-
  attention, sometimes called intra-attention, is an attention mechanism
  relating different positions of a single sequence in order to compute a
  representation of the sequence." The orange output vector = the word's new
  contextual representation; the red arrows = attention over ALL positions.

## Figures used by this slide

- **None downloaded** — the diagram is instructor-drawn vector art; there is no
  external figure to bank.

## What the source CONFIRMS (data behind the slide)

- The conceptual mapping only: every word in the sentence attends to every
  other word (fully-connected arrows across the word graph); the operation maps
  an input embedding (blue icon) to a context-aware output embedding (orange
  icon). This is precisely §3.2.1's self-attention definition and the
  "Attention(Q,K,V)" mechanism, and §3.1's stack where it sits.
- The example sentence's word set is internally consistent with the graph: the
  6 nodes are the sentence's unique words ("the" appears twice in the sentence
  but once as a node — a course simplification, not an error).
- Arrow-thickness variation (thick Boy<->garden, Boy<->tree, Boy<->climbs,
  garden<->tree vs thin in<->the etc.) matches the attention-weight idea
  (weight = strength of attention), consistent with the paper's weighted
  softmax(QKᵀ/√d_k)V — qualitative teaching, no numeric claim on the frame.

## Course-authored elements (no source counterpart — do not "fix" to source)

- The whole composition: node placement, arrow routing/thickness, colors, the
  block arrow, both "Boy" result nodes, vector-icon design, title, sentence
  box, badge "24". The pen icon on the garden<->tree arrow is a live-annotation
  artifact (omit in a clean recreation).

## [?] Uncertain items

- [?] The exact arrow set (raw marks several edges `[?]` — in<->Boy, the<->garden,
  climbs<->tree, the<->tree presence) — a frame-level fact the raw's vision pass
  should pin; web research cannot confirm a course-drawn edge.
- [?] Whether "garden" deliberately has no embedding icon (raw marks `[?]`) —
  same: only the frame decides.

## Corrections

none — no external data exists to correct against; the slide's conceptual claims
match the paper's self-attention definition. Nothing to correct.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
