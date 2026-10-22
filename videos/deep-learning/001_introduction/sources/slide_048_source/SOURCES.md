# slide_048 — Standard Neural Network (NN) vs Convolutional Neural Network (ConvNet/CNN) — SOURCES

Slide content (from `analysis/slide_048_raw.json`): two pipeline rows inside a red
frame — NN row: cat-meme photo → "Flatten (1-D)" dot column → five orange FC blocks
(Layer 1–5, "O/P" over last) → Loss. CNN row: Siamese-cat photo (parallelogram) →
Conv. layer 1 → ReLU layer 1 → Max pool. 1 → Conv. layer 2 → ReLU layer 2 →
Max pool. 2 → Layer 5 (FC) → Layer 6 (O/P) → Loss. Bottom: long red arrow, caption
"Deep Learning (too Many Layers)". Note: founder frame swap recorded
(new 48 ← old 79; kept frame_05043.jpg).

## Sources consulted (web-verified 2026-10-12)

1. **Goodfellow, Bengio, Courville — Deep Learning, ch. 9 (§9.1–9.2)**
   URL: https://www.deeplearningbook.org/contents/convnets.html
   Confirmed (the conceptual backbone of the comparison):
   - "Convolutional networks are simply neural networks that use convolution in place
     of general matrix multiplication in at least one of their layers." — the NN row
     (dense FC only) vs CNN row (conv stages) contrast is exactly this definition.
   - Sparse interactions (Fig. 9.2): "When s is formed by convolution with a kernel of
     width 3, only three outputs are affected by x... When s is formed by matrix
     multiplication, connectivity is no longer sparse, so all the outputs are affected
     by x3." — why the standard-NN row must FLATTEN the image into a 1-D vector first.
   - "Parameter sharing refers to using the same parameter for more than one function
     in a model. In a traditional neural net, each element of the weight matrix [is
     used exactly once]" — the second CNN-row advantage implicit in the comparison.
2. **CS231n — Convolutional Networks (Stanford), "Architecture Overview"**
   URL: https://cs231n.github.io/convolutional-networks/
   Confirmed:
   - "Regular Neural Nets don't scale well to full images... a single fully-connected
     neuron in a first hidden layer of a regular Neural Network would have 32*32*3 =
     3072 weights." — motivates the slide's Flatten(1-D)→FC depiction of a standard NN
     on images.
   - ConvNet layer pattern `INPUT -> [[CONV -> RELU]*N -> POOL?]*M -> [FC -> RELU]*K
     -> FC` — matches the CNN row's Conv/ReLU/MaxPool stages followed by FC → O/P →
     Loss (see slide_049 SOURCES for the full quote).
3. **Web search (agy)** — a provenance search for this specific meme-style comparison
   figure hung and was aborted after ~5 min; no primary deck identified (see [?]).

## Downloaded figures

- None. The slide's imagery (confused-cat meme, Siamese-cat photo) is
  lecturer-supplied artwork, not from a citable source; no site figure matches it.
  CS231n/Goodfellow diagrams for the same concepts are banked in neighboring slides'
  source dirs (046: pool.jpeg/maxpool.jpeg; 049: lenet.svg) and apply here too.

## Confirmations vs the slide

- Standard NN on an image = flatten to 1-D vector, then fully-connected layers:
  CONFIRMED (CS231n Architecture Overview; Goodfellow Fig. 9.2 dense-matrix case).
- ConvNet = conv stages (with non-linearity + pooling) before the FC classifier
  stages, ending in O/P + Loss: CONFIRMED (CS231n layer pattern; Goodfellow 9.3).
- "Deep Learning (too Many Layers)" caption: qualitative, matches the deep-stacks
  framing of AlexNet-era ConvNets (CS231n case studies; no numeric claim to check).

## Corrections / discrepancies

- None of the pipeline content contradicts the sources. One nuance to record: the
  CNN row's "Non Linearity" tags sit under the ReLU slabs — correct per the standard
  pattern (non-linearity follows conv); sources consistently place ReLU between conv
  and pool (CS231n `CONV -> RELU -> POOL`).

## Open questions

- [?] Provenance of the exact comparison figure (cat-meme + parallelogram-cat style):
  likely the lecturer's own construction (deck style is hand-built throughout);
  provenance search aborted on a hanging provider — unresolved, frame wins recreation.
- [?] Cat-meme top caption is blurry in the frame ('I CAN HAS ...'?) — recreation must
  take its text from the frame or leave as-is; not resolvable from any source.
