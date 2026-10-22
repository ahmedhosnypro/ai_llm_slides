# Slide 042 — "Output dimensions of Convolution?" — web sources

Slide content (from `../analysis/slide_042_raw.json`): 3D input volume labeled
w_in/h_in/d_in (with a small "s" stride arrow on its face), a stack of n_f colored
filter slices labeled w_f/h_f/d_f, a large "=" sign, an output volume labeled
w_out/h_out/d_out, and an equation box:
- h_out = (h_in - h_f)/s + 1
- w_out = (w_in - w_f)/s + 1
- d_out = n_f
- d_f = d_in
plus a variable legend (h height, w width, d depth, f filter, n filters count, S stride).

## Source URLs (fetched 2026-10-12)

1. **CS231n — Convolutional Neural Networks**
   <https://cs231n.github.io/convolutional-networks/>
   Confirms every element of the slide's rule set:
   - Output spatial size: "We can compute the spatial size of the output volume as a
     function of the input volume size (W), the receptive field size of the Conv Layer
     neurons (F), the stride with which they are applied (S), and the amount of zero
     padding used (P)" — formula (W - F + 2P)/S + 1. The slide's formula is the
     P = 0 ("valid") special case: (W - F)/S + 1.
   - "the depth of the output volume ... corresponds to the number of filters" -> d_out = n_f.
   - "The extent of the connectivity along the depth axis is always equal to the depth
     of the input volume" -> d_f = d_in (each filter spans the full input depth).
2. **Goodfellow, Bengio & Courville, *Deep Learning* (MIT Press), ch. 9 "Convolutional
   Networks"** — <http://www.deeplearningbook.org/contents/convnets.html>
   Confirms the P=0, S=1 case verbatim: "If the input image has width m and the kernel
   has width k, the output will be of width m - k + 1." (This chapter also contains the
   cascade-shrinkage discussion relevant to the neighboring slides.)
3. **Wikipedia — Convolutional neural network** —
   <https://en.wikipedia.org/wiki/Convolutional_neural_network>
   "Spatial arrangement" section: "Three hyperparameters control the size of the output
   volume of the convolutional layer: the depth, stride, and padding size" — same
   parameter set as the slide's equation box; also defines "same" padding (preserve
   spatial size), which is the padding generalization the slide omits.

## Downloaded figures (original filenames kept)

- `Conv_layer.png` — Wikipedia CNN-article figure (634x426) showing a 3D input volume,
  a convolutional kernel sliding over it, and the resulting output volume — the same
  input-volume/filter/output-volume layout as the slide's diagram.
  Source: <https://commons.wikimedia.org/wiki/Special:FilePath/Conv_layer.png>
  (file page: <https://en.wikipedia.org/wiki/File:Conv_layer.png>)

## Confirmed vs the slide

- All four equations CONFIRMED standard. The slide's spatial formula is the classic
  output-size formula in its zero-padding (P=0) form; the fully general form is
  (W - F + 2P)/S + 1 (CS231n). d_out = number of filters and filter-depth = input-depth
  are stated verbatim by CS231n.
- Notational note (understanding only): the general formula also requires a floor when
  (W - F + 2P) is not divisible by S; with the slide's S=1 valid convolution the
  division is always exact, so the slide's plain fraction is correct as written.

## Corrections vs the slide

None — the slide's equations are correct for the valid-convolution case it depicts
(no padding). If a later slide introduces padding, the slide-wins rule still applies;
the general formula lives here for provenance.

## Open questions

- [?] The exact source deck of the DIAGRAM (orange input slab + 5 colored filter slices
  + large "=" + output box, labels w_in/h_in/d_in, w_f/h_f/d_f, n_f) is unidentified —
  the notation differs from CS231n's (W,F,S,P,K) and from Goodfellow's (m,k,p,s). Web
  search providers (agy search, DuckDuckGo) were unavailable during this run (403 /
  bot-challenge). Content is fully confirmed; only the figure's teaching-deck provenance
  is unverified.
