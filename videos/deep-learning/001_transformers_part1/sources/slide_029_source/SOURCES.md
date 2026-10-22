# SOURCES — slide 29 — "Self Attention Mechanism (as Query and {Key-Value} Dictionary)"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: 2026-10-11. The course notation quoted below is the
recreation target — kept VERBATIM. The paper is the semantic reference only.

## 1. Source URLs

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.2.1 opening paragraph (fetched
  2026-10-11).

## 2. Downloaded figures

- None. The slide re-annotates the slide-26 diagram with K/V badges and lookup
  captions — a course-original drawing; no source page hosts a matching figure.

## 3. Course notation → paper mapping

- "Query ALL Keys with X2" ≡ query q_2 = x_2 (raw embedding as query; the paper's
  queries come from W^Q — the course introduces projections on slide 37).
- "Matched KEYS with Relevance Percentage" ≡ softmaxed compatibility weights w_2j
  (non-negative, sum to 1 → "percentages").
- "Retrieve VALUES Weighted by their Relevance" ≡ output Σ_j w_2j v_j with v_j =
  x_j at this stage.
- K/V badges on the non-focus words, Q role on X2: same vector set split into a
  query role and key/value roles.

## 4. What the sources CONFIRM

- The Q/K/V dictionary re-annotation is the paper's own framing, §3.2.1 opening
  (near-verbatim): "An attention function can be described as mapping a query and a
  set of key-value pairs to an output, where the query, keys, values, and output
  are all vectors. The output is computed as a weighted sum of the values, where
  the weight assigned to each value is computed by a compatibility function of the
  query with the corresponding key."
- The three captions ("Query ALL Keys with X2" / "Matched KEYS with Relevance
  Percentage" / "Retrieve VALUES Weighted by their Relevance") each map to one
  clause of that passage — semantics confirmed.

## 5. Course vs paper discrepancies (NOT defects — recreation keeps course notation)

- Course still uses raw embeddings as Q/K/V at this stage (no learned projections);
  the paper's Q, K, V are linear projections of the layer input. Course sequencing
  (projections on slide 37), kept verbatim.
- Course labels the softmaxed weights "Relevance Percentage"; paper calls them "the
  weights on the values". Course label kept.

## 6. Numeric verification

- n/a (0/0).

## 7. Open questions

- none.

## Corrections

Cross-checked against script-12 raw transcription (correction worker W-F resumption,
2026-10-11): none — consistent.

- All course labels match the established notation verbatim: KEYs / Values / Dot
  Product / Soft max / Σ, W₂₁–W₂₄ (subscripted), K / Q / V badges, X₂ (subscripted),
  Y, badge "29".
- Q/K/V callouts are course-authored text confirmed against the paper's framing
  (internal consistency only, per §3/§4): "Query ALL Keys with X₂" / "Matched KEYS
  with Relevance Percentage" / "Retrieve VALUES Weighted by their Relevance" /
  "Values of Matched Keys are returned when Running Query" — all present verbatim
  in the raw.
- Subtitle "(Query using X₂ All Keys in Dictionary and retrieve Corresponding Values"
  transcribed verbatim (unclosed-paren pattern kept; it recurs unchanged on
  slide 30, consistent with 30←29).
- No attention formulas printed (only symbolic labels) — nothing to check against
  the course formula set. Arrow weights encode relevance with no printed numbers —
  n/a (0/0). No [?] items in the raw. No patches.
