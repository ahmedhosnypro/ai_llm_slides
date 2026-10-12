# Slide 034 — "What would a k-D filter looks like?" — SOURCES

## Slide content (from analysis/slide_034_raw.json)
Title "What would a k-D filter looks like?". Left: "e.g. Sobel 2-D filter"
caption over Grumpy Cat meme with large red matrix [-1 0 1 / -2 0 2 / -1 0
1] overlaid. Right: three overlapping tinted copies of the same meme (red
back, green middle, blue front) labeled "3-D Filter", plus an isometric
3x3x3 digit cube annotated "Third D" (yellow label, depth-axis arrows).
Point: a 2-D filter slides over a grayscale image; on RGB the filter gains
a THIRD dimension (depth = channels) — a k-D filter.

## Primary source A: Sobel operator (Sobel & Feldman 1968)
- Wikipedia "Sobel operator" (wikitext banked by research fleet:
  scratch_research_031_040/sobel.wikitext): "It is named after Irwin Sobel
  and Gary M. Feldman, colleagues at the Stanford Artificial Intelligence
  Laboratory (SAIL). Sobel and Feldman presented the idea of an 'Isotropic
  3x3 Image Gradient Operator' at a talk at SAIL in 1968."
  Also known as "Sobel–Feldman operator". Discrete differentiation operator
  approximating the image gradient.
- agy search confirmation (2026-10-12): attribution SAIL 1968; standard Gx
  kernel = [[-1,0,1],[-2,0,2],[-1,0,1]] — EXACT match to the slide's red
  matrix (same sign convention).

## Primary source B: OpenCV Sobel Derivatives tutorial
URL: https://docs.opencv.org/3.4/d2/d92/tutorial_sobel_derivatives.html
(docs.opencv.org is Cloudflare-gated; markdown source fetched from
https://raw.githubusercontent.com/opencv/opencv/4.x/doc/tutorials/imgproc/
imgtrans/sobel_derivatives/sobel_derivatives.markdown)

Confirmed — exact formulation:
- "The Sobel Operator is a discrete differentiation operator. It computes
  an approximation of the gradient of an image intensity function."
- "The Sobel Operator combines Gaussian smoothing and differentiation."
- Gx = [ -1 0 +1 ; -2 0 +2 ; -1 0 +1 ] * I  (IDENTICAL to the slide
  matrix); Gy = [ -1 -2 -1 ; 0 0 0 ; +1 +2 +1 ]; G = sqrt(Gx^2+Gy^2) or
  |Gx|+|Gy|. Scharr note for 3x3 accuracy ([?] not on the slide).

## k-D / 3-D filter concept (see also slide 036/037 SOURCES)
- CS231n (https://cs231n.github.io/convolutional-networks/): "Each neuron
  in the convolutional layer is connected only to a local region in the
  input volume spatially, but to the full depth (i.e. all color channels)":
  on RGB, the filter's third dimension = 3 channels — the slide's R/G/B
  tinted stack and "Third D" cube visualize exactly this.
- d2l.ai ch. 7.4 Channels: kernel must have "the same number of input
  channels as the input data" (shape c_i x k_h x k_w).

## Downloaded figures (original filenames)
From Wikipedia Sobel-operator article (via Wikimedia Commons
Special:FilePath; classic "bikesgray" Sobel demo):
- Bikesgray.jpg (640x480) — original grayscale photo of bicycles.
- Bikesgraygh.jpg — image after horizontal-change (Gx-style) filtering.
- Bikesgraygv.jpg — image after vertical-change (Gy-style) filtering.
- Bikesgraysobel.jpg — combined Sobel gradient magnitude (edges).
From OpenCV tutorial source (raw.githubusercontent.com/opencv/opencv 4.x):
- Sobel_Derivatives_Tutorial_Theory_0.jpg (200x240) — theory figure: an
  image with an obvious edge ("we want to detect the edges present in the
  image").

## Confirmations vs corrections
- Slide's Sobel matrix is EXACTLY OpenCV's canonical Gx kernel ✓.
- Attribution: Sobel & Feldman, SAIL, 1968 (talk); sometimes dated 1970 in
  older course notes [?]. Wikipedia/ResearchGate (Irwin Sobel 2014, "History
  and Definition of the Sobel Operator") support 1968.
- 3-D filter = filter depth equals input depth (3 for RGB) — consistent
  with CS231n/d2l. No corrections.

## Open questions
- [?] Cube digits uncertain in places (analysis marked top row "2,3,[?]");
  original frame is ground truth for the digit values.
- [?] Course may cite "Sobel 1968/1970" wording in narration; slide text
  itself just says "e.g. Sobel 2-D filter".
