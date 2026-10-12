#!/usr/bin/env python3
"""Curation reconciliation for deep-learning/001_introduction (80 extracted groups -> 49 founder-curated slides).

Per the curation-metadata law (videos/deep-learning/AGENTS.md + lessons 2026-10-11):
- md5 content-hash matching (script 11 copied frames byte-exact).
- Resolution order: match survivor against OLD GROUPS' KEPT FRAMES first; full-frame
  search only for founder swaps (attributed to a group by frame-number span, keeping
  the old sequence monotonic).
- Founder group splits (one old group -> two survivors) and frame swaps are recorded,
  never second-guessed.
- Old index preserved as slides_index_old80.json; slides_index.json rewritten for the
  curated set; new2old_mapping.json rebuilt.
Outputs printed + asserted: every file matched, <=2 survivors per old group,
monotonic old sequence.
"""
import hashlib
import json
import os
import shutil
import sys
from collections import defaultdict

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
FRAMES = os.path.join(BASE, "frames")
US = os.path.join(BASE, "unique_slides")


def md5_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def fnum(name):
    return int(name.split("_")[1].split(".")[0])


# --- 1. md5 every frame -> md5 -> [frame numbers] (content repeats exist; keep lists)
md5_to_fnums = defaultdict(list)
for fn in sorted(os.listdir(FRAMES)):
    if fn.endswith(".jpg"):
        md5_to_fnums[md5_file(os.path.join(FRAMES, fn))].append(fnum(fn))
print(f"frames hashed: {sum(len(v) for v in md5_to_fnums.values())}, distinct contents: {len(md5_to_fnums)}")

# --- 2. old index, preserved
old_path = os.path.join(US, "slides_index.json")
old_idx = json.load(open(old_path))
assert len(old_idx) == 80, f"expected 80 old entries, got {len(old_idx)}"
shutil.copyfile(old_path, os.path.join(US, "slides_index_old80.json"))

kept_md5 = {md5_file(os.path.join(FRAMES, e["kept_frame"])): e for e in old_idx}
# group span in frame numbers: frame N covers second N-1; group start_sec..end_sec -> N in [start+1, end+1]
groups = []
for e in old_idx:
    groups.append({
        "old": e["slide"], "kept_frame": e["kept_frame"],
        "start_sec": e["start_sec"], "end_sec": e["end_sec"],
        "f_lo": int(e["start_sec"]) + 1, "f_hi": int(e["end_sec"]) + 1,
        "frame_count": e["frame_count"],
    })
by_old = {g["old"]: g for g in groups}

# --- 3. survivors
survivors = sorted(fn for fn in os.listdir(US) if fn.endswith(".jpg"))
assert len(survivors) == 49, f"expected 49 survivors, got {len(survivors)}"

results = []
prev_old = 0
for sfn in survivors:
    new_num = fnum(sfn)
    h = md5_file(os.path.join(US, sfn))
    rec = {"new": new_num, "image": sfn}
    if h in kept_md5:
        e = kept_md5[h]
        rec.update({
            "old_group": e["slide"], "match": "kept_frame",
            "kept_frame": e["kept_frame"], "start_sec": e["start_sec"],
            "end_sec": e["end_sec"], "frame_count": e["frame_count"],
            "founder_frame_swap": False,
        })
    else:
        # founder swap: full-frame search. Candidate groups = groups whose span contains
        # a frame with this content; prefer the earliest group that keeps monotonicity.
        fnums = md5_to_fnums.get(h)
        if not fnums:
            rec.update({"match": "UNMATCHED"})
            results.append(rec)
            continue
        cand = set()
        for g in groups:
            if any(g["f_lo"] <= fn <= g["f_hi"] for fn in fnums):
                cand.add(g["old"])
        cand = sorted(c for c in cand if c >= prev_old) or sorted(cand)
        g_old = cand[0]
        g = by_old[g_old]
        in_group = [fn for fn in fnums if g["f_lo"] <= fn <= g["f_hi"]]
        rec.update({
            "old_group": g_old, "match": "founder_frame_swap",
            "kept_frame": f"frame_{min(in_group):05d}.jpg",
            "start_sec": min(in_group) - 1, "end_sec": g["end_sec"],
            "frame_count": g["frame_count"], "founder_frame_swap": True,
            "original_kept_frame": g["kept_frame"],
        })
    prev_old = rec["old_group"]
    results.append(rec)

# --- 4. assertions
bad = [r for r in results if r.get("match") == "UNMATCHED"]
assert not bad, f"UNMATCHED survivors: {[r['image'] for r in bad]}"
olds = [r["old_group"] for r in results]
assert olds == sorted(olds), f"old sequence not monotonic: {olds}"
per_group = defaultdict(list)
for r in results:
    per_group[r["old_group"]].append(r["new"])
assert all(len(v) <= 2 for v in per_group.values()), f">2 survivors in a group: {per_group}"
splits = {k: v for k, v in per_group.items() if len(v) == 2}
swaps = [r for r in results if r["founder_frame_swap"]]

# --- 5. write outputs
new_idx = [{
    "slide": r["new"], "image": r["image"], "kept_frame": r["kept_frame"],
    "start_sec": r["start_sec"], "end_sec": r["end_sec"],
    "frame_count": r["frame_count"],
    "old_group": r["old_group"],
    "founder_frame_swap": r["founder_frame_swap"],
    **({"original_kept_frame": r["original_kept_frame"]} if r["founder_frame_swap"] else {}),
} for r in results]
with open(old_path, "w") as f:
    json.dump(new_idx, f, indent=2)

mapping = {
    "_note": ("Rebuilt from content hashes 2026-10-12 after the founder's curation of the 80 "
              "extraction groups to 49 slides (deletions of blank transitions + annotation-state "
              "duplicates; dense renumbering). old index preserved as slides_index_old80.json. "
              "Founder group splits and frame swaps are recorded, never second-guessed."),
    "video": "deep-learning/001_introduction",
    "curation": {"date": "2026-10-12", "from_groups": 80, "to_slides": 49,
                 "group_splits": {str(k): v for k, v in sorted(splits.items())},
                 "frame_swaps": {str(r["new"]): {"old_group": r["old_group"],
                                                "original_kept_frame": r["original_kept_frame"],
                                                "founder_kept_frame": r["kept_frame"]}
                                for r in swaps}},
    "mapping": [{"new": r["new"], "old_group": r["old_group"], "image": r["image"],
                 "kept_frame": r["kept_frame"]} for r in results],
}
with open(os.path.join(US, "new2old_mapping.json"), "w") as f:
    json.dump(mapping, f, indent=2)

# --- 6. report
print(f"\n49 survivors matched: {len(results)}; splits={splits}; swaps={[(r['new'], r['old_group']) for r in swaps]}")
print("\nnew -> old (interesting slides for the founder dep graph):")
dep_slides = [9, 16, 17, 18, 19, 24, 25, 35, 36, 37, 41]
for r in results:
    if r["new"] in dep_slides:
        print(f"  new {r['new']:3d} <- old group {r['old_group']:3d}  "
              f"(kept {r['kept_frame']}, {r['start_sec']:.0f}-{r['end_sec']:.0f}s"
              f"{', FOUNDER SWAP' if r['founder_frame_swap'] else ''})")
print("\nfull new->old table:")
print("  " + ", ".join(f"{r['new']}<-{r['old_group']}" for r in results))
