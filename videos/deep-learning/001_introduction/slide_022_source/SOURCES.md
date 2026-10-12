# SOURCES.md — slide 022 ("Visualization of Single Perceptron")

Research date: 2026-10-12. Worker: web-research lane, slides 021–030.

## Slide content verified

Perceptron model in "augmented vector" form: X = (x₁..xₙ) ⇒ X = (1, x₁..xₙ)ᵀ
("Ugmented Vector" — verbatim slide typo for "Augmented"), W = (b, w₁..wₙ)ᵀ ("Model
Weights"), decision rule d(X) = WᵀX = w₁x₁ + ... + wₙxₙ + b·1 with three cases
(>0 ⇒ Class I, <0 ⇒ Class II, =0 ⇒ Undefined Class), the signal-flow diagram
(inputs x₁..xₙ + red bias input 1, weights w₁..wₙ + b, Σ circle, step-function block,
O/P), and the callout "Binary Classification (2 Classes)".

## Source URLs and what each confirmed

1. **Wikipedia — "Perceptron"** — https://en.wikipedia.org/wiki/Perceptron
   - Status: FETCHED (via curl; WebFetch timed out from this network).
   - **CONFIRMS the slide's formulation exactly.** The page defines the perceptron as
     f(x) = h(w·x + b) with h the Heaviside step function, and then states verbatim:
     "since w·x + b = (w,b)·(x,1), we can add the bias term b as another weight and add
     a coordinate 1 to each input x" — i.e. exactly the slide's augmented vector
     X = (1, x₁..xₙ) with W = (b, w₁..wₙ) and decision d(X) = WᵀX. It also confirms the
     perceptron is "an algorithm for learning a **binary classifier**" (matches the
     slide's "Binary Classification (2 Classes)" callout) and gives the history:
     Rosenblatt, Cornell Aeronautical Laboratory, Mark I Perceptron (1958–1960).
   - Classic perceptron diagram on the page: **Perceptron.svg** (see download below),
     captioned "The appropriate weights are applied to the inputs, and the resulting
     weighted sum passed to a function that produces the output o."

2. **CS231n — "Neural Networks: Basics 1" (Stanford)** — https://cs231n.github.io/neural-networks-1/
   - Status: FETCHED (via curl).
   - Confirms: "A single neuron can be used to implement a **binary classifier**";
     the neuron model figure shows the weighted-sum + activation computation
     ("biological neuron (left) and a common mathematical model (right)", inputs
     interacting multiplicatively w₀x₀ with synaptic weights) — the same
     inputs→weights→sum→nonlinearity→output structure as the slide's diagram.

3. **Rosenblatt 1958 — primary source (provenance)** — "The Perceptron: A Probabilistic
   Model for Information Storage and Organization in the Brain", *Psychological Review*
   65(6): 386–408. DOI: https://doi.org/10.1037/h0042519
   - Status: canonical citation confirmed via Wikipedia's history section; the paper PDF
     itself was NOT downloadable from this network (CMU mirror 404, DTIC 403,
     UPenn 403, archive.org 503) [?].

4. **Duda & Hart, *Pattern Classification and Scene Analysis* (1973), §2.2 Linear
   Discriminant Functions** — augmented pattern vector x̃ = (1, x₁..xₙ), augmented weight
   vector, g(x) = w̃ᵀx̃.
   - Status: surfaced by the agy research pass as the textbook origin of the exact
     "augmented" terminology and the >0/<0/=0 three-case decision reading; not directly
     fetch-confirmed (book not open-access online) [?].

## Downloaded files (original filenames as downloaded)

1. **Perceptron.svg** — from https://upload.wikimedia.org/wikipedia/commons/3/31/Perceptron.svg
   (Wikipedia/Commons classic perceptron neuron diagram). Labels: inputs 1, 2, …, n;
   weights ×W; summation circle (+); step function block f; output o. This is the
   canonical modern rendering of the exact diagram structure the slide draws
   (inputs + bias 1 → weights → Σ → step → O/P).
2. **neuron_model.jpeg** — from https://cs231n.github.io/assets/nn1/neuron_model.jpeg
   (CS231n fig: "biological neuron (left) and a common mathematical model (right)",
   w₀x₀ notation) — secondary reference for the neuron-model diagram.

## Confirmed / corrected vs the slide

- CONFIRMED standard: the augmented-vector bias absorption (prepend 1 to X, b to W) is
  the standard perceptron/linear-discriminant formulation (Wikipedia states it
  explicitly; Duda & Hart §2.2 is the textbook source).
- CONFIRMED standard: the three-case reading of d(X)=WᵀX (>0 / <0 / =0 with =0 on the
  decision boundary = "undefined" class) is the standard linear-classifier decision
  rule; binary classification (2 classes) is what a single perceptron implements.
- No factual corrections to the slide's math. Notation note: the slide writes the
  decision function as d(X) (discriminant) rather than f(x) — both are standard;
  the slide's d(X) is the pattern-recognition (Duda & Hart) convention.
- Verbatim typo on the slide: "**Ugmented** Vector" (missing 'A' of "Augmented") —
  keep verbatim in recreation per the fidelity law; flagged for the slide owner.

## Open questions

- [?] Rosenblatt 1958 PDF could not be downloaded from this network (all mirrors
  403/404/503); the DOI citation is recorded instead. If the original Figure 1 of the
  paper is ever needed for provenance, fetch from a network with access.
- [?] Whether the lecturer's exact "d(X)" + "Ugmented Vector" spelling traces to one
  specific Egyptian-university pattern-recognition text (Duda & Hart §2.2 is the
  closest standard match; not fetch-confirmed).
