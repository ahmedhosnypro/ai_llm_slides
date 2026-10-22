# SOURCES.md — slide_019 "The Complete Deep Learning Model" (base-diagram state, no starburst)

Research date: 2026-10-12. Web-research worker pass (reverse order 020→012).

## What the slide is

Course-authored ML pipeline diagram — the SAME base diagram as slide_020 in an earlier
annotation state: full pipeline (Training Data ellipse → Input Samples → Pre processing
→ Feature Extraction → Feature Selection → Classification → Predicted Labels → vertical
"PREDICTION ERROR (LOSS FUNCTION)" ← Samples Labels; dashed red container around the four
middle stages; four green dashed feedback arrows; pale-green annotation box
"Update Model Parameters in order to MINIMIZE error / (difference between model
prediction and Actual labels" (unbalanced paren verbatim)) but WITHOUT slide 020's
yellow "The BIG challenge" starburst and thick red block arrows. A small pencil (✎) icon
sits on the "Pre processing" box. Founder dep graph: 19←9 (annotation-state family of
one base diagram). Kept frame frame_00904 (736–903 s) vs slide 020's frame_00920
(913–919 s) — the professor drew the starburst/arrow emphasis minutes later.

NOTE ON METHOD: agy websearch DOWN all session (5 failures: CLI misfire, TLS timeout,
2 hangs, MCP HTTP 403 location-eligibility). Fallback per protocol: direct canonical
fetches (curl/WebFetch), done this session for the same diagram (slide_020 research).

## Source URLs and what each confirmed

1. **Course provenance — YouTube playlist "Deep Learning DSAI 308 Fall 2024 - Zewail",
   channel Dr. Khaled Mostafa Elsayed**
   https://www.youtube.com/playlist?list=PL5JZLxl_tFCcmulUU7suv9DkAFrOTm34w
   - Playlist title fetched live (curl 2026-10-12). The diagram is COURSE-AUTHORED
     (professor's own slide; no external figure cited). 0 files downloaded — no site
     figure exists for a course-authored diagram.

2. **d2l.ai — Dive into Deep Learning, ch. 3 "Linear Regression"**
   https://d2l.ai/chapter_linear-regression/linear-regression.html
   - CONFIRMED (fetched 2026-10-12): "Loss functions quantify the distance between the
     real and predicted values of the target."; "we seek parameters (w*, b*) that
     minimize the total loss across all training examples"; gradient-descent update rule.
   - Maps to: Prediction Error (Loss Function) box comparing Predicted vs Samples
     Labels; green feedback annotation "Update Model Parameters ... MINIMIZE error".

3. **CS231n — "Optimization: Stochastic Gradient Descent"**
   https://cs231n.github.io/optimization-1/
   - CONFIRMED (fetched 2026-10-12): "the loss function lets us quantify the quality of
     any particular set of weights W. The goal of optimization is to find W that
     minimizes the loss function."
   - Maps to: the feedback loop into the four learnable stages (the dashed container).

4. **Wikipedia, "Supervised learning"**
   https://en.wikipedia.org/wiki/Supervised_learning
   - CONFIRMED (fetched 2026-10-12): labeled training data ("the training data is
     labeled with the expected answers"); feature selection as dimensionality reduction
     discarding irrelevant features (the Feature Selection box).

## Confirmations vs the slide

- Content = standard supervised-ML loop; every node label consistent with the canonical
  sources above. No corrections. Original frame is ground truth for recreation (this
  state's distinguishing features: NO starburst, NO red block arrows, pencil ✎ on
  Pre processing, green annotation box present).
- "Samples Labels" / "Pre processing" verbatim as printed; unbalanced opening
  parenthesis in the green box verbatim.

## Open questions

- [?] External origin of the diagram (if any): none cited on-slide; course-authored is
  the working conclusion (agy search down all session). Same [?] as slide_020.
