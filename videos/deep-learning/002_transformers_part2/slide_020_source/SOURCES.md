# SOURCES.md — slide 020 "Pre-processing of Input Sequence"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Vision transcript of record: `transcripts/slide_020_webverify.txt` (2026-10-11,
default `images` route, `--thinking high`, via `scripts/16_vision_gate.sh`).

## Slide identity

- Frame `unique_slides/slide_020.jpg`, badge "20" (timeline: t≈776–884 s —
  109 frames, heavily taught; old extraction 40). First member of pattern
  group P2 [20,21,22,34]; no hard dep edge. Directly precedes the verified
  slide 021 ("[1] Position Encoding" concept intro).
- Frame facts (vision transcript, ground truth): title "Pre-processing of
  Input Sequence". Four dotted-container rows over a gray panel:
  Row 1 "Word 0..Word 5, …, Word N-2, Word N-1" (red boxes; left label
  "Sequence of words with Length N", gray italic).
  Row 2 "X_0..X_5, …, X_{N-2}, X_{N-1}" (each labeled token box followed by
  a stack of small empty cells = the embedding vector; left label "Word
  Embedding e.g. word2vec", green).
  Row 3 "Pos 0..Pos 5, …, Pos N-2, Pos N-1" (blue boxes, small orange curved
  arrows at box right edges = rotation/encoding motif; left label "Position
  Information", blue); below it "+δ" symbols (6) marking the element-wise
  addition.
  Red banner: "Combine Word Encoding and Position Information (for Each
  Word)" ("Combine" in yellow); two thick arrows feed it from rows 2 and 3.
  Row 4 "I/P 0..I/P 5, …, I/P N-2, I/P N-1" (light pink boxes); caption
  "Input to first Self Attention Layer in Transformer" (blue).
  Inset panel bottom-left (white, green border): "Positional Encoding"
  (circular icon) → box "Input Embedding" [?low-res] → "inputs", with the
  outside label "Input to Encoder" — a miniature of the Vaswani Figure 1
  input path redrawn top-to-bottom.
- Video artifacts (do not recreate): black letterbox strips at the frame
  bottom; JPEG softness on the inset's small text.

## Primary sources (verified live 2026-10-11)

- **Vaswani et al. 2017** — https://arxiv.org/html/1706.03762v7
  (WebFetch-confirmed verbatim this session):
  §3.5: "Since our model contains no recurrence and no convolution … we must
  inject some information about the relative or absolute position of the
  tokens in the input sequence." AND **"To this end, we add 'positional
  encodings' to the input embeddings at the bottoms of the encoder and
  decoder stacks."** — the slide's whole message (Word Embedding + Position
  Information → combined input) in the paper's own words.
  §3.5: "positional encodings have the same dimension d_model as the
  embeddings, so that the two can be summed" — the premise of the row-2 +
  row-3 → I/P combination.
  §3.1 (live this session): "The encoder is composed of a stack of N=6
  identical layers." — the "Input to Encoder" inset label's context; the
  inset is the banked **Figure 1** input path (Inputs → Input Embedding ⊕
  Positional Encoding), original banked in
  `../001_transformers_part1/slide_18_source/The Transformer - model
  architecture..png` (sha-verified provenance there).
- **word2vec example** — carried from this playlist's verified records:
  Part I map row "20–25 RESOLVED" (slide 21 = TensorFlow word2vec tutorial,
  slide 22 = Mikolov 2013 arXiv:1301.3781, figure verified byte-identical)
  and 002's slide-021/022 rows. The slide's "Word Embedding e.g. word2vec"
  is the standard learned-embedding example; the paper's §3.1 uses learned
  embeddings of dimension d_model. The course's word2vec naming is an
  example choice, kept verbatim.

## Figures used by this slide

- The INSET explicitly redraws the banked **paper Figure 1** input path
  (Positional Encoding + Input Embedding → inputs) — reference the bank;
  nothing new downloaded.
- The main 4-row composition is **course-authored** (an instructional
  expansion of Fig 1's input path; the transcript's explicit finding: matches
  no single published figure verbatim). [?] possible style inspiration: Jay
  Alammar's `transformer_positional_encoding_vectors.png`
  (https://jalammar.github.io/images/t/transformer_positional_encoding_vectors.png
  — inventory verified live this session) shows word-embedding + position-
  encoding + sum in a row-of-vectors style; no confident direct reuse → NOT
  downloaded. Zoom before build if pixel identity matters.

