# SOURCES.md — slide 026 ("Update the weights by moving in the negative direction of the Gradient of the Loss function with respect to model weights")

Research date: 2026-10-12. Worker: web-research lane, slides 021–030 (reverse run).

## IDENTIFICATION PATH (IMPORTANT — this slide has NO raw JSON yet)

`analysis/slide_026_raw.json` does NOT exist (script 12 has not run for this slide).
Content was identified from the review-packet contact sheet fallback:
- `unique_slides/new2old_mapping.json`: new **26** ← old_group **31** (no founder swap),
  kept frame `frame_01332.jpg` (≈1332–1361 s), image `unique_slides/slide_026.jpg`.
- Visual read from `review_packet/contact_sheet_page2.jpg` (pre-curation old numbering),
  old slide 31, zoom-cropped for legibility. The original frame is ground truth; the
  readings below must be re-verified by script 12 when it runs [?].

## Slide content (as read from the frame)

Title (two lines, red then blue): "Update the weights by moving in the negative
direction of the **Gradient of the Loss function with respect to model weights**".
A blue-framed derivation panel with beige sub-panels, live-lecture style:

1. `Net_j = Σ_i (w_ji O_i)`  ⇒  `∂Net_j/∂w_ji = O_i`
2. `O_j = f(Net_j) = 1/(1+e^(−Net_j))`  (For **Sigmoid Function**)
3. `E = ½ Σ_j (t_j − O_j)²`  (**Error at Output layer ONLY**)
4. `Δw_ji = −η ∂E/∂w_ji = −η (∂E/∂Net_j)(∂Net_j/∂w_ji)`  (chain rule)
5. `Δw_ji = −η (∂E/∂Net_j) O_i`  — `Let  δ_j = − ∂E/∂Net_j`
6. `Δw_ji = η δ_j O_i`  — `then  w_ji^new = w_ji^old + Δw_ji`

(Subscript i/j readings are small at contact-sheet resolution [?] — re-verify against
`unique_slides/slide_026.jpg`; the consistent pattern is: output unit j receives inputs
O_i over weights w_ji.)

## Slide nature

The gradient-descent weight-update rule for one sigmoid output unit with SSE loss —
i.e. the **generalized delta rule** (the output-layer case of backpropagation), stated
in negative-gradient form and closed with `w_new = w_old + Δw`.

## Source URLs

1. **Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986), "Learning representations
   by back-propagating errors", Nature 323, 533–536** — the primary source of the delta
   rule.
   - PDF (Hinton's own Toronto mirror): https://www.cs.toronto.edu/~hinton/absps/naturebp.pdf
     (FETCHED and CONFIRMED 2026-10-12: 4-page Nature letter, "© 1986 Nature Publishing
     Group"; the PDF is a scan — text layer carries only the copyright line, so the
     equations are verified via the search synthesis below, not grep).
   - Delta rule as confirmed by web search (agy, 2026-10-12): `Δw_ij = η δ_j o_i` with
     error signal `δ_j = (t_j − o_j) f'(net_j)` for output units and
     `net_j = Σ_i w_ij o_i` — **algebraically identical to the slide's** rule:
     the slide's `δ_j = −∂E/∂Net_j` equals `(t_j − O_j) f'(Net_j)` exactly when
     E = ½Σ(t_j−O_j)² and O_j = sigmoid(Net_j), since ∂E/∂Net_j = (O_j−t_j)·O_j(1−O_j).
     The slide additionally SPELLS OUT the chain rule and the negative-gradient form
     (`Δw = −η ∂E/∂w`), which RHW86 derives but presents in the δ-form.

2. **d2l.ai — §12.3 "Gradient Descent"**
   - URL: https://d2l.ai/chapter_optimization/gd.html
   - Status: FETCHED and CONFIRMED (2026-10-12, 189 KB HTML).
   - Confirms the title's claim verbatim as the standard principle: "moving in the
     direction of the **negative gradient** will decrease f ... we pick a fixed step
     size η > 0 and choose ε = −η f'(x)" with the update `x ← x − η∇f(x)` — i.e.
     `w_new = w_old + Δw` with `Δw = −η ∂E/∂w` is exactly textbook gradient descent
     (η = learning rate).

3. **Nielsen — *Neural Networks and Deep Learning*, ch. 2 "How the backpropagation
   algorithm works"** (http://neuralnetworksanddeeplearning.com/chap2.html) — the
   standard modern book treatment of the same four equations (BP1–BP4: the SSE cost,
   sigmoid, output-layer error δ = (a−y)⊙σ'(z), and the gradient ∂C/∂w = a_in·δ_out).
   Not fetched from this network [? — corroborative; d2l + RHW86 carried the
   confirmations].

## Downloaded files

Downloaded into `slide_026_source/` (original filename preserved):

1. `naturebp.pdf` (485,917 bytes, 4-page PDF 1.3, scan)
   - https://www.cs.toronto.edu/~hinton/absps/naturebp.pdf
   - Rumelhart, Hinton & Williams (1986), "Learning representations by back-propagating
     errors", Nature 323:533–536 — the primary source of the delta rule the slide
     derives. Scanned original; text layer minimal (copyright only).

Process note: a first fetch attempt pulled
`www.cs.toronto.edu/~osindero/PUBLICATIONS/ncfast.pdf` on the strength of a UvA-2016
course-page citation adjacency — it turned out to be a DIFFERENT paper (Hinton, Osindero
& Teh 2006, "A Fast Learning Algorithm for Deep Belief Nets"), i.e. not relevant to this
slide; it was removed immediately and is NOT part of this slide's evidence.

## Confirmed / corrected vs the slide

- The negative-gradient update (`Δw = −η ∂E/∂w`, `w_new = w_old + Δw`) CONFIRMED as
  textbook gradient descent (d2l §12.3) — the slide title's "moving in the negative
  direction of the Gradient of the Loss function with respect to model weights" is the
  standard principle, verbatim in spirit.
- The delta rule `Δw_ji = η δ_j O_i` with sigmoid + SSE CONFIRMED against RHW 1986's
  generalized delta rule; the slide's δ definition (−∂E/∂Net_j) and RHW86's
  ((t−o)·f′(net)) are the same quantity for this loss/activation.
- "Error at Output layer ONLY" annotation CONFIRMED as correct scoping: the
  ½Σ(t_j−O_j)² + δ_j = −∂E/∂Net_j derivation as written applies to output units (hidden
  units need δ propagated backward via the next layer — RHW86's chain, and the reason
  later slides re-derive δ layer-wise).
- Nothing to correct in the mathematics as read from the frame.
- Provenance [?]: this slide family (old 21–31: "Complete Deep Learning Model",
  "Compare to ML training", "Visualization of Single Perceptron", "Neural Network
  Model", this update rule) was NOT found verbatim in the UvA Gavves decks checked
  (nov2019 lecture4 CNN, nov2016 lecture2/lecture3) — UvA 2016 lecture2 "Learning with
  Neural Networks" covers the same topics (backpropagation, gradient descent, sigmoid
  modules) but with different phrasing. Exact upstream deck unresolved; does not affect
  recreation (frame is ground truth).

## Open questions

- [?] Exact subscript indices (i vs j) and one ambiguous glyph in `Net_j = Σ_i (w_ji O_i)`
  — re-verify against `unique_slides/slide_026.jpg` during script 12 analysis (this
  slide's raw JSON is MISSING and analysis still needs to run; the SOURCES.md covers the
  research obligation, not the vision analysis).
- [?] Whether the lecture annotates further (the kept frame is one annotation state of a
  live-stylus slide; earlier states exist in the old group's frames).
