# Slide 041 — "The Convolution Process" — web sources

Slide content (from `../analysis/slide_041_raw.json`): 5x5 image with numeric overlay,
3x3 convolutional filter (values [1,0,1 / 0,1,0 / 1,0,1], annotated a=1, b=1), the 2D
convolution equation `I(x,y) * h = Sum_{i=-a}^{a} Sum_{j=-b}^{b} I(x-i, y-j) . h(i,j)`
(kernel "odd dimension"), an "Inner product" brace under the highlighted 3x3 window, a
3x3 "Result" grid whose top-left value is 4, and the instruction to move the filter ONE
pixel (stride 1) and re-calculate.

## Source URLs (fetched 2026-10-12)

1. **Wikipedia — Kernel (image processing)**
   <https://en.wikipedia.org/wiki/Kernel_(image_processing)>
   Confirms the slide's equation EXACTLY (modulo variable names). The page's "general
   expression of a convolution" is `g(x,y) = omega * f(x,y) = Sum_{i=-a}^{a} Sum_{j=-b}^{b}
   omega(i,j) f(x-i, y-j)`, with the kernel scanned over `-a <= i <= a`, `-b <= j <= b` —
   the same odd-dimension-kernel formulation (image f = slide's I, kernel omega = slide's
   h). This is the standard textbook form (Gonzalez & Woods, *Digital Image Processing*,
   spatial-filtering chapter, uses the same a=(m-1)/2, b=(n-1)/2 indexing).
2. **CS231n — Convolutional Neural Networks: Architecture**
   <https://cs231n.github.io/convolutional-networks/>
   The page's "Convolution Demo" describes convolution as iterating over output
   activations, "each element is computed by elementwise multiplying the highlighted
   input with the filter, summing it up" — i.e. the slide's "Inner product" walk. The
   demo uses a W1=5, H1=5 input with F=3 filters (slide: 5x5 image, 3x3 filter). The
   page also states the output-size formula (5 - 3 + 2*1)/2 + 1 = 3 for its S=2, P=1
   demo parameters.
3. **Dumoulin & Visin, "A guide to convolution arithmetic for deep learning"
   (arXiv:1603.07285)** — <https://arxiv.org/abs/1603.07285>
   Companion figure repo: <https://github.com/vdumoulin/conv_arithmetic>
   The paper's "no padding, no strides" convolution figure shows exactly the slide's
   setting: a 3x3 kernel sliding by one pixel over an unpadded input, output =
   (W - F)/S + 1 per axis.

## Downloaded figures (original filenames kept)

- `2D_Convolution_Animation.gif` — Wikipedia Commons file "2D Image-Kernel Convolution
  Animation" (author Michael Plotke, 28 Jan 2013, CC BY-SA 3.0), from the Kernel
  (image processing) page: a 3x3 kernel sliding over an image, the output matrix being
  filled one cell at a time — the same process the slide teaches.
  Source: <https://upload.wikimedia.org/wikipedia/commons/1/19/2D_Convolution_Animation.gif>
- `no_padding_no_strides.gif` — Dumoulin & Visin (arXiv:1603.07285) conv_arithmetic
  figure "no padding, no strides": 3x3 dark-blue kernel sliding over 4x4 blue input,
  2x2 cyan output (= (4-3)/1 + 1 = 2). Same "one pixel at a time" walk as the slide.
  Source: <https://raw.githubusercontent.com/vdumoulin/conv_arithmetic/master/gif/no_padding_no_strides.gif>

## Confirmed vs the slide

- Equation: CONFIRMED standard 2D convolution (odd-size kernel, symmetric index range
  -a..a, -b..b; 3x3 kernel => a=b=1 matches the slide's "a=1, b=1").
- Process: CONFIRMED — sliding-window inner product (elementwise multiply + sum), stride
  1, valid (unpadded) convolution.
- Arithmetic CHECK (hand-verified): slide's top-left 3x3 window [1,1,1 / 0,1,1 / 0,0,1]
  times filter [1,0,1 / 0,1,0 / 1,0,1] = 1+0+1+0+1+0+0+0+1 = 4 — matches the slide's
  "Result ... 4". Output size 5x5 -> 3x3 with F=3, S=1, P=0 via (5-3)/1+1 = 3.
- The filter [1,0,1 / 0,1,0 / 1,0,1] is a symmetric "X-pattern" toy kernel, not one of
  the classic named kernels (identity / box blur / Sobel / sharpen) tabulated on the
  Wikipedia page — consistent with a teaching example, no correction needed.

## Corrections vs the slide

None. The slide's equation and arithmetic are standard and self-consistent.

## Open questions

- [?] The small photo underneath the 5x5 numeric grid (described by vision as a
  "classical painting/scene with greenish tones") could not be identified against a
  known source image; provenance unknown. It is decorative in the slide's demo; the
  grids, filter, equation, and result are fully verified without it.
