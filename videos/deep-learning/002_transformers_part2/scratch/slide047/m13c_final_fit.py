#!/usr/bin/env python3
"""m13c_final_fit.py — DEFINITIVE chrome re-fit on slide_047.jpg.

Landmarks are the CORE (darkest) pixel of each chrome border, read off the raw
profiles printed by m13b (its count-based picks were 1px bleed):
  L core x=58  (113,41,53)   R core x=901 (121,48,29)
  T core y=43  (108,47,55)   B core y=516/517 (191,93,108)/(116,8,24)
Chrome model: panel x 42..918 pt, y 45..540 pt -> sx=(fx-OX)/SX, sy=fy/SY.
"""
SX = (901 - 58) / (918 - 42)
OX = 58 - SX * 42
SY = 43 / 45.0
print(f'landmarks: L=58 R=901 T=43 B=516 (frame px, core pixels; B ink spans 516-517)')
print(f'FIT: SX={SX:.6f}  OX={OX:.3f}  SY={SY:.6f}  OY=0')
print(f'B check: 516/SY={516/SY:.2f}  517/SY={517/SY:.2f}  (panel bottom = 540)')
print()
for name, (SXp, OXp, SYp) in {
    'deck-given (0.961232,17.628,0.955556)': (0.961232, 17.628, 0.955556),
    '045-certif (0.962329,17.582,0.955556)': (0.962329, 17.582, 0.955556),
    'THIS-FIT   (0.962329,17.582,0.955556)': (SX, OX, SY),
}.items():
    e = lambda fx, s: OXp + SXp * s - fx
    print(f'{name}: errL {e(58,42):+.2f} errR {e(901,918):+.2f} errT {SYp*45-43:+.2f} errB {SYp*540-516:+.2f} (px)')
print()
sx = lambda fx: (fx - OX) / SX
sy = lambda fy: fy / SY
print('round-trip: fx(42)=%.2f fx(918)=%.2f fy(45)=%.2f fy(540)=%.2f' %
      (OX + SX * 42, OX + SX * 918, SY * 45, SY * 540))
badge_cx, badge_cy, badge_d = 879.5, 71.0, 35.0
print(f'badge (frame): center ({badge_cx},{badge_cy}) d~{badge_d} -> slide pts: '
      f'cx {sx(badge_cx):.1f} cy {sy(badge_cy):.1f} d {badge_d/SX:.1f}'
      '  [house chrome law draws it at (893,71) d36 — chrome law WINS, frame position is a curation artifact]')
