# Slide 036 — "How many Parameters are in the RGB Image filter (K=3)" — SOURCES

## Slide content (from analysis/slide_036_raw.json)
Two-line dark-red title "How many Parameters are  in the  RGB / Image
filter  ( K=3 )". Hand-drawn diagram: orange RGB slab ("3 dims", 7x7 edge
labels, cyan-outlined column on its face) x (blue X, dashed cyan lines)
small cyan filter slab ("3" below, "7" right) = "=" + "+" + neuron icon.
Question: "How many weights for this neuron?" Answer in red: "7 · 7 · 3 =
147". Founder frame swap recorded (new 36 <- old 48; kept frame_02344).
NOTE: slide 37 builds on this slide (dep graph 37<-36).

## Primary source: CS231n — Convolutional Neural Networks (Stanford)
URL: https://cs231n.github.io/convolutional-networks/ (fetched 2026-10-12)

Confirmed — exact quotes:
- Per-neuron parameter counting (page's real-world AlexNet example): "there
  are 55*55*96 = 290,400 neurons in the first Conv Layer, and each has
  11*11*3 = 363 weights and 1 bias."
  -> the slide does the same counting with F=7, D1=3: 7*7*3 = 147 weights
  per neuron (weights only; the page counts the bias separately, which
  matches the small gray "+" drawn beside the "=" on the slide).
- "Each neuron in the convolutional layer is connected only to a local
  region in the input volume spatially, but to the full depth (i.e. all
  color channels)." -> the single neuron = one 7x7 patch x all 3 RGB
  channels; "(K=3)" in the title = input depth/channels.
- Page also defines "depth column (or fibre)" for neurons sharing a
  receptive field (see slide 037 SOURCES for continuation).

## Secondary source: d2l.ai ch. 7.4 "Channels" (fetched 2026-10-12)
URL: https://d2l.ai/chapter_convolutional-neural-networks/channels.html
- "When the input data contains multiple channels, we need to construct a
  convolution kernel with the same number of input channels as the input
  data" — kernel spans all 3 RGB channels, shape 3 x k_h x k_w.

## Search confirmation (agy, 2026-10-12)
Per-filter weights 7×7×3 = 147 (weights) + 1 bias = 148 parameters —
standard count; the slide's "147" counts weights only, consistent with the
CS231n arithmetic and its separate bias.

## Downloaded figures (original filenames)
- depthcol.jpeg (464x326) — CS231n figure: input volume (32x32x3) + first
  CONV layer; caption: each neuron connected to a local 2D region but FULL
  input depth — canonical equivalent of the slide's single-neuron diagram.

## Confirmations vs corrections
- Arithmetic 7·7·3 = 147 correct (weights per neuron/filter, no bias).
- The "+" between "=" and the neuron icon plausibly denotes the bias term
  (+1) — [?] interpretation; if so the CS231n "363 weights and 1 bias"
  pattern is the exact parallel. Original frame is ground truth.
- No disagreements with sources.

## Open questions
- [?] Whether "+" is bias annotation or a stray mark — decide from the
  original frame during recreation; do not remove it without evidence.
