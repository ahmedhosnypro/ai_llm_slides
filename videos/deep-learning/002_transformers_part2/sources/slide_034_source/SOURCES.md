# SOURCES.md — slide 034 "[2] Position Embedding" (trainable/learned position embedding)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_034_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner) cross-checked against `analysis/slide_034_raw.json` (raw
agrees on all labels and the green-box lines). Web evidence: paper §3.5
(banked `scratch/webverify/paper_v7.html`) + two fresh live fetches this run
(BERT ar5iv, Kazemnejad-2023 abs) + one `agy` query (arXiv ID resolution).
This slide is the **[2] branch of the P2 family** (siblings 020/021/022 per
`slide_dependencies.json`; 021's record established the
"[1] fixed parameters / [2] TRAINABLE parameters" dichotomy with BERT/GPT-1
as the trainable exemplars).

## Slide identity

- New (curated) slide **034** ← old extraction **69** —
  `unique_slides/new2old_mapping.json`, frame `unique_slides/slide_034.jpg`.
  P2 pattern group member [20,21,22,34].
- Frame facts (vision transcript): title "[2] Position Embedding" ("[2]" red,
  rest blue); subtitle "(Similar to Word Embedding)" (red); badge "34".
  Three-stage vertical flow:
  1. Dashed-blue container: position boxes 0,1,2,3,4,5, …(5 dots)…, N-2, N-1;
     left labels "Position Information" + "(similar to word tokenization)".
  2. Purple bar "Embedding Layer to Learn Position Vectors"; left label
     "Positional Embedding" + "(Trained on Position Values)".
  3. Dashed-green container: Vector_P0 … Vector_P5, …, Vector_PN-2,
     Vector_PN-1 (pink boxes, red borders); red curly brace grouping them.
  - Green annotation box: "Real valued vectors representing  positions" /
    "(Vector for each position)" / "Positions > N-1  can NOT be Embedded" /
    "(Must Train Embedding on Max Expected Seq. Length)" (Train underlined) /
    "Vector Length  = Word Embedding length".
  - Artifacts: mouse cursor near Vector_P3; bottom letterbox bar.

## Primary sources

1. **arXiv 1706.03762v7 §3.5** (live curl 2026-10-11, banked) — verbatim:
   - "There are many choices of positional encodings, **learned and fixed**
     [9]." — the slide's "[2]" branch is the paper's *learned* option.
   - "We also experimented with using **learned positional embeddings** [9]
     instead, and found that the two versions produced nearly identical
     results (see Table 3 row (E)). We chose the sinusoidal version because
     it may allow the model to extrapolate to sequence lengths longer than
     the ones encountered during training." — the paper's own statement of
     the learned-PE trade-off the slide teaches (trainable ≈ same quality;
     sinusoidal extrapolates).
   - Reference **[9] = Gehring, Auli, Grangier, Yarats, Dauphin,
     "Convolutional Sequence to Sequence Learning", arXiv:1705.03122 (2017)**
     (identity extracted from the same banked fetch) — the learned-position-
     embedding exemplar the paper cites.
2. **Devlin et al., "BERT" (arXiv:1810.04805)** — ar5iv body fetched live this
   run (`scratch/webverify/bert_ar5iv.html`): "For a given token, its input
   representation is constructed by **summing the corresponding token,
   segment, and position embeddings**" (§3.2 / Figure 2 "BERT input
   representation"). Summing forces the position embedding to carry the SAME
   dimension as the hidden size — confirming the slide's "Vector Length =
   Word Embedding length"; BERT is the canonical deployed example of a
   trained-on-position-values embedding layer (max position embeddings are
   fixed at training time).
3. **Kazemnejad et al., "The Impact of Positional Encoding on Length
   Generalization in Transformers" (arXiv:2305.19466, NeurIPS 2023)** — abs
   fetched live this run (`scratch/webverify/kaz23_abs.html`): among
   "the most commonly used positional encoding methods, such as ALiBi,
   Rotary, and **APE [Absolute Position Embedding]**, [those] not well suited
   for **length generalization** in downstream tasks" — the formal statement
   of the slide's "Positions > N-1 can NOT be Embedded (Must Train Embedding
   on Max Expected Seq. Length)" limitation.

## What the sources CONFIRM (line by line)

- "[2] Position Embedding" as the trainable alternative to [1] Position
  Encoding — paper §3.5 "learned and fixed" + P2 sibling 021's verified
  record (dichotomy + BERT/GPT-1 exemplars).
- "Positional Embedding (Trained on Position Values)" / "Embedding Layer to
  Learn Position Vectors" — BERT's learned position embeddings (§3.2, summed
  with token embeddings); Gehring et al. 2017 (paper ref [9]).
- "Positions > N-1 can NOT be Embedded (Must Train Embedding on Max Expected
  Seq. Length)" — Kazemnejad 2023 (APE not suited to length generalization);
  paper's rationale for choosing sinusoidal instead ("extrapolate to
  sequence lengths longer than the ones encountered during training").
- "Vector Length = Word Embedding length" — BERT §3.2 (position embeddings
  summed with token embeddings into T_i ∈ R^H ⇒ same dimension); paper
  §3.5 d_model-equality sentence (banked on slide 032's record).
- The three-stage token-row → embedding-bar → vector-row diagram mirrors the
  course's own word-embedding pedagogy (P2 family style); no published
  figure is reproduced.

## Figures used by this slide

- **None.** Course-authored diagram (vision: original to this lecture; only
  "in spirit" similar to Alammar-style embedding-row illustrations). No
  download.

## Course-authored elements

- The "similar to word tokenization" aside, the "(Similar to Word Embedding)"
  subtitle, the N-2/N-1 box labels, the double space in "representing
  positions", the underlined "Train", the curly brace — keep verbatim for
  recreation; badge "34".

## [?] Uncertain items

- none open. (agy's first guess for the Kazemnejad-2023 arXiv ID —
  2305.19402 — resolved to an unrelated paper; verified live that the
  correct ID is 2305.19466; the wrong ID is recorded here so it is never
  reused.)

## Corrections

- none — vision transcript and script-12 raw agree; every claim matches the
  sources.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. Sources
confirm/correct DATA and record provenance; they never license inventing or
"improving" content the slide doesn't show.
