# SOURCES.md — slide 023 ("Visualization of Single Layer Perceptron")

Research date: 2026-10-12. Worker: web-research lane, slides 021–030.

## Slide content verified

A single layer of m perceptrons for **multi-class classification**: one discriminant per
class — d₁(X) = W₁ᵀX = w₁₁x₁ + ... + w₁ₙxₙ + b₁·1, d₂(X) = W₂ᵀX = ..., dₘ(X) = WₘᵀX = ...
— each computed by its own Σ neuron fed by all inputs x₁..xₙ plus the bias input 1,
passed through a step-function block, and read out as a per-class binary decision:
">0 Class j" / "<0 Not Class j". Weight notation wⱼᵢ (output j, input i) and bias bⱼ.

## Source URLs and what each confirmed

1. **d2l.ai — Dive into Deep Learning, "Softmax Regression" (§4.1, current build)**
   - URL: https://d2l.ai/chapter_linear-classification/softmax-regression.html
   - Status: FETCHED (via curl).
   - **Confirms the "single-layer" architecture**: "Softmax regression is a
     **single-layer neural network**" (**Fig. 4.1.1**) — inputs feeding one fully
     connected layer with one output unit per class, weights gathered as
     o = Wx + b. This is exactly the slide's diagram structure (all inputs → every
     Σ neuron, one per class; weights wⱼᵢ; bias bⱼ), with softmax instead of the
     step function as the output nonlinearity.
   - The chapter's figure file `softmaxreg.svg` downloaded (see below).

2. **scikit-learn — Multiclass and multilabel algorithms (OneVsRestClassifier)**
   - URL: https://scikit-learn.org/stable/modules/multiclass.html
   - Status: FETCHED (via curl).
   - **Confirms the per-class decision reading**: "The one-vs-rest strategy, also known
     as one-vs-all... consists in fitting **one classifier per class**. For each
     classifier, the class is fitted **against all the other classes**." The slide's
     ">0 Class j / <0 Not Class j" is precisely this one-vs-rest reading, one binary
     perceptron decision per class (sign of that class's discriminant).

3. **Wikipedia — "Perceptron"** — https://en.wikipedia.org/wiki/Perceptron
   - Status: FETCHED earlier this run (see slide_022_source/SOURCES.md).
   - Confirms the augmented-vector formulation each d_j uses (X=(1,x₁..xₙ),
     W=(b,w₁..wₙ), WᵀX) and that a single perceptron is a binary classifier — the
     slide's layer is m of them in parallel, one per class.
   - Note: Wikipedia's "Multiclass perceptron" section describes the *structured*
     perceptron (argmax with joint features, Collins 2002) — NOT the slide's
     formulation; the slide uses the classic pattern-recognition one-discriminant-
     per-class machine, confirmed by the one-vs-rest reference above.

4. **Textbook provenance (not fetch-confirmed)** [?]: the one-discriminant-per-class
   linear machine (m discriminants g_j(x) = w_jᵀx̃) traces to the classic
   pattern-recognition literature — Duda & Hart, *Pattern Classification and Scene
   Analysis* (1973), linear-discriminant / multicategory case; Nilsson, *Learning
   Machines* (1965); Haykin's *Neural Networks* uses the exact term "single-layer
   perceptron". These books are not open-access online; the agy research pass
   corroborated the attribution but the search backend 403'd on the final provenance
   query, so it stands as background, marked [?].

## Downloaded files (original filenames as downloaded)

1. **softmaxreg.svg** — from https://d2l.ai/_images/softmaxreg.svg — the d2l.ai site's
   own Fig. 4.1.1 figure ("Softmax regression is a single-layer neural network"):
   inputs → one fully-connected layer → one output per class. The canonical modern
   reference diagram for the slide's single-layer multi-output network (difference:
   softmax vs step activation).

## Confirmed / corrected vs the slide

- CONFIRMED standard: one Σ neuron per class, all inputs fully connected to every
  neuron, bias absorbed via the constant-1 input (same augmentation as slide 022).
- CONFIRMED standard: the per-output ">0 ⇒ Class j, <0 ⇒ Not Class j" decision is the
  one-vs-rest (one-vs-all) multiclass strategy (scikit-learn's canonical description).
- Terminology note: "Single Layer Perceptron" here means ONE layer of m perceptron
  units (no hidden layer) — consistent with Haykin's usage and with d2l's
  "single-layer neural network" statement for softmax regression [? Haykin not
  fetch-confirmed].
- No factual corrections to the slide's math; the equations are the per-class
  generalization of slide 022's discriminant.
- Nuance recorded for understanding (not recreation): with one-vs-rest sign decisions,
  samples can fall in 0 or 2+ classes simultaneously (the "=0/undefined" and overlap
  cases are not resolved by argmax here; classic linear machines use argmax over d_j
  instead — the slide's presentation follows the one-vs-rest convention).

## Open questions

- [?] Exact textbook the lecturer's d_j(X) = W_jᵀX one-per-class notation comes from
  (Duda & Hart is the closest standard match; not fetch-confirmed — book not open
  access; the dedicated agy provenance search stalled/403'd).
