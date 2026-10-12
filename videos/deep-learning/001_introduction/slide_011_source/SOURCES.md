# SOURCES.md — slide_011 "Feature Extraction" (features may include: CoG, Aspect Ratio, Length/Width, Number of intersections, Moments, Geometrical Features, Colors, Transformations)

Research date: 2026-10-12. Web-research worker pass (range 011–020).

## What the slide is

A professor-authored list of handcrafted feature types used in the ML classification
pipeline (this lecture's "Feature Extraction" step). It is a TEXT LIST — the slide does
not reuse any figure from a paper or website, so no source figure was downloaded (0 files;
this is not a graph/diagram slide).

## Source URLs and what each confirmed

1. **Hu, M.-K. (1962), "Visual Pattern Recognition by Moment Invariants", IRE
   Transactions on Information Theory 8(2):179–187** — the primary source behind the
   "Moments" bullet (moment features / moment invariants for shape description).
   - IEEE Xplore record: https://ieeexplore.ieee.org/document/1057692
   - DOI: https://doi.org/10.1109/TIT.1962.1057692
   - Confirmed: Hu's seven moment invariants, invariant to translation, scale,
     rotation — the canonical "Moments" feature family in pattern recognition.
   - Confirmed via web search (agy) + cross-checked against Wikipedia (below).

2. **Wikipedia, "Image moment"** — https://en.wikipedia.org/wiki/Image_moment
   - Confirmed: centroid ("Center of Gravity location") = {x̄ = M10/M00, ȳ = M01/M00}
     computed from first-order raw moments; raw moment M_pq = ΣΣ x^p y^q I(x,y);
     central moments μ_pq (translation invariant); normalized moments η_pq
     (translation+scale invariant); Hu's seven rotation invariants I1..I7 built from η_pq.
   - Confirms "Center of Gravity location" and "Moments" as standard image features, and
     that Hu 1962 is the primary source (page cites Hu 1962, IRE Trans. IT 8(2):179–187,
     DOI 10.1109/TIT.1962.1057692).

3. **Wikipedia, "Feature engineering"** (redirect target of "Feature extraction") —
   https://en.wikipedia.org/wiki/Feature_extraction
   - Confirms feature extraction/engineering as a standard preprocessing step in ML, and
     the general principle that feature choice is problem-dependent ("Features vary in
     significance"; feature selection is application-driven) — consistent with the slide's
     headline "Features Types are Problem dependent".
   - Note: the article does NOT enumerate the slide's specific feature list; the specific
     list matches the classic textbook treatment (next item).

4. **Gonzalez & Woods, "Digital Image Processing" (4th ed.), Ch. 11 "Feature Extraction"**
   and **Duda, Hart & Stork, "Pattern Classification"** (feature extraction/selection
   chapters) — identified via web search as the classic textbook provenance of exactly
   this family of features (moments, centroid, aspect ratio/eccentricity, Euler number /
   intersections, color and transform-based invariants) with OCR and signature
   verification as the standard example applications. Books are not web-fetchable; cited
   as standard references, not as the source of a copied figure.
   [?] Book chapter page numbers not verified online (paywalled print editions).

5. **CVonline (Univ. of Edinburgh), "Analysis of Binary Images" lecture notes** —
   https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/OWENS/LECT2/node3.html
   - Fetched: confirms the classic context where these shape features are computed
     (binary silhouettes from thresholding; object identification, text interpretation).

## Confirmed vs corrected

- Confirmed: every bullet in the slide's list is a standard, textbook feature type in
  classical pattern recognition / image analysis (no invented or non-standard entries).
- Confirmed: "Feature types are problem dependent" matches the standard ML literature
  (feature selection is application-driven).
- No corrections needed: the slide makes no quantitative claim that could contradict a
  source (no equations, no numbers).
- [?] The slide's headline as transcribed reads "Features Types are is Problem dependent"
  — the doubled verb ("are is") is in the original frame (vision analysis verbatim);
  presumably intended "Feature types are problem dependent". Recreation keeps the
  original text (slide wins for recreation).
- [?] "Transformations" (last real bullet) is ambiguous in the source-free sense: in the
  literature this usually means transform-domain features (Fourier/Hough/wavelet) or
  transformation-invariant features; the slide gives no definition. Confirmed as a
  legitimate feature family name; exact intended meaning unverified.
- [?] "Number of intersections" — standard topological/crossing-count feature in
  character/signature recognition (cf. Euler number / crossing counts in Gonzalez &
  Woods Ch. 11); the slide gives no worked definition. Literature confirmed the feature
  family, not the professor's exact intended definition.

## Downloaded files

None. The slide reuses no external figure; downloaded figures would not be genuinely
relevant (rule: download only the site's own figures when they exist and are genuinely
relevant).
