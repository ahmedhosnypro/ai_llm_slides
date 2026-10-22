# SOURCES.md — slide 042 "Multi-Head Self Attention"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
Peter Bloem's transformers post (current page + 2021 Wayback capture) and arXiv
HTML v7. No vision calls run; no image access — frame facts below come from the
script-12 raw transcription, which is the record of the frame.

## Slide identity

- New (curated) slide **042** ← old extraction slide **101**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_042.jpg`,
  badge "42".
- Frame facts (raw transcription): red centered title "Multi-Head Self
  Attention"; two-line red bold subtitle "Combining several self attention
  mechanisms  give the self attention greater power of discrimination"
  (double space preserved); dark-red-bordered box with four blue statements:
  1. "Each Head is indexed with "r""
  2. "Each head has its own matrices Wq^r , Wk^r ,Wv^r ." (bold W, red
     superscript r, green subscripts q/k/v)
  3. "For input X each attention head produces a different output vector Y^r."
  4. "All Output vectors are concatenated , and pass through a linear
     transformation to reduce the dimension back to original X dimension."
  Mouse-cursor artifact over line 1 (recording overlay — exclude).
- Position in the course: the DEFINITION slide of the multi-head section (40 =
  Wide/Narrow divider; 43 = Wide/Narrow comparison, 44/45 = Wide/Narrow of
  word X₂). This slide states the general multi-head construction before the
  two variants are built.

## Primary sources

- **Course notation source — the slide's notation is BLOEM'S, verbatim**:
  Peter Bloem, "Transformers from scratch" — https://peterbloem.nl/blog/transformers
  (verified live 2026-10-11; notation re-confirmed in the 2021 Wayback capture
  https://web.archive.org/web/2021/https://peterbloem.nl/blog/transformers):
  - Head index **r** with per-head matrices written **W_q^r, W_k^r, W_v^r** —
    "each with different matrices W_q^r, W_k^r, W_v^r. These are called
    attention heads." The slide's "Each Head is indexed with "r"" and
    "Wq^r , Wk^r ,Wv^r" match this exactly (course capitalizes W's subscript;
    Bloem writes lowercase).
  - Multi-head output: "We concatenate these, and pass them through a linear
    transformation to **reduce the dimension back to k**." — the slide's
    bullet 4 is a near-verbatim paraphrase of this sentence ("back to original
    X dimension").
- **Paper**: https://arxiv.org/html/1706.03762v7 — "Attention Is All You Need"
  (Vaswani et al., 2017) (verified live 2026-10-11), §3.2.2 — the math behind
  every bullet:
  - MultiHead(Q, K, V) = Concat(head₁, …, head_h)·Wᴼ, with
    head_i = Attention(QW_i^Q, KW_i^K, VW_i^V);
  - W_i^Q, W_i^K ∈ ℝ^(d_model×d_k); W_i^V ∈ ℝ^(d_model×d_v);
    Wᴼ ∈ ℝ^(h·d_v × d_model); h = 8, d_k = d_v = d_model/h = 64;
  - motivation: "Multi-head attention allows the model to jointly attend to
    information from different representation subspaces at different
    positions. With a single attention head, averaging inhibits this."
  - cost note: "Due to the reduced dimension of each head, the total
    computational cost is similar to that of single-head attention with full
    dimensionality."

## Figures used by this slide

**None** — text slide. Download decision: nothing downloaded into this dir.

## What the sources CONFIRM (data behind the slide)

- **Per-head private matrices, indexed r** — Bloem verbatim (above); the
  paper is the same construction with subscript head index i and capital
  superscripts (W_i^Q). Notation provenance: the course takes Bloem's r.
- **A different output vector per head** — paper: each head_i is a full
  Attention output (one per head, from different representation subspaces);
  Bloem: each head has its own matrices and produces its own output. The
  slide's Y^r bullet matches.
- **Concat + linear "back to original X dimension"** — Bloem's sentence
  verbatim; paper's Wᴼ ∈ ℝ^(h·d_v × d_model) is precisely the linear map from
  the concatenated (h·d_v)-dim vector back to d_model = the input dimension.
- **"Greater power of discrimination" (subtitle)** — course phrasing of the
  paper's multi-head motivation quote above (different representation
  subspaces; single-head averaging inhibits).
- **Connection to the Wide/Narrow fork**: the "reduce the dimension back"
  construction (heads of reduced dim d/h) is the paper's (narrow-style)
  config — the cost note confirms it; the course presents the Wide variant
  (full-dim heads) first at 43/44, then Narrow. This slide's general
  statement is dimension-agnostic and consistent with both.
- **Numeric verification**: the slide transcribes no numeric values; the
  paper's h=8 / d_model=512 / d_k=d_v=64 config is the only numeric anchor
  and is quoted from the verified §3.2.2 text (not recomputed — nothing to
  recompute).

## Course-authored elements (no source counterpart — do not "fix" to a source)

- The subtitle wording, all four bullet wordings (Bloem's sentence is
  paraphrased, not quoted on the frame), the color coding (red math symbols,
  green subscripts, blue body text), the bordered box, the gray background
  chrome, the quoted-r typography, and the spacing quirks ("concatenated ,",
  "Wk^r ,Wv^r ." without space after comma) — all instructor's own; preserve
  verbatim.

## [?] Uncertain items

- [?] None at the data level. Minor typographic re-check at build: whether the
  frame's line 2 prints "Wq^r , Wk^r ,Wv^r ." with exactly the transcribed
  spacing (raw itself preserves it; no patch).
- [?] Notation cross-reference (not an error): the paper indexes heads by
  subscript i, the course/Bloem by superscript r. If a future judge flags
  "r vs i", the answer is provenance, not a fix.

## Corrections

- **Cross-check 2026-10-11 (W-G, post-banking):** none — consistent. No
  patches to `analysis/slide_042_raw.json`: sources confirm every bullet; the
  only [?]s are a build-time spacing re-check and a notation-provenance note,
  neither answerable from the raw record. Frame facts in this file re-verified
  against the raw verbatim (all four bullets, subtitle double space, red/green
  math coloring, cursor artifact). Slide identity confirmed: 042 ← old 101
  (`unique_slides/new2old_mapping.json`; note 041's SOURCES.md previously
  misrecorded 101 for itself — corrected there to 84).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). The sources confirm/correct DATA and record
provenance; they never license inventing or "improving" content the slide
doesn't show. If source and slide disagree, record the discrepancy — the slide
wins for recreation, the source wins for understanding.
