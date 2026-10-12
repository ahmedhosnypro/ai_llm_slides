// P2 FINAL-MEMBER VERIFICATION NOTE — slide 034 ("[2] Position Embedding", P2#4 of [20,21,22,34]).
// P2 is now COMPLETE (all four members certified: 020 PASS, 021 PASS, 022 PASS, 034 PASS).
//
// PATTERN VERIFICATION vs the group's earlier certified members (per 17_worker_instructions.md
// rule 4 — verify the pattern, then reuse): concrete cross-member greps of the build scripts
// (2026-10-12):
//   * shared chrome import `shared_patterns/house_chrome.js` — 2 refs in EACH of
//     slide_020/021/022/034.js (require + doc comment); numeral per member = own frame number.
//   * dashed row lanes (sysDash family + dash dashcontainers) — present in all four.
//   * raster brace mechanism (LO mis-renders brace presets -> generated PNG per member,
//     embedded at w=px/600) — brace_020.png / brace_021.png / brace_034.png in build/assets/.
//   * closed-loop discipline: per-frame chrome-landmark mapping fit re-measured per member
//     (ax drift family: 020=18.628, 021=18.13, 022=17.753, 034=17.943 — fit YOUR frame);
//     PIL band self-check vs original before judging (slide034: 28 regions, all OK,
//     scratch/slide034/selfcheck_attempt_1_output.txt); dense-region crop comparisons
//     (qa/slide034/cropcheck_*.txt — 5 crops, all CROP VERDICT: MATCH).
//   * JPEG-dark color class (dark maroon 8A2436-family instead of spec's bright CC0000),
//     5-dot ellipsis grid, cap-pinned text, spec-vs-frame reconciliation records — same
//     convention in all four, per p2_member_notes_021.js / p2_member_notes_022.js.
//
// 034 FAMILY DELTAS (for any future slide reusing the P2 lane pattern):
//   * Two SEPARATE dashed lanes (no shared navy-bordered panel like 022): token lane
//     (lavender fill CCCCFC, dash 26266E, digit boxes) then a full-width purple bar
//     (8E0094, yellow keywords) between the lanes, then the vector lane (pink-lavender
//     FBDCFC, dash 5F7382, "Vector pK" boxes with inline subscripts).
//   * TWO block arrows lane->bar->lane (8A1620), and the raster brace sits UNDER the
//     vector lane pointing at a green-outline summary box (not inside a bordered panel).
//   * No +δ annotation band (that is 020/021/022-only); no Problems panel (022-only).
//   * Known MINORs accepted by judge attempt 1: arrow tone darker than original's bright
//     red; brace curvature flatter than the original curly brace; ellipsis dots greyer —
//     all sub-tolerance, documented in judge_attempt_1.txt.
//
// NO SUCCESSOR MEMBER: P2 ends here. Nothing below banks an obligation forward.
