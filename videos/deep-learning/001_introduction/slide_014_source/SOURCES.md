# SOURCES.md — slide_014 "How Training Takes Place to learn the model ?" (training loop flowchart)

Research date: 2026-10-12. Web-research worker pass (range 011–020).

## What the slide is

Professor-drawn training-loop flowchart: Training Sample → Classification Model (with
Model Parameters) → Predicted Class (Label) → Error ← True Label of the Sample, with the
takeaway "Try to update model parameters (Iteratively) to minimize error (Loss Function)".
This is the standard supervised-learning training loop, drawn by the professor — no
external figure is copied, so no figure was downloaded (0 files).

## Source URLs and what each confirmed

1. **CS231n (Stanford), "Optimization: Minimizing Loss" notes** —
   https://cs231n.github.io/optimization-1/ (fetched, verified)
   - Confirms the slide's takeaway sentence almost verbatim as the standard description
     of training: "**The loss function lets us quantify the quality of any particular set
     of weights W. The goal of optimization is to find W that minimizes the loss
     function.**"
   - Confirms the iterative-update mechanism the slide describes: the "Random Local
     Search" strategy code applies an update step `W + δW` and accepts it "if the loss
     at the perturbed W + δW is lower, we will perform an update", leading to gradient
     descent (iterative parameter updates in the direction that reduces loss).
   - Confirms the pipeline structure (score/parameterized function → loss → update):
     "two key components... A (parameterized) score function mapping the raw image
     pixels to class scores... [and] a loss function".

2. **Mitchell, T., "Machine Learning", McGraw Hill 1997** — book page:
   http://www.cs.cmu.edu/~tom/mlbook.html (fetched, verified)
   - Confirms the classic framing of learning as automatic improvement through
     experience: "Machine Learning is the study of computer algorithms that improve
     automatically through experience." (The lecture's training concept descends from
     this textbook tradition.)
   - The site also provides free PDF downloads of the book and extra chapters.

3. **Goodfellow, Bengio & Courville, "Deep Learning", MIT Press 2016, Ch. 5 "Machine
   Learning Basics"** — https://www.deeplearningbook.org/contents/ml.html
   - Standard reference that formalizes exactly this loop (estimate parameters by
     minimizing a cost/error measure on training data, typically via iterative
     gradient-based updates). Identified as the canonical reference by web search.
   - [?] Site unreachable from this network on 2026-10-12 (curl/WebFetch both timed out,
     3 attempts) — URL recorded for later verification; content claims here are NOT
     independently re-verified against the page text today.

## Confirmed vs corrected

- Confirmed: the slide's central claim — training = iteratively updating model
  parameters to minimize the error/loss function — is the textbook-standard description
  of supervised learning (CS231n quote above).
- Confirmed: the flowchart structure (input sample → model with parameters → prediction;
  error computed from prediction vs true label) is the standard training-loop diagram
  (prediction compared against ground-truth label to produce the training error/loss).
- No corrections needed: no equations or numbers on the slide.
- [?] Terminology nuance (understanding, not recreation): "error" vs "loss function" are
  used near-interchangeably on the slide; in the literature "loss" is per-example and
  "error/cost" often aggregates over the training set (Goodfellow Ch. 5 convention).
  The slide's single takeaway sentence merges the two ("error (Loss Function)") — kept
  verbatim.
- Recording artifacts (gray cursor icon) are video-recording overlays, not content.

## Downloaded files

None. Professor-authored flowchart; no site figure is reused by the slide.
