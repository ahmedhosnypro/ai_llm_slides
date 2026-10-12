// components/house_chrome.js — per-video chrome primitive for 001_introduction.
//
// PLAYLIST LAW (founder directive 2026-10-11, videos/deep-learning/AGENTS.md): every
// recreated slide in this playlist uses the SAME outer chrome, measured from
// 001_transformers_part1/unique_slides/slide_001.jpg. This module DELEGATES to the
// playlist-certified shared pattern (single source of truth) instead of re-deriving:
//   canvas FFFFFF | panel E9E9E7 x42..918px y45..bottom, C00000 border
//   badge d36px @ (893,71): FDFD96 fill, 6A5ACD ~2pt ring, bold 333333 numeral (18pt Arial)
// Children import THIS path (stable): require('./components/house_chrome').
// NOTE (001_introduction/AGENTS.md 2026-10-12): this lecture's original frames carry no
// printed badge; the numeral is the slide's file number (assumption PENDING FOUNDER VETO).
// Closed-loop checker: videos/deep-learning/shared_patterns/house_chrome_check.py.
module.exports = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
