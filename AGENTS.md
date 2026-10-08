# AGENTS.md — AI Agent Context for ai_llm_slides

## What this project is

A pipeline that cuts a course video into unique slide frames, analyzes each slide with a
vision model (verbatim text + layout + colors + charts), validates the extraction with a
text model, and saves PowerPoint-recreation-ready JSON. The outputs feed a later
"generate PowerPoint slides with AI" step — **fidelity of content and visualization
description is the whole point**.

## Model & Endpoint

| Setting | Value |
|---|---|
| Base URL | `http://localhost:17844/v1` (local IronRouter **dist** lane) |
| API key | `.analyze-image-key` in the project root (mode 600); `IR_API_KEY` env overrides |
| Vision model | `images` (IronRouter virtual model; fallback that worked on a codespace: `glm-5.3-flash`) |
| Validation model | `glm-5.3` |

## Hard-won operational facts (do not relearn these)

1. **Always stream** (`stream=True`) — the NVIDIA NIM upstream gateway cuts non-streaming
   responses at ~60s. Big vision analyses take 3–5 min; non-streaming requests die as
   `ServiceTimeout` on every key while the router churns the key pool. Streaming works.
2. `finish_reason=length` with `content=null` and a filled `reasoning_content` means the model
   spent its whole budget thinking — raise `max_tokens` (analysis uses 16000).
3. Vision-frame token cost: **~540 tokens/frame** at 960px JPEG q4. Budget accordingly.
4. **phash dedup with threshold 8** groups slide builds/animations reliably. Keep the
   **last** frame of each group (fully-built slide), not the first.
5. Analysis is slow (~3–5 min/slide including upstream key churn). Validate with
   `finish=stop` per slide in the log; retry individual failures by deleting the
   `slide_XXX_raw.json` and re-running — both 12 and 13 are idempotent (skip existing outputs).
6. glm-5.3 occasionally returns empty content (parse error "Expecting value: line 1 column 1") —
   just re-run script 13; it retries only the missing finals.
7. YouTube blocks anonymous downloads from datacenter/rate-limited IPs — use
   `--cookies /tmp/yt-cookies.txt` (exported from Chrome).

## Directory layout

```
scripts/   10_extract_frames.sh, 11_unique_slides.py, 12_analyze_slides.py, 13_validate_slides.py
frames/    1 FPS extraction (gitignored — large)
unique_slides/  kept slide images + slides_index.json
analysis/  slide_XXX_raw.json (vision) → slide_XXX_final.json (validated),
           slides_final.json (combined artifact), summary.md
```

## Output contract (what the PPTX-generation step consumes)

`analysis/slides_final.json` — array of slide objects with: `slide_title`,
`verbatim_text` (bullets/labels/equations — VERBATIM, no paraphrasing), `layout`
(arrangement + regions), `visual_elements` (type, chart data values, colors, position),
`imagery`, `colors` (approx hex), `typography_notes`, `recreation_brief` (numbered
recreation checklist), and a `validation` block (verdict, fixes, uncertain items
marked `[?]`, recreatability score). Never invent facts — uncertain content keeps its
`[?]` marker.
