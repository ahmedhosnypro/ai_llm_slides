# Slide 045 — "Apply Convolution as a NEW MODULE" — web sources

Slide content (from `../analysis/slide_045_raw.json`): convolution reframed as an NN
layer/module — "Since Convolution is a DOT product (between filter values and
corresponding image values), It can be applied as if it is a NN Layer. Input: image
values, Weights: filter values, Activation: Linear, Bias:0"; "Remember: for training, it
is required to have the gradient of Output w.r.t both Input and weights"; equations
- a_{r,c} = Sum_{i=-a}^{a} Sum_{j=-b}^{b} x_{r-i,c-j} * theta_{ij}
- a_{r,c} ~ x_region^T . theta
- d a_{r,c} / d theta_{i,j} = Sum_{r=0}^{N-2a} Sum_{c=0}^{N-2b} x_{r-i,c-j}
with legend theta_ij => filter weights, r,c => row,column, a_rc => activation = Sum.

## Source URLs (fetched 2026-10-12)

1. **CS231n — Convolutional Neural Networks**
   <https://cs231n.github.io/convolutional-networks/>
   - CONFIRMS the dot-product claim verbatim ("Implementation as Matrix
     Multiplication"): "the convolution operation essentially performs dot products
     between the filters and local regions of the input", commonly implemented as one
     big matrix multiply via im2col — i.e. exactly a linear layer applied to stretched
     local regions.
   - CONFIRMS weight sharing ("Parameter sharing"): neurons in a depth slice "use the
     same weights and bias" — the reason the slide's gradient w.r.t. a filter weight
     theta_ij SUMS over all output positions (r,c): every position reuses theta_ij.
2. **Dive into Deep Learning (d2l.ai), ch. 7.2 "Convolutions for Images"**
   <https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html>
   CONFIRMS the module view verbatim: "A convolutional layer cross-correlates the input
   and kernel and adds a scalar bias to produce an output. The two parameters of a
   convolutional layer are the kernel and the scalar bias. When training models based on
   convolutional layers, we typically initialize the kernels randomly, just as we would
   with a fully connected layer." The slide's "Activation: Linear, Bias: 0" is the
   stripped-down special case (linear activation, no bias).
3. **Wikipedia — Kernel (image processing)**
   <https://en.wikipedia.org/wiki/Kernel_(image_processing)>
   The a_{r,c} = Sum Sum x_{r-i,c-j} h(i,j) equation is the same convolution formula
   already verified for slide 041, here with theta as the learnable kernel.

## Downloaded figures (original filenames kept)

- `neuron_model.jpeg` — CS231n's neuron model diagram (input x, weights w, sum, output
  activation f) — the "as if it is an NN Layer" module view the slide's blue box states.
  Source: <https://cs231n.github.io/assets/nn1/neuron_model.jpeg>
- `correlation.svg` — d2l Fig. 7.2.1, the two-dimensional cross-correlation computation
  (input tensor, kernel, output) — the operation whose kernel is the learnable "weights".
  Source: <https://d2l.ai/_images/correlation.svg>

## Confirmed vs the slide

- "Essentially a dot product, similar to linear layer": CONFIRMED (CS231n im2col
  passage; d2l "two parameters ... kernel and scalar bias ... just as we would with a
  fully connected layer").
- "Gradient w.r.t. the parameters": the term d(total activation)/d theta_{ij} =
  Sum_{r,c} x_{r-i,c-j} is the standard weight-sharing gradient (each filter weight
  receives gradient contributions from every position it is applied to). Structure
  CONFIRMED.
- Gradient w.r.t. input (the "Remember" box mentions both): the standard
  d a_{r,c} / d x_{u,v} = theta_{r-u, c-v} — consistent with the same equation family.

## Notational caveats recorded (source wins for understanding)

- [?] The transcribed summation limits Sum_{r=0}^{N-2a} Sum_{c=0}^{N-2b}: for an N x N
  input with a (2a+1) x (2b+1) kernel the valid output has N-2a rows (indices
  0..N-2a-1), so the standard limit would be N-2a-1 / N-2b-1 (one fewer). Likely a
  handwritten-notation slip or a vision transcription nuance — re-derive from the
  frame at recreation time (slide wins for recreation).
- [?] LHS/RHS mismatch: the left side is written d a_{r,c} / d theta_{i,j} (single
  position) while the right side sums over r,c; the sum is the gradient of the TOTAL
  (position-summed) activation — the weight-sharing accumulation. Standard concept,
  sloppy notation.

## Corrections vs the slide

None beyond the notational caveats above; the module/dot-product/shared-gradient
content is standard.
