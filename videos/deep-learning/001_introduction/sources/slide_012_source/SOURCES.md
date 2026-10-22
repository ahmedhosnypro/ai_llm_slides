# SOURCES.md — slide_012 "Feature Invariants" (Rotation / Scaling / Translation / Mirroring Invariant)

Research date: 2026-10-12. Web-research worker pass (range 011–020).

## What the slide is

A professor-authored list of the standard feature-invariance types a handcrafted feature
may need: Rotation Invariant, Scaling Invariant, Translation invariant, Mirroring
Invariant, with the headline "Features Invariants are is Problem dependent" (verbatim
quirks: doubled verb "are is"; bullet 3 lowercase "invariant"). TEXT LIST slide — no
external figure is reused, so no figure was downloaded (0 files).

## Source URLs and what each confirmed

1. **Hu, M.-K. (1962), "Visual Pattern Recognition by Moment Invariants", IRE Trans.
   Information Theory 8(2):179–187** — primary source for the invariance taxonomy.
   - https://ieeexplore.ieee.org/document/1057692 ; DOI https://doi.org/10.1109/TIT.1962.1057692
   - Confirmed: Hu's moment invariants are the canonical example of features invariant
     to **translation, scale, and rotation** — exactly three of the slide's four bullets.
     "Mirroring" (reflection) behavior is also defined by Hu's set (next item).

2. **Wikipedia, "Image moment"** — https://en.wikipedia.org/wiki/Image_moment (fetched)
   - Confirmed: central moments are translation invariant; normalized central moments
     η_pq add scale invariance; Hu's I1..I7 add rotation invariance.
   - Confirmed the 4th bullet's standard name: "**The first six, I1..I6, are reflection
     symmetric, i.e. they are unchanged if the image is changed to a mirror image. The
     last one, I7, is reflection antisymmetric (changes sign under reflection)**" —
     i.e. "Mirroring Invariant" is standard terminology (reflection/mirror invariance).

3. **Lowe, D. G. (2004), "Distinctive Image Features from Scale-Invariant Keypoints",
   IJCV 60(2):91–110** — the canonical modern example of invariant features (SIFT).
   - Author's own PDF: https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf (fetched, 28 pp.,
     verified by extracting page 1; not saved into this dir — the slide reuses no figure
     from it).
   - Abstract quote (verified): "The features are **invariant to image scale and
     rotation**, and are shown to provide robust matching across a substantial range of
     affine distortion, change in 3D viewpoint, addition of noise, and change in
     illumination."
   - Confirms "Scaling Invariant" + "Rotation Invariant" as the standard pair of
     feature-invariance claims in the vision literature.
   - DOI: https://doi.org/10.1023/B:VISI.0000029664.99615.94

4. **Flusser, J. & Suk, T. (1999 + follow-ups)** — reflection/affine moment invariants
   (via search): reflection-invariant moment sets are an established literature line
   (Wikipedia Image moment cites Flusser 2000 "On the Independence of Rotation Moment
   Invariants", https://library.utia.cas.cz/prace/20000033.pdf). Confirms "Mirroring
   Invariant" as a formal, studied property class, not an ad-hoc term.

## Confirmed vs corrected

- Confirmed: all four listed invariance types (rotation, scaling/translation, mirroring)
  are the standard invariance classes in pattern recognition; the standard taxonomy even
  extends beyond the slide (affine, projective, illumination, viewpoint invariance) —
  the slide is a pedagogical subset, no error.
- Confirmed: the header's claim that which invariances are needed is problem-dependent
  matches the literature (invariances are chosen per application; cf. Hu's set is
  closed under rigid+scale transforms only).
- No corrections needed: the slide makes no quantitative claims.
- [?] Verbatim oddity in original frame: header "Features Invariants are is Problem
  dependent" (doubled verb) and bullet 3 lowercase "invariant" — kept verbatim per the
  fidelity law; intended reading "Feature invariants are problem dependent".

## Downloaded files

None. Text-list slide; no site figure is reused. (SIFT paper PDF was fetched to /tmp only
for verification, not banked — not a figure the slide reuses.)
