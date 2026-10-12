# SOURCES.md — slide_018 "The Complete Deep Learning Model" (End-To-End variant)

Research date: 2026-10-12. Web-research worker pass (reverse order 020→012).

## What the slide is

Course-authored diagram — the deep-learning ("End-To-End model") variant of the same
base pipeline as slides 019/020: Training Data ellipse → dashed red container
[Pre processing → Feature Extraction → Feature Selection → Classification] →
Classifier Output; a dashed navy double-headed arrow arcs from Training Data all the
way to Classifier Output under an "End-To-End model" chip (the deep model consumes raw
data and produces the output directly); a red double-headed arrow labeled
"Deeeeeeep Model" spans the pipeline; gray callouts annotate the stages:
"Based on Training Data (Model Choice)", "Model choose Best feature for given training
data", "Model Reduces the features (if required)", "Classify using Trained Model",
starburst "Based on Trained Model"; bottom statement box (bold red):
"No Interaction from Human" / "It is Based on Training Data". Founder dep graph:
18←9 (annotation-state family). This slide's claim = deep learning learns the feature
pipeline from data instead of human hand-engineering.

NOTE ON METHOD: agy websearch DOWN all session (5 failures). Fallback per protocol:
direct canonical fetches (curl), 2026-10-12. 0 figures downloaded — course-authored
diagram, no external site figure exists.

## Source URLs and what each confirmed

1. **Course provenance — YouTube playlist "Deep Learning DSAI 308 Fall 2024 - Zewail",
   channel Dr. Khaled Mostafa Elsayed**
   https://www.youtube.com/playlist?list=PL5JZLxl_tFCcmulUU7suv9DkAFrOTm34w
   - Playlist title fetched live (curl 2026-10-12); the diagram is the instructor's own.

2. **d2l.ai — Dive into Deep Learning, ch. 1 "Introduction"**
   https://d2l.ai/chapter_introduction/index.html
   - CONFIRMED "End-To-End model", verbatim: "Arguably the most significant commonality
     in deep learning methods is end-to-end training. That is, rather than assembling a
     system based on components that are individually tuned, one builds the system and
     then tunes their performance jointly."
   - CONFIRMED the handcrafted-vs-learned contrast, verbatim: "in computer vision
     scientists used to separate the process of feature engineering from the process of
     building machine learning models. The Canny edge detector (1987) and Lowe's SIFT
     feature extractor (Lowe, 2004) reigned supreme ... manually-engineered [features]".
   - CONFIRMED "No Interaction from Human", verbatim: "deep learning replaces not only
     the shallow models at the end of traditional machine learning pipelines, but also
     the labor-intensive process of feature engineering." and "representational learning
     focuses on how to automatically find the appropriate way to represent data."
   - Maps to: the callouts "Model choose Best feature for given training data" (learned
     feature selection), "Model Reduces the features (if required)" (dimensionality
     reduction learned), "No Interaction from Human".

3. **Wikipedia, "Feature engineering"**
   https://en.wikipedia.org/wiki/Feature_engineering
   - CONFIRMED that classic feature engineering "is a preprocessing step which
     transforms raw data into a more effective set of inputs" (the human-driven front
     end the deep model replaces); "Automation of feature engineering is a research
     topic that dates back to the 1990s" (the automation the slide attributes to the
     deep model).

4. **d2l.ai ch. 3 + CS231n optimization-1** (fetched for slide_020 this session)
   https://d2l.ai/chapter_linear-regression/linear-regression.html
   https://cs231n.github.io/optimization-1/
   - Loss/parameter-update loop background for the family (details in
     ../slide_020_source/SOURCES.md); this slide shows the forward (inference) half only.

## Confirmations vs the slide

- Every claim on the slide matches the canonical literature: end-to-end training
  (d2l ch.1), learned vs hand-engineered features (d2l ch.1; Wikipedia), inference
  stages labeled per the same pipeline as 019/020. No corrections.
- Typos are AS-PRINTED verbatim and kept: "Deeeeeeep Model" (7 e's), "Model choose
  Best" (singular verb), "End-To-End model" (lowercase m).
- The mouse cursor on the "Deeeeeeep Model" label is a screen-recording artifact, not
  slide content (recreation brief already excludes it).

## Open questions

- [?] External origin of the diagram (if any): none cited on-slide; course-authored
  working conclusion (agy search down all session). Same [?] as slides 019/020.
