# slide_047 — AVERAGE POOLING Layer (Take Average Value) — SOURCES

Slide content (from `analysis/slide_047_raw.json`): average pooling as a new module;
sliding window [h_f, w_f]; keep the average at each location; activation
`a_{r,c} = (1/(r·c)) Σ_{i,j∈Ω(r,c)} x_{ij}`; gradient `∂a_{r,c}/∂x_{ij} = 1/(r·c)`;
worked example 4×4 → 2×2 (outputs 5, 8, 4, 5) with a red 1/2 fraction.

## Sources consulted (web-verified 2026-10-12)

1. **d2l.ai — Dive into Deep Learning, §7.5 Pooling**
   URL: https://d2l.ai/chapter_convolutional-neural-networks/pooling.html
   Confirmed:
   - "pooling operators are deterministic, typically calculating either the maximum
     or the average value of the elements in the pooling window" — max/average
     pooling naming as on the slide.
   - "Average pooling is essentially as old as CNNs. The idea is akin to downsampling
     an image." — supports the slide's framing of average pooling as a classic module.
   - "the pooling layer contains no parameters (there is no kernel)" — consistent with
     the slide presenting pooling as a module defined only by input/output/gradient.
   - Worked numeric example on the page: same 3×3 input, max → [[4,5],[7,8]],
     average pooling → [[2,3],[5,6]] (i.e. true 2×2 average = sum/4).
2. **CS231n — Convolutional Networks (Stanford), "Pooling Layer" section**
   URL: https://cs231n.github.io/convolutional-networks/
   (WebFetch timed out twice; retrieved via curl.)
   Confirmed:
   - Pooling layer geometry `W2 = (W1 − F)/S + 1`, "Introduces zero parameters since
     it computes a fixed function of the input".
   - "In addition to max pooling, the pooling units can also perform other functions,
     such as average pooling... Average pooling was often used historically but has
     recently fallen out of favor compared to the max pooling operation."
   - 2×2 filter / stride 2 downsampling ("discarding 75% of the activations") matches
     the slide's 4×4 → 2×2 example geometry.
   - Backprop through max pooling routes gradient to the max input ("switches");
     CS231n does not state the average-pooling gradient explicitly on this page.
3. **Web search (agy) — average pooling forward/backward formulas**
   Confirmed standard result: forward `output = (1/n) Σ x_i` over the n window
   elements; backward `∂output/∂x_i = 1/n` — the upstream gradient is distributed
   uniformly with weight 1/n (n = window area). With n = h_f·w_f = r·c (window rows ×
   window cols), this is exactly the slide's `∂a_{r,c}/∂x_{ij} = 1/(r·c)`.

## Downloaded figures

- `pooling.svg` — d2l.ai Fig. 7.5.1, caption: "Max-pooling with a pooling window
  shape of 2×2. The shaded portions are the first output element as well as the
  input tensor elements used for the output computation: max(0, 1, 3, 4)=4."
  Kept as the site's own illustration of the 2×2 sliding-window mechanics the slide's
  example uses. NOTE: it depicts MAX pooling (d2l has no average-pooling figure);
  do not use it as ground truth for the slide's average example.

## Confirmations vs the slide

- Average pooling = deterministic mean over the sliding window: CONFIRMED (d2l 7.5).
- Pooling module has no learnable parameters; defining input/output/gradient is the
  standard way to spec it: CONFIRMED (d2l, CS231n).
- Backward pass of average pooling: every input in the window receives
  `1/(window area)` of the upstream gradient — matches the slide's
  `∂a_{r,c}/∂x_{ij} = 1/(r·c)` when r·c is read as the window area: CONFIRMED.
- 4×4 → 2×2 non-overlapping pooling with stride 2: CONFIRMED geometry (CS231n).

## Corrections / discrepancies (frame wins recreation, source wins understanding)

- **Worked-example arithmetic [?]:** the slide's own formula
  `a_{r,c} = (1/(r·c)) Σ x_{ij}` with a 2×2 window implies divisor 4. The slide's
  example outputs 5, 8, 4, 5 = quadrant sums (10, 16, 8, 10) × **1/2** (the red
  fraction). True 2×2 averages are 2.5, 4, 2, 2.5. d2l's own worked example confirms
  average-over-2×2 = sum/4. So the slide's example computes sum × 1/2, inconsistent
  with its stated formula — recreate the example VERBATIM (5, 8, 4, 5 with 1/2), but
  understanding-wise this is an error/simplification in the original lecture slide.
- **Notation [?]:** in `a_{r,c}`, (r,c) are the output position indices (per the
  slide's Where-legend: r=Row, c=Column), so writing the divisor as "r·c" is sloppy —
  the constant is the window area h_f·w_f (=4 here), as the same symbol is reused in
  the gradient. Recreation keeps the slide's notation verbatim.

## Open questions

- [?] Whether the lecturer intends "1/2" as a deliberate variant (e.g. pooling 1×2
  sub-windows) or an arithmetic slip — cannot be resolved from the frame; the
  standard definition (divide by window area) is unambiguous in all sources.
- The slide cites no external source; style matches a hand-built lecture deck
  (same family as the neighboring pooling slides). No original-paper figure to trace
  (LeNet-era average pooling per d2l "essentially as old as CNNs").
