# SOURCES_MAP.md — 001_transformers_part1 (Transformers — Part I, Deep Learning DSAI 308)

Fleet-level source map, 2026-10-11. Written by the web-research worker per the
video's AGENTS.md (web-verified analysis mandatory). Scope: identify the primary
sources behind the deck's slide FAMILIES and the course-level materials, so
per-slide workers can confirm per slide and download figures into
`slide_NNN_source/` dirs.

## How this was researched (method)

- 6 `agy -p` queries: (1) DSAI 308 course slides, (2) course videos/GitHub mirrors,
  (3) seq2seq encoder-decoder diagram origin (Cho vs Sutskever), (4) attention
  origin (Bahdanau vs Luong), (5) positional-encoding figure sources, (6) the
  lecture video itself.
- Every URL below was re-verified on 2026-10-11 via WebFetch / curl / yt-dlp —
  nothing is recorded from an unverified search snippet. One URL agy produced was
  HALLUCINATED and is recorded in "Failed findings" so it is never reused.

## Confidence legend

- **CONFIRMED** — verified live; the artifact is known to be the slide family's
  source (founder-declared or figure-identity established).
- **HIGH (origin)** — verified live; established as the canonical origin of this
  family's diagram/idea; per-slide figure match still needs the per-slide worker's
  image check (course redraws figures in its own style — topology/labels match the
  paper, pixels are the slide's).
- **[?]** — plausible alternate or guess; NOT confirmed for any specific slide.

## 1. Course-level materials (task item 3) — VERIFIED

| What | URL | Status |
|---|---|---|
| The lecture video itself | https://www.youtube.com/watch?v=Ff8KU1dyJMA | CONFIRMED (oEmbed + yt-dlp): title "[11] Transformers - Part I", channel "Dr. Khaled Mostafa Elsayed" (@dr.khaledmostafaelsayed7516), uploaded 2024-12-11, **description is EMPTY — no slide links** |
| Course playlist | https://www.youtube.com/playlist?list=PL5JZLxl_tFCcmulUU7suv9DkAFrOTm34w | CONFIRMED (yt-dlp): "Deep Learning DSAI 308 Fall 2024 - Zewail"; contains `[11] Transformers - Part I` (= our video), `[12] Transformers - Part II` (1vYxr2TmkLA), `[10] LSTM and GRU` (dfTD6eeMZHE), `[9] RNN` (7Zz-hQfp5xM) |
| Instructor channel | https://www.youtube.com/@dr.khaledmostafaelsayed7516 | CONFIRMED (oEmbed author_url). Other playlists: "Zewail CIE 633 Deep learning", "NLP-Transformers", "Zewail ML Fall 2022/2023", etc. |
| Zewail public course site / slide decks | — | NOT FOUND: no public DSAI 308 slide decks (agy x2 + no links in the video description; materials live on the internal Moodle https://moodle.zewailcity.edu.eg). **A public deck does not exist as far as verifiable — the papers below remain the sources.** |

Metadata note: the brief said "Dr. Khalid Nustafa Elsayed / Dr. Mohamed Maher
Amin, Aug 2020"; the verified channel is "Dr. Khaled Mostafa Elsayed" and the
upload is 2024-12-11 in the Fall 2024 playlist. Same lecture title and course;
record the verified naming here. [?] whether a 2020-era recording exists
separately — nothing verifiable was found.

## 2. Slide-range → source map

| Slides | Family / content | Primary source | Confidence | What specifically matches |
|---|---|---|---|---|
| 14–19 | Encoder-Decoder Transformer figures | **arXiv 1706.03762v7 "Attention Is All You Need"** — figures banked in `slide_18_source/` (Fig 1 full architecture; Fig 2 left Scaled Dot-Product; Fig 2 right Multi-Head) | CONFIRMED | See `slide_18_source/SOURCES.md`. Slides 14/15/16/17 = Fig 1 only; 18/19 = Fig 1 + Fig 2 left + Fig 2 right. Slides 38 and 44 embed Fig 2-left / Fig 2-right insets (per `slide_dependencies.json`). |
| 6–7 (seq2seq diagram) | RNN encoder-decoder with context vector c | **Cho et al. 2014, "Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation"** (EMNLP 2014), arXiv:1406.1078 — Figure 1 "An illustration of the proposed RNN Encoder–Decoder" | HIGH (origin); per-slide match [?] | Figure 1 topology: encoder RNN chain (x₁…x_T) → single context vector c → decoder RNN chain (y₁…y_T′). This is the canonical "context vector between encoder and decoder" diagram the slide family describes. Paper verified via ar5iv; figure asset: `/html/1406.1078/assets/rnn_encdec.svg` |
| 6–10 (alternates) | seq2seq LSTM variant; redraw source | **Sutskever, Vinyals, Le 2014, "Sequence to Sequence Learning with Neural Networks"** (NeurIPS 2014), arXiv:1409.3215 — Figure 1 (deep LSTM, ABC→WXYZ, <EOS>) | [?] alternate | Figure 1 = stacked-LSTM seq2seq with reversed input and EOS; the course may redraw either Cho's simple-RNN version or this LSTM version. d2l.ai's seq2seq chapter figures (https://d2l.ai/_images/seq2seq.svg, `seq2seq-predict.svg`) are another very common redraw source [?] |
| 8–9 (challenges) | bottleneck / sequential processing / vanishing gradient | No single canonical figure — standard lecture framing | [?] course-authored | Likely course-authored text over generic diagrams. Conceptual refs: d2l.ai RNN/seq2seq chapters (https://d2l.ai/chapter_recurrent-modern/seq2seq.html), Sutskever §3.4/§4 (long-sentence degradation = bottleneck evidence). If the slide shows a specific diagram, per-slide worker must identify it via image analysis first |
| 10 (attention) | attention mechanism intro | **Bahdanau, Cho, Bengio 2014, "Neural Machine Translation by Jointly Learning to Align and Translate"** (ICLR 2015 oral), arXiv:1409.0473 — Figure 1 "graphical illustration of the proposed model" | HIGH (origin); per-slide match [?] | Figure 1 topology: bidirectional encoder producing annotations (h₁…h_T) + decoder attending over ALL of them with alignment weights α at each output step (the fix to the fixed-c bottleneck). Figure asset: `/html/1409.0473/assets/rnnsearch.svg`; alignment heatmaps = Figure 3 (`/assets/EEA.png`, `1511.png`, `2799.png`, `374.png`) |
| 10 (alternates) | attention variants | Luong, Pham, Manning 2015, "Effective Approaches to Attention-based Neural Machine Translation" (EMNLP 2015), arXiv:1508.04025 — Fig 2 global (`attn_soft.png`), Fig 3 local (`attn_hard.png`), Fig 4 input-feeding (`attn_input.png`) | [?] alternate | Cite if the slide shows global/local attention machinery rather than the Bahdanau model |
| 20–25 [?] content | positional encoding / embeddings / transformer details / summaries | **arXiv 1706.03762 §3.5 (positional encoding), §3.1 (embeddings)** — formula & definition ground truth is the paper already banked; well-known illustration sources: Jay Alammar "The Illustrated Transformer" (https://jalammar.github.io/illustrated-transformer/) and d2l.ai (https://d2l.ai/chapter_attention-mechanisms-and-transformers/self-attention-and-positional-encoding.html) | Paper: CONFIRMED as data source; illustration reuse [?] | Alammar's positional-encoding image: https://jalammar.github.io/images/t/attention-is-all-you-need-positional-encoding.png (verified live); d2l sinusoidal figure: https://d2l.ai/_images/position-encoding.svg (verified live). Whether the slides reuse any of these pixels is unknown — course redraws; per-slide worker confirms |
| 20–25 RESOLVED per slide (correction worker, 2026-10-11) | 20 = course-authored section divider (no source); 21 = **TensorFlow word2vec tutorial** https://www.tensorflow.org/tutorials/representation/word2vec — body text verbatim-confirmed live (paper 1301.3781 is the underlying literature but NOT the wording source); 22 = **Mikolov 2013 Fig 1** (arXiv:1301.3781), original downloaded & verified byte-identical in `slide_022_source/efficient-models.svg` — course RECOLORED it (paper figure is grayscale); 23 = standard math, Wikipedia cosine-similarity confirms (course-drawn diagrams); 24 = course-authored self-attention diagram (agy: "boy climbs tree" sentence has no published source); 25 = figure family: Fig 1 + Fig 2 left + Fig 2 right redrawn as a zoom ladder (`slide_18_source/` bank). See each `slide_0NN_source/SOURCES.md` | as listed | per-slide records supersede this family row |
| 26–30, 34, 35, 37, 43, 44, 45 | self-attention / scaling / multi-head math | arXiv 1706.03762 §3.2.1 (Attention(Q,K,V) = softmax(QKᵀ/√d_k)V), §3.2.2 (multi-head); figure bank in `slide_18_source/` (Fig 2 left/right for 38/44 insets) | CONFIRMED (figures); math equations from the paper | Another worker covers per-equation sources; figure provenance already recorded in `slide_18_source/SOURCES.md` |
| 31–33, 36, 39–42 [?] content | unknown (likely FFN / Add&Norm / why-self-attention / training / results) | arXiv 1706.03762 (§3.3 FFN, §3.1 Add&Norm, §3.2 why self-attention + Table 1 complexities, §5 training, §6 results/Table 2) | [?] until slide content is seen | Content-blind: do not assign sources before a per-slide analysis sees the slide. The paper is the default candidate for any transformer-internals slide |
| 1–5 | title / intro / agenda | course-authored | CONFIRMED course-authored (no external source expected) | Title/agenda slides are house-made; nothing to web-source unless a specific figure appears (then per-slide worker identifies it) |
| 11–13 | unknown | — | [?] unknown | Content-blind; resolve per slide |

Dependency-gating reminder (from `slide_dependencies.json`): analysis (12/13) is
never dep-gated; figure sourcing above gives every slide in 6–10 and 20–25 a
starting source, but each slide's own `slide_NNN_source/SOURCES.md` must record
what was actually confirmed against ITS frame.

## 3. Download candidates (for per-slide workers — verified live 2026-10-11)

**This worker downloaded NOTHING** (rule: only download when highly confident a
specific slide directly reuses a specific figure; slide pixels were not
inspectable here, and the course is established to redraw figures). Fetch targets
below; save into the slide's own `slide_NNN_source/` dir, unrenamed, and log in
that dir's `SOURCES.md`.

For slides 6–10 (seq2seq / attention family):

1. Cho 2014 Fig 1 (RNN encoder-decoder, context vector c) — SVG:
   `https://ar5iv.labs.arxiv.org/html/1406.1078/assets/rnn_encdec.svg`
   (paper: https://arxiv.org/abs/1406.1078; ar5iv render:
   https://ar5iv.labs.arxiv.org/html/1406.1078)
2. Sutskever 2014 Fig 1 (deep LSTM seq2seq ABC→WXYZ) — PNG:
   `https://ar5iv.labs.arxiv.org/html/1409.3215/assets/Diagram1.png`
   (paper: https://arxiv.org/abs/1409.3215)
3. Bahdanau 2014 Fig 1 (RNNsearch attention model) — SVG:
   `https://ar5iv.labs.arxiv.org/html/1409.0473/assets/rnnsearch.svg`;
   Fig 3 alignment heatmaps — PNG:
   `https://ar5iv.labs.arxiv.org/html/1409.0473/assets/EEA.png`
   (+ `1511.png`, `2799.png`, `374.png` same dir)
   (paper: https://arxiv.org/abs/1409.0473)
4. Luong 2015 Fig 2/3/4 (global / local / input-feeding) — PNG:
   `https://ar5iv.labs.arxiv.org/html/1508.04025/assets/attn_soft.png`,
   `attn_hard.png`, `attn_input.png` (paper: https://arxiv.org/abs/1508.04025) [?]
5. d2l.ai seq2seq figures (common redraw source) — SVG:
   `https://d2l.ai/_images/seq2seq.svg`, `https://d2l.ai/_images/seq2seq-predict.svg`
   (chapter: https://d2l.ai/chapter_recurrent-modern/seq2seq.html) [?]

For the 20–25 range [?] (positional encoding / embeddings / details):

6. Alammar positional encoding image — PNG:
   `https://jalammar.github.io/images/t/attention-is-all-you-need-positional-encoding.png`
   (page: https://jalammar.github.io/illustrated-transformer/)
7. d2l.ai figures — SVG: `https://d2l.ai/_images/position-encoding.svg`;
   `https://d2l.ai/_images/transformer.svg`
   (chapters: https://d2l.ai/chapter_attention-mechanisms-and-transformers/self-attention-and-positional-encoding.html,
   https://d2l.ai/chapter_attention-mechanisms-and-transformers/transformer.html)
8. Transformer paper figures — ALREADY BANKED in `slide_18_source/`; do not
   re-download arXiv 1706.03762 figures; reference that dir.

ar5iv note: ar5iv mirrors the arXiv source render; for papers of this era arXiv
has no native HTML, so ar5iv asset URLs are the canonical direct-figure links.
If a URL 404s later, the ar5iv article page lists all assets.

## 4. Failed findings / do-not-reuse (recorded to prevent relearning)

- `https://www.youtube.com/playlist?list=PL-W1XJq5u_b4z91_z787d5t-s5-H2G-mI` —
  agy-provided playlist ID; **does NOT exist** (yt-dlp: "The playlist does not
  exist"). The real playlist is `PL5JZLxl_tFCcmulUU7suv9DkAFrOTm34w` (above).
- The video description contains no links; no Zewail-hosted slide deck is public.
- `agy` stream intermittently dies mid-answer with "error: interrupted" —
  re-mint with `agy -p "hi"` and retry shorter queries.

## 5. How per-slide workers extend this file

- Append a row to §2 (or annotate the existing row) with the slide's own finding;
  never delete family-level rows.
- Every slide that downloads a figure creates `slide_NNN_source/` (curated
  numbering, zero-padded 3 digits; the existing `slide_18_source/` dir name is
  historical) with the figures + a `SOURCES.md` per the video's AGENTS.md
  pattern (URL, figure number + caption, what was confirmed/corrected, `[?]`
  open questions).
- A `[?]` in this map is removed ONLY by the per-slide worker after image-level
  confirmation against the frame, with the confirming URL recorded in that
  slide's `SOURCES.md` (fidelity law: slide frame is ground truth for what is
  shown; source confirms data/provenance).

---

# Part II (002_transformers_part2) — appended 2026-10-11 by the Part II web-research worker

Per `videos/deep-learning/002_transformers_part2/AGENTS.md`: Part II rows are
APPENDED here (never edit/delete the Part I rows above). Same confidence legend
and fidelity law as above.

## How this was researched (method)

- **8 `agy -p` queries**: (1) course materials for Part II, (2) PE source
  landscape, (3) the 2-D sin/cos circle pedagogy, (4) training §5.3 details +
  which tutorials reproduce them with figures, (5) beam-search references,
  (6) variants/applications arXiv IDs, (7) attention-visualization tools,
  (8) decoder architecture (mandatory, for slide 57).
- **yt-dlp verification** (no agy spent): Part II video = `[12] Transformers -
  Part II`, Dr. Khaled Mostafa Elsayed, uploaded 2024-12-15, 1:30:40,
  id `1vYxr2TmkLA` — https://www.youtube.com/watch?v=1vYxr2TmkLA — CONFIRMED.
  **Description is EMPTY** (no slide links), same as Part I; playlist is the
  same verified `PL5JZLxl_tFCcmulUU7suv9DkAFrOTm34w`. No public DSAI 308 deck.
- **Every URL below re-verified live 2026-10-11** (curl/WebFetch). The banked
  001 figure assets were sha256-compared against the live arXiv assets — all
  three byte-identical (see below), so Part I's figure-bank provenance carries
  into Part II unchanged.

## State of record for per-slide confirmation (2026-10-11)

- 002 is curated to **60 slides** (59 real frames slide_002..060 + slide 001 =
  PLACEHOLDER cover — skip it entirely; no source research applies).
- **Only 3 raw analyses exist**: `slide_002` (title slide), `slide_003`
  ("Review of Part I" divider), `slide_032` ("Sin/Cos Positional Encoder").
  **Every Part II row below is therefore family-level and marked
  `[pending raw]` unless noted** — per-slide workers must confirm against the
  frame and create `slide_NNN_source/` per the video AGENTS.md.
- Timeline mapping (slide ← old extraction, t=seconds) was extracted from
  `unique_slides/slides_index.json` (read-only) and is noted per family.

## Part II slide-range → source map

| Slides | Family / content (evidence) | Primary source | Confidence | What specifically matches |
|---|---|---|---|---|
| 002–003 | Title "Transformers / Part II / Aug. 2020" + "Review of Part I" divider (raws exist) | course-authored | CONFIRMED (raws 2026-10-11) | Title + divider; nothing to web-source. Part I reference: self-attention recap points at 001's 26–45 family |
| 004 | architecture recap | **banked Figure 1** (001 `slide_18_source/`, = arXiv 1706.03762v7 Fig 1, ModalNet-21.png) | CONFIRMED by dependency `4 ← 001:15 AND 001:18` | Recap of the full encoder-decoder figure; `[pending raw]` frame check |
| 008, 013 | self-attention dataflow recap | 001 slide-33 record (`slide_033_source/SOURCES.md`; paper §3.2 + Peter Bloem) | CONFIRMED via deps `8 ← 001:33`, `13 ← 001:33` | Same course-authored dataflow composition, new badge; `[pending raw]` |
| 011, 015, 017 | multi-head recap | 001 slide-43 record (`slide_043_source/SOURCES.md`; paper §3.2.2 + Bloem "wide" origin) | CONFIRMED via deps `11/15/17 ← 001:43` | Same recap pattern; `[pending raw]` |
| 019, 037 | block-anatomy recap (Norm/FFN/Residual callouts) | 001 slide-19 record + banked Fig 1/2L/2R | CONFIRMED via deps `19 ← 001:19`, `37 ← 001:19` | Same trio-of-figures + callouts composition; `[pending raw]` |
| 005–007, 009, 010, 012, 014, 016, 018 | review block (P1 pattern group 9/10/12/14/16; 10←9) | Part I families above are the default candidates | `[?]` `[pending raw]` | Content-blind — resolve per slide when raws land |
| 020–027, 034 (P2: 20/21/22/34) | unknown review/detail block (t≈13–24 min) | paper (§3.x) default candidate | `[?]` `[pending raw]` | Content-blind — do not assign sources before raws land |
| **026–034** | **positional-encoding development** (28←[27,26], 29←28; 032 = "Sin/Cos Positional Encoder", raw exists: vector [sin(ωt); cos(ωt)], bounded −1..1, constant consecutive distance, unbounded t, "cannot combine with word embedding") | **arXiv 1706.03762 §3.5** — formula ground truth, verbatim verified live 2026-10-11: PE(pos,2i)=sin(pos/10000^(2i/d_model)), PE(pos,2i+1)=cos(pos/10000^(2i/d_model)); 2-D circle pedagogy: **Kazemnejad, "Positional Encoding in Transformers"** https://kazemnejad.com/blog/transformer_architecture_positional_encoding/ (live; figures `…/positional_encoding.png` 43,159 B, `…/time-steps_dot_product.png` 30,320 B) + Brandon Rohrer "Transformers from Scratch" https://e2eml.school/transformers.html (live); illustrations: Alammar + d2l (below) | 032: CONFIRMED family (raw); rest `[pending raw]` | The course's 2-D [sin(ωt);cos(ωt)] vector with constant-step circle argument matches the tutorial "pair on a unit circle, constant rotation per step" framing (agy: Kazemnejad/Rohrer/Shibuya use it); paper §3.5 is the formula source |
| 030, 031, 033 | PE-matrix / curves neighbors of 032 (t=27.5–36 min; 31 spans 304 frames = heavily taught) | same PE family; illustration candidates: Alammar `attention-is-all-you-need-positional-encoding.png` (13,305 B, live), `transformer_positional_encoding_large_example.png` (36,534 B), `transformer_positional_encoding_vectors.png`; d2l `position-encoding.svg` (188,475 B, live) | `[?]` `[pending raw]` | Content-blind; check whether frames reuse any of these pixels (course redraws per Part I precedent) |
| 035–044 | unknown (t≈45–59 min; P3 = 42/43/44) | paper default (training/decoder/results [?]) | `[?]` `[pending raw]` | Content-blind |
| **045–048** | chain 45←28, 46←45, 47←46, 48←47 (builds on the PE block; t≈61–65 min) — plausibly decoder-side build-up [?] | **arXiv 1706.03762 §3.1 (Decoder)** + banked Figure 1 decoder column | `[?]` `[pending raw]` | Content-blind; §3.1 verified live (see 057 row) |
| 049, 050 | 49 = pattern-derived (26 family, founder assumption pending veto); 50 unknown | 026-family sources when 026 resolves | `[pending raw]` | Do not clone 26's composition (per deps note) |
| **051** | **split halves of 001's slide-18 Figure 1** (old extraction 122, t≈4129 s) | **banked Figure 1** — provenance already established: banked `The Transformer - model architecture..png` = live ModalNet-21.png, 159,152 B, sha256[:16] `56d69ccc192b90c3` (byte-identical, verified 2026-10-11) | CONFIRMED (provenance) — placement `[pending raw]`/vision | **`slide_051_source/` CREATED** with the two machine-derived halves (`fig1_left_half_x0-760.png`, `fig1_right_half_x760-1520.png`, cut at midline x=760, reassembly pixel-identical; midline clips the 9-px K/V connector at x=758–766/y=802–1107; alternative band cuts x=736/784 `[?]`) + full SOURCES.md. Halves' placement/size on the frame = vision worker's job |
| 052–056 | unknown (t≈69–81 min; P4 = 54/55) | paper default [?] | `[pending raw]` | Content-blind |
| **057** | **encoder + decoder composed professionally on ONE slide** (old extraction 147, t≈4934 s; dep 57←47) | **arXiv 1706.03762 §3.1 (Decoder)** — verified live: "The decoder is also composed of a stack of N=6 identical layers"; sub-layers masked MHA → encoder-decoder cross-attention → FFN, each Add&Norm; shifted-right inputs; final Linear+softmax. **Figure 1 = canonical encoder+decoder composition** (research-confirmed); first candidate = banked Fig 1 | CONFIRMED (decoder research done); frame reuse `[pending raw]`/vision | **`slide_057_source/` CREATED**: mandatory decoder research recorded + downloaded Alammar decoder candidates `Transformer_decoder.png` (879×279, 38,751 B) and `The_transformer_encoder_decoder_stack.png` (1218×793, 127,812 B) + full SOURCES.md. Whether the frame reuses banked Fig 1, a course redraw, or the Alammar candidates = vision worker's job |
| 058–060 | closing block (59←38 pattern-derived, founder assumption pending veto; 60 spans 312 frames = long summary) | 038-family sources when 038 resolves | `[pending raw]` | Content-blind |

## Part II download candidates (verified live 2026-10-11)

**Banked (do NOT re-download; reference 001's bank)**: arXiv v7 Figure 1 =
`The Transformer - model architecture..png` (159,152 B = ModalNet-21.png),
Figure 2 left = `slide18 scaled dot-production attention figure.png`
(26,323 B = ModalNet-19.png), Figure 2 right = `slide18 Multi-Head Attention\n\n.png`
(65,853 B = ModalNet-20.png). All three sha256-verified byte-identical to
https://arxiv.org/html/1706.03762v7/Figures/ModalNet-{21,19,20}.png on
2026-10-11. Correct asset path is **`/Figures/`** (not `/assets/`).

For the PE family (026–034) — fetch per slide, save unrenamed into the slide's
own `slide_NNN_source/`:

1. Kazemnejad figures — `https://kazemnejad.com/img/transformer_architecture_positional_encoding/positional_encoding.png` (43,159 B), `…/time-steps_dot_product.png` (30,320 B) (page live)
2. Alammar PE images — `https://jalammar.github.io/images/t/attention-is-all-you-need-positional-encoding.png` (13,305 B), `transformer_positional_encoding_large_example.png` (36,534 B), `transformer_positional_encoding_vectors.png` (page https://jalammar.github.io/illustrated-transformer/, live)
3. d2l — `https://d2l.ai/_images/position-encoding.svg` (188,475 B), `transformer.svg` (276,521 B) (chapters live)
4. Rohrer — https://e2eml.school/transformers.html (live; circle/"wiggle" framing; figure URLs not yet enumerated)

For the training family [?] (if any slide covers §5.3/§5.4):

5. The Annotated Transformer — https://nlp.seas.harvard.edu/annotated-transformer/ (live) reproduces β₁=0.9/β₂=0.98/ε=1e-9, Noam lrate formula with warmup=4000, ε_ls=0.1; its figures (PE matrix, LR schedule) are **base64-embedded in the page — no direct asset URLs**
6. Paper §5.3/§5.4 verbatim (verified live): "We used the Adam optimizer [20] with β1=0.9, β2=0.98 and ϵ=10−9."; "lrate = d_model^{-0.5} · min(step_num^{-0.5}, step_num · warmup_steps^{-1.5})", warmup_steps=4000; "During training, we employed label smoothing of value ϵ_ls=0.1 [36]."

For later families [?] (only if raws show such slides):

7. Beam search — algorithm in Cho 2014 §3.2 / Sutskever 2014 §2.3 / Bahdanau 2014 (no dedicated diagrams); the widely-reused teaching diagram is the Stanford CS224N (Lecture 8) slide set, https://web.stanford.edu/class/cs224n/slides/ `[?]` unverified for this deck
8. Variants/applications — BERT arXiv:1810.04805 (Devlin 2018), GPT-3 arXiv:2005.14165 (Brown 2020), GPT-1/2 OpenAI tech reports (not on arXiv), paper §4/Table 2; BertViz attention visualizer https://github.com/jessevig/bertviz (Vig, ACL 2019 demo, https://aclanthology.org/W19-8604.pdf) `[?]` — none confirmed for any slide yet

## Part II failed findings / do-not-reuse

- `https://arxiv.org/html/1706.03762v7/assets/ModalNet-*.png` — **404**: the
  assets live under `/Figures/`, not `/assets/`. (Also fixes the path pattern
  recorded in Part I's §3 for future papers.)
- `https://jalammar.github.io/images/t/attention_is_all_you_need_17_positional_encoding.png`
  — 404 (wrong filename guess); the live file is
  `attention-is-all-you-need-positional-encoding.png` (hyphens, no "17").
- Part II video description is empty; no public slide deck (agy query 1
  confirmed independently of Part I's finding).
- Naoki Shibuya's blog was named by agy for the 2-D circle framing but no URL
  was returned/verified — do not cite a URL for it until verified.

## How Part II per-slide workers extend this file

Same rules as Part I (§5 above): append per-slide findings, never edit family
rows or 001's rows; every downloaded figure lands in that slide's own
`slide_NNN_source/` with a SOURCES.md; `[pending raw]` marks here are cleared
by the per-slide worker only after script-12 + frame-level confirmation.

## Part II per-slide rows — slides 021–030 (web-verification worker, 2026-10-11)

Vision transcripts banked under `videos/deep-learning/002_transformers_part2/slide_0NN_source/transcripts/`
(default `images` route, `--thinking high --max-tokens 65536`, gated). Confidence per the legend above.
| 021 (002) | "[1] Position Encoding" concept intro — positions 0..N-1 → "function to map the positions to real valued vectors" → Vector_P0..Vector_PN-1; notes "[1] Function with Fixed Parameters / [2] Function with TRAINABLE Parameters"; "Vector Length = Word Embedding length" (transcript 2026-10-11) | **arXiv 1706.03762 §3.5** (live curl: "we must inject some information about the relative or absolute position…", "positional encodings have the same dimension d_model as the embeddings", "There are many choices of positional encodings, learned and fixed"); trainable alt = BERT 1810.04805 / GPT-1 (agy) | CONFIRMED (data); drawing course-original (no figure download) | Paper's learned-vs-fixed dichotomy = slide's [1]/[2] note; d_model-equality = green box text. SOURCES.md: `slide_021_source/` |
| 022 (002) | "Suggested Positional Encoders (Use Word Index as Position Encoding)" — strawman linear-index PE, "+δ" steps, δ=1, first=0/last=N-1, "Depends on Seq. Length"; Problems: (1) large N dominates embedding, (2) trained max len 256 can't extrapolate, (3) scalar PE vs vector word embedding (transcript 2026-10-11) | **Kazemnejad PE blog** (live curl: "assign a number to each time-step linearly… values could get quite large… face sentences longer than the ones in training"); **MLM positional-encoding tutorial** (live curl: "a single number, such as the index value, is not used… each position/index is mapped to a vector"); arXiv 1706.03762 §3.5 (d_model resolution) | CONFIRMED (all three problems); wording/example numbers (1024, 256, δ) course-authored; drawing course-original (no figure download) | SOURCES.md: `slide_022_source/` |
| 023 (002) | "Suggested Positional Encoders (Normalize Seq. Length to \"1\")" — normalized-index strawman: δ=1/Seq.Length, row 0,δ,2δ,…,1-δ,1; Problems: δ depends on length (position #4 differs short vs long seq), scalar-vs-vector (transcript 2026-10-11) | **MLM tutorial** (live curl: "normalize the index value to lie between 0 and 1… problems for variable length sequences… normalized differently"); **Kazemnejad** ([0,1]-range idea; "time-step delta doesn't have consistent meaning across different sentences", agy-retrieved from the same fetched page); arXiv 1706.03762 §3.5 | CONFIRMED (scheme + both problems); wording course-authored; drawing course-original (no figure download) | SOURCES.md: `slide_023_source/` |
| 024 (002) | "Suggested Positional Encoders (Rules Controlling Good Positional Encoder)" — 3 numbered rules over the same strawman rows: [1] δ same for long/short seq, [2] range independent of seq length (fixed ranges 0..1 / "form -1 to 1" typo kept), [3] PE is a vector same dim as word embedding (transcript 2026-10-11) | **Kazemnejad** (live curl: criteria list "consistent across sentences with different lengths… bounded… d-dimensional vector, not a single number"); arXiv 1706.03762 §3.5 ("same dimension d_model… so that the two can be summed") | CONFIRMED (all 3 rules); numbering/wording course-authored; drawing course-original (no figure download) | SOURCES.md: `slide_024_source/` |
| 002 (002) | Title slide "Transformers / Part II / Aug. 2020" — course-authored house slide, no figures, no equations | **None (course-authored)** — lecture video https://www.youtube.com/watch?v=1vYxr2TmkLA "[12] Transformers - Part II" (oEmbed re-verified live 2026-10-11 by the build worker); title text CONFIRMED against the verified video title | CONFIRMED (identity); slide pixels = frame-only ground truth | Capture artifacts (pen cursor, bottom letterbox) omitted per judge ground rules (c). SOURCES.md: `002_transformers_part2/slide_002_source/` |

## Part II per-slide rows — slides 041–050 (web-verification worker, 2026-10-11)

Vision transcripts banked under `videos/deep-learning/002_transformers_part2/slide_0NN_source/transcripts/`
(default `images` route, `--thinking high --max-tokens 65536`, all calls through `scripts/16_vision_gate.sh`).
Slides 041–045's own SOURCES.md files were co-produced by a parallel run; the second worker appended
independent cross-checks to each (nothing edited). 046–050 SOURCES.md written fresh by this worker.
| 041 (002) | "Normalization" — taxonomy tree: "Normalization of" → Activations Outputs → {Batch, Instance, Group, Layer Normalization}; → Weights → {Weight Normalization}; top box prints only "Normalization of" (second line "of") on the frame | **Wu & He 1803.08494** (ar5iv live: BN/LN/IN/GN = the feature-normalization family; WN "normalizes filter weights rather than features") + **Salimans & Kingma 1602.07868** (abs live) + Huang survey **2009.12836** (abs live; activation/weight split not in abstract [?]) | CONFIRMED (taxonomy); diagram course-original | Script-12 raw exists and agrees verbatim. SOURCES.md: `slide_041_source/` |
| 042 (002) | "Batch Data (Feature Vectors)" — CNN-background: 1×5 vector → 5×5 plane → 5-slab batch cuboid; axes "Feature Vector / Channels (4 Filters) / Batch size (5 samples)"; 5 columns drawn vs "4 filters" label (course artifact, frame wins) | **P3 shared source: Wu & He 1803.08494 Figure 2** (`all_norms.svg`, banked `slide_042_source/all_norms.svg`, sha f5f57e932869f740) — axis structure confirmed; cube pixel style course's own [?] | CONFIRMED (axis semantics/taxonomy); pixels [?] course redraw | No script-12 raw for 042 — the two independent banked vision transcripts are the frame evidence and agree. SOURCES.md: `slide_042_source/` |
| 043 (002) | "Batch Normalization" — callout "Calculate (then Normalize) μ, σ for ALL Samples in the batch (for each channel)"; bottom box: per-mini-batch stats / "will differ from mini-batch to another (Source of Error)" / "Mini Batch Size should be large enough (Constrain)"; paired cube blocks w/ axis arrows | **Ioffe & Szegedy 1502.03167** (abs live: "performing the normalization for each training mini-batch") + **P3: Wu & He Fig 2** BatchNorm subplot (one channel over all N) + Wu&He §1 batch-size sensitivity | CONFIRMED (definition + both caveats); cube pixels [?] course redraw | P3 family verified once (042's record), referenced here. SOURCES.md: `slide_043_source/` |
| 044 (002) | "Layer , Group, and Instance Normalization" — 4 cube stacks (reference / GN "(Group of Channels) General Case" / IN "ONE Channel in ONE Sample (Output of ONE Filter)" / LN "ALL Channels in the Same Sample" + yellow "Transformer choice" callout); heading "Sample Based Normalization" | **P3 shared source: Wu & He 1803.08494 Figure 2** (`all_norms.svg` banked in BOTH `slide_042_source/` and `slide_044_source/`, byte-identical) — LN=(C,H,W)/sample, IN=(H,W)/sample/channel, GN groups w/ LN,IN extremes, all verified; "Transformer choice" = Vaswani 1706.03762 §3.1 LayerNorm (live) | CONFIRMED (all four scopes + LN-as-transformer-norm); cube pixels [?] course redraw | Closest single-figure match of P3. SOURCES.md: `slide_044_source/` |
| 045 (002) | "Feed Forward Neural Network" — per-token stack: X row → Multi Head Self Attention Block → ⊕ + Layer Normalization (dashed group) → per-token FFN "One Hidden with RELU Activation [Size: at least double Input dimension]" + "Linear Activation Output [Size: same Input Vector dimension]" → Y rows; caption "Word_Embedding + Positional_Information" | **Vaswani 1706.03762v7 §3.3** (live: FFN(x)=max(0,xW1+b1)W2+b2, "two linear transformations with a ReLU activation in between", d_model=512/d_ff=2048) + §3.1 (live: "LayerNorm(x + Sublayer(x))") | CONFIRMED (per-position FFN, ReLU-between-two-linear, post-norm order); "at least double" = course lower bound vs paper 4× (recorded, kept) | Chain 45←28 — parent families: 002 map rows 026–034 (PE block) + 001 rows 26–30 (MHA math, CONFIRMED there). SOURCES.md: `slide_045_source/` |
| 046 (002) | untitled full-bleed encoder block: X row → MHA block → ⊕+LayerNorm (green dashed) → "Feed Forward Networks [ One Hidden with  RELU Activation]" (per-token MLP glyphs) → 2nd ⊕+LayerNorm → Y rows tagged "Final Output"; rightmost token subscripts low-res [?] (plausibly N-2/N-1, cf. 047) | **Vaswani 1706.03762v7 §3.1/§3.3** (live, same quotes as 045); canonical Fig 1 banked in 001 `slide_18_source/` | CONFIRMED (two-sub-layer topology + per-sub-layer residual+LN); drawing course-original; subscripts [?] | Chain 46←45; script-12 raw exists and agrees. SOURCES.md: `slide_046_source/` |
| 047 (002) | "Encoder Block" (vertical label; Block Input/Block Output): cleanest full-encoder frame of the 45→46→47 chain — resolves subscripts as X_{N-2}, X_{N-1} / Y_{N-2}, Y_{N-1}; two dashed (⊕ + LayerNorm) groups; per-token pink FFN sub-boxes | **Vaswani 1706.03762v7 §3.1** (live: "Each layer has two sub-layers… LayerNorm(x + Sublayer(x))") + §3.3 | CONFIRMED (exact two-sub-layer + both Add&Norm groups); drawing course-original (no published match asserted [?]) | Chain 47←46. SOURCES.md: `slide_047_source/` |
| 048 (002) | "Encoder Block" variant of 047 + RIGHT INSET (V/K/Q → Multi-Head Attention → Add & Norm → Feed Forward → Add & Norm, black residual paths) + "Layer Normalization (NOT Batch N…" bands + "Transformers Encoder" thumbnail; badge oval clipped (reads 48 [?]; script-12 raw said 49 — resolved toward 48, founder check pending [?]) | Inset = **Jay Alammar "The Illustrated Transformer" encoder zoom** — `Transformer_encoder.png` DOWNLOADED into `slide_048_source/` (792×411, sha c6d3360f8c0a4701, live). Main diagram = **Ketan Doshi, TDS "Transformers Explained Visually (Part 2)"** https://towardsdatascience.com/transformers-explained-visually-part-2-how-it-works-step-by-step-b49fa4a64f34/ — agy-confirmed content match (Block Input/Output, NOT-Batch-Norm bands, dashed groups, plus-circles) | Inset CONFIRMED (figure identity; pixel equality [?]); main diagram HIGH (origin, agy) — TDS unfetchable from here (2× ETIMEDOUT), pixels [?] | "MLA" cell labels plausibly "MLP" [?]. Chain 48←47. SOURCES.md: `slide_048_source/` |
| 049 (002) | "Transformer Stacked Encoder Blocks" — Word row → "Word Embedding" bar ABOVE "Positional Encoding / Embedding" bar → X vectors → "Transformer Encoder" container with "Encoder Block 0,1,2,…,M" → Y vectors; left labels Input Seq / Embedding Words & Pos. / Encoder Input / Encoder Output | **Vaswani 1706.03762v7 §3.1** (live: "The encoder is composed of a stack of N=6 identical layers") — course generalizes depth to 0..M; **Alammar stack figure** `The_transformer_encoders_decoders.png` DOWNLOADED into `slide_049_source/` (756×474, sha dc659655cf7305f7, live); bigger Alammar stack already banked in `slide_057_source/` | CONFIRMED (stack semantics); bar ORDER (WE above PE) = course quirk vs paper Fig 1, kept; drawing course redraw [?] | Chain 49←26 (founder assumption pending veto) — reuses 26-family (PE block) patterns without cloning composition. SOURCES.md: `slide_049_source/` |
| 050 (002) | "Transformer Decoder" — pure section divider (title + badge 50 only; pen pointer + letterbox = video artifacts) | **None needed (course-authored divider)**; introduces paper §3.1 Decoder ("The decoder is also composed of a stack of N=6 identical layers" — live-verified; decoder research + figures already banked in `slide_057_source/`) | CONFIRMED (course-authored, like 002 slide 003 divider) | No figures, no open questions. SOURCES.md: `slide_050_source/` |
| 025 (002) | "Sine/Cosine Encoders (an industrial application of Motor Control System)" — industrial aside: AC motor + sin/cos encoder disk (cos red / sin green quadrature traces), "Line count =16 (16 signal periods per revolution)", CCW/CW; cites "EXTRACTION OF HIGH RESOLUTION POSITION INFORMATION FROM SINUSOIDAL ENCODERS / J. Burke, J. F. Moynihan, K. Unterkofler" (transcript 2026-10-11) | Domain facts CONFIRMED live: Wikipedia "Rotary encoder" ("sine encoders, which output sinusoidal waveforms in quadrature (i.e., sine and cosine)") + Design World/MotionControlTips sine-encoder article (line count, quadrature, interpolation). **Citation venue [?]** — agy says PCIM-Europe 1999 (ADI authors) but unverifiable from this network (analog.com unreachable, AN-710.pdf 404, agy self-contradicts on AN-710; failed paths recorded in SOURCES.md) | Domain CONFIRMED; venue [?]; figures course-drawn/clip-art (no download) | Motivates §3.5 sin/cos PE (block 026–034). SOURCES.md: `slide_025_source/` |
| 026 (002) | "Sin/Cos Encoders (an industrial application of Motor Control System)" — FULL SYSTEM BLOCK DIAGRAM of TI reference design TIDA-00176: Fine Angle atan(A/B) → 16-bit/12-bit options, Coarse Angle incremental count, 12-bit ADC, eQEP, Host MCU Interface (SPI/Analog/TTL), Dual ADC, Comparators, 24V→5V/3.3V power, Encoder Supply 5.25 V, differential A±/B± + Marker R±, shielded twisted pairs 50...150m, 1-VPP (transcript 2026-10-11) | **TI TIDA-00176** "Interface to Sin/Cos Encoders With High-Resolution Position Interpolation" — tool page live (ti.com/tool/TIDA-00176); **design guide DOWNLOADED**: `slide_026_source/tidua05b.pdf` (TIDUA05B, 4,636,630 B, ti.com/lit/ug/tidua05b/tidua05b.pdf) — **slide = course redraw of guide Figure 1-1 "Simplified System Block Diagram of TIDA-00176"** (every label verbatim-matched in the PDF text) | CONFIRMED (figure identity established; the Part II family row's "[pending raw]" for 026 clears) | Heads the PE-family chain (children 027/028/029); [?] on-frame glyph atan1 vs atan(A/B) noted in SOURCES.md. SOURCES.md: `slide_026_source/` |

## Part II per-slide verification results — slides 002–011 (appended 2026-10-11 by the Part II web-verification worker, storm-resume run)

Per-slide records supersede the `[pending raw]`/`[?]` marks in the family rows
above for these slides. Method: ONE vision probe per slide (default `images`
route, `--thinking high --max-tokens 65536`, through `scripts/16_vision_gate.sh`;
transcript banked at
`videos/deep-learning/002_transformers_part2/slide_0NN_source/transcripts/slide0NN_vision_2026-10-11.txt`;
cross-checked against `analysis/slide_0NN_raw.json` where a raw existed) +
7 `agy -p` queries (002+003 combined, 004+005 combined, 006, 007, 009, 010, 011;
answers banked under `videos/deep-learning/002_transformers_part2/scratch/agy_s*.txt`).
NO downloads were needed: every published-figure source in this range is already
banked in `slide_18_source/` (Part I), and the rest is course-authored. Full
per-slide provenance in each `slide_0NN_source/SOURCES.md`.

| Slide | Content | Source | Confidence | Confirmed / open |
|---|---|---|---|---|
| 002 | Title "Transformers / Part II / Aug. 2020" | course-authored (agy: no public deck carries these slides) | CONFIRMED | Vision + raw agree; badge 2. "Aug. 2020" vs verified 2024 upload = same discrepancy as Part I's title rows; slide wins |
| 003 | "Review of Part I / Self Attention Mechanism" divider | course-authored (agy) | CONFIRMED | Divider targets 001's self-attention family (26–45) |
| 004 | "Encoder – Decoder Transformer": Figure 1 plain + recolored | banked Figure 1 (`slide_18_source/The Transformer - model architecture..png` = ModalNet-21.png, sha256-verified) | CONFIRMED (child 4 ← 001:15 AND 001:18) | Composition matches 001:15 (2 red up-arrows, transition arrow, full label set). NEW vs parent: 2 semi-transparent orange highlight rectangles over the attention blocks. [?] right-panel encoder spelling "Multiheaded" vs "Multi-Head" — build-time zoom |
| 005 | Figure 1 + Fig 2 left + Fig 2 right zoom ladder + callout banners | banked Figures 1/2L/2R (same dir; asset URLs re-confirmed by agy) | CONFIRMED | Banner wording identical to 001's slide-18 family; course deltas: orange/yellow highlight overlays, clock icons at Positional Encoding, stacked-shadow h heads. [?] encoder attention label obscured by highlight |
| 006 | Agenda (6 items: Parallelization… What is Next ?) | course-authored (agy: sequence matches no published deck) | CONFIRMED | Verbatim spacing anomalies (double spaces, "What is Next ?") are frame truth, not errors |
| 007 | "Parallelization / Implementation Issues" section header | course-authored; topic background = Vaswani §3.2 + Table 1 (agy quotes) | CONFIRMED | Slide empty except title/badge/cursor |
| 008 | Self-attention dataflow for X₂ (Linear Transformation of Inputs) | course-authored; paper §3.2/§3.2.1 + Bloem (child 8 ← 001:33) | CONFIRMED (child) | Row alignment RESOLVED on this frame (X₄↔K₄ … X₁↔K₁, both reads agree). [?] W superscript (0) vs (1), query q₂ vs q1, dot-box label K.q/K..q/K₂q, 4th ⊗ node — build-time zooms. Output reads "Y" (parent read Y₂) |
| 009 | "Using  FF NN  for Multiplication of a Vector by a Matrix" (FC net + Yᵀ = Sigmoid{X·W+b} graphic) | course-authored; Goodfellow et al. *Deep Learning* ch. 6 https://www.deeplearningbook.org/contents/mlp.html (agy) | CONFIRMED | Indexing verified internally consistent: w_ij first index = OUTPUT → equals standard σ(Wx+b); no numeric cells. [?] one tiny matrix-cell glyph (w_13 group) |
| 010 | "…of ONE Vector by a Matrix": W_q example; Sigmoid→Linear ("IF No Non-linearity") and bias→0 ("IF No Bias") deltas | course-authored; Goodfellow ch. 6 (linear/affine baseline) + paper §3.2.2 W^Q (agy) | CONFIRMED | Deltas mathematically exact (attention projections are linear, bias-free in the paper). "W_q is Squared Matrix" = course d×d bookkeeping (001 slide-37/43 precedent — convention difference, not an error). Vision transcript truncated after §4 (§5/§6 missing, no substance lost). [?] several left-panel edge subscripts |
| 011 | "Multi Head Self Attention of Word X₂" — five-head cascaded recap (Wide) | course-original; paper §3.2.2 + Bloem wide (child 11 ← 001:43) | CONFIRMED (child) | Scaling by √d present (unlike 008); h=5 vs paper h=8 (illustration, per parent). NEW rendering vs parent: 5 fanned overlapping head panels + red arc + emphasis ellipses/beam. [?] two-digit W codes (agy: ad-hoc, not a published convention), arc label "1st Heads"/"h Heads", concat/linear labels not seen on this frame — build-time zooms |

Storm-resume note: the previous verification run for this range banked nothing;
this table is the complete fresh record. Slides 012+ remain the responsibility of
their own per-slide workers.

## Part II per-slide rows — slides 41–50 (web-verification worker, 2026-10-11; APPEND ONLY)

Per-slide records complete: every slide below has `videos/deep-learning/
002_transformers_part2/slide_0NN_source/SOURCES.md` + a banked vision
transcript (`slide_0NN_source/transcripts/`; 042's transcript was banked by the
earlier interrupted run and reused). Confidence legend as above.

| Slide | Content (frame-verified) | Primary source | Confidence | Figures / notes |
|---|---|---|---|---|
| 041 | "Normalization" taxonomy tree: Normalization of → Activations Outputs (Batch/Instance/Group/Layer) + Weights (Weight Norm) | Wu & He ECCV 2018, arXiv:1803.08494 §2 (taxonomy of activation-norms vs weight-norm); Salimans & Kingma 2016 (1602.07868); Ba et al. 2016 (1607.06450) — all abs pages verified live | CONFIRMED (taxonomy); course-made drawing | No figure (course text tree). Top box reads only "Normalization of" at the frame [?] mid-build/never-completed. Motivates the transformer's LayerNorm (§3.1) |
| 042 | "Batch Data (Feature Vectors)": one filter → 4 filters [4 Channels] → mini-batch 5-samples cube; axes Feature Vector / Channels (4 Filters) / Batch size | Wu & He 2018 **Figure 2** (`all_norms.svg` from ar5iv assets, 184,742 B, 820×215, 4 subplots verified) — (N,C,feature) axis structure | CONFIRMED (axis structure + family); pixel style course's [?] | **P3 family bank**: `slide_042_source/all_norms.svg`. Drawn 5 columns vs "4 filters" label = course artifact (frame wins) |
| 043 | "Batch Normalization": cube block + callout "Calculate (then Normalize) μ, σ for ALL Samples in the batch (for each channel)"; bottom panel: mini-batch vs whole data, per-mini-batch variation (Source of Error), batch-size constraint | Ioffe & Szegedy 2015 (1502.03167, verified live) + Wu & He Fig 2 BatchNorm subplot (family bank 042) | CONFIRMED | P3 member. Cube style course's; no numbers |
| 044 | "Layer , Group, and Instance Normalization" (verbatim spacing): "Sample Based Normalization"; 4 cube stacks (reference/GN/IN/LN); LN box "μ,σ for ALL Channels in the Same Sample"; black oval "Transformer choice" on LN | Wu & He 2018 **Figure 2** (4 subplots = the 4 stacks); Ba et al. 2016 (LN); Vaswani §3.1 (Add&Norm); Ulyanov 2016 (1607.08022, IN) | CONFIRMED | P3 member. Vision transcript's "Figure 1 style" guess CORRECTED to Figure 2 (Fig 1 = error-vs-batch-size). Course order GN→IN→LN vs paper BN→LN→IN→GN |
| 045 | "Feed Forward Neural Network": per-token dataflow X row → MHSA Block → residual ⊕ → LayerNorm → per-token FFN (one hidden, RELU, "[Size: at least double Input dimension]"; linear output, same dim) | Vaswani §3.3 verbatim (fetched: "applied to each position separately and identically", "two linear transformations with a ReLU activation in between", FFN eq. 2, d_model=512, d_ff=2048); §3.1 LayerNorm(x+Sublayer(x)); Fig 1 bank in 001 `slide_18_source/` | CONFIRMED | Course "at least double" vs paper 4× — recorded, not a contradiction. All rows labeled Y_i (course notation) |
| 046 | untitled full-bleed: FULL encoder layer, zero-based X₀…X_{N-1}, split yellow|pink cells "Word Embedding + Positional Information", TWO ⊕+LayerNorm groups, "Final Output" | Vaswani §3.1 (two sub-layers, residual+LayerNorm around each) + §3.5 (PE added to embeddings at stack bottoms) — verbatim fetched | CONFIRMED | Founder-kept mid-group frame of the 46/47 split. "N3" glyph [?] → RESOLVED as N−2 by 47. Indexing differs from 45 (X₁..X_N) — course inconsistency, frame wins |
| 047 | untitled "Encoder Block": same diagram wrapped (Block Input/Output boxes, "Encoder Block" vertical label, tan panel, orange FFN boxes) | Vaswani §3.1 ("encoder is composed of a stack of N=6 identical layers"; two residual+LayerNorm wraps) | CONFIRMED | 47←46. Nx repetition tag omitted (course choice). Penultimate subscript = N−2 (resolves 46) |
| 048 | "Encoder Block" + right inset (V/K/Q → Multi-Head Attention → Add & Norm → Feed Forward → Add & Norm, residual loops) + bottom-left inset "The Original Encoder Block"; "Layer Normalization (NOT Batch N…)" | Jay Alammar Illustrated Transformer — **`Transformer_encoder.png`** downloaded into `slide_048_source/` (792×411, 32,628 B; figure sits at "broken down into two sub-layers" in the page, verified); Vaswani §3.1 (LayerNorm, ref [1]) | CONFIRMED (inset family); pixel match [?] build-time | Main panel = 47's composition + insets. FFN-cell tiny label "MHA"/"MLP" [?]; "The Original Encoder Block" thumbnail identity [?] (candidate: banked Fig 1 encoder half). Rows end X_{N-1},X_N (differs from 47 — course inconsistency, frame wins) |
| 049 | "Transformer Stacked Encoder Blocks": Word 0..N-1 → Word Embedding + Positional Encoding/Embedding bars → X tokens → Encoder Block 0,1,2,…,M → Y tokens; left labels Input Seq/Encoder Input/Encoder Output | Vaswani §3.1 (stack of N=6 identical layers; course generalizes to M+1) + §3.5 (PE + embeddings summed at bottom); Alammar stack figures referenced (not downloaded, no direct reuse); dep 49←26 = 001 self-attention family PATTERN (do not clone; 26's record: 001 `slide_026_source/SOURCES.md`) | CONFIRMED (semantics); drawing course-original | Middle token subscripts small [?]; pattern 0..N−1 unambiguous |
| 050 | "Transformer Decoder" — plain section-divider title card (7-frame group) | none — course-authored divider (001/002 divider precedent) | CONFIRMED course-authored | No content to verify; decoder content researched at 051+/057 rows |

Notes for downstream workers:
- P3 (42/43/44) verified once against Wu & He Figure 2; the family figure bank
  lives at `002_transformers_part2/slide_042_source/all_norms.svg` — reference
  it, do not re-download.
- Paper v7 HTML was fetched once this run (scratch/v7.html in the video's
  scratch/ dir); all §3.1/§3.3/§3.5 quotes in the SOURCES.md files above were
  extracted from that live fetch.
- No failures this run; every URL cited was fetched live 2026-10-11. agy was
  used for source identification (normalization taxonomy, GN Figure 2); WebFetch
  direct on arxiv.org timed out once (WebFetch) and DNS failed once (curl rc=6)
  — both succeeded on retry; recorded per storm-resilience protocol.
| 027 (002) | "Sequence of 5 words — Positions are defined as angles" — clock-face circle: Word 0..4 at 30° counterclockwise steps, "+ω" arcs, inset "Sin(ω t) / Cos(ω t) / t=0,1,2,3,...." (transcript 2026-10-11) | **Kazemnejad** (canonical origin of the 2-D sin(ωt);cos(ωt) circle pedagogy; BOTH figures DOWNLOADED into `slide_027_source/`: positional_encoding.png 43,159 B + time-steps_dot_product.png 30,320 B — sizes match the map's records; slide drawing itself is course-authored, not pixel-copied); arXiv 1706.03762 §3.5 (sin/cos formulas + fixed-offset linearity) | HIGH origin confirmed for concept; drawing course-original | Child of 026 (dep 28←[27,26]); [?] ω numeric-vs-symbolic. SOURCES.md: `slide_027_source/` |

## Part II per-slide rows — slides 016–020 (web-verification worker, resumed run, 2026-10-11)

Slides 016–020 processed by the resumed range worker (previous two runs died in
provider storms). Vision transcripts banked under
`videos/deep-learning/002_transformers_part2/slide_0NN_source/transcripts/`
(default `images` route, `--thinking high --max-tokens 65536`, all calls through
`scripts/16_vision_gate.sh`). Confidence per the legend above.

| Slide (video) | Content (evidence) | Primary source | Confidence | Notes |
|---|---|---|---|---|
| 016 (002) | "Using FF NN for Multiplication of Multiple Vectors by Multiple Matrices" — 5 embedding rows X_1..X_5 (4-dim) × three per-head 4x4 W_k grids ("W_k of Head 1/2/3") = three 5-row output stacks ("Corresponding Projections at Head 1/2/3"); callout "Sequence of 5 Words / Network with 3 Heads / Embedding Dimension=4"; subtitle "Usage: Multiply Vectors of All Words by Multiple (different) W_k (Keys of Multiple Heads)" (transcript banked by earlier run 2026-10-11, reused) | **Vaswani 1706.03762v7 §3.2.2** (live WebFetch this session: "linearly project the queries, keys and values h times with different, learned linear projections", head_i = Attention(QW^Q_i, KW^K_i, VW^V_i), MultiHead = Concat·W^O, h=8) + **Bloem** (live: per-head W_q^r/W_k^r/W_v^r, k×k wide matrices, per-head y_i^r) — same source pair as P1 siblings 012/014 | CONFIRMED (data); drawing course-original (no figure download) | P1 family [9,10,12,14,16] completion: 012 = 1 vector × many W_q, 014 = all vectors × 1 W, 016 = all vectors × per-head W_k. SOURCES.md: `slide_016_source/` |
| 028 (002) | "Sequence of 9 words — Positions are defined as angles" — 9-word sibling of 027: circle with Word 0..8 counterclockwise, "+ω" arcs ×9, same inset Sin(ωt)/Cos(ωt)/t=0,1,2,3,.... (transcript 2026-10-11; old group 60 split 028/029, founder frame swap kept mid-group frame) | Same family bank: Kazemnejad (figures banked in `slide_027_source/`) + arXiv 1706.03762 §3.5; no new claims vs 027 | CONFIRMED (family); drawing course-original; no new downloads (references 027's bank) | Dep 28←[27,26]. SOURCES.md: `slide_028_source/` |
| 017 (002) | "Multi Head Self Attention of Word X_2" — cascaded h=1..h=5 panels (per-head W_k^h/W_v^h/W_q^h → Dot Product "K:q" → Scaling by √d → Soft max → Σ weighted sum) + "Concatenated Vector" bar 1×dH + "Linear Transformation [T]" (edge label d×H×d [?]) → 1×d; "+H Heads" curved arrow; bottom-right inset legend 1×d·W(d×d)=1×d, "d : Embedding Length" (transcript 2026-10-11) | **Cross-video child of 001:43** — parent record `../001_transformers_part1/slide_043_source/SOURCES.md` (paper §3.2.2 + Bloem) CARRIES per the recap rule; both sources re-confirmed live this session (Vaswani §3.2.2 verbatim + Bloem k×k wide) | CONFIRMED (carried); composition this frame's own | Shows Concat+Linear labels explicitly (015's [?absent] resolved on THIS frame); "d×H×d" vs parent "dH×d" tiny-glyph [?]. SOURCES.md: `slide_017_source/` |

### Reconciliation note — slides 41–50 double-run (this worker, 2026-10-11, APPEND ONLY)

A parallel web-verification worker processed the SAME range 041–050
concurrently (provider-storm resume double-dispatch); its table above
(rows "041 (002)"–"050 (002)") and this worker's table above (rows
"041"–"050") are two independent records of the same slides. Facts agree on
every substantive point (P3 = Wu & He Fig 2; 45–47 = Vaswani §3.1/§3.3; 48 =
Alammar encoder zoom + course variant; 49 = §3.1 stack + §3.5; 50 = divider).
File-level outcome, verified on disk:

- `slide_041..045_source/SOURCES.md` — this worker's records with the parallel
  worker's independent Cross-check sections appended (both intact).
- `slide_046..050_source/SOURCES.md` — this worker's records survived the
  concurrent writes; the parallel worker's unique per-slide findings (046
  script-12 raw agreement; 048 Ketan Doshi TDS main-diagram source + badge
  49-vs-48 raw note; 049 downloaded Alammar stack figure + WE-above-PE quirk)
  are now mirrored into those files as attributed Cross-check/reconciliation
  sections. No content was deleted; figures banked by either worker are
  preserved unrenamed.
- Figures now on disk: `slide_042_source/all_norms.svg` (+ byte-identical copy
  in `slide_044_source/`, sha f5f57e932869f740),
  `slide_048_source/Transformer_encoder.png` (sha c6d3360f8c0a4701),
  `slide_049_source/The_transformer_encoders_decoders.png` (sha dc659655cf7305f7).
- Downstream workers: treat the two tables as CORROBORATION, not four
  independent sources; per-slide SOURCES.md is the record of truth.
| 029 (002) | "Sequence of 12 words — Positions are defined as angles" — 12-word circle (Word 0..11, 30° steps), "+ω" arcs, same inset; NEW callout "Using smaller ω value, allow representation of longer sequences (practically use ω = 1/10000)" (transcript 2026-10-11; final frame of old group 60) | **arXiv 1706.03762 §3.5** (live curl: base 10000 in PE formulas, "wavelengths form a geometric progression from 2π to 10000·2π", "may allow the model to extrapolate to sequence lengths longer…"); Kazemnejad ("decreasing their frequencies…") | CONFIRMED (ω=1/10000 = paper's base in the 2-D toy setting; motivation verbatim-matched); drawing course-original (family bank `slide_027_source/`) | Dep 29←28. SOURCES.md: `slide_029_source/` |
| 030 (002) | no title, badge 30 — rotation-matrix derivation: [sin(ωt);cos(ωt)] and [Sin(ω(t+δ));cos(ω(t+δ))] (capital Sin verbatim), "Remember:" sin(a+b)/cos(a+b) identities, expansion lines, matrix [cos(ωδ) sin(ωδ); −sin(ωδ) cos(ωδ)]×[sin(ωt);cos(ωt)] under brace "Independent of Position t", box "From Computer Graphics: Rotation Matrix … angle ωδ e.g ω, 2ω, 3ω, …" (transcript 2026-10-11) | **Kazemnejad "Relative Positioning" section** (live curl: identical addition-theorem expansion, M_{φ,k} = [[cos, sin],[−sin, cos]], "does not depend on t", "very similar to the rotation matrix"); arXiv 1706.03762 §3.5 ("PE_{pos+k} can be represented as a linear function of PE_pos") | CONFIRMED (equation-by-equation); composition course-authored; no figures | Ends the 026-family chain (29←28, 30 next in deck flow). SOURCES.md: `slide_030_source/` |
| 018 (002) | "Adding Position Information" — two-line agenda box: "[1] Position Encoding" / "[2] Position Embedding" (no diagram, no equations); cursor + letterbox artifacts (transcript 2026-10-11) | **arXiv 1706.03762v7 §3.5** (live WebFetch this session: "There are many choices of positional encodings, learned and fixed [9]." — the slide's dichotomy verbatim; d_model-equality sentence) + [2]-branch trainable variant carried from 021's verified record (BERT 1810.04805 / GPT-1, agy) | CONFIRMED (data); agenda slide course-authored (no figure download) | Introduces the PE block (019–026). SOURCES.md: `slide_018_source/` |
| 019 (002) | "Encoder – Decoder Transformer" — three green-outlined panels: course redraws of paper Fig 2 left (Scaled Dot-Product) + Fig 2 right (Multi-Head, "h" annotation) + full encoder-decoder panel (Inputs / Outputs (shifted right), Positional Encoding, Add & Norm, Feed Forward, Masked MHA, Linear, Softmax, Output Probabilities, N×) with red dotted zoom-callout lines, dashed red cross-connection arcs, Q/K/V circles; presenter overlay "WE ARE HERE" pin + 2 yellow highlighter blobs (transcript 2026-10-11) | **Cross-video child of 001:19** — parent record + figure bank (`../001_transformers_part1/slide_18_source/`) CARRY; paper §3.1 re-confirmed live this session ("The encoder is composed of a stack of N=6 identical layers."); right panel = paper Fig 1 data in Alammar styling — candidate `The_transformer_encoder_decoder_stack.png` (1218×793) ALREADY BANKED in `slide_057_source/`, referenced not re-downloaded | CONFIRMED (carried); right-panel Alammar styling HIGH (transcript identification), pixel identity [?] | Open [?]: encoder column order reads inverted on the frame (zoom t≈746–762 s); Mask-vs-Scale order [?]. SOURCES.md: `slide_019_source/` |
| 020 (002) | "Pre-processing of Input Sequence" — 4 dotted rows: Word 0..N-1 → X_0..X_{N-1} ("Word Embedding e.g. word2vec", empty vector cells) → Pos 0..N-1 ("Position Information", orange rotation arrows, "+δ" ×6) → red banner "Combine Word Encoding and Position Information (for Each Word)" → I/P_0..I/P_{N-1} → caption "Input to first Self Attention Layer in Transformer"; inset = miniature of paper Fig 1 input path (Positional Encoding → Input Embedding → inputs), "Input to Encoder" (transcript 2026-10-11) | **arXiv 1706.03762v7 §3.5** (live this session: "To this end, we add 'positional encodings' to the input embeddings at the bottoms of the encoder and decoder stacks." + d_model-equality sentence) + §3.1 (encoder stack N=6, live) + banked Figure 1 (inset redraw); word2vec example carried from Part I's verified 021/022 records (Mikolov 2013) | CONFIRMED (data); 4-row composition course-authored; Alammar PE-vectors figure [?] style-candidate only (not downloaded) | P2 first member; 0-based indexing on THIS slide (frame wins vs 012/014/016's 1-based). [?] inset small text + row-4 ellipsis. SOURCES.md: `slide_020_source/` |
| 031 (002) | "Squared Distance Between Vector of Pos "t+δ" and Vector of Pos "t"" + "[ Two Consecutive Positions ]" — two top panels ([sin(ωt);cos(ωt)] → yellow-chip [sin(a);cos(a)]; angle-addition expansion vector = expanded form → a/b vector), boxes "Let ωt=a , ωδ=b" / "sin²(a)+cos²(a)=1", 7 printed derivation rows ending in box "=2 (1-cos(ωδ) )" (navy bold) + rotated ribbon "Irrespective of Position "t"" (transcript 2026-10-11 + build-worker PIL) | **Kazemnejad "Positional Encoding in Transformers"** (neighboring-time-step distance property, Fig 3 dot-product heatmap) + **arXiv 1706.03762 §3.5** ("PE_{pos+k} can be represented as a linear function of PE_pos"); fresh agy 2026-10-11 re-confirmed ||e(t+δ)−e(t)||² = 2(1−cos(ωδ)) position-independent via sin²+cos²=1 + addition theorem | CONFIRMED (result + machinery); printed 7-row derivation course-authored (no published step-by-step counterpart; algebra line-checked) | Frame overrides spec: banner colors alternate red/blue mid-title; rows 2-6 black; row 1 has 2 yellow chips; "=" column detached x767..783. SOURCES.md: `002_transformers_part2/slide_031_source/` |

## Part II per-slide records — appended 2026-10-11 (web-verification worker, slides 052–056, 058–060; range resume after provider storm; 051/057 were already banked)

One row per slide, resolving the `[pending raw]` marks of the Part II range
table above at frame level (vision transcripts banked per slide under
`videos/deep-learning/002_transformers_part2/slide_NNN_source/transcripts/`;
full provenance in each `slide_NNN_source/SOURCES.md`). Same confidence
legend. Storm notes: several `agy` calls died (`error: interrupted`, one
300 s proxy timeout, one ~17 min hang) — each retried per the storm
protocol; agy twice CONFABULATED figure origins (claims contradicted by the
live pages, recorded in 052's SOURCES.md) — live fetches were treated as
authoritative every time.

| Slide | Content (frame-verified) | Primary source | Confidence | What specifically matches / open |
|---|---|---|---|---|
| **052** | Decoder walkthrough: encoder "I feel Sick" → decoder "SOS Je me sens malade", masked MHA + "Encode Decoder Attention" (K/V from encoder, Q from decoder) + FFN, residual+LayerNorm bars, "Word and Position Encoding" | **arXiv 1706.03762 §3.1/§3.2.2** (decoder anatomy, shifted-right inputs, Q-from-decoder/K,V-from-encoder) + Alammar Illustrated Transformer (live-verified: its example is "je suis étudiant"→"i am a student" — slide's sentence/labels are course-authored) | CONFIRMED (architecture); figure origin course-authored `[?]` | Downloaded `Transformer_decoder.png`, `transformer_resideual_layer_norm.png` into `slide_052_source/`. agy claimed the slide's exact cartoon is Alammar's — live page disproves (no "malade"/"SOS"/its labels); do not repeat that claim |
| **053** | "Self Attention Look Ahead Mask (Used in Decoder first Block)": 5×5 mask matrix 0 (lower-tri) / −∞ (upper-tri) over SOS Je me sens malade + softmax σ(x_j)=e^{x_j}/Σ_i e^{x_i} + "Mask Values are ADDED…" callout | **arXiv 1706.03762 §3.2.1** ("masking out (setting to −∞) all values in the input of the softmax which correspond to illegal connections") + **§3.2.3.1** (position i attends only to < i) + softmax definition (Wikipedia, live) | CONFIRMED (mechanism); figure course-authored `[?]` | No downloads (no published figure matches the course's pixels). Mechanism explainer identified via agy + Wayback-verified: Mongaras "How Do Self-Attention Masks Work?" (gmongaras.medium.com) — same mechanism, different example ("cómo estás") |
| **054** | "Self Attention Mechanism for Decoder (Adding Mask)": single-query pipeline Z→W_k^(0)/W_v^(0)/W_q^(1)→K.q→Scaling by √d→Mask[−∞,−∞,0,0]→Softmax(0)→⊗V→Σ→Z; legend 1×d·(d×d)=1×d, "d: Embedding Length" | **arXiv 1706.03762 §3.2.1 Eq(1)** + §3.2.2 (learned projections) + §3.2.3.1 (mask); Alammar step-by-step (live, lacks the slide's labels) + Mongaras (mask) | CONFIRMED (mechanism); figure course-authored `[?]` | **P4 LEAD** — shared pattern verified once here; 055 references it. agy stream died once mid-answer (retried). Open: W superscript semantics (0)/(1) `[?]`, top output glyph `[?]` |
| **055** | "Encoder-Decoder Attention Mechanism (In Decoder)": cross-attention single-head walkthrough — encoder outputs Y₁–Y₄ ("From Encoder Output") → W_k/W_v → K/V; decoder Z₂ ("From Decoder Self Attention Layer") → W_q → q₂ → Dot Product → Scaling √d → Softmax → ⊗ → Σ → O | **arXiv 1706.03762 §3.2.3** ("queries come from the previous decoder layer, and the memory keys and values come from the output of the encoder" — live-verified) + P4-shared §3.2.1/§3.2.2 (see 054) | CONFIRMED (mechanism); figure course-authored `[?]` | **P4 FOLLOW** — references `slide_054_source/SOURCES.md`; no extra agy spend. Subtitle loosely says "Self Attention of word Z₂ w.r.t All words in Sentence (Y₁…Y₄)" — drawn dataflow is cross-attention (slide wording wins for recreation). Open: "K₁.q" vs "K₂.q" read `[?]` |
| **056** | "Decoder Final Output": Last Decoder Block → Linear Projection (4 green circles fan to 16 magenta) → Softmax → 16 probability circles, "Probability of each word in Vocab", "Vocab Size" labels | **arXiv 1706.03762 §3.1** ("use the usual learned linear transformation and softmax function to convert the decoder output to predicted next-token probabilities" — live) + Alammar "The Final Linear and Softmax Layer" section (live) | CONFIRMED | Downloaded `transformer_decoder_output_softmax.png` (869×561, live) into `slide_056_source/`. Brief transitional slide (2 frames) |
| **058** | "Transformer Encoder as a Classifier" — plain section divider, no content | course-authored (frame-verified divider); topic anchor: BERT (arXiv:1810.04805) encoder-classifier pattern | CONFIRMED course-authored; topic anchor HIGH | No figures. Open: which classifier recipe the following section uses (CLS vs pooling) `[?]` — resolved by 059: it teaches Global Average Pooling |
| **059** | Encoder-classifier architecture: Word Embedding Vectors X₁…X_{N−1} ⊕ Position Information Vectors Vector_P0…Vector_P(N−2) → stacked Transformer Blocks → Output Sequence Y → Global Average Pooling ("Single vector representing the whole sequence") → Softmax Layer (Σ nodes) → C₁ C₂ C₃ | **arXiv 1706.03762 §3.1** (embeddings+PE, N identical layers) + **keras.io "Text classification with Transformer" by Apoorv Nandan** (live-verified: TokenAndPositionEmbedding → TransformerBlock → GlobalAveragePooling1D → Dense softmax) — GAP tail matches the Keras example, not BERT's [CLS] | CONFIRMED (mechanism; agy query converged on the same keras.io example); figure course-authored `[?]` | Founder pattern-derived dep 59←001:38 honored (family pattern referenced, composition NOT cloned). Open: Vector_P0 vs X_1 indexing-offset quirk (slide's own, keep verbatim) `[?]` |
| **060** | "What is Next (as of 2020)" closing list: GPT-1/2, BERT, RoBERTa, Transformer-XL, T5, GPT-3 (175B, Beta June 2020) | The slide CITES its sources — all six verified live: GPT-1 Jun 2018 + GPT-2 Feb 2019 (Wikipedia; openai.com bot-blocked), BERT arXiv:1810.04805 (v2 24 May 2019), RoBERTa arXiv:1907.11692 (26 Jul 2019), Transformer-XL arXiv:1901.02860 (Dai et al., CMU+Google Brain), T5 arXiv:1910.10683, GPT-3 arXiv:2005.14165 + API beta Jun 11 2020 | CONFIRMED (2 minor slide-side date/name slips recorded: RoBERTa "June 2019" vs arXiv Jul 2019; "Zhang Dai" vs Zihang Dai — slide wins for recreation) | No figures. No downloads needed (text list) |

Range close-out: slides 052–056, 058–060 now have SOURCES.md + banked vision
transcripts; 051 and 057 were already banked (untouched this run). The
`[pending raw]` marks for these rows in the Part II range table above are
resolved by these records (marks left in place per append-only law).

## Part II per-slide rows — slides 039–040 (web-research worker, 2026-10-11; range 021–040 completion, APPEND ONLY)

| 039 (002) | "Normalization" — covariate-shift motivation: italic quote box + "{Covariate shift }" tag, 3-box causal chain (weights change → activation outputs change → next-layer inputs change distribution), "Normalization: Transforming the inputs to be Zero mean and unit variance", bottom 2 bullets (stable distribution / accelerate training, no tiny learning rates) | **Ioffe & Szegedy 1502.03167** (abstract/§1 statements verbatim-confirmed against the banked live fetch `002.../scratch/webverify/bn_ar5iv.html`; internal-covariate-shift definition, "zero means and unit variances", stable-distribution/acceleration rationale). Slide WORDING is course-authored (agy attribution attempt was grep-contradicted and corrected in the record) | CONFIRMED (concepts); wording course-authored | Record finalized this run: the complete SOURCES.md had been left as `SOURCES.md.tmp` (interrupted write); now live at `slide_039_source/SOURCES.md` (content cross-checked against `analysis/slide_039_raw.json` — full agreement) |
| 040 (002) | "Normalization Parameters" — intro paragraph (γ/β learnable scale/shift relaxing strict zero-mean/unit-variance) + algorithm panel reproducing **Ioffe & Szegedy Algorithm 1** verbatim: Input 𝓑={x_{1..m}}, Parameters γ,β; Output {y_i=BN_{γ,β}(x_i)}; μ_𝓑, σ²_𝓑, x̂_i, y_i equations with the paper's own `// mini-batch mean / mini-batch variance / normalize / scale and shift` comments; course color-highlight overlays | **Ioffe & Szegedy 1502.03167, Algorithm 1** — every line (incl. the four `//` comments and the 𝓑 calligraphic) verbatim-confirmed against the banked live fetch; §3 text confirms the γ/β mechanism ("represent the identity transform", "learned along with the original model parameters", "restore the representation power") | CONFIRMED (algorithm box verbatim); intro wording + all highlights course-authored | Record written this run: `slide_040_source/SOURCES.md` (from the full script-12 raw + the banked fetch; 0 new agy/WebFetch spent). No figure download — the panel is a course re-typeset, not published pixels. [?] intro-paragraph wording provenance beyond the paper; [?] ε vs ϵ glyph at build zoom |

## Part II raw-landing verification — slides 041–052 (raw pass worker, 2026-10-11; APPEND ONLY)

Script-12 raws landed for 041–044, 046, 048–050, 052 (045 and 047 have NO raws — their
records stand on the banked vision transcripts). Each slide's SOURCES.md now carries a
dated "Raw-landing verification" append reading the raw in full. Summary of deltas that
supersede or refine rows above:

- 041, 043, 044, 050, 052: raws agree verbatim with the existing records; no source or
  provenance changes (52's three [?]s re-statused in its record; 46/48 notes below).
- 042: raw reads the middle grid as **4 columns × 5 rows (20 cubes)** — the drawn count
  MATCHES "[ 4 Channels]"; the 042 row's "5 columns drawn vs 4 filters (course artifact)"
  flag is SUPERSEDED. Slab-color readings differ between the two transcripts
  (magenta/orange/yellow/blue-gray vs magenta/yellow/orange/green/blue) [?] build-time PIL check.
- 046: raw re-reads the two rightmost token subscripts as "N3"/"N4" (possibly N−3/N−4);
  the 047-clean-frame resolution (N−2/N−1) stays primary; build-time zoom [?]. Raw does NOT
  corroborate the "last two boxes highlighted yellow" claim [?].
- 048: FFN-cell tiny label RESOLVED as **"MLP"** (raw, ×6). Badge conflict ELEVATED: two
  independent script-12 raws read the printed badge as **"49"** vs file id 48 (root house
  rule: badge = printed number; 002 AGENTS.md: badge = file id — cannot both hold).
  Founder + PIL-zoom check pending [?]; do not silently pick in the build.
- 049: middle subscripts CONFIRMED (digits 2–5); final X subscript raw-read "N−3", likely
  N−1 (blurry) [?].

## Part II range 002–020 closeout — script-12 raws landed + cross-checked (raw-verification worker, 2026-10-11, APPEND ONLY)

Every slide in 002–020 now has a script-12 raw in `videos/deep-learning/
002_transformers_part2/analysis/` EXCEPT 015 (no raw — SKIPPED-no-raw; its
earlier transcript-based SOURCES.md stands untouched). The raw-verification
worker re-read each raw in full and appended a dated "Script-12 raw
cross-check" section to each existing `slide_0NN_source/SOURCES.md`
(002–014, 016–020) — append-only, prior records intact. This clears the
remaining `[pending raw]`/`[?]` marks of the family rows "005–007, 009, 010,
012, 014, 016, 018" and "020–027…" for these slides; the per-slide SOURCES.md
files are the record of truth. Key raw-level resolutions (details per file):

- 004: raw reads "Multi-Head Attention" on BOTH panels — resolves the
  "Multiheaded vs Multi-Head" [?] toward the paper spelling.
- 011: arc label = italic "h Heads"; no concat/linear labels on this frame
  (confirmed by 2nd read); bottom row = exactly X₁..X₄.
- 012: Head-2 marker = magenta X_2 below the matrix pointing up at cell W_43.
- 013: output box label "V" (resolves V-ish vs Y₂); W superscript leans "(r)".
- 014: exactly 3 Σ neurons visible (y₁..y₃); fanned X₃/X₄/X₂/X₁ label deck added.
- 016: Head-1 first cell = W₁₁ (all three grids identical).
- 017: Linear box label = "d×H·d"; W_qᴴ; concat segments Y₁ᴴ..Y₅ᴴ; 3-vs-4 key
  count contested (zoom stands).
- 019: encoder column in PAPER order (attention below FFN — transcript
  mis-order resolved); Scale below Mask (opt.); V/K/Q under both decoder
  attention boxes.
- 020: inset = "Input Embedding"; row 4 has NO ellipsis dots; 6 "+δ".
- Script-13 finals already landed for 002/003/016/019/020 (all
  PASS_WITH_FIXES; titles verbatim-carried raw→final). No figure downloads and
  no new web fetches were needed for this pass (all sources verified live
  2026-10-11 by the rows above; raws surfaced no new published-figure claims).
