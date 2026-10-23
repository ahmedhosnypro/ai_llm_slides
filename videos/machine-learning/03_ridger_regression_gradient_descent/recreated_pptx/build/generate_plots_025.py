#!/usr/bin/env python3
"""Generate 4 3D surface plots for slide 025 - Types of Loss function shapes.

Original frame: 960x540, 1px = 1pt = 1/72 in
Slide: LAYOUT_WIDE 13.333 x 7.5 in

Plot positions (frame px, from PIL measurement):
- Top-left (concave dome): x ~60-450, y ~100-280 -> w=390, h=180 px
- Top-right (convex bowl): x ~500-890, y ~100-280 -> w=390, h=180 px
- Bottom-left (non-convex): x ~60-450, y ~280-520 -> w=390, h=240 px
- Bottom-right (gradient descent): x ~500-890, y ~280-520 -> w=390, h=240 px

Converted to inches at 300 dpi for matplotlib:
Each plot at 300 dpi: w_in = w_px/72, h_in = h_px/72
Then render at 300 dpi -> px = w_in * 300 = w_px * 300/72 = w_px * 4.167
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import os

OUTDIR = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets"
os.makedirs(OUTDIR, exist_ok=True)

# Frame px dimensions (1px = 1pt = 1/72 in)
PLOT_W_PX = 390
PLOT_H_TOP = 180
PLOT_H_BOTTOM = 240
DPI = 300

# Convert to inches for matplotlib figure size
w_in = PLOT_W_PX / 72.0
h_top_in = PLOT_H_TOP / 72.0
h_bot_in = PLOT_H_BOTTOM / 72.0

# Jet/rainbow colormap (MATLAB-style)
jet = plt.get_cmap('jet')

# ============================================================
# Plot 1: Top-Left - Concave Dome (One Maximum)
# z = -(x^2 + y^2) scaled - inverted bowl = dome
# Red horizontal lines at upper portion (maxima)
# Axis ticks: vertical (z) 0, 5, 2; horizontal (x/y) -2
# ============================================================
fig = plt.figure(figsize=(w_in, h_top_in), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.view_init(elev=30, azim=-60)

# Generate dome surface
x = np.linspace(-2, 2, 50)
y = np.linspace(-2, 2, 50)
X, Y = np.meshgrid(x, y)
# Concave: z = 5 - (x^2 + y^2)*1.25  -> max 5 at center, 0 at edges
Z = 5 - (X**2 + Y**2) * 1.25
Z = np.clip(Z, 0, 5)

# Plot with jet colormap
surf = ax.plot_surface(X, Y, Z, cmap=jet, rstride=1, cstride=1,
                       linewidth=0, antialiased=True, shade=True)

# Red horizontal reference lines at upper portion (z=4 and z=3.5)
# Draw lines at constant z across the surface
for z_line in [4.0, 3.5]:
    # Line across x at y=0
    x_line = np.linspace(-2, 2, 100)
    y_line = np.zeros_like(x_line)
    z_line_arr = np.full_like(x_line, z_line)
    ax.plot(x_line, y_line, z_line_arr, color='red', linewidth=1.5, zorder=10)
    # Line across y at x=0
    y_line2 = np.linspace(-2, 2, 100)
    x_line2 = np.zeros_like(y_line2)
    ax.plot(x_line2, y_line2, z_line_arr, color='red', linewidth=1.5, zorder=10)

# Axis formatting
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(0, 5)
ax.set_xticks([-2])
ax.set_yticks([-2])
ax.set_zticks([0, 2, 5])
ax.set_xlabel('', color='black', fontsize=8)
ax.set_ylabel('', color='black', fontsize=8)
ax.set_zlabel('', color='black', fontsize=8)

# Style
for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    axis._axinfo['grid'].update(color='#DDDDDD', linewidth=0.5)
    axis.line.set_linewidth(0.5)

# Tick labels
for t in (ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()):
    t.set_fontsize(7)
    t.set_color('#444444')

# Remove axis lines/panes for clean look
ax.xaxis.set_tick_params(pad=-2)
ax.yaxis.set_tick_params(pad=-2)
ax.zaxis.set_tick_params(pad=-2)

plt.savefig(os.path.join(OUTDIR, 'plot_025_tl.png'), dpi=DPI, facecolor='white', bbox_inches='tight', pad_inches=0)
plt.close(fig)
print("Generated plot_025_tl.png")

# ============================================================
# Plot 2: Top-Right - Convex Bowl (One Minimum)
# z = (x^2 + y^2) scaled
# Red horizontal lines at lower portion (minima)
# Axis: vertical (z) ×10^4 ticks 1.5, 0.5; horizontal -100 to 100
# ============================================================
fig = plt.figure(figsize=(w_in, h_top_in), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.view_init(elev=30, azim=-60)

x = np.linspace(-100, 100, 50)
y = np.linspace(-100, 100, 50)
X, Y = np.meshgrid(x, y)
# Convex bowl: z = (x^2 + y^2) * 1e-4 * 1.5  -> min 0, max ~3 at corners
# Scale to match ×10^4 axis: z in units of 10^4
Z = (X**2 + Y**2) * 1.5e-4

surf = ax.plot_surface(X, Y, Z, cmap=jet, rstride=1, cstride=1,
                       linewidth=0, antialiased=True, shade=True)

# Red horizontal lines at lower portion (z=0.5 and z=0.2 in 10^4 units)
for z_line in [0.5, 0.2]:
    x_line = np.linspace(-100, 100, 100)
    y_line = np.zeros_like(x_line)
    z_line_arr = np.full_like(x_line, z_line)
    ax.plot(x_line, y_line, z_line_arr, color='red', linewidth=1.5, zorder=10)
    y_line2 = np.linspace(-100, 100, 100)
    x_line2 = np.zeros_like(y_line2)
    ax.plot(x_line2, y_line2, z_line_arr, color='red', linewidth=1.5, zorder=10)

ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_zlim(0, 1.5)
ax.set_xticks([-100, 0, 100])
ax.set_yticks([-100, 0, 100])
ax.set_zticks([0, 0.5, 1.5])

for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    axis._axinfo['grid'].update(color='#DDDDDD', linewidth=0.5)
    axis.line.set_linewidth(0.5)

for t in (ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()):
    t.set_fontsize(7)
    t.set_color('#444444')

plt.savefig(os.path.join(OUTDIR, 'plot_025_tr.png'), dpi=DPI, facecolor='white', bbox_inches='tight', pad_inches=0)
plt.close(fig)
print("Generated plot_025_tr.png")

# ============================================================
# Plot 3: Bottom-Left - Non-Convex (Multiple Minima/Maxima)
# z = sin(x)*cos(y) or similar multi-modal function
# Annotations: Global Maxima, Local Maxima, Local Minima, Global Minima
# One red horizontal reference line
# Axis ticks: vertical 6, 4, 2, 0, -2, -4
# ============================================================
fig = plt.figure(figsize=(w_in, h_bot_in), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.view_init(elev=30, azim=-60)

x = np.linspace(-3, 3, 80)
y = np.linspace(-3, 3, 80)
X, Y = np.meshgrid(x, y)
# Non-convex: combination of sine waves
Z = 3 * np.sin(X) * np.cos(Y) + 1.5 * np.sin(2*X) * np.cos(2*Y)
Z = np.clip(Z, -4, 6)

surf = ax.plot_surface(X, Y, Z, cmap=jet, rstride=1, cstride=1,
                       linewidth=0, antialiased=True, shade=True)

# One red horizontal reference line at z=0
x_line = np.linspace(-3, 3, 100)
y_line = np.zeros_like(x_line)
z_line = np.zeros_like(x_line)
ax.plot(x_line, y_line, z_line, color='red', linewidth=1.5, zorder=10)
y_line2 = np.linspace(-3, 3, 100)
x_line2 = np.zeros_like(y_line2)
ax.plot(x_line2, y_line2, z_line, color='red', linewidth=1.5, zorder=10)

# Annotation positions (approximate peaks/valleys)
# Global Maxima: near (0, 0) where Z~4.5
# Local Maxima: near (±2.5, 0) or similar
# Global Minima: where Z~-4
# Local Minima: intermediate valleys

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-4, 6)
ax.set_xticks([-2])
ax.set_yticks([-2])
ax.set_zticks([-4, -2, 0, 2, 4, 6])

for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    axis._axinfo['grid'].update(color='#DDDDDD', linewidth=0.5)
    axis.line.set_linewidth(0.5)

for t in (ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()):
    t.set_fontsize(7)
    t.set_color('#444444')

plt.savefig(os.path.join(OUTDIR, 'plot_025_bl.png'), dpi=DPI, facecolor='white', bbox_inches='tight', pad_inches=0)
plt.close(fig)
print("Generated plot_025_bl.png")

# ============================================================
# Plot 4: Bottom-Right - Gradient Descent Path
# Surface + black curved path with arrows descending to minimum
# No red reference line
# ============================================================
fig = plt.figure(figsize=(w_in, h_bot_in), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.view_init(elev=30, azim=-60)

x = np.linspace(-3, 3, 80)
y = np.linspace(-3, 3, 80)
X, Y = np.meshgrid(x, y)
# Bowl with a valley
Z = (X-0.5)**2 + (Y+0.5)**2
Z = np.clip(Z, 0, 8)

surf = ax.plot_surface(X, Y, Z, cmap=jet, rstride=1, cstride=1,
                       linewidth=0, antialiased=True, shade=True, alpha=0.9)

# Gradient descent path: starts high, spirals down to minimum
# Path: start at (-2.5, 2.5) -> spiral to (0.5, -0.5)
t = np.linspace(0, 4*np.pi, 200)
# Spiral inwards
path_x = 0.5 + 3.0 * np.exp(-0.2*t) * np.cos(t)
path_y = -0.5 + 3.0 * np.exp(-0.2*t) * np.sin(t)
path_z = (path_x-0.5)**2 + (path_y+0.5)**2

ax.plot(path_x, path_y, path_z, color='black', linewidth=2.5, zorder=20, solid_capstyle='round')

# Add arrowheads along the path
arrow_indices = [30, 60, 90, 120, 150, 180]
for idx in arrow_indices:
    if idx < len(path_x)-1:
        dx = path_x[idx+1] - path_x[idx]
        dy = path_y[idx+1] - path_y[idx]
        dz = path_z[idx+1] - path_z[idx]
        # Draw small cone/arrow
        ax.quiver(path_x[idx], path_y[idx], path_z[idx],
                  dx, dy, dz, color='black', arrow_length_ratio=0.1,
                  linewidth=2, zorder=21)

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(0, 8)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    axis._axinfo['grid'].update(color='#DDDDDD', linewidth=0.5)
    axis.line.set_linewidth(0.5)

plt.savefig(os.path.join(OUTDIR, 'plot_025_br.png'), dpi=DPI, facecolor='white', bbox_inches='tight', pad_inches=0)
plt.close(fig)
print("Generated plot_025_br.png")

print("All 4 plots generated.")