#!/usr/bin/env python3
"""Write the 7 zoom prompts to scratch files."""
import os
D = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013/zoom_prompts'
os.makedirs(D, exist_ok=True)

P = {}
P['zoom_title'] = """Zoom of the TITLE area of a lecture slide (two bold lines). Report:
1. Quote LINE 1 exactly, word for word. Which words are black and which are blue?
2. Quote LINE 2 exactly, character for character as printed (including every parenthesis, even if unbalanced). Which characters are RED (X symbols? subscript digits?)? Are the digits real subscripts (smaller, lowered)?
3. Font: sans or serif? Bold? Which line is larger?
4. Any other marks in this strip?"""

P['zoom_left'] = """Zoom of the LEFT part of a self-attention lecture slide (frame pixels 55..290 x, 160..435 y, upscaled 2x). Report precisely:
1. The large translucent blue-gray ellipse at left: how many rows of content inside it? Each row: how many small cells, their colors (approx hex), any text/label inside the row (quote it, give color)? Red arrows exiting rows to the right: how many, from which rows?
2. The bright green ellipse to its right: does it contain bordered rectangles/boxes, or only text drawn directly on the green? Quote the exact text of each label top to bottom (watch subscripts like k and superscripts like (r) vs (1) vs others — say exactly what glyphs you see), and the label color (approx hex).
3. Yellow shapes peeking at the left edge of the green ellipse: what are they (cells? box edges?), how many, where (which rows)?
4. The K labels at/near the green ellipse's right edge: quote each exactly (subscripts?), their color, and describe any small cell stacks (vectors) attached: how many cells, colors, which row each belongs to.
5. Any dashed curves or arrows connecting the blue-gray ellipse upward/downward to other elements."""

P['zoom_circles'] = """Zoom of the CENTER part of a self-attention lecture slide (frame pixels 440..650 x, 220..400 y, upscaled 2x). Report precisely:
1. The small circular nodes in this view: how many? Arrangement — vertical line, or diagonal staircase (drifting right as you go down)? For EACH node top to bottom: approx center position in the image, diameter px, fill color, border color, and the symbol inside (times X? asterisk? something else) and its color.
2. Red arrows connecting the nodes to each other: from which node to which, directions.
3. Red arrows entering from the LEFT edge (from the tall purple block) and from the RIGHT edge: which node does each attach to?
4. Red arrows leaving each node upward: where do they go (toward the sigma box at top-left?).
5. The tall purple/lavender block at the left edge: text color, orientation of its text.
6. Anything else visible (partial yellow band at right, labels). Approx hex colors for everything."""

P['zoom_top'] = """Zoom of the TOP-CENTER part of a self-attention lecture slide (frame pixels 480..700 x, 105..200 y, upscaled 2x). Report precisely:
1. The dashed-border box near the top: border color, dash style; fill — empty peach, or does it contain small colored cells (how many, colors)? Any text/label inside it: exact text, color, and its position within the box (left/center/right).
2. The green shape below the box: exact shape (block arrow pointing up? triangle? diamond?), colors, and whether there is a small red arrowhead on it and a thin gray line anywhere.
3. The horizontal light-blue box lower: fill hex, and the big glyph inside it (sigma?): color, approx size.
4. The white pill above that box: text (exact), color.
5. Any other marks (arrow stubs entering/leaving the sigma box). Approx hex for everything."""

P['zoom_right'] = """Zoom of the RIGHT part of a self-attention lecture slide (frame pixels 600..900 x, 190..420 y, upscaled 2x). Report precisely:
1. The yellow vertical band (center of this view): does it hold bordered rectangles/boxes? Border color? Quote the text inside EACH box top to bottom exactly (watch subscript letters like v and superscripts like (r) vs (1) vs (2)(3)(4) — say exactly which glyphs), text color (approx hex).
2. Left of the band: red labels (V with subscript digits) — quote EACH top to bottom with its subscript; next to each, a small 2-cell colored vector (cell colors?); red arrows from the vectors pointing LEFT toward the multiply nodes: how many, from which rows?
3. The dashed-green rounded container at the right: border color, fill (empty peach?), how many rows inside, cells per row, cell colors per row, the red X labels (quote each with subscript digit), and any arrows exiting the container leftward.
4. Below the container: any thin dashed curves/arrows going down/left (to the dimension note?). Approx hex for everything."""

P['zoom_bottom'] = """Zoom of the BOTTOM strip of a self-attention lecture slide (frame pixels 60..900 x, 405..516 y, upscaled 2x; wide image, two halves). Report precisely:
LEFT HALF (frame x 60..500):
1. The rounded container with dashed green border: fill (peach/empty or pale green?), how many rows of small cells inside, cells per row, cell colors per row (left to right), and the red X labels (quote each with its subscript digit, left-to-right order).
2. A dashed highlight box around ONE of the rows: which row (position 1-4 top to bottom), highlight color, dash style.
3. A thick red shape near the bottom pointing up at that row: describe it (arrow? cursor?) — is it an annotation overlay rather than a slide shape?
4. Any arrow leaving the container's top edge upward (to what?).
RIGHT HALF (frame x 700..900):
5. The dashed-green rounded box: contents left to right — a small cell stack (how many cells, colors) with a label under/next to it (quote exactly, e.g. 1*d); an arrow; a square with a letter inside (square fill + border + letter color); a label beneath the square (quote exactly, e.g. d*d); an equals sign; another cell stack with label; then a caption line below (quote exactly, e.g. d: Embedding Length) and its color.
6. Any arrows/curves connecting the right container (above) down into this box.
Give approx hex for everything and positions (left/center/right, top/middle/bottom)."""

P['zoom_dp'] = """Zoom of the 'Dot Product' stage of a self-attention lecture slide (frame pixels 250..400 x, 140..500 y, upscaled 2x). Report precisely:
1. The gray box: fill hex, border color, approx position.
2. Text at the box's top-left: quote exactly, how many lines, color.
3. Text at the box's top-right: quote exactly. Is it a single 'K.q' label at the top-right, or are there separate labels near EACH dot (like K_1.q, K_2.q, K_3.q, K_4.q)? Color.
4. The dots inside the box: how many, arrangement (diagonal staircase?), each dot's core color + halo (outer ring) color, approx diameter.
5. Red arrows: between dots (which direction?), entering the box's left edge from outside, exiting the right edge toward the purple block — describe each with its endpoints.
6. BELOW the box: a red label (q with subscript 2?), a tiny 2-cell colored vector (cell colors), and a white box with red border (quote the text inside, its color); red arrows connecting these up into the gray box.
7. The white pill ABOVE the box: text, color.
Approx hex for everything."""

for name, txt in P.items():
    with open('%s/%s.txt' % (D, name), 'w') as f:
        f.write(txt)
print('wrote', len(P), 'prompts to', D)
