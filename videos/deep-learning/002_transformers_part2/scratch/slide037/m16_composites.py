#!/usr/bin/env python3
"""Stack related crops into labeled composite probe images (2x zoom preserved)."""
from PIL import Image, ImageDraw

def stack(name, parts, sep=14):
    imgs = [Image.open(p) for p, _ in parts]
    w = max(i.size[0] for i in imgs)
    labels = [t for _, t in parts]
    H = sum(i.size[1] for i in imgs) + sep * (len(imgs) - 1) + 18 * len(imgs)
    out = Image.new("RGB", (w, H), (255, 255, 255))
    d = ImageDraw.Draw(out)
    y = 0
    for i, (im, lab) in enumerate(zip(imgs, labels)):
        d.rectangle([0, y, w, y + 16], fill=(180, 0, 0))
        d.text((6, y + 2), lab, fill=(255, 255, 255))
        y += 18
        out.paste(im, (0, y))
        y += im.size[1]
        if i < len(imgs) - 1:
            d.rectangle([0, y, w, y + sep - 1], fill=(0, 0, 0))
            y += sep
    out.save(name)
    print(name, out.size)

stack("probe_A_encoder.png", [
    ("crop_enc_stack.png", "A1: ENCODER CONTAINER x628-742 y253-420 (frame px)"),
    ("crop_enc_pe.png",    "A2: ENCODER PE/EMBED/INPUTS x575-745 y370-505"),
    ("crop_enc_nx.png",    "A3: ENCODER Nx CIRCLE x580-655 y300-375"),
])
stack("probe_B_decoder.png", [
    ("crop_dec_top.png",  "B1: DECODER TOP x728-862 y100-210"),
    ("crop_dec_stack.png","B2: DECODER STACK x733-852 y190-320"),
    ("crop_dec_mid.png",  "B3: DECODER MID x733-852 y285-425"),
])
stack("probe_C_pe.png", [
    ("crop_dec_pe.png", "C1: DECODER PE/EMBED/OUTPUTS x735-900 y395-505"),
])
stack("probe_D_overlays.png", [
    ("crop_highlight.png", "D1: RED HIGHLIGHT CIRCLE + GLOW x625-775 y305-465"),
    ("crop_pin.png",       "D2: WE ARE HERE PIN x570-700 y145-295"),
])
stack("probe_E_left_brace.png", [
    ("crop_left_top.png", "E1: LEFT INSET HEADER+TOP x48-215 y220-335"),
    ("crop_brace.png",    "E2: h BRACE x470-545 y240-430"),
])
