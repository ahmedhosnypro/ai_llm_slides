# SOURCES.md — slide_017 "The Complete ML Classification Process" (annotation state: Trained Model vs Human Experience)

Research date: 2026-10-12. Web-research worker pass (range 011–020).

## What the slide is

Annotation state of the slide_016 pipeline (dependency graph: 17←16; same six-node
chain Training Data → Pre processing → Feature Extraction → Feature Selection →
Classification → Classifier Output). Deltas vs 016: two-color title ("ML" in blue),
a red DASHED divider line under the chain, "Apply Model" now paired with a yellow
starburst "**Based on Trained Model!**", and a second starburst "**Based on Human
Experience**" anchoring the bottom annotation band (the human-decision callouts:
"Based on your inspection / You select the techniques", "Handcrafted features (by
You)", "Your decision / And using which / approach"). Professor-authored diagram; no
external figure reused, so no figure was downloaded (0 files).

## Source URLs and what each confirmed

1. **scikit-learn, "Getting Started — Fitting and predicting: estimator basics"** —
   https://scikit-learn.org/stable/getting_started.html (fetched, verified)
   - Confirms the "Apply Model — Based on Trained Model!" callout's semantics (inference
     applies the ALREADY-TRAINED model, no re-training at application time). Verified
     quote: "**Once the estimator is fitted, it can be used for predicting target values
     of new data. You don't need to re-train the estimator**: clf.predict(X) — predict
     classes of the training data."
   - Also confirms the training-side semantics: "Each estimator can be fitted to some
     data using its fit method" with X (samples matrix, n_samples × n_features) and y
     ("integers for classification").

2. **CS231n, "Image Classification Pipeline"** — https://cs231n.github.io/classification/
   (fetched for slide_016 research; verified there)
   - Confirms the evaluation/apply step: "we evaluate the quality of the classifier by
     asking it to **predict labels for a new set of images that it has never seen
     before**. We will then compare the true labels of these images to the ones
     predicted by the classifier."

3. **Goodfellow, Bengio & Courville, "Deep Learning", Ch. 1** —
   https://www.deeplearningbook.org/contents/intro.html (via web search; see
   slide_015/016 SOURCES.md)
   - Confirms the "Based on Human Experience" starburst's pedagogical meaning: in the
     classical ML pipeline the choices of preprocessing, handcrafted features, and
     approach are human decisions based on expertise — the textbook contrast with deep
     learning's learned representations.
   - [?] deeplearningbook.org unreachable from this network on 2026-10-12; passage
     confirmed via search synthesis, not a live fetch today.

4. Pipeline-stage sources identical to slide_016 (scikit-learn feature selection 1.13;
   CS231n classification pipeline) — the underlying flowchart content is unchanged.

## Confirmed vs corrected

- Confirmed: the slide's dichotomy is the standard one — the pipeline's process steps
  run from a trained model ("Based on Trained Model!"), while the design choices in the
  annotation band are human/expertise-driven ("Based on Human Experience"). This is the
  standard classical-ML characterization (Goodfellow Ch. 1 contrast; sklearn's fixed
  hand-designed estimator+feature workflow).
- No corrections needed: no equations or numbers; all labels verbatim from the frame.
- [?] The dashed red divider is a stylistic delta vs 016 (separates machine-executed
  flow from human-decision annotations) — professor's own device, no external
  provenance to verify.
- Recording artifacts (mouse cursor icon, black letterbox bar) are non-content.

## Downloaded files

None. Annotation-state of the professor's own slide_016 diagram; no site figure reused.
