# SOURCES.md — slide 001 "Ridge Regression, Gradient Descent, And Perceptron"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19); method = agy web
search (MCP, `agy_web_search`) for discovery + live fetch with `curl -sL` (WebFetch fallback
returned timeouts on this host, so curl was the fetch tool of record) + verification against
the fetched page text. Frame facts come from `analysis/slide_001_final.json`; vision transcripts
banked separately. No vision calls were made by this worker.

## Slide identity

- File: `unique_slides/slide_001.jpg` (960x540, 1px = 1pt), badge numeral **1**.
- Curated numbering: founder-curated 2026-10-19; slides 001-009 are all numbered by the
  founder. This is a title slide, so no pre-curation remap applies (the pre-curation index was
  intentionally removed by the founder — pre-curation state is unrecoverable; see deck
  AGENTS.md "Deck-specific notes").
- `analysis/slide_001_final.json` verdict PASS_WITH_FIXES; recreatability 9/10.
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.

## Primary source(s)

All three URLs were Fetched live in this work window (HTTP 200, JSON bodies recorded verbatim
below). They are the Zewail City public CMS API that backs the browsable pages
`https://www.zewailcity.edu.eg/course-catalog` and
`https://www.zewailcity.edu.eg/ar/about/member/53` (both pages render client-side; the CMS API
endpoint is the data actually served and was therefore fetched as the source of record).

1. **https://zcadminpanel.zewailcity.edu.eg/api/courses/264** — official Zewail City course
   catalog entry for CSAI 253. Fetched live, HTTP 200. Verbatim record:
   ```json
   {"data":{"id":264,"attributes":{"title":"Machine Learning","description":"Machine learning
   is one of the most powerful tools that is used for data-driven decision making. Topics covered
   include: regression, classification, clustering, prediction, learning reinforcement, and
   dimensionality reduction. Selected applications in data mining, pattern recognition, and text
   and language processing.","code":"CSAI 253","credits":3,"lectureHours":2,"practiceHours":3,
   "prerequisites":"$CSAI 201|257$, $MATH 105|490$","corequisites":"",
   "academicYear":"2024-2025"}},"meta":{}}
   ```
2. **https://zcadminpanel.zewailcity.edu.eg/api/members/53** — official faculty record, Dr.
   Khaled Mostafa El Sayed. Fetched live, HTTP 200. Verbatim key fields:
   `"name":"Dr. Khaled Mostafa El Sayed"`, `"email":"kmelsayed@zewailcity.edu.eg"`,
   `"rank":"Professor, Computational Sciences and Artificial Intelligence School"`,
   `"administrativePositionsTitle":"Director of Data Science Program"`,
   `"phdYear":"1998"`, `"phdUniversity":"Cairo University"`, `"homeInstitute":"Zewail City"`,
   `"officeLocation":"Academic Building"`, `"roomNumber":"S018"`.
3. **https://zcadminpanel.zewailcity.edu.eg/api/members/29** — official faculty record, Dr.
   Mohamed Maher Ata. Fetched live, HTTP 200. Verbatim key fields:
   `"name":"Dr. Mohamed Maher Ata"`, `"email":"momaher@zewailcity.edu.eg"`,
   `"rank":"Associate Professor, Computational Sciences and Artificial Intelligence School"`,
   `"biography":"Mohamed Maher Ata is an Associate professor at School of Computational Sciences
   and Artificial intelligence (CSAI), Zewail city of science and Technology, Egypt. ... His
   research area of interest was utilized in the field of signal processing, image processing,
   Multimedia, machine and deep learning, video processing, and computer vision."`.

Sibling discovery note: the first agy search surfaced `zewailcity.edu.eg` results whose links
were Google grounding redirects; those were resolved with `curl -D -` (302 →
`/ar/about/member/53` and `/about-.../undergraduate-studies/program/40`) to reach the live
site, and the CMS API behind them was then fetched directly.

## Figures used by this slide

- Downloaded `ZC_logo_41f290fbd1.png` — the official Zewail City logo asset hosted at
  `https://zcadminpanel.zewailcity.edu.eg/uploads/ZC_logo_41f290fbd1.png` (referenced as
  `og:image` on every `zewailcity.edu.eg` page), saved as-served (never renamed):
  1312 bytes, PNG 103x78, 8-bit colormap. SHA-256
  `30a890d6dce313d5f5eb4c3232ff072f974fb1b53b47f2bb74006ecf9b466da8`.
  Re-fetch byte-identity result: refetched once and byte-identical (same SHA-256, 1312 bytes).
