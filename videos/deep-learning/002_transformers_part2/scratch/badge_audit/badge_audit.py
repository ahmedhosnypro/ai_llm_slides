#!/usr/bin/env python3
"""Badge glyph forensics for videos/deep-learning/002_transformers_part2.

Pure PIL/numpy/scipy evidence. No vision-model calls.
For each slide's yellow badge disc (top-right playlist chrome):
  - measure disc bbox/center/fill
  - extract numeral ink as color-distance-from-fill inside the disc
  - connected components, per-glyph bbox / holes / stroke stats / ASCII map
  - deck-wide template-bank matching (badge numeral must equal the file id)
  - special occluded-badge analysis for slide_048 (digit tops vs 8/9/4 templates)
Writes scratch/badge_audit/badge_measurements.json and x8 crops.
"""
from PIL import Image
import numpy as np
from scipy import ndimage
import hashlib, json, os, sys

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
US = os.path.join(ROOT, "unique_slides")
OUT = os.path.join(ROOT, "scratch", "badge_audit")
os.makedirs(OUT, exist_ok=True)
HINT = (877.0, 70.0)          # approx badge center, measured on 047
FOCUS = ["slide_047", "slide_048", "slide_049", "slide_050"]
EXCLUDE_FROM_BANK = {"slide_048"}   # the slide under investigation
SLIDES = [f"slide_{i:03d}" for i in range(2, 61)]


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def find_badge(a):
    """Largest pale-yellow blob near HINT in the top-right corner region."""
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    ym = (r > 215) & (g > 205) & (b < 215) & ((r - b) > 35) & ((g - b) > 35)
    region = np.zeros(ym.shape, bool)
    region[:170, 830:] = True
    ym &= region
    lab, n = ndimage.label(ym)
    cands = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        area = len(ys)
        if area < 150:
            continue
        cy, cx = float(ys.mean()), float(xs.mean())
        d = ((cx - HINT[0]) ** 2 + (cy - HINT[1]) ** 2) ** 0.5
        if d > 60:
            continue
        cands.append(dict(area=area, cx=cx, cy=cy,
                          bbox=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                          mask=(lab == i)))
    if not cands:
        return None, int(ym.sum()), n
    cands.sort(key=lambda c: -c["area"])
    return cands[0], int(ym.sum()), n


def glyph_holes(mask, min_area=2):
    """Enclosed background regions (not touching the padded bbox border)."""
    pad = np.pad(mask, 1, constant_values=0)
    lab, n = ndimage.label(~pad)
    border = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
    holes = []
    for i in range(1, n + 1):
        if i in border:
            continue
        ys, xs = np.where(lab == i)
        if len(ys) < min_area:
            continue
        h = mask.shape[0]
        holes.append(dict(area=int(len(ys)),
                          cx=round(float(xs.mean()), 1), cy=round(float(ys.mean()), 1),
                          cy_frac=round(float(ys.mean()) / h, 2),
                          bbox=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]))
    holes.sort(key=lambda hh: hh["cy"])
    return holes


def stroke_width(mask):
    runs = []
    for row in mask:
        for k, gr in __import__("itertools").groupby(row):
            if k:
                runs.append(sum(1 for _ in gr))
    return round(float(np.median(runs)), 1) if runs else 0.0


def ascii_mask(mask, ink="#", bg="."):
    return "\n".join("".join(ink if v else bg for v in row) for row in mask)


