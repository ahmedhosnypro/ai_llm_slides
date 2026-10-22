# slide_049 — Convnets in practice — SOURCES

Slide content (from `analysis/slide_049_raw.json`): recipe slide, 4 bullets —
(1) Several convolutional layers ( 5 or more); (2) After the convolutional layers
non-linearities are added (The most popular one is the ReLU); (3) After the ReLU
usually some pooling ( Most often max pooling); (4) After 5 rounds of cascading:
→ Vectorize the last convolutional layer (Flatten); → Use as Input to the first
fully connected layer (FC); → Proceed as in a traditional classification neural
network. Text-only slide (red top rule, blue-bordered content box).

## Sources consulted (web-verified 2026-10-12)

1. **CS231n — Convolutional Networks (Stanford), "Layer Patterns" section**
   URL: https://cs231n.github.io/convolutional-networks/
   Confirmed (near-verbatim support for the slide's recipe):
   - "the most common form of a ConvNet architecture stacks a few CONV-RELU layers,
     follows them with POOL layers, and repeats this pattern until the image has been
     merged spatially to a small size. At some point, it is common to transition to
     fully-connected layers. The last fully-connected layer holds the output, such as
     the class scores."
   - The canonical pattern: `INPUT -> [[CONV -> RELU]*N -> POOL?]*M -> [FC -> RELU]*K
     -> FC` — exactly the slide's conv → ReLU → pool cascade → FC pipeline.
   - AlexNet case study: "featured Convolutional Layers stacked on top of each other
     (previously it was common to only have a single CONV layer always immediately
     followed by a POOL layer)" — supports "Several convolutional layers ( 5 or
     more)" as the post-2012 practice (AlexNet/ZFNet have 5 conv layers).
2. **d2l.ai — Dive into Deep Learning, §7.6 Convolutional Neural Networks (LeNet)**
   URL: https://d2l.ai/chapter_convolutional-neural-networks/lenet.html
   Confirmed:
   - "In order to pass output from the convolutional block to the dense block, we
     must flatten each example in the minibatch." ← slide: "Vectorize the last
     convolutional layer (Flatten)" + "Use as Input to the first fully connected
     layer (FC)".
   - LeNet: convolutional encoder → dense block (FC 120 → 84 → 10) → classification —
     ← slide: "Proceed as in a traditional classification neural network".
   - "Note that while ReLUs and max-pooling work better, they had not yet been
     discovered" (LeNet used sigmoid + average pooling) — confirms the slide's
     "The most popular one is the ReLU" and " Most often max pooling" as MODERN
     practice (post-2012), i.e. the slide describes contemporary ConvNet practice,
     not LeNet-era practice.
3. **Web search (agy)** — corroborated the standard conv/ReLU/pool ordering and
   flatten→FC handoff; ReLU's popularity as the default CNN non-linearity (popularized
   by Krizhevsky et al. 2012 AlexNet).

## Downloaded figures

- `lenet.svg` — d2l Fig. 7.6.1: "Data flow in LeNet. The input is a handwritten
  digit, the output is a probability over 10 possible outcomes." — a real in-practice
  ConvNet flow diagram (conv → pool → ... → flatten → dense) matching the slide's
  recipe end to end.
- `lenet-vert.svg` — d2l Fig. 7.6.2: "Compressed notation for LeNet-5." — compact
  conv/pool/FC pipeline notation.

## Confirmations vs the slide

- conv → ReLU (non-linearity) → pooling, cascaded several rounds, then flatten → FC
  → standard classification NN: CONFIRMED as the canonical pattern (CS231n Layer
  Patterns; d2l LeNet).
- ReLU as most popular non-linearity; max pooling as most common pooling: CONFIRMED
  (CS231n "The most common form is a pooling layer... using the MAX operation";
  d2l's note that ReLUs and max-pooling "work better" than the LeNet-era choices).
- Flatten/vectorize last conv output → first FC layer: CONFIRMED (d2l flatten step).

## Corrections / discrepancies

- None material. The slide's "( 5 or more)" is a reasonable rule-of-thumb (LeNet-5
  has 2 conv layers; AlexNet/ZFNet 5; the slide says "several... 5 or more" — the
  "or more" covers VGG-class stacks). No source contradicts it.
- Slide's odd spacing "( 5 or more)", "( Most often max pooling)" is verbatim
  original-slide text — recreate verbatim (typography note, not a source issue).

## Open questions

- [?] Whether the lecturer's "After 5 rounds of cascading" refers specifically to a
  known 5-block example (e.g. AlexNet/ZFNet's five conv layers) or is a generic
  round count — the frame does not cite a network; recorded as unresolved, frame
  wins for recreation.