## What the sources CONFIRM

- Word embeddings are learned vectors of d_model; positional encodings are
  ADDED to the input embeddings (per word/position) before entering the
  encoder stack: §3.1/§3.5 verbatim. CONFIRMED — this is the slide's "+δ /
  Combine … (for Each Word)" step and its I/P row.
- Positions run 0..N-1 (the course's 0-based indexing here: Word 0, X_0,
  Pos 0 … Word N-1): consistent with the paper's "relative or absolute
  position of the tokens" framing and with the PE formula's pos index
  (§3.5: PE(pos, 2i)=sin(pos/10000^(2i/d_model)), verified live this
  session on the slide-018 record). Note: earlier review slides (012/014/016)
  used 1-based Word #1..#5 — different slides, different indexing, frame wins.
- "Input to first Self Attention Layer in Transformer": the summed vectors
  are what self-attention consumes (§3.2 opening sentence — live this
  session: "An attention function can be described as mapping a query and a
  set of key-value pairs to an output"; inputs formed per §3.1). CONFIRMED.

## Course vs paper discrepancies (NOT defects — recreation keeps course form)

- "+δ" notation: the course's symbol for the element-wise add (later slides
  022–023 reuse δ as the position step). The paper just says "add". Kept
  verbatim.
- Orange rotation arrows on Pos boxes: the course's rotation motif
  (foreshadows the 2-D circle sin/cos pedagogy, slides 025–032). Course-authored.
- Empty vector cells in row 2 (X boxes followed by unlabeled cells): visual
  shorthand for "a vector of length d" — course-authored.

## Open questions

- [?] Inset's small box text: reads "Input Embedding" [?] (possibly "Inputs
  Embedding") — low-res; zoom t≈776–884 s before building.
- [?] Row 4 ellipsis: transcript notes NO ellipsis circles drawn between
  I/P 5 and I/P N-2 (unlike rows 1–3) — possibly drawn but faint. Zoom
  before build.
- [?] Alammar PE-vectors figure as pixel-level inspiration [?] (not
  asserted by the transcript; no download made).

## Script-12 raw cross-check (raw-verification worker, 2026-10-11 — raw + final
both now on disk; the record's frame facts were transcript-based)

- `analysis/slide_020_raw.json` read in full (model `images`; old extraction 40;
  kept_frame frame_00885, 109 frames — heavily taught, as the record notes).
  Four-row composition, banner, captions, and inset confirmed.
- [?] RESOLVED (inset box text): raw reads the inset's pink box as "Input
  Embedding" (with an orange lightning bolt on it), plus "inputs" (gray, with a
  black up-arrow), "Positional Encoding" (black text + white circle with sine
  glyph), and the outside green label "Input to Encoder" — resolves the
  record's "Input Embedding [?] (possibly 'Inputs Embedding')" toward
  "Input Embedding".
- [?] RESOLVED (row 4 ellipsis): raw confirms NO ellipsis dots between I/P 5 and
  I/P N-2 ("Empty pink gap (no dots)") while rows 1–3 carry dot ellipses —
  resolved as frame truth.
- [?] NARROWED (Pos-row glyphs): raw reads small orange lightning-bolt icons
  BENEATH alternating boxes (under Pos 1, Pos 3, Pos 5) plus one on the inset's
  Input Embedding box; the record's transcript read "orange curved arrows at
  box right edges". Shape contested at glyph level (bolt vs arrow) — frame wins
  at build; zoom glance stands.
- Raw additions for the build: FOUR thick red block arrows (row 2 → banner,
  row 3 → banner, banner → row 4, brace → caption); exactly SIX "+δ" symbols
  (five under the Pos 0–5 region + one under Pos N-1); row-2 boxes each contain
  a cell strip with one pink cell bearing a red X_i; banner "Combine" in yellow
  (#FFD700) on dark red (#990000); large red underbrace beneath the I/P row.
- 0-based indexing (Word 0..Word N-1 / X_0..X_{N-1} / Pos 0..Pos N-1 / I/P
  0..I/P N-1) confirmed — consistent with the record's indexing note.
- Script-13 final ALREADY LANDED: `analysis/slide_020_final.json`
  (PASS_WITH_FIXES); `slide_title` matches the raw verbatim. Corrections: none
  yet at title level — verify against the final's fix list when building.
