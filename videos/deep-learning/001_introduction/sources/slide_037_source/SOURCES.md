# Slide 037 — "How many filter can we apply on the image" — SOURCES

## Slide content (from analysis/slide_037_raw.json)
Title "How many filter can we apply on the image". Body: "We can Apply
multiple filters on the same location (e.g. 5 different filters on the same
location. For Example: [ one to detect edges, one to detect lines, one to
detect curves, ...etc)". Diagram: orange RGB input slab ("3 dims", X mark,
7x7 patch) -> 5 colored filter slabs ("5" above, "3" below) = tan output
cube with 5 colored circles, "Depth=5 dims"; question "How many weights for
these 5 neurons?" answered in red: "5 · 7 · 7 · 3 = 735".
NOTE: slide 37 depends on slide 36 (founder dep graph 37<-36; 36's original
carries a content-crowding issue per founder note).

## Primary source: CS231n — Convolutional Neural Networks (Stanford)
URL: https://cs231n.github.io/convolutional-networks/ (fetched 2026-10-12;
local copy scratch_research_031_040/cs231n_conv.html)

Confirmed — exact quotes:
- "Note, there are multiple neurons (5 in this example) along the depth, all
  looking at the same region in the input: ... these 5 neurons do not share
  the same weights, but they are associated with 5 different filters ... they
  share the same receptive field but not the same weights."
  -> CS231n's own worked example is ALSO 5 filters on the same location —
  the slide's "e.g. 5 different filters" matches CS231n's example size.
- "We will refer to a set of neurons that are all looking at the same region
  of the input as a depth column (some people also prefer the term fibre)."
  -> the slide's output "Depth=5 dims" = depth column of 5.
- "different neurons along the depth dimension may activate in presence of
  various oriented edges, or blobs of color" -> slide's "detect edges /
  lines / curves" specialization per filter.
- Weight count for the 5 neurons at one location: 5 · (7·7·3) = 735 —
  CS231n: "F·F·D1 weights per filter, total (F·F·D1)·K" (see slide 038
  SOURCES; same counting, weights only, no biases).

## Downloaded figures (original filenames)
- depthcol.jpeg (464x326) — CS231n figure: input volume (32x32x3 CIFAR-10)
  + first CONV layer volume; caption states the 5-neuron depth column
  looking at the same receptive field — the canonical version of this
  slide's hand-drawn diagram.

## Confirmations vs corrections
- Concept, example count (5), receptive-field arithmetic (7x7x3) and weight
  total (735) all consistent with CS231n. No corrections needed.
- The course's filter examples (edges/lines/curves) are pedagogical; CS231n
  says "oriented edges, color blots" — compatible, no conflict.

## Open questions
- [?] Output-cube top-face circles (tan,tan,tan,dark-brown,green) vs
  front-face circles (teal,green,red,yellow,purple) — the mixed top-face
  colors are unusual; original frame is ground truth for exact colors.
