# SOURCES.md — slide_001 (Deep Learning DSAI 308 — title slide)

Slide content: course title "Deep  Learning DSAI 308", "Prepared By" Dr. Khaled Mostafa ElSayed
(kmelsayed@zewailcity.edu.eg), "Instructors:" Dr. Khaled Mostafa ElSayed + Dr. Mohamed Maher Ata
(momaher@zewailcity.edu.eg), Zewail City teal emblem + bilingual university-name box.

## Source URLs

1. **YouTube playlist "Deep Learning DSAI 308 Fall 2024 - Zewail"** — channel "Dr. Khaled Mostafa Elsayed"
   https://www.youtube.com/playlist?list=PL5JZLxl_tFCcmulUU7suv9DkAFrOTm34w
   (found via DuckDuckGo: https://duckduckgo.com/html/?q=%22Khaled+Mostafa+ElSayed%22+Zewail+City)
   - Confirms the course code **DSAI 308 = "Deep Learning"** at Zewail, and the instructor's name
     spelling **"Dr. Khaled Mostafa Elsayed"** — exactly as the vision analysis read it. The video
     being processed (001_introduction.mp4, 2026 playlist) is a re-offering of this course.
   - Channel also hosts "DSAI 325 Information Theory Spring 2025" — same instructor.
   - NOTE: the fleet brief's "Dr. Ahmed Mustafa ElSayed" does not match the web evidence; the
     course instructor is Khaled Mostafa Elsayed. The slide's printed name (ground truth) agrees.

2. **Zewail City official website** — https://zewailcity.edu.eg/
   - Current official name: "Zewail City of Science, Technology and Innovation".
   - Contains the **University of Science and Technology (UST)** — matches the white box on the
     slide: "جامعة العلوم والتكنولوجيا / University of Science and Technology".
   - Address: Ahmed Zewail Road, October Gardens, 6th of October City, Giza, Egypt.

3. **Zewail City founding date** (via agy web search → Wikipedia infobox, 2026-10-12):
   - Established by presidential decree **May 11, 2011**; inaugurated **November 1, 2011**.
   - **Confirms the slide emblem's tiny text "ESTABLISHED 2011" / "INAUGURATED 2011"** — the raw
     analysis's `[?]` markers on these two lines can be resolved to CONFIRMED.

4. **Zewail City UST faculty/programs page** — https://zewailcity.edu.eg/faculty-members
   - Lists the **"Data Science and Artificial Intelligence, Information Technology"** program —
     corroborates the DSAI course prefix (DSAI 308).

## Downloaded files (site's own figures, original filenames)

| File | What it is | Provenance |
|---|---|---|
| `zcLogo.svg` | Official Zewail City logo, SVG vector (emblem teal ≈ `#00b4d1`; text converted to paths, no text nodes) | https://zewailcity.edu.eg/Images/zcLogo.svg |
| `mini_logo_e57c2a3adc.png` | Official Zewail City logo, PNG 1748×1384, 8-bit colormap | https://zcadminpanel.zewailcity.edu.eg/uploads/mini_logo_e57c2a3adc.png |

These are the institution's own current logo assets — the closest official analogue to the emblem
printed on the slide. The slide's emblem (approx `#2BB3AB`) is the same design; hue difference vs
`#00b4d1` is recording/compression shift. For recreation the slide frame is ground truth; use the
official assets only as vector-drawing reference.

## Confirmed / corrected vs the slide

- CONFIRMED: "ESTABLISHED 2011" and "INAUGURATED 2011" tiny lines in the emblem (presidential
  decree 2011-05-11; inauguration 2011-11-01).
- CONFIRMED: instructor "Dr. Khaled Mostafa ElSayed" and email domain zewailcity.edu.eg
  (course playlist is owned by the instructor's channel of that name; official site uses the
  same domain).
- CONFIRMED: the emblem's Arabic "مدينة زويل" = "Zewail City"; the current official branding is
  "Zewail City of Science, Technology and Innovation" — the slide-era logo ("ZEWAIL CITY" +
  "مدينة زويل") matches the emblem used on the official site today.
- NOT CORRECTED: nothing on the slide contradicts the sources.

## Open questions

- `[?]` "Dr. Mohamed Maher Ata" (second instructor, momaher@zewailcity.edu.eg) could not be
  independently verified on the web (faculty directory is JS-rendered; name searches timed out
  on the provider). The slide wins for recreation; identity plausible (same email domain).
- `[?]` The raw analysis flagged the Arabic inside the emblem as "مدينة زويل [?]" — consistent
  with the official logo, but the emblem text is too small in the frame for a certainty claim;
  the downloaded SVG's text is path-only so a character-level diff was not possible.

---

## ADDENDUM (reverse-order fleet worker, 2026-10-12) — resolves the Maher Ata [?]

The official Zewail City directory API (behind /faculty-members, Next.js ->
Strapi: https://zcadminpanel.zewailcity.edu.eg/api/members?populate=categories&
pagination[pageSize]=500) INDEPENDENTLY VERIFIES the second instructor:

- "Dr. Mohamed Maher Ata" — email **momaher@zewailcity.edu.eg** (EXACT match to
  the slide), rank **Associate Professor, Computational Sciences and Artificial
  Intelligence School** (CSAI), room S028-D-AB; PhD Tanta University (co-op
  Regina University, Canada); research: signal/image/video processing, machine
  and deep learning, computer vision.
- Also CONFIRMS "Dr. Khaled Mostafa El Sayed" — email kmelsayed@zewailcity.edu.eg
  (EXACT match), **Professor, CSAI**, Director of Data Science Program, PhD Cairo
  University 1998.

Both are UST (University of Science and Technology) members — consistent with the
DSAI 308 course prefix and the slide's logo box. Institutional history from the
official site (/about-zewail-city) confirms this file's dates: Cabinet decree
May 11, 2011 named it "Zewail City of Science and Technology" (National Project
for Scientific Renaissance); officially inaugurated November 1, 2011; Law 161 of
December 20, 2012 granted final legal status; foundation stone January 1, 2000.

The two `[?]` open questions above can be treated as RESOLVED for the instructor
identities; the emblem-text [?] (Arabic "مدينة زويل" legibility in the frame)
stands as-is (frame remains ground truth).
