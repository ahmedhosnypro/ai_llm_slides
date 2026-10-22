# Slide 039 — "How many filters we should apply" (parameter sharing / stationarity) — SOURCES

## Slide content (from analysis/slide_039_raw.json)
Title: "How many filters we should apply". Hypothesis: "Natural images are
stationary" / "Visual features are common for different parts of one or
multiple image". Conclusion: "It is not required to use different filters for
different spatial locations in the image (in other words, apply same filter
for ALL positions in the image)" (highlighted). Two meme photos with
red/yellow/green detection rectangles; bottom annotation: Red filter -> ears,
yellow -> nose, Green -> edges, each "in the whole image".

This slide is the classic PARAMETER SHARING argument of CNNs.

## Primary source A: CS231n — Convolutional Neural Networks (Stanford)
URL: https://cs231n.github.io/convolutional-networks/ (fetched 2026-10-12)

Confirmed, exact quotes from the page's "Parameter Sharing" section:
- "Parameter sharing scheme is used in Convolutional Layers to control the
  number of parameters."
- "...we are going to constrain the neurons in each depth slice to use the
  same weights and bias... Alternatively, all 55*55 neurons in each depth
  slice will now be using the same parameters."
- "If detecting a horizontal edge is important at some location in the image,
  it should intuitively be useful at some other location as well due to the
  translationally-invariant structure of images. There is therefore no need
  to relearn to detect a horizontal edge at every one of the 55*55 distinct
  locations."
-> This IS the slide's hypothesis->conclusion argument (slide uses
"stationary" for "translationally-invariant structure").

## Primary source B: d2l.ai ch. 7.1 "From Fully-Connected Layers to Convolutions"
URL: https://d2l.ai/chapter_convolutional-neural-networks/why-conv.html

Confirmed:
- "our network should respond similarly to the same patch, regardless of
  where it appears in the image" (translation invariance principle).
- "This is only possible if V and U do not actually depend on (i,j)" —
  kernel independent of location; "V is referred to as a convolution kernel,
  a filter, or simply the layer's weights".
- Waldo illustration (Fig. 7.1.1/7.1.2): what Waldo looks like does not
  depend on where Waldo is located -> features common across image parts.

## Primary source C (document): LeCun, Bottou, Bengio, Haffner 1998
"Gradient-Based Learning Applied to Document Recognition", Proc. IEEE 86(11)
— the canonical CNN paper stating the stationarity/weight-sharing argument
(conventional wisdom often cited as: "Natural images are stationary, i.e.,
the statistics of one part of the image are the same as any other part").
Downloaded: lecun-98.pdf (46 pages) from
http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf
[?] The PDF's embedded Type3 fonts have no ToUnicode map: pdftotext/pypdf
extraction is GARBLED, so the exact "stationary" sentence could not be
machine-verified from this copy. Attribution kept [?]; concept confirmed by
sources A and B.

## Downloaded figures (original filenames)
- waldo-football.jpg (2048x1149) — d2l Fig. 7.1.1 "Can you find Waldo"
  (photo credit William Murphy): where-you-look must not change what you
  search for — illustrates features common across image locations.
- waldo-mask.jpg (3599x2024) — d2l Fig. 7.1.2 "Detect Waldo": locality
  (only a small neighborhood needed) — companion to the invariance argument.
- weights.jpeg (627x248) — CS231n figure "Example filters learned by
  Krizhevsky et al.": each of the 96 [11x11x3] filters is shared by the
  55*55 neurons of one depth slice (page caption = parameter sharing).

## Confirmations vs corrections
- Slide's hypothesis/conclusion matches CS231n parameter sharing + d2l
  translation-invariance reasoning; teaching content is standard.
- Slide annotation (Red->ears, Yellow->nose, Green->edges, applied to the
  whole image) is the course's own demonstration; no external figure to
  fetch for it (photos are course-displayed memes).
- [?] Verbatim LeCun "stationary" sentence unverified by extraction (garbled
  fonts in yann.lecun.com PDF).

## Open questions
- [?] Which colored rectangle on the meme photos maps to which filter is a
  narration-dependent detail; original frame is ground truth.
