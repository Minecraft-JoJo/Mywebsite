# -*- coding: utf-8 -*-
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
FG, MUTED, GRID, ACC, LINE = "#b8c2cc", "#8b949e", "#3f4650", "#58a6ff", "#f0883e"

rng = np.random.default_rng(2024)
area = np.array([45,52,58,63,68,74,80,86,92,98,104,110,117,124,132,140,148,156,163,171], float)
price = np.round(3.2*area + 35 + rng.normal(0, 18, area.size), 1)
m = area.size

def J(w,b): return float(np.mean((w*area+b-price)**2)/2)
def grad(w,b):
    r = w*area + b - price
    return float(np.mean(r*area)), float(np.mean(r))

W0, B0, alpha = 2.5, 30.0, 2e-5
gw, gb = grad(W0, B0)
w1, b1 = W0 - alpha*gw, B0 - alpha*gb
print("J0      = %.4f" % J(W0,B0))
print("gw      = %.4f" % gw)
print("gb      = %.4f" % gb)
print("delta w = %.6f" % (-alpha*gw))
print("delta b = %.6f" % (-alpha*gb))
print("w1 b1   = %.4f  %.4f" % (w1, b1))
print("J1      = %.4f" % J(w1,b1))

w,b = W0,B0
for _ in range(50):
    g1,g2 = grad(w,b); w,b = w-alpha*g1, b-alpha*g2
print("50 steps: w=%.4f b=%.4f J=%.4f" % (w,b,J(w,b)))
X = np.c_[area, np.ones_like(area)]
sol,*_ = np.linalg.lstsq(X, price, rcond=None)
print("opt      : w=%.4f b=%.4f J=%.4f" % (sol[0], sol[1], J(*sol)))

# ---- 图 ----
plt.rcParams["axes.unicode_minus"] = False
def style(ax):
    ax.set_facecolor("none"); ax.tick_params(colors=MUTED, labelsize=9)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_color(GRID)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)

fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=200)
fig.patch.set_alpha(0)
ax.scatter(area, price, s=44, color=ACC, alpha=.9, edgecolor="none", zorder=3)
style(ax)
ax.set_xlabel("面积 x（平方米）", color=FG, fontsize=11)
ax.set_ylabel("成交价 y（万元）", color=FG, fontsize=11)
ax.set_xlim(38, 180); ax.set_ylim(150, 640)
fig.tight_layout()
Path("img").mkdir(exist_ok=True)
fig.savefig("img/exercise-houses.png", transparent=True)
plt.close(fig)
print("figure saved")
