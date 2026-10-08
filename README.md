# ai_llm_slides — Slide Extraction & Analysis Pipeline

Extract unique slides from course videos and produce **precise, validated, PowerPoint-recreation-ready**
specifications for each slide using vision + text models through the local IronRouter gateway
(`http://localhost:17844/v1`).

## Pipeline

```
video (mp4)
  │
  ▼  scripts/10_extract_frames.sh     → frames/          (1 FPS, 960px wide JPEG q4)
  │
  ▼  scripts/11_unique_slides.py      → unique_slides/    (phash grouping; last frame per slide kept)
  │
  ▼  scripts/12_analyze_slides.py     → analysis/         (vision model: verbatim text, layout, colors,
  │                                                      charts, recreation brief — JSON per slide)
  ▼  scripts/13_validate_slides.py   → analysis/         (glm-5.3 QA pass → slide_XXX_final.json,
                                                         slides_final.json, summary.md)
```

## Usage

```bash
# 0. download the video into this directory (see README download command)
# 1. frames
./scripts/10_extract_frames.sh <video.mp4> frames
# 2. first N unique slides
python3 scripts/11_unique_slides.py frames unique_slides --limit 10 --threshold 8
# 3. vision analysis (model: images; override with IR_VISION_MODEL / --model)
python3 scripts/12_analyze_slides.py unique_slides analysis --slides 10
# 4. validation (model: glm-5.3)
python3 scripts/13_validate_slides.py analysis --slides 10
```

Final outputs live in `analysis/`: `slides_final.json` (all validated slides, the artifact for
PowerPoint generation), `summary.md` (verdict table), and per-slide `slide_XXX_final.json`.

## Configuration

| Item | Default | Override |
|---|---|---|
| Router base URL | `http://localhost:17844/v1` | `IR_BASE_URL` env |
| API key | `.analyze-image-key` (project root, mode 600) | `IR_API_KEY` env |
| Vision model | `images` | `IR_VISION_MODEL` env / `--model` |
| Validation model | `glm-5.3` | `IR_TEXT_MODEL` env / `--model` |

## Download the video

```bash
yt-dlp --cookies /tmp/yt-cookies.txt -f "bv*[height<=1080]+ba/b" \
  --merge-output-format mp4 -o "ml-intro.mp4" \
  "https://www.youtube.com/watch?v=mRUgi0Be2ds"
```

(YouTube blocks anonymous datacenter/rate-limited IPs; the cookies file carries a logged-in
session. Re-export with `yt-dlp --cookies-from-browser chrome --cookies /tmp/yt-cookies.txt --simulate <url>`
if the file is gone.)
