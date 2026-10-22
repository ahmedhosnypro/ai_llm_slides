# slide_046 — POOLING — SOURCES

Slide content (from `analysis/slide_046_raw.json`): pooling concept — "Aggregate
multiple values into a single value"; "Invariance to small transformations";
"Reduces the size of the layer output/input to next layer → Faster computations";
"Keeps most important information for the next layer"; two option boxes "Max pooling"
/ "Average pooling"; bottom diagram: 2×2 green matrix [a b; c d] → block arrow →
green cell z; `Pool( <tiger photo> ) == <smaller tiger photo>`, caption
"Size is reduced".

## Sources consulted (web-verified 2026-10-12)

1. **Goodfellow, Bengio, Courville — Deep Learning, §9.3 "Pooling"**
   URL: https://www.deeplearningbook.org/contents/convnets.html
   (fetched full chapter text; the site serves one big HTML with letter-spacing
   artifacts in extraction)
   Confirmed (near-verbatim matches to the slide's bullets):
   - "A pooling function replaces the output of the net at a certain location with a
     summary statistic of the nearby outputs." ← slide: "Aggregate multiple values
     into a single value".
   - "Other popular pooling functions include the average of a rectangular
     neighborhood..." (max pooling cited to Zhou and Chellappa, 1988) ← slide's
     "Max pooling" / "Average pooling" option boxes.
   - "In all cases, pooling helps to make the representation become approximately
     invariant to small translations of the input. Invariance to translation means
     that if we translate the input by a small amount, the values of most of the
     pooled outputs do not change." ← slide: "Invariance to small transformations".
   - "Invariance to local translation can be a useful property if we care more about
     whether some feature is present than exactly where it is." ← slide: "Keeps most
     important information for the next layer" (max-pooling semantics).
2. **CS231n — Convolutional Networks (Stanford), "Pooling Layer" section**
   URL: https://cs231n.github.io/convolutional-networks/
   Confirmed: "Its function is to progressively reduce the spatial size of the
   representation to reduce the amount of parameters and computation in the network,
   and hence to also control overfitting." ← slide: "Reduces the size of the layer
   output/input to next layer → Faster computations". Also the depth-preserving
   downsampling figure (`pool.jpeg`).
3. **Web search (agy)** — pooling = local aggregation giving approximate translation
   invariance + downsampling for cheaper computation; no single canonical origin for
   a tiger-photo pooling illustration was identified (search returned only generic
   lecture usage, no primary deck). Recorded as unresolved, see [?] below.

## Downloaded figures

- `pool.jpeg` — CS231n figure beside "General pooling": input volume [224x224x64]
  pooled with filter size 2, stride 2 → output [112x112x64], "Notice that the volume
  depth is preserved." — the site's own illustration of spatial size reduction
  (matches the slide's "Size is reduced" message).
- `maxpool.jpeg` — CS231n max-pooling figure (each max taken over a 2×2 square,
  stride 2) — relevant to the slide's "Max pooling" option.

## Confirmations vs the slide

- Pooling = aggregating a neighborhood into one summary value: CONFIRMED (Goodfellow
  9.3 first sentence).
- Invariance to small transformations: CONFIRMED (Goodfellow 9.3, near-verbatim).
- Size reduction → faster computation: CONFIRMED (CS231n).
- Max pooling and average pooling as the two standard choices: CONFIRMED
  (Goodfellow 9.3, CS231n, d2l 7.5).
- 2×2 → single value (a,b,c,d → z) diagram: CONFIRMED as the canonical 2×2 stride-2
  pooling geometry (CS231n/d2l examples).

## Corrections / discrepancies

- None on the bullets — the slide's four claims match the standard textbook treatment
  almost word for word.

## Open questions

- [?] Provenance of the tiger photo "Pool(image) == smaller image" device: not found
  in Goodfellow ch. 9, CS231n, or d2l. It reads as the lecturer's own illustrative
  metaphor (a photo pooled → same photo smaller). The tiger image itself (leaping
  over water) has no identified primary source — treat as lecturer-supplied artwork;
  recreation must source/replace a similar leaping-tiger photo, original frame is
  ground truth for layout.
- [?] Exact divisor/operator for "z" is deliberately unspecified on this slide
  (generic "Pool" function) — consistent with sources (pool function family: max,
  average, L2, weighted average per Goodfellow 9.3).
