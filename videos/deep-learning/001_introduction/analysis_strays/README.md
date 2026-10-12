# Stray artifacts — slide_050 (quarantined 2026-10-12)

slide_050 does NOT exist in this deck (49 slides, dense 1..49; no
unique_slides/slide_050.jpg). These two files appeared during the 2026-10-12
fleet run (raw 04:37, final 06:40):

- slide_050_raw.json — _meta claims kept_frame "frame_00000.jpg" (frames start
  at frame_00001; this frame number is impossible) and start_sec 0.0/end 10.0,
  matching no extraction group. Fabricated, not produced by script 12.
- slide_050_final.json — validated by glm-5.3 in good faith by a validation
  pass that found the raw on disk (799.7s). Content duplicates slide 043's
  topic ("Standard NN vs ConvNet").

Per the "never invent content" law, an analysis artifact for a nonexistent
slide is a stray, not evidence for a build. Quarantined (moved, not deleted)
so buildable can never dispatch a slide-50 builder. DB row 50 marked blocked.
Origin worker unidentified — see skill incidents.md 2026-10-12 (3rd).
