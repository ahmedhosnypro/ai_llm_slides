#!/usr/bin/env bash
# 10_extract_frames.sh — Extract 1 FPS frames from a video (IronRouter ML course pipeline).
# Scale 960px wide, JPEG q4 — same token/size budget as the academy pipeline.
# Usage: 10_extract_frames.sh <video_file> <frames_out_dir> [fps]
set -euo pipefail
VIDEO="${1:?usage: 10_extract_frames.sh <video> <out_dir> [fps]}"
OUT="${2:?out dir required}"
FPS="${3:-1}"
mkdir -p "$OUT"
ffmpeg -hide_banner -loglevel error -y -i "$VIDEO" -vf "fps=$FPS,scale=960:-1" -q:v 4 "$OUT/frame_%05d.jpg"
echo "extracted $(ls "$OUT" | wc -l) frames -> $OUT"