- Downloaded `mini_logo_e57c2a3adc.png` — the second hosted logo asset
  (`/uploads/mini_logo_e57c2a3adc.png`, the Arabic-locale site logo), 36534 bytes, PNG
  1748x1384. SHA-256
  `345ee80ef9b6d6226a29ea98401ae011c9d996bf19bb91a0d2c1d88ec6bd61f3`.
  Refetched once, byte-identical.
- **Palette forensics (why these are NOT the slide's badge):** the slide's logo badge
  (`slide_001_final.json` visual_elements / recreation_brief step 13) is a *solid teal `#008080`
  left panel with white "ZEWAIL CITY"* and a white right panel carrying the Arabic text above
  black "University of Science and Technology". Neither hosted original matches: the official
  `ZC_logo` is white-dominant with cyan `#00B5D1` accents (no solid teal panel), and the
  Arabic `mini_logo` is dark green `#47704C`-dominant. The slide's badge is therefore a
  **course-authored composite/redraw of the institutional mark**, not the official asset — no
  "fix" toward the official logo is licensed; the frame stays ground truth for pixels.
- No paper/tutorial figure exists for a title slide — nothing else was hosted by these sources.

## What the source(s) CONFIRM

- **"CSAI 253 - Spring 2024"`: the code CSAI 253 is a real Zewail City course — title
  "Machine Learning", 3 credits (2 lecture + 3 practice hours), prerequisites CSAI 201 and
  MATH 105, academic year "2024-2025" (which covers the Spring 2024 semester printed on the
  slide). CONFIRMED.
- **Deck topic vs. catalog scope:** the catalog description names "regression, classification"
  among the covered topics — consistent with this lecture's title "Ridge Regression, Gradient
  Descent, And Perceptron" (ridge = regression; perceptron = classification). CONFIRMED at
  topic level; the title itself is course-authored wording, not a catalog string.
- **"Dr. Khaled Mostafa ElSayed" + "kmelsayed@zewailcity.edu.eg":** exact email match in the
  official faculty record; rank "Professor, Computational Sciences and Artificial Intelligence
  School", administrative position "Director of Data Science Program", PhD 1998 Cairo
  University, home institute "Zewail City". CONFIRMED.
- **"Dr. Mohamed Maher Ata" + "momaher@zewailcity.edu.eg":** exact email match; rank
  "Associate Professor, Computational Sciences and Artificial Intelligence School"; biography
  lists machine/deep learning and computer vision research — consistent with him instructing
  this CSAI course. CONFIRMED.
- **Institution identity:** the slide's logo text "ZEWAIL CITY / جامعة العلوم والتكنولوجيا /
  University of Science and Technology" is the official naming of Zewail City of Science,
  Technology and Innovation; the CMS `footer` record gives the canonical address "Ahmed Zewail
  Road, October Gardens, 6th of October City, Giza, Egypt" (fetched live, HTTP 200,
  `https://zcadminpanel.zewailcity.edu.eg/api/footer/3`). CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The lecture title itself ("Ridge Regression, Gradient Descent, And Perceptron"), the
  "Prepared By" / "Instructors:" headings and their text styling, and the arrangement of the
  title/subtitle/attribution blocks are all course-authored. No hosted source dictates them.
- **The Zewail City logo badge on the slide is a course-authored redraw** (solid teal
  `#008080` panel; Arabic strip above "University of Science and Technology"). The official
  assets are cyan-on-white and green (see Palette forensics above). The frame's version is what
  gets recreated (brief step 13 stands); the downloaded originals are reference-grade for the
  institutional identity only.
- The slide-number badge, colors (#C00000 title, #0000FF body, #FFFF00 badge) and the gray
  border are deck chrome per the deck's house template — no web counterpart exists.
- Spelling variance recorded, not corrected: the slide prints "ElSayed" while the official
  faculty record prints "El Sayed". The frame's spelling is transcribed frame text and stays
  as-is for recreation (corrections patch annotations only).

## [?] Uncertain items

- Whether the slide's logo badge is a specific third-party cut (e.g. an older official logo
  revision) rather than a course redraw — resolution path: ask the deck owner for the original
  asset if a pixel-perfect logo is wanted. Currently judged a course-authored composite on
  palette evidence.
- `slide_001_final.json`'s own uncertain items (exact logo artwork, exact two-line title wrap
  point, exact point sizes) are frame-level facts with no web resolution path — they remain
  open by design and are not web-resolvable.

## Corrections

- Proposed patch (DOCUMENT ONLY — not applied by this worker; the orchestrator applies
  patches): none required. No dimension, attribute, or provenance guess in
  `analysis/slide_001_final.json` is contradicted by these sources. The single external-facing
  observation — official name spelled "El Sayed" vs the slide's "ElSayed" — is frame text and
  therefore NOT patched (it stays verbatim in recreation); it is recorded above under
  course-authored/discrepancy notes.
- No edit to `analysis/*.json` was made by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
