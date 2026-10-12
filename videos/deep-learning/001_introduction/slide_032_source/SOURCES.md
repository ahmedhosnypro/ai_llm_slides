# Slide 032 — "Where to Get Filters for Recognition" (2-D images, 2-D parameters) — SOURCES

## Slide content (from analysis/slide_032_raw.json)
Title "Where to Get Filters for Recognition". Three blue paragraphs:
"If images are 2-D, parameters should also be organized in 2-D" / "That way
they can learn the local correlations between input variables" / "That way
they can "exploit" the spatial nature of images". Right diagram: red
"2-D Image" label; box with handwritten "Grayscale", pen-nib icon, brown
perspective plane (2-D image), small blue filter rectangle, red handwritten
"Filters" + arrow. This is the LOCALITY argument (first half of a pair with
slide 033's k-D extension).

## Primary source A: CS231n — Convolutional Neural Networks (Stanford)
URL: https://cs231n.github.io/convolutional-networks/ (fetched 2026-10-12)

Confirmed — exact quote (Local Connectivity section):
- "When dealing with high-dimensional inputs such as images, as we saw
  above it is impractical to connect neurons to all neurons in the previous
  volume. Instead, we will connect each neuron to only a local region of
  the input volume. The spatial extent of this connectivity is a
  hyperparameter called the receptive field of the neuron (equivalently
  this is the filter size)."
-> 2-D image inputs take 2-D local connectivity = 2-D parameter
   organization ("parameters organized in 2-D" = the receptive field).

## Primary source B: d2l.ai ch. 7.1 "From Fully-Connected Layers to Convolutions" (fetched 2026-10-12)
URL: https://d2l.ai/chapter_convolutional-neural-networks/why-conv.html
- Locality principle: "The earliest layers of the network should focus on
  local regions, without regard for the contents of the image in distant
  regions" / "we believe that we should not have to look very far away
  from location (i,j) in order to glean relevant information".
-> "local correlations between input variables" = d2l's locality.

## Primary source C: LeCun et al. 1998 (Gradient-Based Learning Applied to
## Document Recognition, Proc. IEEE 86(11))
The canonical origin of the local-correlation argument (local receptive
fields + shared 2-D kernels exploiting image structure). PDF copy already
banked with slide 039 (lecun-98.pdf, yann.lecun.com) — its embedded fonts
prevent text extraction, so verbatim quotes are [?]; agy search (2026-10-12)
confirms the doctrine chain: "Local correlations -> convolution with
shared kernels; Spatial structure -> 2-D kernels respecting image
topology; Local receptive fields -> limited-size patches".

## Downloaded figures (original filenames)
- correlation.svg — d2l Fig. 7.2.1: two-dimensional cross-correlation —
  a 2-D input with a 2-D kernel, the exact 2-D-parameters-on-2-D-image
  situation the slide describes (grayscale plane + blue 2-D filter).

## Confirmations vs corrections
- Slide's three paragraphs are the standard CNN design rationale (local
  receptive fields / local correlations / spatial structure). No conflict
  with sources. Course quotes around "exploit" are verbatim.
- [?] Exact phrase "exploit the spatial nature of images" may derive from
  LeCun's writings or a prior course deck; wording stays verbatim.

## Open questions
- [?] Pen-nib icon purpose (hand-annotation marker) — decorative; original
  frame is ground truth.
