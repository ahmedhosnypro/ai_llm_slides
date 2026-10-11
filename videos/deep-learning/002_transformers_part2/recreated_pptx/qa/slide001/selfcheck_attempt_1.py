#!/usr/bin/env python3
"""PIL geometry comparison — 002 slide-001 PLACEHOLDER cover vs 001's CERTIFIED cover render.

Context (placeholder-cover law, founder directive 2026-10-11): 002 slide 001 has NO
ground-truth frame; it mirrors 001's certified cover. Its render is therefore compared
against 001's certified 150dpi render (videos/deep-learning/001_transformers_part1/
recreated_pptx/qa/slide001/render_1.png). Per dispatch: title/logo/chrome geometric
positions must match within ~4 render px; deltas documented below.

Both renders: 150 dpi, 2001x1125 px (1 render px = 1/200 in; frame px = render px * 72/150).
"""
import numpy as np
from PIL import Image

MINE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide001/render_1.png"
REF = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide001/render_1.png"

TOL = 4  # render px, per dispatch


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(int)


def bbox_of(mask):
    ys, xs = np.where(mask)
    if not len(xs):
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def red_ink(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return (r > 120) & (g < 110) & (b < 110)


def blue_ink(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return (r < 110) & (g < 110) & (b > 90)


def gray_ink(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return (np.abs(r - 184) < 30) & (np.abs(g - 184) < 30) & (np.abs(b - 184) < 30)


def components_rows(mask, gap=5):
    """Split a 2D mask into row-bands separated by >=gap empty rows; return bboxes."""
    rows = np.where(mask.any(axis=1))[0]
    if not len(rows):
        return []
    bands, s, p = [], rows[0], rows[0]
    for i in rows[1:]:
        if i > p + gap:
            bands.append((s, p))
            s = i
        p = i
    bands.append((s, p))
    out = []
    for (y0, y1) in bands:
        sub = mask[y0:y1 + 1]
        xs = np.where(sub.any(axis=0))[0]
        out.append((int(xs.min()), int(y0), int(xs.max()), int(y1)))
    return out


def window(mask, x0, y0, x1, y1):
    return mask[y0:y1, x0:x1]


def measure(im):
    """All geometry measurements on one render. Returns dict name -> bbox (x0,y0,x1,y1)."""
    m = {}
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

    # --- chrome: gray panel extent (sample a text-free row band near the bottom)
    gray = (np.abs(r - 233) < 16) & (np.abs(g - 233) < 16) & (np.abs(b - 231) < 18)
    band = gray[1000:1100, :]
    cols = np.where(band.sum(axis=0) > 90)[0]
    m["panel_x"] = (int(cols.min()), None, int(cols.max()), None)
    bandc = gray[:, 110:220]
    rows = np.where(bandc.sum(axis=1) > 90)[0]
    m["panel_y"] = (None, int(rows.min()), None, int(rows.max()))

    # --- chrome: badge yellow disc
    yel = (r > 200) & (g > 200) & (b < 190)
    bb = bbox_of(window(yel, 1770, 70, 1950, 230))
    if bb:
        m["badge"] = (bb[0] + 1770, bb[1] + 70, bb[2] + 1770, bb[3] + 70)

    # --- title: red ink band (exclude panel border strokes at x~88 and x~1913)
    tmask = window(red_ink(im), 150, 240, 1850, 580)
    bands = components_rows(tmask, gap=5)
    if len(bands) >= 2:
        m["title_L1"] = (bands[0][0] + 150, bands[0][1] + 240, bands[0][2] + 150, bands[0][3] + 240)
        m["title_L2"] = (bands[1][0] + 150, bands[1][1] + 240, bands[1][2] + 150, bands[1][3] + 240)

    # --- credit block: red "Prepared By"
    cmask = window(red_ink(im), 699, 600, 1449, 700)
    bb = bbox_of(cmask)
    if bb:
        m["credit_preparedby"] = (bb[0] + 699, bb[1] + 600, bb[2] + 699, bb[3] + 600)
    # credit name + email: blue ink, row-split
    nmask = window(blue_ink(im), 699, 640, 1449, 800)
    bands = components_rows(nmask, gap=5)
    if len(bands) >= 2:
        m["credit_name"] = (bands[0][0] + 699, bands[0][1] + 640, bands[0][2] + 699, bands[0][3] + 640)
        m["credit_email"] = (bands[1][0] + 699, bands[1][1] + 640, bands[1][2] + 699, bands[1][3] + 640)

    # --- instructors block: red heading
    hmask = window(red_ink(im), 105, 832, 795, 915)
    bb = bbox_of(hmask)
    if bb:
        m["instr_heading"] = (bb[0] + 105, bb[1] + 832, bb[2] + 105, bb[3] + 832)
    # items: blue ink, row-split (4 lines: name/email/name/email)
    imask = window(blue_ink(im), 150, 895, 1100, 1110)
    bands = components_rows(imask, gap=5)
    names = ["instr_name1", "instr_email1", "instr_name2", "instr_email2"]
    for nm, bd in zip(names, bands[:4]):
        m[nm] = (bd[0] + 150, bd[1] + 895, bd[2] + 150, bd[3] + 895)

    # --- logo lockup: ink that differs from the panel gray, in the logo window
    logowin = im[970:1100, 1230:1895]
    ink = (np.abs(logowin[:, :, 0] - 233) > 12) | (np.abs(logowin[:, :, 1] - 233) > 12) | \
          (np.abs(logowin[:, :, 2] - 231) > 12)
    bb = bbox_of(ink)
    if bb:
        m["logo"] = (bb[0] + 1230, bb[1] + 970, bb[2] + 1230, bb[3] + 970)

    # --- crosshair '+' artifact
    xmask = window(gray_ink(im), 330, 390, 420, 460)
    bb = bbox_of(xmask)
    if bb:
        m["crosshair"] = (bb[0] + 330, bb[1] + 390, bb[2] + 330, bb[3] + 390)

    return m


def main():
    mine, ref = load(MINE), load(REF)
    print(f"mine: {mine.shape[1]}x{mine.shape[0]}  ref: {ref.shape[1]}x{ref.shape[0]}")
    mm, rm = measure(mine), measure(ref)

    keys = sorted(set(mm) | set(rm))
    print(f"\n{'element':<20} {'mine (x0,y0,x1,y1)':<26} {'ref (x0,y0,x1,y1)':<26} delta(px) verdict")
    all_ok = True
    for k in keys:
        a, b_ = mm.get(k), rm.get(k)
        if a is None or b_ is None:
            print(f"{k:<20} MISSING (mine={a}, ref={b_})")
            all_ok = False
            continue
        d = [abs(a[i] - b_[i]) for i in range(4) if a[i] is not None and b_[i] is not None]
        ok = all(x <= TOL for x in d)
        all_ok = all_ok and ok
        print(f"{k:<20} {str(a):<26} {str(b_):<26} {str(d):<10} {'OK' if ok else 'FAIL'}")

    # full-image pixel diff
    if mine.shape == ref.shape:
        diff = np.abs(mine - ref).sum(axis=2)
        n = int((diff > 0).sum())
        print(f"\nfull-image diff: {n} / {diff.shape[0]*diff.shape[1]} px differ "
              f"({100.0*n/(diff.shape[0]*diff.shape[1]):.4f}%)")
        if n:
            ys, xs = np.where(diff > 0)
            print(f"  differing region bbox: x {xs.min()}-{xs.max()}, y {ys.min()}-{ys.max()}")
            mx = int(diff.max())
            print(f"  max channel-sum abs diff: {mx}")
    else:
        print("shape mismatch — cannot full-diff")

    print("\nSELF-CHECK:", "PASS" if all_ok else "FAIL", f"(tolerance {TOL} render px per element edge)")
    raise SystemExit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