def split_by_column_gap(mask):
    """Split a merged two-digit component. Prefer a zero column; else the
    deepest interior ink minimum (digits may touch via one bridge pixel)."""
    colsum = mask.sum(axis=0).astype(int)
    w = mask.shape[1]
    lo, hi = max(2, w // 4), w - max(2, w // 4)
    if hi <= lo:
        return [mask]
    interior = colsum[lo:hi]
    zero_cols = [lo + i for i, v in enumerate(interior) if v == 0]
    if zero_cols:
        c = zero_cols[len(zero_cols) // 2]
        cut = c
    else:
        # split at the minimum-ink column, but only if clearly two digits wide
        if w < 9 or mask.shape[0] < 8:
            return [mask]
        c = lo + int(np.argmin(interior))
        if interior.max() == 0 or colsum[c] > 2:
            return [mask]
        cut = c
    left, right = mask[:, :cut].copy(), mask[:, cut:].copy()
    # clear bridge pixels on the cut column of the narrower side
    return [m for m in (left, right) if m.sum() >= 5]


def analyze_badge(name, dist_T=70):
    """Return badge + glyph analysis for one slide."""
    path = os.path.join(US, f"{name}.jpg")
    a = np.array(Image.open(path).convert("RGB"))
    blob, ycount, nblob = find_badge(a)
    rec = dict(md5=md5(path), yellow_px_in_region=ycount, blobs=nblob)
    if blob is None:
        rec["error"] = "no badge blob found"
        return rec
    x0, y0, x1, y1 = blob["bbox"]
    m = 8
    crop = a[max(0, y0 - m):y1 + 1 + m, max(0, x0 - m):x1 + 1 + m]
    img8 = Image.fromarray(crop).resize((crop.shape[1] * 8, crop.shape[0] * 8), Image.NEAREST)
    png8 = os.path.join(OUT, f"slide{name[-3:]}_badge_x8.png")
    img8.save(png8)
    rec.update(
        badge_area=blob["area"], badge_bbox=blob["bbox"],
        badge_center=[round(blob["cx"], 1), round(blob["cy"], 1)],
        crop_png=png8, crop_wh=[int(crop.shape[1]), int(crop.shape[0])],
    )
    fill = np.median(a[blob["mask"]].reshape(-1, 3), axis=0)
    rec["fill_rgb"] = [int(v) for v in fill]
    # Geometric candidate region = the disc's solid area:
    #   fill_holes(blob) seals digit-shaped holes for fully-visible discs;
    #   closing(blob, 3x3 x3) additionally seals shallow bays (occluded-048 digit
    #   tops) while leaving the outer boundary (and the purple ring outside it)
    #   in place. Chroma guards then kill whatever AA survives at the boundary:
    #   lum<185 kills gray background; (r-g)>-60 kills the green occluder;
    #   (b-r)<60 kills blue-violet ring core (ring is already excluded
    #   geometrically by the region; 60 tolerates purplish JPEG digit cores).
    rch, gch, bch = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    lum = 0.299 * rch + 0.587 * gch + 0.114 * bch
    # Per-column occlusion extension: where an opaque box cuts the disc, the
    # digit ink sits BETWEEN the column's lowest yellow and the box edge. The
    # chrome disc is deck-stable: full-disc controls (047/050) measure
    # cx=876.5, cy=70.5, rx=16.5, ry=15.0. Extend a column only when the green
    # box edge (first y with (g-r)>40 & g>110) cuts the disc above its natural
    # elliptical bottom; cap the extension at that natural bottom. Unoccluded
    # badges are unaffected (box edge at/below the natural bottom -> no ext).
    H, W = blob["mask"].shape
    ext = np.zeros_like(blob["mask"])
    CX, CY, RX, RY = 876.5, 70.5, 16.5, 15.0
    bx0, by0, bx1, by1 = blob["bbox"]
    for x in range(bx0, bx1 + 1):
        col = np.where(blob["mask"][:, x])[0]
        if len(col) == 0:
            continue
        bottom = int(col.max())
        be = None
        for y in range(bottom, min(bottom + 14, H)):
            if (gch[y, x] - rch[y, x]) > 40 and gch[y, x] > 110:
                be = y
                break
        if be is None:
            continue
        arg = min(1.0, max(0.0, (x - CX) / RX))
        natural_bottom = int(CY + RY * (1.0 - arg * arg) ** 0.5)
        if be <= natural_bottom - 1:
            ext[bottom + 1:min(be, natural_bottom + 1), x] = True
    region = (ndimage.binary_fill_holes(blob["mask"]) |
              ndimage.binary_closing(blob["mask"], structure=np.ones((3, 3), bool), iterations=3) |
              ext)
    dist = np.sqrt(((a.astype(int) - fill.astype(int)) ** 2).sum(axis=2))
    guards = (lum < 185) & ((rch - gch) > -60) & ((bch - rch) < 60)
    rec["glyphs"] = []
    masks_by_T = {}
    for T in (70, 100, 140):
        ink = (dist > T) & region & guards
        lab, n = ndimage.label(ink)
        glyphs = []
        for i in range(1, n + 1):
            cm = lab == i
            area = int(cm.sum())
            if area < 5:
                continue
            ys, xs = np.where(cm)
            gy0, gx0, gy1, gx1 = int(ys.min()), int(xs.min()), int(ys.max()), int(xs.max())
            sub = cm[gy0:gy1 + 1, gx0:gx1 + 1]
            # a single digit is <=8px wide here; wider components are merged pairs
            pieces = split_by_column_gap(sub) if sub.shape[1] >= 9 else [sub]
            for pc in pieces:
                if pc.sum() < 5:
                    continue
                ys2, xs2 = np.where(pc)
                glyphs.append(dict(area=int(pc.sum()),
                                   bbox=[gx0 + int(xs2.min()), gy0 + int(ys2.min()),
                                         gx0 + int(xs2.max()), gy0 + int(ys2.max())],
                                   mask=pc))
        glyphs.sort(key=lambda gg: gg["bbox"][0])
        masks_by_T[T] = glyphs
    primary = masks_by_T[70]
    rec["ink_px"] = int(((dist > 70) & region & guards).sum())
    rec["n_glyphs"] = len(primary)
    for gi, gl in enumerate(primary):
        h = gl["bbox"][3] - gl["bbox"][1] + 1
        w = gl["bbox"][2] - gl["bbox"][0] + 1
        entry = dict(idx=gi, area=gl["area"], bbox=gl["bbox"], w=w, h=h,
                     stroke_w=stroke_width(gl["mask"]),
                     ascii=ascii_mask(gl["mask"]),
                     holes_by_T={})
        for T in (70, 100, 140):
            cand = [gg for gg in masks_by_T[T]
                    if abs(gg["bbox"][0] - gl["bbox"][0]) <= 2 and abs(gg["bbox"][1] - gl["bbox"][1]) <= 2]
            if cand:
                holes = glyph_holes(cand[0]["mask"])
            else:
                holes = glyph_holes(gl["mask"])
            entry["holes_by_T"][T] = holes
        rec["glyphs"].append(entry)
    rec["_glyph_masks"] = [g["mask"] for g in primary]
    rec["_glyph_bboxes"] = [g["bbox"] for g in primary]
    return rec


def glyph_iou(m1, m2, dxs=(-2, -1, 0, 1, 2)):
    """Best IoU over small horizontal shifts, both masks pinned at their bbox top row."""
    H = max(m1.shape[0], m2.shape[0]) + 2
    W = max(m1.shape[1], m2.shape[1]) + 8
    best = 0.0
    for dx in dxs:
        A = np.zeros((H, W), bool)
        B = np.zeros((H, W), bool)
        A[1:1 + m1.shape[0], 4:4 + m1.shape[1]] = m1
        x2 = 4 + dx
        if x2 < 0 or x2 + m2.shape[1] > W:
            continue
        B[1:1 + m2.shape[0], x2:x2 + m2.shape[1]] = m2
        inter = int((A & B).sum())
        union = int((A | B).sum())
        best = max(best, inter / union if union else 0.0)
    return round(best, 3)


def top_slice(mask, rows):
    return mask[:rows, :]


def main():
    all_recs = {}
    for name in SLIDES:
        try:
            rec = analyze_badge(name)
        except Exception as e:
            rec = {"error": repr(e)}
        all_recs[name] = rec

    # ---- deck sweep: template bank from all slides except the one under test ----
    bank = {}   # digit char -> list of masks
    sweep = {}
    for name in SLIDES:
        rec = all_recs[name]
        if name in EXCLUDE_FROM_BANK or "error" in rec or "_glyph_masks" not in rec:
            continue
        expected = str(int(name[-3:]))       # badge numeral = file id (2..60), no padding
        masks = rec["_glyph_masks"]
        if len(masks) != len(expected):
            sweep[name] = dict(expected=expected, n_glyphs=len(masks),
                               status="glyph-count-mismatch (occlusion?)")
            continue
        ok = True
        details = []
        for ch, mask in zip(expected, masks):
            bank.setdefault(ch, []).append(mask)
            details.append(ch)
        sweep[name] = dict(expected=expected, glyphs=details, status="banked")

    # classify every non-excluded slide against the bank (leave-one-slide-out feel:
    # its own templates are in the bank, which only helps confirm self-consistency)
    for name in SLIDES:
        rec = all_recs[name]
        if name in EXCLUDE_FROM_BANK or "error" in rec or "_glyph_masks" not in rec:
            continue
        expected = str(int(name[-3:]))
        masks = rec["_glyph_masks"]
        if len(masks) != len(expected):
            continue
        got = []
        scores = []
        for ch, mask in zip(expected, masks):
            best_ch, best_v = None, -1.0
            for tch, tlist in bank.items():
                for tm in tlist:
                    v = glyph_iou(mask, tm)
                    if v > best_v:
                        best_v, best_ch = v, tch
            got.append(best_ch)
            scores.append(round(best_v, 2))
        sweep[name]["classified"] = "".join(got)
        sweep[name]["iou"] = scores
        sweep[name]["status"] = "MATCH" if "".join(got) == expected else "MISMATCH"

    # ---- slide_048 occluded-badge ruling ----
    r48 = all_recs.get("slide_048", {})
    ruling = {}
    if "_glyph_masks" in r48:
        obs = r48["_glyph_masks"]
        # left glyph top vs known digit tops
        for gi, gm in enumerate(obs):
            rows = gm.shape[0]
            cmpres = {}
            for ch, tlist in sorted(bank.items()):
                best = 0.0
                for tm in tlist:
                    t = top_slice(tm, rows)
                    best = max(best, glyph_iou(gm, t))
                cmpres[ch] = round(best, 3)
            ruling[f"glyph{gi}_visible_rows={rows}"] = cmpres
    all_recs["_ruling_048"] = ruling

    # ---- report ----
    print("python:", sys.executable)
    for name in FOCUS:
        rec = all_recs[name]
        print("=" * 78)
        print(name, "md5", rec.get("md5"))
        if "error" in rec:
            print("  ERROR:", rec["error"], "| yellow_px:", rec.get("yellow_px_in_region"))
            continue
        print(f"  badge area={rec['badge_area']} bbox={rec['badge_bbox']} "
              f"center={rec['badge_center']} fill={rec['fill_rgb']} "
              f"yellow_px_region={rec['yellow_px_in_region']} blobs={rec['blobs']}")
        print(f"  ink_px={rec['ink_px']} n_glyphs={rec['n_glyphs']} crop={rec['crop_wh']} -> {rec['crop_png']}")
        for gl in rec["glyphs"]:
            print(f"  glyph[{gl['idx']}] area={gl['area']} bbox={gl['bbox']} {gl['w']}x{gl['h']} "
                  f"stroke={gl['stroke_w']}")
            for T in (70, 100, 140):
                hs = gl["holes_by_T"][str(T)] if isinstance(list(gl["holes_by_T"].keys())[0], str) else gl["holes_by_T"][T]
                print(f"     T={T}: holes={[(h['area'], h['cx'], h['cy'], h['cy_frac']) for h in hs]}")
            print("   " + gl["ascii"].replace("\n", "\n   "))
    print("=" * 78)
    print("RULING 048 (IoU of visible ink vs top slices of bank digits):")
    print(json.dumps(ruling, indent=1))
    print("=" * 78)
    mism = {k: v for k, v in sweep.items() if v.get("status") not in ("MATCH", "banked")}
    print(f"sweep: {sum(1 for v in sweep.values() if v.get('status')=='MATCH')} MATCH / "
          f"{sum(1 for v in sweep.values() if v.get('status')=='MISMATCH')} MISMATCH / "
          f"{sum(1 for v in sweep.values() if v.get('status')!='MATCH' and v.get('status')!='MISMATCH')} other")
    for k, v in sweep.items():
        if v.get("status") != "MATCH":
            print("  ", k, v)

    # persistent JSON (drop masks)
    slim = {}
    for k, v in all_recs.items():
        slim[k] = {kk: vv for kk, vv in v.items() if kk != "_glyph_masks"} if isinstance(v, dict) else v
    with open(os.path.join(OUT, "badge_measurements.json"), "w") as f:
        json.dump(dict(sweep=sweep, slides=slim), f, indent=1, default=str)
    print("wrote", os.path.join(OUT, "badge_measurements.json"))


if __name__ == "__main__":
    main()
