# Slide 035 — "How to Apply Filter on image" — SOURCES

## Slide content (from analysis/slide_035_raw.json)
Title "How to Apply Filter on image". Left: 5x5 binary "Image" grid
(11100/01110/00111/00110/01100, green numerals, red border, faint photo
behind). Middle: 3x3 yellow "Filter" (101/010/101). Right: computation
panel — same 5x5 grid with top-left 3x3 highlighted yellow and tiny red
x1/x0 multipliers, a 3x3 output grid whose first cell holds "4", black
curved arrow. Caption (yellow box, blue border): "Apply Filter on Image is
a Dot product between image values and filter values (can be modeled by
PERCEPTRON )" — PERCEPTRON in red bold underlined. Founder frame swap
recorded (new 35 <- old 43; kept frame_01881).
NOTE: slide 41 depends on slide 35 (dep graph 41<-35).

## Arithmetic verification (independent)
- Dot product, patch = rows1-3 cols1-3 of image [1 1 1; 0 1 1; 0 0 1],
  filter [1 0 1; 0 1 0; 1 0 1]:
  (1·1)+(1·0)+(1·1)+(0·0)+(1·1)+(1·0)+(0·1)+(0·0)+(1·1) = 4. Slide "4" ✓
- Output grid 3x3: (W-F+2P)/S+1 = (5-3+0)/1+1 = 3 (CS231n size formula) ✓
- The slide's x1/x0 multipliers are the elementwise products; their sum is
  the dot product — matches the highlighted-cell walkthrough.

## Primary source A: CS231n — Convolutional Neural Networks (Stanford)
URL: https://cs231n.github.io/convolutional-networks/ (fetched 2026-10-12)

Confirmed — exact quotes:
- "each [neuron] computing a dot product between their weights and a small
  region they are connected to in the input volume."
- Numpy example section: "we are computing the dot product as seen before
  in ordinary neural networks" (V[0,0,1] = np.sum(X[:5,:5,:] * W1) + b1).
- Output-volume size formula (W1-F+2P)/S+1 gives the slide's 3x3 output.
- Brain view: "every entry in the 3D output volume can also be interpreted
  as an output of a neuron that looks at only a small region in the input"
  — the slide's "modeled by PERCEPTRON" (a neuron = dot product of weights
  and inputs; Rosenblatt's perceptron computes exactly this weighted sum).

## Primary source B: d2l.ai ch. 7.2 "Convolutions for Images" (fetched)
URL: https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html
- "the input subtensor contained in that window and the kernel tensor are
  multiplied elementwise and the resulting tensor is summed up yielding a
  single scalar value" — the slide's x-multiplier walkthrough verbatim.
- Worked example Eq. 7.2.1 (0×0+1×1+3×2+4×3=19 etc.) and Fig. 7.2.1
  (fig-correlation): same pedagogy, different numbers.

## Search confirmation (agy, 2026-10-12)
Confirmed: at each location the conv output = dot product of the flattened
kernel with the flattened patch (+ bias); one filter = shared weights for
one perceptron per spatial location (local receptive field).

## Downloaded figures (original filenames)
- correlation.svg — d2l Fig. 7.2.1 "Two-dimensional cross-correlation
  operation. The shaded portions are the first output element as well as
  the input and kernel tensor elements used for the output computation" —
  canonical equivalent of the slide's yellow 3x3 + arrow + "4" cell.
- conv-multi-in.svg — d2l Fig. 7.4.1 (multi-input-channel summation);
  supplementary context for the dot-product-over-channels view (also filed
  with slide 038 where it is the primary figure).

## Confirmations vs corrections
- Slide arithmetic (result 4, 3x3 output) verified correct.
- "Modeled by PERCEPTRON" is the standard neuron view (CS231n brain view /
  Rosenblatt); no correction needed.
- The 5x5 image + 3x3 filter numbers are course-specific (d2l uses a 3x3
  input with 2x2 kernel, result 19) — slide wins for recreation; sources
  confirm the method, not the specific matrices.

## Open questions
- [?] The faint green-tinted photo behind the Image grid is indistinct in
  analysis — original frame is ground truth for whether it carries content.
