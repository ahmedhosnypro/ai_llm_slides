# Slide 040 — "How many filters we should apply" — SOURCES

## Slide content (from analysis/slide_040_raw.json)
Title: "How many filters we should apply". Bullets: "Example: 30 different
filters" / "Each filter can detect different information from the image" /
"Apply those 30 filters on the image (each one should be applied on the whole
locations on the image)". Visuals: Grumpy Cat meme + dog-in-bed photo with
object-detection-style bounding boxes; small montage (~6x6 colorful patches)
of CNN filter visualizations; yellow text box, blue border, dark-blue text.

## Primary source: CS231n — Convolutional Neural Networks (Stanford)
URL: https://cs231n.github.io/convolutional-networks/

Confirmed (quote, from the page's CONV layer section):
- "the depth of the output volume is a hyperparameter: it corresponds to the
  number of filters we would like to use, each learning to look for something
  different in the input. For example, if the first Convolutional Layer takes
  as input the raw image, then different neurons along the depth dimension
  may activate in presence of various oriented edges, or color blots."
  -> Directly matches slide bullets: number of filters = each detects
  different information.
- "Example architecture: INPUT [32x32x3] ... CONV ... [32x32x12] if we decided
  to use 12 filters" -> the "Example: N different filters" pattern (course
  uses 30; CS231n uses 12; concept identical — slide wins for recreation).
- On the montage: "Example filters learned by Krizhevsky et al. Each of the
  96 filters shown here is of size [11x11x3]" -> the slide's small square of
  ~36 colorful patches is this same genre of first-layer learned-filter
  visualization (Krizhevsky et al. 2012 / cuda-convnet style; Zeiler & Fergus
  2013 popularized the deconv visualization grid).
- Re "each one should be applied on the whole locations": CS231n explains a
  filter is shared by all neurons in one depth slice ("parameter sharing"),
  i.e. one filter slides over every location producing one activation map.

## Downloaded figures (original filenames, from cs231n.github.io)
- weights.jpeg (627x248) — CS231n figure: "Example filters learned by
  Krizhevsky et al." — the 96 first-layer [11x11x3] filters visualized as a
  montage of colorful patches; matches the slide's bottom-right filter-grid
  thumbnail genre.
- depthcol.jpeg (464x326) — CS231n figure: input volume + first CONV layer
  volume, showing multiple neurons (filters) along the depth looking at the
  SAME receptive field — illustrates "apply those 30 filters on the image".

## Secondary source (context, not fetched for figures)
- Zeiler & Fergus, "Visualizing and Understanding Convolutional Networks",
  ECCV 2014 / arXiv:1311.2901 — deconv filter visualizations (grids of
  Gabor-like edge/color patches). [agy search 2026-10-12]

## Confirmations vs corrections
- Slide's teaching content fully supported by CS231n: depth = number of
  filters; each filter learns to look for something different; every filter
  is applied at every location (parameter sharing / convolution).
- [?] The exact source image for the ~6x6 montage thumbnail on the slide
  (could be Krizhevsky cuda-convnet weights, ZF Fig.2, or a course-made
  montage) — decide during recreation against the original frame.

## Open questions
- [?] The two photos' bounding boxes look like object-detection output
  (different detector pass), not filter outputs — decorative motivation
  imagery; no canonical figure to fetch.
