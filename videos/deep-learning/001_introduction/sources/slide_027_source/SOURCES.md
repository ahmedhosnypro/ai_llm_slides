# SOURCES.md — slide 027 ("[4] Introduction to Deep Learning and CNN")

Research date: 2026-10-12. Worker: web-research lane, slides 021–030 (reverse run).

## Slide nature

Pure **section-divider / title slide** announcing section [4], "Introduction to Deep
Learning and CNN". No bullets, definitions, equations, numbers, or diagrams — only the
four-line stacked red title inside the red frame (plus a recorded mouse cursor and a
video-player black bar at the bottom, both artifacts). As with slide 021 (section [3]
divider, same precedent), the web-verification obligation is discharged by confirming the
canonical references for the topic the section announces.

## Source URLs

1. **Goodfellow, Bengio & Courville (2016) — *Deep Learning*, Chapter 9 "Convolutional
   Networks"** — http://www.deeplearningbook.org/contents/convnets.html
   - Status: canonical reference for the announced topic, confirmed by web search
     (agy, 2026-10-12). Direct fetch of deeplearningbook.org NOT possible from this
     network (timeouts, same as slide 021's attempt) [? — corroborative only].

2. **LeCun, Bottou, Bengio & Haffner (1998) — "Gradient-based learning applied to
   document recognition", Proceedings of the IEEE 86(11), 2278–2324**
   - Canonical PDF: http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf
   - Status: paper's identity/citation confirmed by web search (agy, 2026-10-12). Direct
     fetch attempts from this network failed: yann.lecun.com silent, NYU mirror
     (cs.nyu.edu/~yann/etc/lecun-98.pdf) HTTP 404, IEEE Xplore bot-walled (HTTP 202)
     [? — the paper is universally cited; fetch-blocked, not fetch-refuted].

3. **d2l.ai — §7.6 "Convolutional Neural Networks (LeNet)"**
   - URL: https://d2l.ai/chapter_convolutional-neural-networks/lenet.html
   - Status: FETCHED and CONFIRMED (2026-10-12, 142 KB HTML) — accessible canonical
     treatment of the CNN topic this section opens.

4. **UvA Deep Learning Course — Lecture 4 "Convolutional Neural Networks"
   (Efstratios Gavves)** — https://uvadlc.github.io/lectures/nov2019/lecture4.pdf
   - FETCHED and CONFIRMED earlier this run (see slide 028 SOURCES.md; PDF banked at
     `../slide_028_source/lecture4.pdf`). Slide 028 — this section's first content slide —
     explicitly attributes the following slides to this deck. Its lecture-overview page
     ("What are the Convolutional Neural Networks? / Differences from standard Neural
     Networks / Why are they important in Computer Vision? / How to train a Convolutional
     Neural Network?") is the topic outline the section actually delivers.

## Downloaded files

None. Title slide with no figures; nothing from the sources is reused on this slide
(consistent with the slide-021 precedent). The UvA deck evidence for the section is
banked once, at `../slide_028_source/lecture4.pdf`.

## Confirmed / corrected vs the slide

- Nothing to correct: the slide carries no factual claims beyond the section title.
- Topic match CONFIRMED: "Introduction to Deep Learning and CNN" matches the standard
  curriculum topic confirmed at Goodfellow ch. 9, d2l §7, LeCun et al. 1998, and the
  credited UvA Lecture 4.
- Observational note (not a correction): the section number "[4]" coincides with the UvA
  deck's "Lecture 4: Convolutional Neural Networks" — consistent with the deck being the
  credited source of the section's content (the DSAI lecturer adopted the section number
  into the section title). Section numbering continuity: slide 021 opened section [3]
  ("Quick revision of Neural Network (NN)"), this opens section [4].
- Fidelity note: mouse cursor and bottom black bar are recording/video artifacts, not
  slide content.

## Open questions

- [?] Fetch-blocked canonicals above (deeplearningbook.org, LeCun 1998 PDF) — recorded,
  non-blocking; the accessible canonicals (d2l, UvA PDF) carry the confirmations.
