#!/usr/bin/env python3
"""recover_mapping.py — reconstruct 002's curation metadata (150 -> 59 + placeholder).

The founder curated the 150 extracted unique frames down to 59 files renamed
slide_002..slide_060.jpg (slide_001 = missing cover, placeholder). Renames preserved
bytes (shutil.copyfile wrote them), so each surviving file resolves back to its source
frame by md5, and the stale 150-entry slides_index.json maps that to the old slide.

Resolution order per file:
  1. md5 matches an OLD GROUP's kept_frame  -> clean match (that is how script 11
     created the file the founder renamed).
  2. else: search all frames; candidates must fall in exactly ONE old group ->
     founder_frame_swap (001 precedent). Ambiguity across groups -> anomaly.

An old group may be used by TWO new files = founder group SPLIT (001 precedent:
7+8 both <- old 14). The split's earlier-state file is flagged swapped; both
entries carry split notes. >2 per group, or any other duplicate, -> anomaly.

Outputs (in unique_slides/):
  slides_index_old150.json  — stale extraction index, renamed (evidence kept)
  slides_index.json         — new 60-entry index (slide 1 = placeholder)
  new2old_mapping.json      — 001-format mapping (old_slide, diff, swapped?, note?)

Exits nonzero on any anomaly WITHOUT writing outputs — founder decides those.
"""
import hashlib
import json
import os
import sys
from collections import defaultdict

