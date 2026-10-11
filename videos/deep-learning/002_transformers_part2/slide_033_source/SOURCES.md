# SOURCES.md — slide 033 "Sin/Cos Positional Encoder" (d-dim generalization: K=d/2 sin/cos pairs)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_033_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner) cross-checked against `analysis/slide_033_raw.json` (raw
agrees on every definition-panel line). Web evidence from the already-live
banked sources (paper §3.5 in `scratch/webverify/paper_v7.html`; Kazemnejad
page on slide 027's run, `scratch/webverify/kazemnejad_pe.html`). No new agy
query spent — the slide's formula content is fully covered by the two
live-verified sources, quoted verbatim below.

## Slide identity

- New (curated) slide **033** ← old extraction **68** (224 frames = heavily
  taught) — `unique_slides/new2old_mapping.json`, frame
  `unique_slides/slide_033.jpg`.
- Frame facts (vision transcript): title "Sin/Cos Positional Encoder" (red);
  subtitle "Positional Vector with Same dimension as Embedding dimension"
  (blue); badge "33". Left: the generic pair box [sin(ωt); cos(ωt)] + green
  box "Sin/Cos pairs / Vector Represents / Position "t" / Any "ω" is
  accepted". Column expansion: pair index column ("Vector Pairs "K""):
  0,1,2,K,[d/2]-1; element index column ("Index "i""):
  0,1,2,3,4,5,2k,2k+1,…,d-1-1 [?],d-1; right column of 5 pairs
  sin(ω_0 t)/cos(ω_0 t) … sin(ω_{d/2} t)/cos(ω_{d/2} t) with tall red bracket
  labeled "dx1". Yellow definition panel: "Word Embedding Dimension "d" [Even
  Num] / Position Encoding Dimension "d" / Number of Vector Pairs "K"=d/2
  [0, 1, 2,... d/2-1] / Elements Index "i" [0, 1, 2, ... d-1] / Even Index
  "i" is Sine Term , i=2*k / Odd Index "i" is Cosine Term, i=2*k+1".
  Yellow "Example:" panel: "d=100 / K=[0 ..49] / i=[0 .. 99] / Sin
  [0,2,4,...] / Cos [1,3,5,...]". Blue rules panel: "Use different "ω" values
  for different "Pairs" / Select "ω" Value Based on "Pair" index "k" /
  Largest "ω" value = 1 (Used in First Pair) / Smallest "ω" value ≈ 1/10000
  (Used in Last Pair) / Note: / "ω" Value depends on Embedding Dimension "d"
  ONLY / "ω" Value does NOT depend on Sequence Length", with the boxed
  equation ω_K = 1/10,000^(2k/d).
  - Artifacts: mouse cursor near the sin(ω_K t) box; bottom letterbox bars.

## Primary sources

1. **arXiv 1706.03762v7 §3.5** (live curl 2026-10-11,
   `scratch/webverify/paper_v7.html`) — verbatim:
   - "we use sine and cosine functions of different frequencies:
     PE_(pos,2i)=sin(pos/10000^(2i/d_model)), PE_(pos,2i+1)=cos(...)", "where
     pos is the position and i is the dimension. That is, each dimension of
     the positional encoding corresponds to a sinusoid. The wavelengths form
     a geometric progression from 2π to 10000·2π."
   - "The positional encodings have the same dimension d_model as the
     embeddings, so that the two can be summed." — the slide subtitle's
     "Same dimension as Embedding dimension" claim.
2. **Kazemnejad, "Positional Encoding in Transformers"** —
   https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
   (live curl 2026-10-11, banked HTML) — verbatim:
   - p_t^(i) = sin(ω_k t) if i=2k, cos(ω_k t) if i=2k+1, "where
     ω_k = 1/10000^(2k/d)" — exactly the slide's boxed equation ω_K =
     1/10,000^(2k/d) (subscript style aside).
   - "the frequencies are decreasing along the vector dimension. Thus it
     forms a geometric progression from 2π to 10000·2π on the wavelengths" —
     the slide's largest-ω=1 / smallest-ω≈1/10000 rules.
   - "You can also imagine the positional embedding p_t as a vector
     containing pairs of sines and cosines for each frequency (Note that d is
     divisble by 2)" — the slide's K=d/2 pair structure and "[Even Num]"
     caveat.

## What the sources CONFIRM (claim by claim)

- Positional vector has the SAME dimension as the embedding — paper §3.5
  d_model-equality sentence (verbatim match to the subtitle).
- K = d/2 sin/cos pairs; even index (i=2k) = sine, odd index (i=2k+1) =
  cosine — Kazemnejad's case definition, verbatim; paper's PE_(pos,2i)/PE_(pos,2i+1).
- ω_k = 1/10000^(2k/d); largest ω = 1 (k=0, first pair); smallest ≈ 1/10000
  (k=d/2−1, last pair; exponent 2(d/2−1)/d → 1) — Kazemnejad formula +
  geometric-progression sentence; paper wavelengths 2π→10000·2π.
- "ω Value depends on Embedding Dimension "d" ONLY / does NOT depend on
  Sequence Length" — the formula has no length term (only k and d); paper
  and Kazemnejad both define ω purely from the dimension index.
- Example d=100 → K=50 pairs, i=0..99, sin at even i, cos at odd i —
  arithmetically consistent (course-chosen small d; paper uses d_model=512).

## Figures used by this slide

- **None.** Course-authored column-expansion schematic; no published figure
  reproduced (vision transcript: no match to Vaswani Fig 1/2, Bloem, Alammar
  heatmap).

## Course-authored elements

- The three-column expansion layout with color-paired boxes, the "Any "ω" is
  accepted" note, the d=100 example panel, the dx1 bracket, the yellow
  highlight emphases — keep verbatim for recreation; badge "33". The boxed
  equation's LHS subscript renders as a capital-K glyph ("ω_K") while the
  right side uses lowercase k — course quirk, keep as printed (frame wins).

## [?] Uncertain items

- [?] the index column's second-to-last label — vision read "d-1-1" (could
  be the literal frame text or a misread of "d−2", the last even index).
  Build-time zoom decides; "d-1" (last, odd → cosine) is consistent either
  way.
- [?] the green/orange fill alternation between pairs 1 and 2 (vision notes
  it appears decorative rather than even/odd-strict) — recreation follows the
  frame pixel colors, semantics irrelevant.

## Corrections

- none — the vision transcript and the script-12 raw agree; all formula
  lines match the paper/Kazemnejad math.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. Sources
confirm/correct DATA and record provenance; they never license inventing or
"improving" content the slide doesn't show.
