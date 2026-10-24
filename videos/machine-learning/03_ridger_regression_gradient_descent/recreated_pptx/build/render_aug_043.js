// PIL renderer for slide 043's middle-left "Augmented Vectors" content:
// header row x1..x6, 6 parenthesised stacked column vectors, class row.
// Deck law: equations/vetors are PIL/matplotlib-rendered transparent PNGs.
const fs = require("fs");
const { execFileSync } = require("child_process");

const DIR = __dirname + "/assets";
const PX = 4;                 // render scale: 1 frame px -> 4 device px
const OUT = DIR + "/aug_043.png";

// measured geometry (frame px)
const COLS = [99, 122, 144, 165, 189, 212];   // column centres
const VEC_TOP = 183, VEC_BOT = 223;           // stacked vector ink span
const CLS_Y = 233;                            // class-row cap top
const X0 = 86, X1 = 232, Y0 = 182, Y1 = 242;  // crop placed onto the slide

const cols = [
  ["1", "1", "1"], ["1", "2", "1"], ["1", "1", "2"],
  ["1", "5", "4"], ["1", "6", "5"], ["1", "6", "6"],
];
const cls = ["C1", "C1", "C1", "C2", "C2", "C2"];

// find a usable DejaVu Sans (ships with matplotlib / PIL-friendly, mathtext family)
let FONT = null;
for (const c of [
  "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
  "/usr/share/fonts/dejavu/DejaVuSans.ttf",
]) { if (fs.existsSync(c)) { FONT = c; break; } }
if (!FONT) {
  const m = execFileSync("python3", ["-c",
    "import matplotlib,os;print(os.path.join(os.path.dirname(matplotlib.__file__),'mpl-data','fonts','ttf','DejaVuSans.ttf'))"],
    { encoding: "utf8" }).trim();
  FONT = m;
}
const BOLD = FONT.replace("DejaVuSans.ttf", "DejaVuSans-Bold.ttf");

const py = `
from PIL import Image, ImageDraw, ImageFont
S=${PX}
COLS=${JSON.stringify(COLS)}
COLS_V=${JSON.stringify(cols)}
CLS=${JSON.stringify(cls)}
COLORS=${JSON.stringify(["#C00000", "#C00000", "#C00000", "#0000FF", "#0000FF", "#0000FF"])}
FONT=r'''${FONT}'''
BOLD=r'''${BOLD}'''
W=(${X1}-${X0}+1)*S; H=(${Y1}-${Y0}+1)*S
img=Image.new("RGBA",(W,H),(0,0,0,0))
d=ImageDraw.Draw(img)
f=lambda pt: ImageFont.truetype(FONT, int(round(pt*S)))
fb=lambda pt: ImageFont.truetype(BOLD, int(round(pt*S)))
VT,VB=${VEC_TOP},${VEC_BOT}
CY=(VT+VB)//2
def cell(txt,pt,cx,cy,col,bold=False):
    ft=fb(pt) if bold else f(pt)
    bb=d.textbbox((0,0),txt,font=ft)
    tw,th=bb[2]-bb[0],bb[3]-bb[1]
    d.text(((cx-${X0})*S-(tw/2)-bb[0], (cy-${Y0})*S-(th/2)-bb[1]), txt, font=ft, fill=col)
# 6 stacked column vectors: ( a ; b ; c ) with tall parens flanking the digits
for i,c in enumerate(COLS):
    cx=COLS[i]
    top,bot=VT,VB
    vals=COLS_V[i]
    n=len(vals)
    step=(bot-top-10)//(n-1) if n>1 else 0
    ys=[top+5+k*step for k in range(n)] if n>1 else [CY]
    for v,yy in zip(vals,ys):
        cell(v,11,cx,yy,"#000000")
    OFF=7          # frame px from column centre to each paren stroke
    for ch,poff in (("(",-OFF),(")",OFF)):
        ft=f(bot-top)                       # render the glyph as tall as the span
        bb=d.textbbox((0,0),ch,font=ft)
        big=Image.new("RGBA",(max(4,bb[2]-bb[0]+4), max(4,bb[3]-bb[1]+4)),(0,0,0,0))
        ImageDraw.Draw(big).text((-bb[0]+2,-bb[1]+2),ch,font=ft,fill="#000000")
        th=int(round((bot-top)*S))
        tw=max(2,int(round(0.10*S)))        # ~3 frame px wide, height spans the vector
        big=big.resize((tw,th),Image.LANCZOS)
        img.paste(big,(int(round((cx+poff-${X0})*S)),int(round((top-${Y0})*S))),big)
# class row
for i,c in enumerate(CLS):
    cell(c,12,COLS[i],${CLS_Y}+5,COLORS[i],bold=True)
img.save(r'''${OUT}''')
print("WROTE",r'''${OUT}''', img.size)
`;
fs.writeFileSync(DIR + "/_render_aug.py", py);
execFileSync("python3", [DIR + "/_render_aug.py"], { stdio: "inherit" });
console.log("AUG_IMG ok");
