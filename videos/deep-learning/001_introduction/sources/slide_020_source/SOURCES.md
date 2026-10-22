# SOURCES.md — slide_020 "The Complete Deep Learning Model"

Research date: 2026-10-12. Web-research worker pass (reverse order 020→012).

## What the slide is

Course-authored end-to-end ML/DL pipeline diagram (professor's own drawing, no external
figure): Training Data ellipse → Input Samples → dashed container [Pre processing →
Feature Extraction → Feature Selection → Classification] → Predicted Labels → vertical
"PREDICTION ERROR (LOSS FUNCTION)" box fed also by Samples Labels; green dashed feedback
arrows from the error back into all four processing boxes; green annotation box
"Update Model Parameters in order to MINIMIZE error (difference between model prediction
and Actual labels" (unbalanced paren verbatim); yellow starburst "The BIG challenge"
pointing at the loss box.

NOTE ON METHOD: agy websearch was DOWN this entire session (CLI misfire that tried to
write files outside the namespace — pollution removed; TLS handshake timeout; 4-min hang;
MCP variant HTTP 403 location-eligibility). Per the run protocol (>3 agy failures), the
fallback was used: direct fetch of canonical URLs (curl/WebFetch) below.

## Source URLs and what each confirmed

1. **Course provenance — YouTube playlist "Deep Learning DSAI 308 Fall 2024 - Zewail",
   channel Dr. Khaled Mostafa Elsayed**
   https://www.youtube.com/playlist?list=PL5JZLxl_tFCcmulUU7suv9DkAFrOTm34w
   - Playlist title fetched live (curl 2026-10-12): "Deep Learning DSAI 308 Fall 2024 -
     Zewail". This lecture (001_introduction) is Dr. Khaled's own deck; the diagram is
     COURSE-AUTHORED — no external paper/website figure is cited on the slide, and no
     site figure was downloaded (0 files; the diagram itself is the professor's).

2. **d2l.ai — Dive into Deep Learning, ch. 3 "Linear Regression"**
   https://d2l.ai/chapter_linear-regression/linear-regression.html
   - CONFIRMED the loss-function + feedback framing, verbatim: "Loss functions quantify
     the distance between the real and predicted values of the target."; "we seek
     parameters (w*, b*) that minimize the total loss across all training examples";
     gradient descent update "(w,b) ← (w,b) − (η/|B|) Σ ∂ l(i)(w,b)".
   - Maps to: "Prediction Error (Loss Function)" comparing Predicted Labels vs Samples
     Labels, and the green feedback annotation "Update Model Parameters in order to
     MINIMIZE error". d2l's own pipeline omits the preprocessing/feature stages — the
     4-stage dashed container is the classic handcrafted-ML front end the professor
     draws explicitly (consistent with this lecture's earlier slides, e.g. slide_011's
     feature list).

3. **CS231n — "Optimization: Stochastic Gradient Descent" notes**
   https://cs231n.github.io/optimization-1/
   - CONFIRMED, verbatim: "the loss function lets us quantify the quality of any
     particular set of weights W. The goal of optimization is to find W that minimizes
     the loss function." and "Optimization is the process of finding the set of
     parameters W that minimize the loss function."
   - Maps to: the two opposing arrows INTO the loss box (predicted vs sample labels)
     and the "Update Model Parameters ... MINIMIZE" feedback loop.

4. **Wikipedia, "Supervised learning"**
   https://en.wikipedia.org/wiki/Supervised_learning
   - CONFIRMED pipeline vocabulary: "In supervised learning, the training data is
     labeled with the expected answers" (Samples Labels vs Predicted Labels);
     feature selection "seek[s] to identify the relevant features and discard the
     irrelevant ones ... an instance of the more general strategy of dimensionality
     reduction" (the Feature Selection box).

## Confirmations vs the slide

- The diagram's CONTENT is the standard supervised-ML loop (data → handcrafted features
  → classification → loss → parameter update); every node label is consistent with
  d2l.ai/CS231n/Wikipedia terminology. No correction needed; the original frame remains
  ground truth for recreation (layout/colors/arrows are the professor's own style).
- "Samples Labels" (not "Sample Labels") and "Pre processing" (no hyphen) are as-printed
  verbatim — kept.

## Open questions

- [?] Whether the professor adapted the diagram from a specific external textbook figure
  (none cited on-slide). agy search down this session, so an exact-figure hunt was not
  possible; all canonical fetches above treat it as the standard pipeline. Course-authored
  is the working conclusion (same pattern as sibling SOURCES_MAP §2 "course-authored"
  rows in 001_transformers_part1).
