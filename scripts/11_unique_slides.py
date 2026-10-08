#!/usr/bin/env python3
"""
11_unique_slides.py — Group extracted frames into unique slides via perceptual hashing.

Sequential grouping: consecutive frames whose phash differs by <= threshold belong
to the same slide (handles animations/builds/cursor movement). A new slide starts
when the hash breaks away. Keeps the LAST frame of each group — the fully-built
slide (all bullets/annotations revealed) — plus the group's time range.

Usage:
    python3 11_unique_slides.py <frames_dir> <slides_out_dir> [--limit 10] [--threshold 8]

Outputs:
    <slides_out_dir>/slide_001.jpg ...
    <slides_out_dir>/slides_index.json
"""

import argparse
import json
import os
import shutil


def main():
    import imagehash
    from PIL import Image

    parser = argparse.ArgumentParser(description="Group frames into unique slides")
    parser.add_argument("frames_dir")
    parser.add_argument("slides_out_dir")
    parser.add_argument("--limit", type=int, default=10, help="Stop after N unique slides")
    parser.add_argument("--threshold", type=int, default=8, help="phash distance for same-slide")
    parser.add_argument("--fps", type=float, default=1.0, help="extraction fps (timestamp math)")
    args = parser.parse_args()

    frames_dir = os.path.abspath(args.frames_dir)
    out_dir = os.path.abspath(args.slides_out_dir)
    os.makedirs(out_dir, exist_ok=True)

    frame_files = sorted(
        os.path.join(frames_dir, f)
        for f in os.listdir(frames_dir)
        if f.lower().endswith((".jpg", ".jpeg"))
    )
    if not frame_files:
        raise SystemExit(f"no frames in {frames_dir}")

    def ts_of(fp: str) -> float:
        n = int(os.path.splitext(os.path.basename(fp))[0].split("_")[-1])
        return (n - 1) / args.fps

    groups = []  # each: {"files": [...], "hash": last_hash}
    cur = None
    for fp in frame_files:
        h = imagehash.phash(Image.open(fp))
        if cur is not None and (h - cur["hash"]) <= args.threshold:
            cur["files"].append(fp)
            cur["hash"] = h  # track the latest state (builds/annotations)
        else:
            if cur is not None:
                groups.append(cur)
            if len(groups) >= args.limit:
                break
            cur = {"files": [fp], "hash": h}
    if cur is not None and len(groups) < args.limit:
        groups.append(cur)

    index = []
    for i, g in enumerate(groups, 1):
        keep = g["files"][-1]  # fully-built slide
        dest = os.path.join(out_dir, f"slide_{i:03d}.jpg")
        shutil.copyfile(keep, dest)
        index.append({
            "slide": i,
            "image": f"slide_{i:03d}.jpg",
            "kept_frame": os.path.basename(keep),
            "start_sec": ts_of(g["files"][0]),
            "end_sec": ts_of(g["files"][-1]),
            "frame_count": len(g["files"]),
        })
        print(f"slide {i:03d}: {ts_of(g['files'][0]):7.1f}s - {ts_of(g['files'][-1]):7.1f}s "
              f"({len(g['files'])} frames, kept {os.path.basename(keep)})")

    with open(os.path.join(out_dir, "slides_index.json"), "w") as f:
        json.dump(index, f, indent=2)
    print(f"\n{len(index)} unique slides -> {out_dir}")


if __name__ == "__main__":
    main()
