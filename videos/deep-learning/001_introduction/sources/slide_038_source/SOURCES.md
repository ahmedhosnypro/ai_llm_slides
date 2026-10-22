# Slide 038 — "Filters parameters" — SOURCES

## Slide content (from analysis/slide_038_raw.json)
Title "Filters parameters". Formula box (color-coded):
"Number of parameters for different filters applied to same location in the
image  = Filter size (2-D) * Number of channels (K) * number of different
filters  = 7*7 * 3 * 5 =735".
Hand-drawn diagram: brown 3D slab (RGB patch, "3 dims", edges 7 and 7) x
five colored 3D filter slabs (cyan/green/red/yellow/purple, each 7x7x3) =
five colored circles (outputs); handwritten "735 weights" fanned up to the
five slabs.

## Primary source A: CS231n — Convolutional Neural Networks (Stanford)
URL: https://cs231n.github.io/convolutional-networks/ (fetched 2026-10-12)

Confirmed — exact quote from the page's summary section:
- "With parameter sharing, it introduces F·F·D1 weights per filter, for a
  total of (F·F·D1)·K weights and K biases."
Slide's arithmetic: F=7, D1=3 channels, K=5 filters -> 7*7*3*5 = 735
weights (weights only; CS231n likewise counts biases separately — slide
counts WEIGHTS, no +5 for biases).
Also confirmed earlier on the page: "the connectivity along the depth axis
must be 3, since this is the depth of the input volume" (filters span the
full input depth — the slide's 3-dims slab).

## Primary source B: d2l.ai ch. 7.4 "Channels" (Multiple Input Channels)
URL: https://d2l.ai/chapter_convolutional-neural-networks/channels.html

Confirmed:
- "When the input data contains multiple channels, we need to construct a
  convolution kernel with the same number of input channels as the input
  data" — kernel shape c_i × k_h × k_w.
- Output = per-channel cross-correlations added (sum over the c_i results).
- 1x1 conv "requires c_o × c_i weights (plus the bias)" — same
  channels-in/channels-out parameter logic.

## Search confirmation (agy, 2026-10-12)
Standard formula confirmed: weights-only = K · F · F · D1 (735 here);
per-filter weights 7×7×3 = 147; with bias +1 per filter (148) — the slide
deliberately counts weights only ("735 weights").

## Downloaded figures (original filenames)
- conv-multi-in.svg — d2l Fig. 7.4.1 (fig-conv-multi-in): 2-channel input,
  one k_h×k_w kernel per input channel, per-channel results summed —
  the vector equivalent of the slide's RGB-slab x filter-stack diagram.

## Confirmations vs corrections
- Formula and arithmetic match CS231n's (F·F·D1)·K exactly; 7*7*3*5=735 is
  arithmetically correct (weights only, no biases).
- Diagram is the course's own hand-drawn visualization; colors/order
  (cyan, green, red, yellow, purple) come from the original frame.
- No disagreement found.

## Open questions
- [?] The slide's K is overloaded: "Number of channels (K)" in the formula
  line vs "number of different filters" as the third factor (CS231n uses D1
  for input depth and K for #filters). Recreate verbatim; do not "fix".
