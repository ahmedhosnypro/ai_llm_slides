import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).parent
rng = np.random.default_rng(42)

def shell(xmax, ymax, ymin=0):
    fig, ax = plt.subplots(figsize=(7.46, 5.625), dpi=200)
    ax.set(xlim=(0, xmax), ylim=(ymin, ymax))
    ax.grid(color="#D9D9D9", linewidth=.6)
    ax.tick_params(labelsize=9)
    return fig, ax

fig, ax = shell(40, 40, -10)
clusters = [(11,20,7,8,350,"#0000FF"),(22.5,19.5,3.5,3,180,"#FF0000"),(33,22,4,6,350,"#00FFFF"),(9.5,11,3.5,2.5,100,"#FFFF00"),(18.5,4,7.5,6,500,"#FF00FF"),(9,2,3,2.5,100,"#00FF00"),(32.7,5.7,3.5,5.5,300,"#000000")]
for cx,cy,sx,sy,n,c in clusters:
    ax.scatter(rng.normal(cx,sx/2,n),rng.normal(cy,sy/2,n),s=18,c=c,edgecolors="none")
fig.savefig(OUT/"slide_042_graph.png",dpi=200,bbox_inches="tight",pad_inches=.08)
plt.close(fig)

fig, ax = shell(50,30)
for cx,cy,sx,sy,n,c in [(11,20,2.5,2.5,70,"#000000"),(19,19,2,2.5,100,"#FF00FF")]:
    ax.scatter(rng.normal(cx,sx/2,n),rng.normal(cy,sy/2,n),s=24,c=c,edgecolors="none")
a=rng.uniform(0,2*np.pi,500); r=rng.uniform(3.2,6.0,500)
ax.scatter(17.5+r*np.cos(a),9.5+.72*r*np.sin(a),s=18,c="#00FF00",edgecolors="none")
ax.scatter(rng.normal(17.8,1.0,60),rng.normal(9.3,.6,60),s=22,c="#00FFFF",edgecolors="none")
a=rng.uniform(-1.9,1.9,350); r=rng.uniform(2.5,7.5,350)
ax.scatter(33.5+r*np.cos(a),16.5+.55*r*np.sin(a),s=20,c="#0000FF",edgecolors="none")
for x in np.arange(27,44,2.5):
    for y in np.arange(8,23,2.5): ax.scatter(x,y,s=24,c="#FF0000",edgecolors="none")
ax.annotate("",xy=(30,20),xytext=(28.5,21),arrowprops={"arrowstyle":"->","color":"black","lw":1})
fig.savefig(OUT/"slide_044_graph.png",dpi=200,bbox_inches="tight",pad_inches=.08)
plt.close(fig)
