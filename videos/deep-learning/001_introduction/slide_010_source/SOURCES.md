# slide_010 — "Pre processing" — SOURCES

Slide content (from slide_010_raw.json, frame = ground truth):
- Lead sentence: "Preprocessing is Problem dependent and data dependent"
- "It may include:" + 10 bullets: Gap filling, Thinning, Contour, Binarization,
  Noise Removal, Color to Gray, Opening touched points, Resizing, Normalization, .......

## What the web confirmed

1. **Thinning / skeletonization** — CONFIRMED as a standard morphological operation:
   scikit-image docs (fetched 2026-10-12):
   https://scikit-image.org/docs/stable/auto_examples/edges/plot_skeleton.html
   - "Skeletonization reduces binary objects to 1 pixel wide representations";
     used for feature extraction and topology representation; Zhang's / Lee's methods.

2. **Pipeline context (binarization -> noise removal -> opening -> gap filling ->
   thinning -> resizing/normalization)** — agy search synthesis (2026-10-12; its live
   web tool was 403-blocked, so this is model knowledge, NOT a fetched page) confirms
   this exact family of ops is the standard preprocessing pipeline for OFFLINE
   HANDWRITTEN CHARACTER / SIGNATURE RECOGNITION (OCR):
   - Binarization: ink/background separation (Otsu / adaptive thresholding).
   - Noise removal: median/morphological filters before/after binarization.
   - Opening: removes small specks; separates points where strokes touch
     ("opening touched points" — separating touching characters/strokes).
   - Gap filling == morphological CLOSING: bridges small stroke breaks.
   - Thinning: Zhang-Suen / Guo-Hall skeletonization to 1-px strokes.
   - Resizing / Normalization: size + stroke-width normalization.
   - "Contour": contour extraction of character components (connected-component step).
   - "Color to Gray": grayscale conversion (step 1 of every such pipeline).
   The slide's "Problem dependent and data dependent" caveat matches the literature:
   op choice/order depends on script, acquisition, and task.

## Figures downloaded

None — the slide is text-only; no site figure applies.

## Corrections / disagreements with the slide

None. The slide lists real, standard preprocessing techniques. No factual error found.

## Open questions

- [?] EXACT ORIGIN OF THE LIST: no canonical published source located for this exact
  10-item bullet list (the phrase "Opening touched points" is distinctive and suggests
  a specific OCR/handwriting-recognition lecture deck or thesis). Search tooling was
  blocked during this run: agy live web search HTTP 403 (location), DuckDuckGo CAPTCHA,
  Bing region-polluted results, Semantic Scholar API 429, Wikipedia ETIMEDOUT.
  TO RE-VERIFY: retry agy (fresh token) with `agy -p "\"opening touched points\" gap
  filling thinning binarization preprocessing handwritten character recognition"` and
  WebFetch any .pdf/.pptx hit; else treat the list as instructor-authored (course-internal).
- [?] Whether "Contour" here means contour extraction (cv2.findContours-style) or
  contour tracing for feature extraction — slide gives no further context.
