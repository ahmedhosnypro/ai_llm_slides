# SOURCES.md — slide_013 "Classification — Examples of Commonly used classifiers:"

Research date: 2026-10-12. Web-research worker pass (range 011–020).

## What the slide is

Title banner "Classification" (white on dark red) + a blue-outlined content box listing
six "commonly used classifiers": Linear Regression, Logistic Regression, Neural Network,
Support Vector Machine, Hidden Markov Model, Decision Trees. TEXT LIST slide — no
external figure reused, so no figure was downloaded (0 files).

## Source URLs and what each confirmed

1. **Wikipedia, "Statistical classification"** — https://en.wikipedia.org/wiki/Statistical_classification (fetched)
   - The "Algorithms" section: "Since no single form of classification is appropriate
     for all data sets, a large toolkit of classification algorithms has been developed.
     The most commonly used include: Artificial neural networks, ..., Logistic
     regression, Naive Bayes classifier, Perceptron, ..., Support vector machine, ..."
   - Confirms: Neural Network, Logistic Regression, and Support Vector Machine are in
     the canonical "most commonly used" classifier list.
   - Notable: this list does NOT include "Linear regression" — consistent with the
     textbook view that plain linear regression is a regression algorithm, not a
     classifier (see "Confirmed vs corrected").
   - Decision trees and HMMs are also absent from that particular Wikipedia sentence,
     but both are standard classifiers per the dedicated sources below.

2. **scikit-learn, "Decision Trees" user guide** — https://scikit-learn.org/stable/modules/tree.html (fetched)
   - Verified quote: "Decision Trees (DTs) are a non-parametric supervised learning
     method used for **classification and regression**."
   - Confirms Decision Trees as a standard classifier family.

3. **Cortes, C. & Vapnik, V. (1995), "Support-Vector Networks", Machine Learning
   20(3):273–297** — canonical SVM paper.
   - https://link.springer.com/article/10.1007/BF00994018 ; DOI https://doi.org/10.1007/BF00994018

4. **Rabiner, L. R. (1989), "A tutorial on hidden Markov models and selected
   applications in speech recognition", Proceedings of the IEEE 77(2):257–286** —
   canonical HMM reference; HMMs are the classic probabilistic sequence classifier.
   - https://ieeexplore.ieee.org/document/18626 ; DOI https://doi.org/10.1109/5.18626

5. Logistic regression / neural networks as classifiers — standard; covered by the
   Wikipedia list above and every ML textbook (Hastie/Tibshirani/Friedman ESL;
   Goodfellow Deep Learning Ch. 5–6 for NNs).

## Confirmed vs corrected

- Confirmed: five of the six bullets (Logistic Regression, Neural Network, SVM, HMM,
  Decision Trees) are standard, textbook classifier families.
- CORRECTED (for understanding; slide still wins for recreation): **"Linear Regression"
  is technically a regression algorithm, not a classifier** — it models a continuous
  target; classification via a regression model requires thresholding (and that
  thresholded construction is essentially logistic regression). Wikipedia's "most
  commonly used classifiers" list omits it. The slide's bullet stays verbatim for
  recreation; this note records the technicality.
- Note: "Logistic Regression" is named "regression" but IS a classifier (standard
  textbook point; Wikipedia's classifier list includes it) — no correction needed.
- No quantitative claims on the slide; verbatim quirks preserved: double space in
  "Logistic  Regression".
- [?] Bottom-left gray toast "[?]ument has just been saved..." is an OS screen-recording
  artifact (not slide content); bottom-right black box is a webcam/off-state overlay —
  both are video artifacts, recreation may omit per the recreation brief.

## Downloaded files

None. Text-list slide; no site figure reused.
