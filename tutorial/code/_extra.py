# -*- coding: utf-8 -*-
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
FG, MUTED, GRID, BLUE, ORANGE, GREEN = "#b8c2cc", "#8b949e", "#3f4650", "#58a6ff", "#f0883e", "#3fb950"
Path("img").mkdir(exist_ok=True)

def style(ax):
    ax.set_facecolor("none"); ax.tick_params(colors=MUTED, labelsize=7)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_color(GRID)
    ax.grid(True, color=GRID, linewidth=0.4, alpha=0.55)

# ============ 图 A：六种损失曲线 ============
t = np.arange(1, 61)
rng = np.random.default_rng(3)

def smooth(a, k, c=0.0):
    return a*np.exp(-k*t) + c

panels = []
# 1 正常
tr1 = smooth(1.0, 0.09, 0.05) * (1 + rng.normal(0, 0.012, t.size))
va1 = smooth(1.15, 0.085, 0.07) * (1 + rng.normal(0, 0.02, t.size))
panels.append(("正常收敛", tr1, va1, "两者一起降，最后贴得很近"))
# 2 过拟合
tr2 = smooth(1.0, 0.13, 0.02) * (1 + rng.normal(0, 0.01, t.size))
va2 = smooth(1.1, 0.18, 0.0) + 0.045*np.clip(t-18, 0, None)**1.35 + rng.normal(0, 0.012, t.size)
panels.append(("过拟合", tr2, va2, "训练还在降，验证开始抬头"))
# 3 学习率太大
tr3 = 1.0 * np.exp(-0.03*t) * (1 + 0.55*np.sin(t*1.5)) + 0.05 + 0.03*t
panels.append(("学习率太大", tr3, None, "上下大幅震荡，整体还在涨"))
# 4 学习率太小
tr4 = smooth(1.0, 0.006, 0.55)
panels.append(("学习率太小", tr4, None, "一直在降，但慢得看不到头"))
# 5 欠拟合
tr5 = smooth(0.15, 0.12, 0.75) * (1 + rng.normal(0, 0.01, t.size))
va5 = smooth(0.17, 0.11, 0.78) * (1 + rng.normal(0, 0.012, t.size))
panels.append(("欠拟合", tr5, va5, "两条都停在很高的位置"))
# 6 数据/批大小问题
tr6 = 0.75 + 0.25*np.exp(-0.05*t) + rng.normal(0, 0.09, t.size)
va6 = 0.80 + 0.25*np.exp(-0.05*t) + rng.normal(0, 0.11, t.size)
panels.append(("数据或批太小", tr6, va6, "曲线毛刺很多，看不出趋势"))

fig, axes = plt.subplots(2, 3, figsize=(9.2, 5.0), dpi=200)
fig.patch.set_alpha(0)
for ax, (title, tr, va, note) in zip(axes.ravel(), panels):
    ax.plot(t, tr, color=BLUE, lw=1.5, label="训练")
    if va is not None:
        ax.plot(t, va, color=ORANGE, lw=1.5, label="验证")
    style(ax)
    ax.set_title(title, color=FG, fontsize=9, pad=6)
    ax.set_xlabel("轮次", color=MUTED, fontsize=7)
    ax.set_ylabel("损失", color=MUTED, fontsize=7)
    ax.set_yscale("log")
    ax.text(0.5, -0.42, note, transform=ax.transAxes, ha="center", va="top",
            color=MUTED, fontsize=7)
    lg = ax.legend(loc="upper right", frameon=False, fontsize=6.5)
    for x in lg.get_texts(): x.set_color(FG)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("img/plot-loss-curves.png", transparent=True)
plt.close(fig)
print("loss curves done")

# ============ 图 B：多项式拟合 ============
rng2 = np.random.default_rng(7)
n = 22
x = np.sort(rng2.uniform(20, 200, n))
y = 520*(1-np.exp(-x/72)) + 40 + rng2.normal(0, 18, n)

xs_grid = np.linspace(15, 205, 400)
deg_list = [1, 2, 3, 9]
fig, axes = plt.subplots(1, 4, figsize=(9.6, 2.8), dpi=200, sharey=True)
fig.patch.set_alpha(0)
for ax, d in zip(axes, deg_list):
    cols = [x**k for k in range(1, d+1)]
    F = np.column_stack(cols)
    mu, sd = F.mean(0), F.std(0)
    Fs = (F-mu)/sd
    coef, *_ = np.linalg.lstsq(np.c_[Fs, np.ones(n)], y, rcond=None)
    G = np.column_stack([xs_grid**k for k in range(1, d+1)])
    Gs = (G-mu)/sd
    pred = Gs @ coef[:-1] + coef[-1]
    train_pred = Fs @ coef[:-1] + coef[-1]
    mse = float(np.mean((train_pred-y)**2))
    ax.scatter(x, y, s=16, color=BLUE, alpha=.85, edgecolor="none", zorder=3)
    ax.plot(xs_grid, pred, color=GREEN, lw=1.8, zorder=4)
    style(ax)
    ax.set_title("%d 次" % d, color=FG, fontsize=9, pad=5)
    ax.set_ylim(0, 700); ax.set_xlim(10, 210)
    ax.text(0.5, -0.30, "训练 MSE %.0f" % mse, transform=ax.transAxes, ha="center",
            va="top", color=MUTED, fontsize=7)
axes[0].set_ylabel("房价（万元）", color=MUTED, fontsize=8)
for ax in axes: ax.set_xlabel("面积", color=MUTED, fontsize=7.5)
fig.tight_layout(rect=(0, 0.06, 1, 1))
fig.savefig("img/poly-fit.png", transparent=True)
plt.close(fig)
print("poly fit done")
