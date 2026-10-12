# SOURCES.md — slide_016 "The Complete ML Classification Process" (pipeline flowchart)

Research date: 2026-10-12. Web-research worker pass (range 011–020).

## What the slide is

Professor-drawn pipeline diagram: Training Data (ellipse) → Pre processing → Feature
Extraction → Feature Selection → Classification → Classifier Output, with four gray
callouts: "Based on your inspection You select the techniques" (under Pre processing),
"Handcrafted features (by You)" (under Feature Extraction), "Your decision And using
which approach" (under Feature Selection), "Apply Model" (under Classification).
The diagram is the professor's own composition — no external figure is copied, so no
figure was downloaded (0 files).

## Source URLs and what each confirmed

1. **scikit-learn, "Feature selection" user guide (1.13)** —
   https://scikit-learn.org/stable/modules/feature_selection.html (fetched, verified)
   - Verified quote: "The classes in the sklearn.feature_selection module can be used
     for **feature selection/dimensionality reduction** on sample sets, either to
     improve estimators' accuracy scores or to boost their performance on very
     high-dimensional datasets."
   - Confirms "Feature Selection" as a standard, distinct ML pipeline stage following
     feature extraction.

2. **CS231n (Stanford), "Image Classification Pipeline" notes** —
   https://cs231n.github.io/classification/ (fetched, verified)
   - Verified quote — the canonical formalization of the slide's flow: "Our complete
     pipeline can be formalized as follows: Input: Our input consists of a set of N
     images, each labeled with one of K different classes. We refer to this data as the
     **training set**. Learning: Our task is to use the training set to learn what
     every one of the classes looks like. We refer to this step as **training a
     classifier**, or **learning a model**. Evaluation: In the end, we evaluate the
     quality of the classifier by asking it to predict labels for a new set of images
     that it has never seen before. We will then compare the true labels of these
     images to the ones predicted by the classifier."
   - Also confirms the preprocessing stage: "Preprocess your data: Normalize the
     features in your data... to have zero mean and unit variance."
   - Confirms the slide's chain: Training Data → (Pre processing → Feature Extraction →
     Feature Selection) → Classification → Classifier Output, with output compared to
     true labels.

3. **Goodfellow, Bengio & Courville, "Deep Learning", Ch. 1** —
   https://www.deeplearningbook.org/contents/intro.html
   - Confirms (via web search; see also slide_015's SOURCES.md) the exact pedagogical
     point the slide's callouts encode: traditional/classical ML pipelines depend on
     **human-specified ("handcrafted") representations/features** and human choices of
     technique — which deep learning replaces with learned representations.
   - [?] deeplearningbook.org unreachable from this network on 2026-10-12 (see
     slide_014/015 SOURCES.md); quote not re-verified against the live page today.

4. The feature types listed in the "Feature Extraction" stage are the ones confirmed in
   slide_011's research (Hu 1962 moments, centroid, aspect ratio, etc. — see
   slide_011_source/SOURCES.md).

## Confirmed vs corrected

- Confirmed: every stage in the slide's chain is a standard, named ML pipeline stage
  (training data, preprocessing, feature extraction, feature selection, classification,
  output), in the standard order.
- Confirmed: the slide's callouts (human inspects data, chooses techniques; features are
  handcrafted; human picks approach; then apply model) correctly characterize the
  CLASSICAL ML workflow — this is the textbook contrast that motivates the lecture's
  next section (deep learning learns features automatically; Goodfellow Ch. 1).
- No corrections needed: no equations or numbers.
- [?] Verbatim quirks kept for recreation: "Pre processing" (space), "Based on your
  inspection You select the techniques", "Handcrafted features (by You)", "Your decision
  And using which approach", "Apply Model" — capitalization is the professor's.
- Recording artifacts (mouse cursor between boxes; gray top/bottom player strips) are
  non-content, already marked in the analysis.

## Downloaded files

None. Professor-authored diagram; no site figure is reused by the slide.
