# SOURCES.md — slide 030 ("Apply filter on 2-D  gray image  (K=1 Channel)")

Research date: 2026-10-12. Worker: web-research lane, slides 021–030 (reverse run).

## Slide nature

Live-demo slide: the Sobel 2-D filter (3×3 kernel [[-1,0,1],[-2,0,2],[-1,0,1]], drawn in
large red numerals between oversized red brackets) applied to a single-channel (K=1,
grayscale) image. Left panel: the Grumpy Cat "I LOVE MATH / IT MAKES PEOPLE CRY!" meme
photo (handwritten caption "e.g. Sobel 2-D filter"); red block arrow; right panel: the
Sobel-filtered (edge-detected, near-black with faint white contours) version of the same
meme. Factual content to verify: the Sobel kernel values, the operator's name/origin, and
the single-channel (K=1) framing.

## Source URLs

1. **Wikipedia — "Sobel operator"**
   - URL: https://en.wikipedia.org/wiki/Sobel_operator
   - Status: FETCHED and CONFIRMED (2026-10-12, curl fallback after WebFetch/docs-fetcher
     timeouts; 221 KB HTML).
   - Confirms: the operator is the **Sobel–Feldman operator** ("Isotropic 3 × 3 Image
     Gradient Operator"), presented by **Irwin Sobel and Gary M. Feldman at the Stanford
     Artificial Intelligence Laboratory (SAIL) in 1968**; it is a **discrete
     differentiation operator** computing an approximation of the **gradient of the image
     intensity function** by convolving the image with a small, separable, integer-valued
     filter in horizontal and vertical directions; used within **edge detection** to
     "create an image emphasizing edges" — exactly the near-black-with-edges output shown
     on the slide's right panel.
   - Kernel: the horizontal kernel **Gx = [[-1,0,1],[-2,0,2],[-1,0,1]]** as printed on the
     slide is the standard Gx (derivative kernel [-1 0 1] ⊗ smoothing [1 2 1]); confirmed
     verbatim by agy search synthesis of library definitions (OpenCV, scikit-image,
     MATLAB all ship this kernel). Vertical Gy is the transpose form
     [[-1,-2,-1],[0,0,0],[1,2,1]] — NOT shown on this slide (K=1 demo uses one kernel).

2. **Sobel & Feldman (1968), "A 3x3 Isotropic Gradient Operator for Image Processing"**,
   Stanford Artificial Intelligence Project (SAIL) — the primary 1968 source named by
   Wikipedia's article as reference [1]. Not independently fetched (1968 SAIL memo; no
   stable canonical URL fetchable from this network) [?].

## Downloaded files

Downloaded into `slide_030_source/` from Wikimedia Commons (original filenames preserved):

1. `Valve_original_(1).PNG` (640×480 PNG, 404,846 bytes)
   - https://upload.wikimedia.org/wikipedia/commons/f/f0/Valve_original_%281%29.PNG
   - Wikipedia Sobel article's lead demonstration: the original photograph of a valve
     (engine) — the "before" half of the canonical Sobel before/after figure pair.
2. `Valve_sobel_(3).PNG` (640×480 PNG, 295,475 bytes)
   - https://upload.wikimedia.org/wikipedia/commons/d/d4/Valve_sobel_%283%29.PNG
   - Caption (Wikipedia): "The Sobel operator applied to that image" — the "after" half:
     near-black image with faint light edge contours, structurally identical to the
     slide's right-panel result. This pair demonstrates the same photo → edge-map
     transformation the slide demonstrates on the meme.

(Other page figures — Bikesgray_sobel.JPG, Bikesgraysobel.jpg,
Sobel_Operator_Gradient_Angle.JPG — exist but are less relevant; not downloaded.)

## Confirmed / corrected vs the slide

- Kernel values CONFIRMED: [[-1,0,1],[-2,0,2],[-1,0,1]] is the canonical Sobel Gx —
  recreation must keep these verbatim.
- "2-D gray image (K=1 Channel)" CONFIRMED as standard framing: the Sobel operator is a
  2-D spatial convolution applied per channel; a grayscale image has K=1 channel.
- Right-panel output appearance CONFIRMED as the expected Sobel result (compare
  `Valve_sobel_(3).PNG`): near-black with faint light edges.
- Imagery origin: the meme is the **Grumpy Cat** photo of **Tardar Sauce** (snowshoe cat
  with dwarfism/underbite), posted to Reddit r/pics on 2012-09-22 by Bryan Bundesen; the
  "I LOVE MATH / IT MAKES PEOPLE CRY!" caption is a user-added image-macro variant, not
  part of the original meme phenomenon. The exact meme image is the slide's own imagery —
  the original frame is ground truth for it (recreation crops from the frame; no download
  attempted).
- Fidelity notes (verbatim, per fidelity law): the slide title carries doubled spaces
  ("2-D  gray") and the meme's top caption ends with "!" while the right panel's top
  caption reads "I LOVE MATH" without "!" — keep both as measured in the raw JSON.
- Raw JSON notes a tiny bottom-left watermark on the right image (possibly "know your
  meme") and a screen-recording mouse cursor over the matrix's bottom-right "1" — both
  video/frame artifacts, not slide content to source.

## Open questions

- [?] The exact upstream page the lecturer screencapped for the meme demo (a "know your
  meme" or similar page) — the watermark is illegible at frame resolution; does not affect
  recreation (frame is ground truth).
- [?] Whether the lecturer's filtered result used |Gx|+|Gy| magnitude or Gx alone —
  not determinable from the frame; irrelevant to recreation (output image is copied as-is).

## ADDENDUM (2026-10-12, later same run) — exact origin found

The slide is lifted from **UvA Deep Learning Course, Lecture 4: Convolutional Neural
Networks (Efstratios Gavves)**, https://uvadlc.github.io/lectures/nov2019/lecture4.pdf —
p.16 "Example filter when K=1 / e.g. Sobel 2-D filter" with the same kernel
−1 0 1 / −2 0 2 / −1 0 1 (pdftotext-verified). Slide 028's attribution ("Some of Slides
are picked from UVA Deep Learning Course EFSTRATIOS GAVVES") names this deck; the PDF is
banked at `../slide_028_source/lecture4.pdf`. The DSAI slide's title ("Apply filter on
2-D  gray image  (K=1 Channel)") is the DSAI lecturer's retitle of UvA's "Example filter
when K=1" — DSAI wording wins for recreation (fidelity law). The Grumpy Cat meme demo is
the DSAI lecturer's addition (UvA p.16 carries its own example imagery).