V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
US = os.path.join(V, "unique_slides")
FRAMES = os.path.join(V, "frames")

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    old_index = json.load(open(os.path.join(US, "slides_index.json")))
    assert len(old_index) == 150, f"expected stale 150-entry index, got {len(old_index)}"

    # md5 of all frames -> list of names (duplicate content occurs across the video)
    frames_by_md5 = defaultdict(list)
    for fn in sorted(os.listdir(FRAMES)):
        if fn.endswith(".jpg"):
            frames_by_md5[md5(os.path.join(FRAMES, fn))].append(fn)
    n_frames = sum(len(v) for v in frames_by_md5.values())
    print(f"hashed {n_frames} frames ({len(frames_by_md5)} distinct contents)")

    import bisect
    starts = [e["start_sec"] for e in old_index]
    def old_group_of(frame_name):
        sec = int(frame_name.split("_")[-1].split(".")[0]) - 1
        i = bisect.bisect_right(starts, sec) - 1
        if i < 0:
            return None
        e = old_index[i]
        return e if sec <= e["end_sec"] else None

    # md5 of every old kept frame -> its group (dedup if two groups kept identical bytes)
    kept_md5 = defaultdict(list)
    for e in old_index:
        kept_md5[md5(os.path.join(FRAMES, e["kept_frame"]))].append(e)

    new_files = sorted(f for f in os.listdir(US) if f.endswith(".jpg"))
    assert len(new_files) == 59, f"expected 59 curated jpgs, got {len(new_files)}"
    assert new_files[0] == "slide_002.jpg" and new_files[-1] == "slide_060.jpg", \
        "curated files are not the contiguous slide_002..slide_060 set"

    anomalies = []
    matches = []  # (new_slide, matched_frame, old_entry, swapped)
    used_old = defaultdict(list)  # old slide -> [new slides]
    for fn in new_files:
        n = int(fn[6:9])
        m = md5(os.path.join(US, fn))
        swapped = False
        if m in kept_md5:
            groups = kept_md5[m]
            if len(groups) > 1:
                anomalies.append(f"slide_{n:03d}: kept-frame md5 matches groups "
                                 f"{[g['slide'] for g in groups]} — ambiguous duplicate")
                continue
            g = groups[0]
            matched = g["kept_frame"]
        else:
            cands = frames_by_md5.get(m)
            if not cands:
                anomalies.append(f"slide_{n:03d}: no byte-identical frame (re-encoded?)")
                continue
            gset = {}
            for c in cands:
                g = old_group_of(c)
                if g is not None:
                    gset.setdefault(g["slide"], (g, c))
            if len(gset) != 1:
                anomalies.append(f"slide_{n:03d}: swap candidates span groups {sorted(gset)}")
                continue
            g, matched = next(iter(gset.values()))
            swapped = True
        used_old[g["slide"]].append(n)
        if len(used_old[g["slide"]]) > 2:
            anomalies.append(f"slide_{n:03d}: old group {g['slide']} used >2 times "
                             f"({used_old[g['slide']]})")
            continue
        matches.append((n, matched, g, swapped))
    if anomalies:
        print("ANOMALIES — not writing outputs:")
        for a in anomalies:
            print("  " + a)
        sys.exit(1)

    # monotonicity: old sequence non-decreasing; equal values only as split pairs
    olds = [g["slide"] for _, _, g, _ in matches]
    for a, b in zip(olds, olds[1:]):
        if b < a:
            print(f"ANOMALY: old-slide sequence not monotonic: {olds}")
            sys.exit(1)
    for old, news in used_old.items():
        if len(news) == 2:
            print(f"old group {old} SPLIT into new slides {news} (founder decision, 001 precedent)")

    # phash diff for swapped/split-earlier files (same library as script 11)
    diffs = {}
    to_diff = [(n, g) for n, _, g, sw in matches if sw]
    if to_diff:
        import imagehash
        from PIL import Image
        for n, g in to_diff:
            h_new = imagehash.phash(Image.open(os.path.join(US, f"slide_{n:03d}.jpg")))
            h_old = imagehash.phash(Image.open(os.path.join(FRAMES, g["kept_frame"])))
            diffs[n] = int(h_new - h_old)

    split_of = {n: [x for x in used_old[g["slide"]] if x != n]
                for n, _, g, _ in matches if len(used_old[g["slide"]]) == 2}

    # ---- write outputs ----
    os.rename(os.path.join(US, "slides_index.json"), os.path.join(US, "slides_index_old150.json"))

    index = [{
        "slide": 1, "image": "slide_001.jpg", "placeholder": True,
        "title": "Deep Learning",
        "note": "cover frame missing from video — rebuilt as a placeholder mirroring "
                "001 slide 1 per the playlist chrome law (founder curation 2026-10-11)",
    }]
    mapping = {"1": {"placeholder": True,
                     "note": "missing cover — no source frame; placeholder per playlist law"}}
    for n, frame, g, swapped in matches:
        e = {
            "slide": n, "image": f"slide_{n:03d}.jpg",
            "kept_frame": frame,
            "start_sec": g["start_sec"], "end_sec": g["end_sec"],
            "frame_count": g["frame_count"],
            "old_slide": g["slide"],
        }
        m = {"old_slide": g["slide"], "diff": 0}
        notes = []
        if n in split_of:
            notes.append(f"old group split with new slide {split_of[n][0]}")
        if swapped:
            e["founder_frame_swap"] = True
            e["original_kept_frame"] = g["kept_frame"]
            m["swapped"] = True
            m["diff"] = diffs.get(n)
            notes.append(f"founder kept {frame} (mid-group state) over the group's final kept frame")
        if notes:
            e["note"] = "; ".join(notes)
            m["note"] = "; ".join(notes)
        index.append(e)
        mapping[str(n)] = m

    with open(os.path.join(US, "slides_index.json"), "w") as f:
        json.dump(index, f, indent=2)
    with open(os.path.join(US, "new2old_mapping.json"), "w") as f:
        json.dump(mapping, f, indent=2)

    sw = [n for n, _, _, s in matches if s]
    print(f"OK: 59/59 matched; old->new {olds[0]}..{olds[-1]}; {len(sw)} non-kept frames {sw}")
    print("wrote slides_index.json (60 entries), new2old_mapping.json, slides_index_old150.json")

if __name__ == "__main__":
    main()
