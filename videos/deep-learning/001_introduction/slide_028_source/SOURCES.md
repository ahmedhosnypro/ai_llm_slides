# SOURCES.md — slide 028 ("Introduction to Convolutional Neural Network (CNN)")

Research date: 2026-10-12. Worker: web-research lane, slides 021–030 (reverse run).

## Slide nature

Section-title slide opening the CNN section. Content: the three-line title plus a small
italic attribution in the bottom-left corner — "Some of Slides are picked from /
UVA Deep Learning Course   EFSTRATIOS GAVVES". The attribution line is the slide's only
factual claim, and it is the key to the whole section's provenance.

## Source URLs

1. **UvA Deep Learning Course (uvadlc.github.io) — "Deep Learning @ UvA",
   Lecture 4: Convolutional Neural Networks, Efstratios Gavves**
   - Course site: https://uvadlc.github.io/ (FETCHED and CONFIRMED 2026-10-12, 39 KB HTML;
     lecture archive pages lectures-nov2016 … lectures-nov2022 exist).
   - Lecture PDF (2019 series): https://uvadlc.github.io/lectures/nov2019/lecture4.pdf
     (FETCHED and CONFIRMED 2026-10-12; 22.6 MB PDF, pdftotext-extracted).
   - Title page verbatim: "Lecture 4: Convolutional Neural Networks / Deep Learning @ UvA /
     **UVA DEEP LEARNING COURSE – EFSTRATIOS GAVVES**" — exactly matching the slide's
     attribution. Gavves's UvA contact (egavves@uva.nl) appears on the nov2020 course page,
     confirming he is the course lecturer.
   - **Provenance of this section CONFIRMED**: the same PDF contains, on its p.15, the
     exact bullet set of slide 029 ("Images are 2-D / 3-D if you also count the extra
     channels / RGB, hyperspectral, etc. / What does a 2-D input really mean? /
     Neighboring variables are locally correlated") and, on its p.16, the exact Sobel
     demo of slide 030 ("Example filter when K=1 — e.g. Sobel 2-D filter" with kernel
     −1 0 1 / −2 0 2 / −1 0 1). The DSAI 308 lecturer's "picked from" note is accurate:
     the following slides are lifted from this Gavves lecture (2019 nov series; the same
     CNN lecture is Lecture 4 in nov2020 and Lecture 5 in nov2021).

2. **Course site archive pages** (cross-checks): https://uvadlc.github.io/lectures-nov2019.html
   (lists "Lecture 4 Convolutional Neural Networks" → lectures/nov2019/lecture4.pdf);
   https://uvadlc.github.io/lectures-nov2020.html ("Lecture 4: Convolutional Neural
   Networks"; contact egavves@uva.nl); https://uvadlc.github.io/lectures-nov2021.html
   ("Lecture 5: Convolutional Neural Networks", November 18, 2021).

## Downloaded files

Downloaded into `slide_028_source/` (site's original filename preserved):

1. `lecture4.pdf` (22,609,966 bytes, PDF 1.3) — https://uvadlc.github.io/lectures/nov2019/lecture4.pdf
   - The credited UvA Deep Learning Course lecture "Lecture 4: Convolutional Neural
     Networks" (Deep Learning @ UvA, Efstratios Gavves) — the deck the attribution refers
     to, and the origin deck for slides 029–030 (verified verbatim, see above). Kept here
     as the provenance evidence for the whole CNN section.

## Confirmed / corrected vs the slide

- Attribution CONFIRMED verbatim: "UVA Deep Learning Course" + "EFSTRATIOS GAVVES" is a
  real course and lecturer, and the "picked from" claim is verifiably true for slides
  029/030 (exact text match in lecture4.pdf pp. 15–16).
- No corrections. The slide is a title slide; title text matches standard CNN section
  naming ("Introduction to Convolutional Neural Network (CNN)").
- Cross-slide note recorded for 029/030 owners (both owned by this lane): UvA original
  p.15 reads "**3-D** if you also count the extra channels" where the DSAI slide reads
  "**k-D** if you also count the extra channels" — the DSAI lecturer's generalization.
  Per fidelity law the DSAI slide's wording wins for recreation; the UvA wording is the
  upstream original. UvA p.16 titles the Sobel demo "Example filter when K=1" where the
  DSAI slide titles it "Apply filter on 2-D  gray image  (K=1 Channel)" — same demo,
  lecturer's own title; DSAI wording wins for recreation.
- Fidelity note: mouse cursor near the attribution and the bottom black bar are
  screen-recording/video artifacts, not slide content.

## Open questions

- [?] Which exact year's UvA deck the DSAI lecturer copied from (2019 nov / 2020 nov /
  2021 nov all carry the same Gavves CNN lecture; the 2019 lecture4.pdf content matches
  verbatim, which is sufficient for provenance). Does not affect recreation.
- [?] Whether additional slides later in this DSAI deck (022–027, 031+) also come from
  lecture4.pdf — to be recorded per-slide in their own SOURCES.md files.
