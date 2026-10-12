# Slide 033 — "Where to Get Filters for Recognition" — SOURCES

## Slide content (from analysis/slide_033_raw.json)
Title "Where to Get Filters for Recognition". Text panel: "Similarly, if
images are k-D, parameters should also be k-D" / "For K=3 (RGB), use K-D
filter (third dim >> K=3)" / "For K=9 (Satellite images) use 9-D filter
(3rd dim = 9)" / "...etc". Diagram: Grayscale = flat plane + flat blue
square filter; RGB = 3-D slab ("3 dims") + 3-D blue filter; Multiple
channels = k-D slab ("k dims") + 3-D blue cube filter; red "Filters"
callout pointing at all three blue filters.

## Primary source A: CS231n — Convolutional Neural Networks (Stanford)
URL: https://cs231n.github.io/convolutional-networks/ (fetched 2026-10-12)

Confirmed — exact quotes:
- "The extent of the connectivity along the depth axis must be 3, since
  this is the depth of the input volume" (Example 1, RGB input) — the
  filter's third dimension is SET BY the input depth.
- Example 2: input [16x16x20], receptive field 3x3 -> every neuron has
  3*3*20 = 180 connections — "local in 2D space, but full along the input
  depth (20)". Generalizes the slide's rule to any K (e.g. K=9): filter
  depth = input depth.
- Note the slide's "K=3"/"K=9" uses K for CHANNELS (CS231n uses K for
  #filters, D1 for input depth) — recreate verbatim, do not "fix".

## Primary source B: d2l.ai ch. 7.4 "Channels" (fetched 2026-10-12)
URL: https://d2l.ai/chapter_convolutional-neural-networks/channels.html
- "When the input data contains multiple channels, we need to construct a
  convolution kernel with the same number of input channels as the input
  data" — kernel shape c_i x k_h x k_w. Exactly the slide's
  images-are-k-D -> parameters-are-k-D rule.

## Search confirmation (agy, 2026-10-12)
"convolution kernel depth = number of input channels, whether those
channels are the three RGB bands or the many bands of a hyperspectral
image" — RGB: kernel k x k x 3; satellite/hyperspectral with B bands:
kernel k x k x B. Supports the slide's K=3 -> 3-D and K=9 -> 9-D pattern.

## Downloaded figures (original filenames)
- conv-multi-in.svg — d2l Fig. 7.4.1 (fig-conv-multi-in): two-channel
  input, one k_h x k_w kernel per channel, per-channel results summed —
  canonical multi-channel filter illustration matching the slide's
  "Multiple channels" slab + cube filter.

## Confirmations vs corrections
- Core rule (filter depth = input channel count) is standard, confirmed by
  CS231n + d2l + agy. Grayscale: a 2-D (single-channel) image takes a 2-D
  filter — consistent (input depth 1 -> kernel depth 1).
- [?] "K=9 (Satellite images)": the specific 9-band count is
  course-specific (real constellations vary: Landsat ~8-11 bands,
  Sentinel-2 13, WorldView-2/3 8-9). The PRINCIPLE is confirmed; the
  exact number stays as the slide says for recreation.

## Open questions
- [?] Title asks "WHERE TO GET" filters but body answers their SHAPE (k-D);
  the "learned vs hand-crafted" answer presumably comes on a neighboring
  slide. No source conflict — note only.
