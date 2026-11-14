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
clusters = [(10,22,5,3,350,"#0000FF"),(22,23,3,1.5,180,"#FF0000"),(33,22,3,4,350,"#00FFFF"),(7,12,2,1,100,"#FFFF00"),(18,8,8,3,500,"#FF00FF"),(6,3,2,1,100,"#00FF00"),(33,7,3,3,300,"#000000")]
for cx,cy,sx,sy,n,c in clusters:
    ax.scatter(rng.normal(cx,sx/2,n),rng.normal(cy,sy/2,n),s=18,c=c,edgecolors="none")
fig.savefig(OUT/"slide_042_graph.png",dpi=200,bbox_inches="tight",pad_inches=.08)
plt.close(fig)

fig, ax = shell(50,30)
for cx,cy,sx,sy,n,c in [(11,20,2.5,2.5,70,"#000000"),(19,19,2,2.5,100,"#FF00FF")]:
    ax.scatter(rng.normal(cx,sx/2,n),rng.normal(cy,sy/2,n),s=24,c=c,edgecolors="none")
a=rng.uniform(0,2*np.pi,500); r=rng.uniform(2.2,4.2,500)
ax.scatter(13+r*np.cos(a),9+.75*r*np.sin(a),s=18,c="#00FF00",edgecolors="none")
ax.scatter(rng.normal(13,.7,50),rng.normal(9.5,.5,50),s=22,c="#00FFFF",edgecolors="none")
a=rng.uniform(-1.3,1.3,300); r=rng.uniform(1.5,3.5,300)
ax.scatter(32+r*np.cos(a),16+r*np.sin(a),s=20,c="#0000FF",edgecolors="none")
for x in np.arange(27,44,2.5):
    for y in np.arange(8,23,2.5): ax.scatter(x,y,s=24,c="#FF0000",edgecolors="none")
ax.annotate("",xy=(30,20),xytext=(28.5,21),arrowprops={"arrowstyle":"->","color":"black","lw":1})
fig.savefig(OUT/"slide_044_graph.png",dpi=200,bbox_inches="tight",pad_inches=.08)
plt.close(fig)
