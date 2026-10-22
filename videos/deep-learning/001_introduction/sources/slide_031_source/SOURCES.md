# Slide 031 — "Where to Get Filters for Recognition" (handcrafted filters, learnable theta) — SOURCES

## Slide content (from analysis/slide_031_raw.json)
Title "Where to Get Filters for Recognition". Blue text: "There are
Several, handcrafted filters in computer vision" / "For example:" / "Canny,
Sobel, Gaussian blur, smoothing, low- level segmentation, morphological
filters, Gabor filters,...". Two red bullets: "Are they optimal for
recognition?" / "Can we learn them from our data?". Bottom: blue label box
"Filter Parameters" next to a red-bordered 3x3 matrix
[theta_1..theta_9] in square brackets. Recording artifacts on frame: mouse
cursor + PowerPoint "...ument has just been saved..." tooltip (do NOT
recreate).

## What each named handcrafted filter is (per Wikipedia articles banked in
## scratch_research_031_040/ + agy checks, 2026-10-12)
- Canny — multi-stage EDGE DETECTION operator, developed by John F. Canny
  in 1986; paper: "A Computational Approach to Edge Detection", IEEE
  TPAMI 8(6):679-698, 1986 (canny.wikitext quote: "It was developed by
  John F. Canny in 1986"). Its optimal edge-detector solution "can be
  approximated by the first derivative of a Gaussian" — the reason
  Gaussian smoothing sits inside Canny.
- Sobel — Sobel-Feldman "Isotropic 3x3 Image Gradient Operator", SAIL
  talk 1968 (full record in slide_034_source/SOURCES.md).
- Gabor filter — "named after Dennis Gabor, who first proposed it as a 1D
  filter" in "Theory of communication" (J. Inst. Electr. Eng., 1946);
  2-D Gabor filters = linear filters for texture analysis (gabor.wikitext).
- Morphological filters — mathematical morphology: dilation/erosion by a
  structuring element (morphology.wikitext; theory due to Matheron & Serra).
- Gaussian blur / smoothing — convolution with a Gaussian kernel
  (standard low-pass operator; underlying Canny's first stage).
- "low-level segmentation" — generic CV stage term; no single canonical
  figure. [?] no external source pinned.

## The theta matrix / learnable-parameters question
- The 3x3 [theta_1..theta_9] box = a generic 3x3 filter written as
  learnable parameters (theta notation is the standard ML convention, e.g.
  Goodfellow et al. "Deep Learning" ch. 5, or CS231n linear classifiers).
- The two red bullets pose the handcrafted-vs-learned question that CNNs
  answer: CS231n's learned-filter figure caption — "Example filters learned
  by Krizhevsky et al." (weights.jpeg, banked with slides 039/040) — and
  LeCun et al. 1998 (filters learned by gradient descent) confirm the
  "learn them from our data" premise. [?] the slide itself does not cite a
  paper; the matrix is generic.

## Downloaded figures (original filenames; Wikimedia Commons
## Special:FilePath, from the Wikipedia articles for each operator)
- Valve_original_(1).PNG (640x480) — original color photo of an engine
  (the classic demo image shared by the Sobel and Canny articles).
- Valve_monochrome_canny_(6).PNG (640x480) — "The Canny edge detector
  applied to a color photograph of a steam engine" (canny.wikitext caption).
- Gabor_filter_function.png (544x542) — "Example of a two-dimensional
  Gabor filter" (gabor.wikitext caption).
- DilationErosion.png (313x390) — "A shape (in blue) and its morphological
  dilation (in green) and erosion (in yellow) by a diamond-shaped
  structuring element" (morphology.wikitext caption).
- Note: Gabor figure timed out once on first download; succeeded on retry
  (same original filename).

## Confirmations vs corrections
- Every named filter is a real, standard handcrafted CV operator with the
  attributions above; slide list order matches no particular canon —
  recreate verbatim (including "low- level" spacing).
- The red questions + theta matrix represent the standard pivot from
  handcrafted to learned filters; no source disagreement.

## Open questions
- [?] No citation on the slide for the theta-matrix convention; treat as
  generic ML notation (recreate as shown).
