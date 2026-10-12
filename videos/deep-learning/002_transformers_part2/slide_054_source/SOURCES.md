# SOURCES.md — 002 slide 054 "Self Attention Mechanism for Decoder (Adding Mask)"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Machine-verified 2026-10-11 by the Part II
web-verification worker: vision transcript banked
(`transcripts/slide_054_vision_2026-10-11.txt`, default `images` route, one
probe, `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`),
web research via `agy` + live fetches. **P4 pattern-group LEAD** (54, 55):
this file carries the shared pattern verification; slide 055's SOURCES.md
references it.

## Slide identity

- Video-2 (002_transformers_part2) curated slide **054** ← old extraction
  slide **134** (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_054.jpg` (kept from t≈4756 s; shown 4681–4755 s =
  75 frames), badge numeral 54.
- Content (banked vision transcript): title verbatim **"Self Attention
  Mechanism for Decoder  (Adding Mask)"** (two spaces before "(Adding…").
  A single-query decoder self-attention walkthrough, left→right: source
  tokens Z (4 striped groups; 2nd highlighted magenta under a red cursor) →
  key branch W_k^(0) → keys K_3/K_2/K_1(…), value branch W_v^(0) →
  V_3/V_2/V_1(…), query branch W_q^(1) → q_1 (q_2 [?]) from the highlighted
  token → tan **"Dot Product"** box (yellow oval "Similarity" above; red
  label "K.q" out) → tall box **"Scaling by √d"** (red fraction "K.q / √d"
  above) → green **"Mask"** column with cells top→bottom
  **[−∞][−∞][0][0]** and black oval **"Look Ahead Mask"** → tall
  **"Soft max"** box (yellow oval "Probabilities"; top output annotated red
  **0**) → red ⊗ nodes multiplying probabilities with V_i → blue **"Σ"**
  box (yellow oval "Weighted SUM") → top output strip **Z** (Z^ [?]).
  Bottom-right green legend inset: strip "1×d" → box "W" → "d×d" → "=" →
  strip "1×d", footnote "d: Embedding Length". Top-right badges: yellow
  box "−∞", red circled multiply symbol, empty yellow rectangle, badge 54.
- In-deck continuity: this is the MASKED twin of the deck's unmasked
  self-attention walkthrough family (001 slide 26 family pattern — founder
  note: "common patterns… not identical"); the Mask column, "Look Ahead
  Mask" oval and the red 0 are the added elements the title announces.
  Slide 053's matrix (SOS Je me sens malade, 0/−∞ lower/upper triangle) is
  the same concept in matrix form; slide 052 is the decoder stack it lives in.

## Primary source — CONFIRMED (mechanism), paper verbatim

- **Paper**: "Attention Is All You Need" — Vaswani et al. 2017,
  arXiv:1706.03762v7. All quotes below verified live 2026-10-11 from
  https://arxiv.org/html/1706.03762v7 (HTML banked at
  `../scratch/paper_v7.html`; reused from the slide-053 session record):
  - §3.2.1: "We compute the **dot products** of the query with all keys,
    **divide each by √d_k**, and apply a **softmax** function to obtain the
    weights on the values." + Eq. (1) **Attention(Q,K,V) =
    softmax(QKᵀ/√d_k)V** — exactly the slide's Similarity → Dot Product
    (K.q) → Scaling by √d → Softmax → weighted-sum-of-V pipeline.
  - §3.2.2: multi-head attention linearly projects Q, K, V "through
    **learned linear projections** W_i^Q, W_i^K, W_i^V" — the slide's
    W_q/W_k/W_v boxes and its legend (1×d)·(d×d) = 1×d (query vector z ∈
    R^{1×d} times projection W ∈ R^{d×d} → q ∈ R^{1×d}, "d: Embedding
    Length") are the same computation in course notation.
  - §3.2.1 masking: "masking out (setting to −∞) all values in the input of
    the softmax which correspond to illegal connections" + §3.2.3.1
    "predictions for position i can depend only on the known outputs at
    positions less than i" — exactly the slide's Mask column with −∞ cells
    zeroed by softmax ("Look Ahead Mask"; top probability annotated 0).
- Mechanism counterparts, both verified live this session (details banked in
  the sibling records): **Jay Alammar, "The Illustrated Transformer"**
  (https://jalammar.github.io/illustrated-transformer/, HTML banked at
  `../scratch/alammar_it.html`) — its self-attention step-by-step teaches
  the same unmasked pipeline ("compute the dot products… divide… by 8 (the
  square root of the dimension of the key vectors)… softmax…"); **Greg
  Mongaras, "How Do Self-Attention Masks Work?"**
  (https://gmongaras.medium.com/how-do-self-attention-masks-work-72ed9382510f,
  Wayback-verified 2026-02-27 snapshot) — mask matrix ADDED to the query-key
  scores before softmax.

## Figure identity — course-authored (agy cross-checked, live-disambiguated)

- One agy attempt died mid-stream ("error: interrupted" — known failure
  mode, SOURCES_MAP §4); the re-minted retry named Alammar's Illustrated
  Transformer "Self-Attention, Step-by-Step". **Grep of the live page
  disproves a figure-identity match**: the strings "Similarity", "Weighted
  SUM", "Look Ahead", "Embedding Length" and any mask column do NOT occur on
  the page (its walkthrough is prose + matrix PNGs, encoder-side, unmasked).
- Conclusion: the stage-labeled pipeline cartoon is **course-authored** —
  topology/labels follow paper §3.2.1–§3.2.3.1 (+ §3.2.2 projections),
  pixels and wording are the slide's. Same conclusion as slides 052/053.
- No figures downloaded: the slide reuses no published figure's pixels (the
  paper's only relevant figure is banked Figure 2 left — Scaled Dot-Product
  Attention — in `../001_transformers_part1/slide_18_source/slide18 scaled
  dot-production attention figure.png`; it shows the same pipeline as paper
  boxes and is the closest published counterpart, reference-only).

## What the source CONFIRMS / CORRECTS

- CONFIRMED: every pipeline stage and its order (dot products → scale by
  √d → add look-ahead mask (−∞/0) → softmax → weights·V → Σ weighted sum);
  learned projections W^Q/W^K/W^V from the source embeddings; the legend's
  shape arithmetic (1×d · d×d = 1×d); causal behavior (future positions get
  −∞ → probability 0 — the top "0" annotation).
- CORRECTED: nothing contradicts the paper. Notation notes (slide's own
  choices, not errors): the deck writes the dot product as "K.q" (paper:
  QKᵀ order); superscripts "(0)"/"(1)" on W_k/W_v/W_q are the course's own
  indexing (paper uses per-head index i: W_i^K etc.) — see [?] below.
- Continuity: mask values [−∞,−∞,0,0] top→bottom over 4 source tokens with
  the 2nd token as current query is self-consistent (keys drawn K_4…K_1
  top→bottom, i.e. bottom-up token order; allowed = self + previous token).

## [?] Open questions

1. Superscript semantics of W_k^(0)/W_v^(0) vs W_q^(1): head indices, or a
   transcription artifact? (transcript: "reads (1) or (0), moderately
   confident"). `[?]` — resolve against the frame in the build pass.
2. The exact top output glyph ("Z^" vs "Z̄") and the Z-group subscripts
   (all four read "Z_?" in the transcript) `[?]` — frame-level read needed.
3. Whether a 4th K label (K_4) and a 4th W_v^(0) row exist but are partly
   hidden (transcript saw 3 clearly, 4 rows drawn) `[?]`.
4. The empty yellow rectangle among the top-right badges (reserved highlight
   or build artifact) `[?]`.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web
sources confirm/correct data and provenance, never license inventing content.
`[?]` markers are removed only with a confirming URL recorded here.

## Script-12 raw cross-check (2026-10-11, web-research verification worker)

Cross-checked against `analysis/slide_054_raw.json` (script-12 raw landed
after this record was written from the banked vision transcript).

- CONFIRMED by raw: title verbatim with the double space before "(Adding";
  the full left→right pipeline (Z stack → W_k → K strips → tan "Dot Product"
  with yellow "Similarity" pill → "Scaling by √d" with fraction K,q/√d →
  green "Mask" column [−∞,−∞,0,0] + black "Look Ahead Mask" ellipse →
  "Soft max" with "Probabilities" pill → four red ⊗ nodes (top arrow labeled
  red "0") fed by V₁–V₄ from W_v → blue Σ with "Weighted SUM" → top output Z);
  magenta-highlighted Z₂ in the bottom container driving W_q → q₂ into the
  Dot Product box; dashed connectors tying the bottom container to both side
  Z stacks; bottom-right legend (1×d)·W(d×d) = 1×d with "d: Embedding
  Length"; top-right badge row (−∞ chip, red circled symbol, empty yellow
  rectangle, badge "54"); identity metadata (old extraction slide 134, kept
  frame_04756, shown 4681–4755 s, 75 frames). No source claims in this
  record are contradicted.
- STRENGTHENED: open question 3 — the raw sees all four K labels (K₁–K₄)
  and all four W_k/W_v rows explicitly (no partly-hidden 4th row); and the
  query label reads "q₂" twice (leaning open-question "q_1 (q_2 [?])"
  toward q₂); the top output cell reads plain "Z" (no ^/bar), leaning open
  question 2 toward plain "Z".
- RAISED / keeps `[?]` (frame-level reads needed in the build pass — none of
  these are resolvable by web sources, they are course-notation/frame reads):
  1. K-label vertical order: the banked transcript read keys drawn
     K_4…K_1 top→bottom (which makes mask [−∞,−∞,0,0] self-consistent with
     query q₂ — self + previous allowed); the raw lists the strips as
     "K₁, K₂, K₃, K₄" without pinning the vertical order. If K₁ were on
     top, the mask column as drawn would be inconsistent with q₂ — so the
     reversed (K₄ top) reading remains the consistency-favored one, but the
     frame must decide. Flagged for the corrections/build pass.
  2. Superscript semantics: raw reads the W-box superscripts as "(r)"
     (possibly "(1)") and marks them `[?]`; the banked transcript read
     "(0)"/"(1)". Two independent reads disagree → open question 1 stays
     `[?]` with a widened candidate set {(0), (1), (r)}.
  3. NEW from raw: a possible dash before √d in the rotated box text
     (raw: "Scaling by −√d [?]"). The paper (§3.2.1, verified in this
     record) divides by √d_k — a literal "−√d" would be a slide
     typo/artifact. Frame-level read flagged; do not "correct" the slide
     without the frame.
  4. NEW from raw: a large ς (final-sigma-like) glyph inside the Softmax
     column, read uncertain (raw marks it `[?]`). Not captured in the
     original record — added here as a new `[?]` element for the build pass.
  5. Open question 4 (empty yellow rectangle among the top-right badges)
     remains `[?]` — the raw also offers no explanation.
  6. Minor notation read: raw writes the dot-product output label "K,q"
     (comma) vs the record's "K.q" (dot) — same trivial build-level check.
- No new published-figure claim appears in the raw (course-authored
  pipeline cartoon, consistent with this record's figure-identity
  conclusion; nothing to fetch).
- Corrections needed: none to source claims; the frame-level flags above go
  to the build pass.
