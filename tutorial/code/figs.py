# -*- coding: utf-8 -*-
"""生成第 1、2 章配图。透明背景，文字用浅灰，贴合站点深色主题。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
FG, MUTED, GRID, ACC = "#b8c2cc", "#8b949e", "#3f4650", "#58a6ff"
LINE = "#f0883e"

out = Path("img"); out.mkdir(exist_ok=True)

def style(ax):
    ax.set_facecolor("none")
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)

# 真实关系：房价 = 3.5 × 面积 + 20（单位：万元）
rng = np.random.default_rng(7)
area = np.array([55, 62, 70, 78, 85, 92, 100, 108, 115, 125, 135, 145], dtype=float)
price = 3.5 * area + 20 + rng.normal(0, 14, area.size)

# ---------- 图 1：第 1 章第二课，讲名词 ----------
fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=200)
fig.patch.set_alpha(0)
ax.scatter(area, price, s=46, color=ACC, alpha=0.9, edgecolor="none", zorder=3)
style(ax)
ax.set_xlabel("面积（平方米）", color=FG, fontsize=11)
ax.set_ylabel("房价（万元）", color=FG, fontsize=11)

i = 6
ax.annotate("一个样本\n（一套房子）", xy=(area[i], price[i]), xytext=(area[i]+14, price[i]-95),
            color=FG, fontsize=10, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.2))
ax.axvline(area[i], color=GRID, lw=0.8, ls="--")
ax.axhline(price[i], color=GRID, lw=0.8, ls="--")
ax.text(area[i], 168, "  特征 x = %.0f" % area[i], color=MUTED, fontsize=9, va="bottom")
ax.text(48, price[i] - 14, "标签 y = %.0f" % price[i], color=MUTED, fontsize=9, va="top")
ax.set_xlim(45, 152); ax.set_ylim(150, 560)
fig.tight_layout()
fig.savefig(out/"house-points.png", transparent=True)
plt.close(fig)

# ---------- 图 2：第 2 章，数据本身 ----------
fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=200)
fig.patch.set_alpha(0)
ax.scatter(area, price, s=46, color=ACC, alpha=0.9, edgecolor="none", zorder=3)
style(ax)
ax.set_xlabel("面积 x（平方米）", color=FG, fontsize=11)
ax.set_ylabel("房价 y（万元）", color=FG, fontsize=11)
ax.set_xlim(45, 152); ax.set_ylim(150, 560)
fig.tight_layout()
fig.savefig(out/"price-points.png", transparent=True)
plt.close(fig)

# ---------- 图 3：随便画一条线 ----------
def line_ax(ax, w, b):
    xs = np.array([45, 152])
    ax.plot(xs, w*xs + b, color=LINE, lw=2.2, zorder=4, label="ŷ = %.1fx + %.0f" % (w, b))

fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=200)
fig.patch.set_alpha(0)
ax.scatter(area, price, s=46, color=ACC, alpha=0.85, edgecolor="none", zorder=3)
line_ax(ax, 1.0, 0)
style(ax)
ax.set_xlabel("面积 x（平方米）", color=FG, fontsize=11)
ax.set_ylabel("房价 y（万元）", color=FG, fontsize=11)
ax.set_xlim(45, 152); ax.set_ylim(0, 560)
lg = ax.legend(loc="upper left", frameon=False, fontsize=10)
for t in lg.get_texts(): t.set_color(FG)
fig.tight_layout()
fig.savefig(out/"line-bad.png", transparent=True)
plt.close(fig)

# ---------- 图 4：逐步调整的三条线 ----------
steps = [(1.0, 0), (2.4, 30), (3.2, 45), (3.5, 20)]
labels = ["初始：w=1.0, b=0", "调一次：w=2.4, b=30", "再调：w=3.2, b=45", "基本拟合：w=3.5, b=20"]
fig, axes = plt.subplots(1, 4, figsize=(8.6, 2.7), dpi=200, sharey=True)
fig.patch.set_alpha(0)
for ax, (w, b), lab in zip(axes, steps, labels):
    ax.scatter(area, price, s=26, color=ACC, alpha=0.8, edgecolor="none", zorder=3)
    line_ax(ax, w, b)
    style(ax)
    ax.set_title(lab, color=FG, fontsize=9, pad=6)
    ax.set_xlabel("面积", color=MUTED, fontsize=8)
axes[0].set_ylabel("房价（万元）", color=FG, fontsize=9)
axes[0].set_xlim(45, 152); axes[0].set_ylim(0, 560)
fig.tight_layout()
fig.savefig(out/"line-tune.png", transparent=True)
plt.close(fig)

print("生成完成：", sorted(p.name for p in out.glob("*.png")))
# ---------- 图 5：J(w) 曲线（b = 0） ----------
m = area.size
def J_w(w):
    return np.mean((w * area - price) ** 2) / 2.0

ws = np.linspace(0.5, 5.2, 400)
Js = np.array([J_w(w) for w in ws])
w_star = float(area @ price / (area @ area))
J_star = J_w(w_star)

fig, ax = plt.subplots(figsize=(7.0, 3.6), dpi=200)
fig.patch.set_alpha(0)
ax.plot(ws, Js, color=ACC, lw=2.4)
style(ax)
ax.set_xlabel("w", color=FG, fontsize=11)
ax.set_ylabel("J(w)  （b = 0）", color=FG, fontsize=11)

for w0, lab in [(1.0, "w=1.0"), (w_star, "w=%.2f（最低点）" % w_star)]:
    y0 = J_w(w0)
    ax.plot([w0], [y0], "o", color=LINE, ms=7, zorder=5)
    ax.annotate(lab, xy=(w0, y0), xytext=(w0 + 0.25, y0 + 260),
                color=FG, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
fig.tight_layout()
fig.savefig(out/"loss-curve.png", transparent=True)
plt.close(fig)

# ---------- 图 6：J(w, b) 等高线 ----------
W, B = np.meshgrid(np.linspace(0.5, 5.2, 260), np.linspace(-120, 130, 260))
Z = np.mean((W[..., None] * area + B[..., None] - price) ** 2, axis=-1) / 2.0

fig, ax = plt.subplots(figsize=(6.4, 5.0), dpi=200)
fig.patch.set_alpha(0)
lv = np.percentile(Z, [2, 4, 7, 11, 16, 23, 32, 45, 60, 78, 92])
lv = np.unique(lv)
cs = ax.contourf(W, B, Z, levels=lv, cmap="inferno", alpha=0.9, extend="both")
cl = ax.contour(W, B, Z, levels=lv, colors="#e6edf3", linewidths=0.5, alpha=0.35)
style(ax)
ax.set_xlabel("w", color=FG, fontsize=11)
ax.set_ylabel("b", color=FG, fontsize=11)

pts = [(1.0, 0, "A  w=1.0, b=0", (0.35, 30)),
       (2.4, 30, "B  w=2.4, b=30", (0.30, 42)),
       (3.2, 45, "C  w=3.2, b=45", (0.32, 34)),
       (3.5, 20, "D  w=3.5, b=20", (0.52, -42))]
for w0, b0, lab, (dx, dy) in pts:
    ax.plot([w0], [b0], "o", color="#f0f6fc", ms=7, mec="#0d1117", mew=1.2, zorder=6)
    ax.annotate(lab, xy=(w0, b0), xytext=(w0 + dx, b0 + dy),
                color="#f0f6fc", fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color="#8b949e", lw=0.9))
ax.plot([3.5747], [11.34], "x", color="#3fb950", ms=12, mew=2.4, zorder=7)
ax.annotate("最低点\n(3.57, 11.34)", xy=(3.5747, 11.34), xytext=(4.05, 62), color="#56d364", fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color="#3fb950", lw=1))
fig.tight_layout()
fig.savefig(out/"loss-contour.png", transparent=True)
plt.close(fig)

print("w* = %.4f, J(w*) = %.2f" % (w_star, J_star))
print("J(1.0, 0) = %.2f" % J_w(1.0))
print("J(3.5, 0) = %.2f" % J_w(3.5))
print("J(3.5, 20) = %.2f" % (np.mean((3.5*area+20-price)**2)/2))
print("J(1.0, 0)*2m = %.1f" % (J_w(1.0)*2*m))
print("m =", m)
# ---------- 图 7：3D 损失曲面 + 下降路径 ----------
from mpl_toolkits.mplot3d import Axes3D  # noqa

def J(w, b):
    return float(np.mean((w * area + b - price) ** 2) / 2.0)

def grad(w, b):
    r = w * area + b - price
    return float(np.mean(r * area)), float(np.mean(r))

# 梯度下降轨迹
w0, b0, lr, steps = 1.0, 0.0, 4.5e-5, 60
path_w, path_b, path_j = [w0], [b0], [J(w0, b0)]
for _ in range(steps):
    gw, gb = grad(path_w[-1], path_b[-1])
    path_w.append(path_w[-1] - lr * gw)
    path_b.append(path_b[-1] - lr * gb)
    path_j.append(J(path_w[-1], path_b[-1]))

W3 = np.linspace(0.6, 5.0, 140)
B3 = np.linspace(-60, 130, 140)
Wg, Bg = np.meshgrid(W3, B3)
Zg = np.mean((Wg[..., None] * area + Bg[..., None] - price) ** 2, axis=-1) / 2.0
Zc = np.log10(1.0 + Zg)

fig = plt.figure(figsize=(7.4, 5.0), dpi=200)
fig.patch.set_alpha(0)
ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor("none")
ax.plot_surface(Wg, Bg, Zc, cmap="turbo", linewidth=0, antialiased=True,
                alpha=1.0, rstride=2, cstride=2, shade=True)
pj = np.log10(1.0 + np.array(path_j))
ax.plot(path_w, path_b, pj + 0.06, color="#ffffff", lw=2.4, zorder=10)
ax.scatter([path_w[0]], [path_b[0]], [pj[0] + 0.06], color="#ffffff", s=34, zorder=11)
ax.scatter([path_w[-1]], [path_b[-1]], [pj[-1] + 0.06], color="#3fb950", s=40, zorder=11)

ax.set_xlabel("w", color=FG, fontsize=10, labelpad=2)
ax.set_ylabel("b", color=FG, fontsize=10, labelpad=2)
ax.set_zlabel("log(1+J)", color=FG, fontsize=9, labelpad=0)
ax.tick_params(colors=MUTED, labelsize=8)
for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
    pane.set_pane_color((0, 0, 0, 0))
    pane.line.set_color(GRID)
ax.grid(False)
ax.set_xticks([1, 2, 3, 4, 5]); ax.set_yticks([-50, 0, 50, 100])
ax.view_init(elev=30, azim=-62)
fig.tight_layout()
fig.savefig(out/"loss-3d.png", transparent=True)
plt.close(fig)
print("path start J=%.1f  end J=%.1f  end w=%.3f b=%.2f" % (path_j[0], path_j[-1], path_w[-1], path_b[-1]))

# ---------- 图 8：局部最低点 vs 全局最低点（1D 剖面） ----------
xs = np.linspace(0.4, 8.6, 600)
def fcurve(x):
    return (-1.00 * np.exp(-((x - 2.1) ** 2) / 0.30)
            - 1.45 * np.exp(-((x - 6.4) ** 2) / 0.85)
            + 0.008 * x ** 2 + 0.45)
fx = fcurve(xs)
ly, ry = float(fcurve(2.1)), float(fcurve(6.4))

fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=200)
fig.patch.set_alpha(0)
ax.plot(xs, fx, color=ACC, lw=2.2)
style(ax)
ax.set_xlabel("参数（比如只看 w 一个方向）", color=FG, fontsize=10)
ax.set_ylabel("J", color=FG, fontsize=10)

ax.plot([2.1], [ly], "o", color="#d29922", ms=9, zorder=6)
ax.annotate("局部最低点\n走到这里就停了", xy=(2.1, ly), xytext=(2.35, 0.12),
            color="#d29922", fontsize=9,
            arrowprops=dict(arrowstyle="->", color="#d29922", lw=1.1))
ax.plot([6.4], [ry], "o", color="#3fb950", ms=9, zorder=6)
ax.annotate("全局最低点\n真正想要的地方", xy=(6.4, ry), xytext=(5.05, 0.45),
            color="#3fb950", fontsize=9,
            arrowprops=dict(arrowstyle="->", color="#3fb950", lw=1.1))

ax.plot([0.9], [float(fcurve(0.9))], "o", color="#f0f6fc", ms=8, zorder=6)
ax.annotate("起点", xy=(0.9, float(fcurve(0.9))), xytext=(0.55, 1.0),
            color="#f0f6fc", fontsize=9,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
ax.set_ylim(-1.0, 1.25)
fig.tight_layout()
fig.savefig(out/"loss-local-min.png", transparent=True)
plt.close(fig)
print("left=%.3f right=%.3f  (right 必须更低)" % (ly, ry))
# ---------- 图 9：切线与步子（b = 0） ----------
def dJdw(w):
    return float(np.mean((w * area - price) * area))

ws_all = np.linspace(0.5, 5.2, 400)
Js_all = np.array([J_w(w) for w in ws_all])
LR = 3.6e-5
marks = [(1.0, "w = 1.0\n坡很陡"), (3.0, "w = 3.0\n坡度中等"), (3.68, "w = 3.68\n几乎平了")]

fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.0), dpi=200, sharey=True)
fig.patch.set_alpha(0)
for ax, (w0, lab) in zip(axes, marks):
    ax.plot(ws_all, Js_all, color=ACC, lw=2.0)
    style(ax)
    j0 = J_w(w0)
    g = dJdw(w0)
    step = -LR * g
    ax.plot([w0], [j0], "o", color="#f0f6fc", ms=7, mec="#0d1117", mew=1.2, zorder=6)
    xt = np.array([w0 - 0.5, w0 + 0.5])
    ax.plot(xt, j0 + g * (xt - w0), color=LINE, lw=1.7, ls="--", zorder=5)
    y_arrow = float(np.max(Js_all)) * 1.10
    if abs(step) >= 0.02:
        ax.annotate("", xy=(w0 + step, y_arrow), xytext=(w0, y_arrow),
                    arrowprops=dict(arrowstyle="-|>", color="#3fb950", lw=2.0, mutation_scale=16))
        ax.text(w0 + step / 2, y_arrow * 1.045, "这一步", color="#3fb950", fontsize=8, ha="center")
    else:
        ax.plot([w0], [y_arrow], "o", color="#3fb950", ms=6)
        ax.text(w0 + 0.55, y_arrow, "几乎不动", color="#3fb950", fontsize=8, va="center")
    ax.set_title(lab, color=FG, fontsize=9, pad=6)
    ax.set_xlabel("w", color=MUTED, fontsize=9)
    ax.set_xlim(0.4, 5.3)
    ax.set_ylim(0, float(np.max(Js_all)) * 1.24)
axes[0].set_ylabel("J(w)", color=FG, fontsize=10)
fig.tight_layout()
fig.savefig(out/"gradient-step.png", transparent=True)
plt.close(fig)
for w0, _ in marks:
    print("w=%.2f  grad=%9.1f  step=%+.4f" % (w0, dJdw(w0), -LR * dJdw(w0)))
# ---------- 图 10：不同学习率的表现（双面板） ----------
def run_gd(lr, steps, w0=1.0, b0=0.0):
    ws, bs, js = [w0], [b0], [J(w0, b0)]
    w, b = w0, b0
    for _ in range(steps):
        gw, gb = grad(w, b)
        w, b = w - lr * gw, b - lr * gb
        if not np.isfinite(w) or abs(w) > 1e6:
            ws.append(np.nan); bs.append(np.nan); js.append(np.nan); break
        ws.append(w); bs.append(b); js.append(J(w, b))
    return np.array(ws), np.array(bs), np.array(js)

cases = [(1e-5, "#8b949e", "α = 1e-5　太小"),
         (4.5e-5, "#3fb950", "α = 4.5e-5　合适"),
         (1.9e-4, "#d29922", "α = 1.9e-4　太大"),
         (2.4e-4, "#f85149", "α = 2.4e-4　爆炸")]
N = 60
fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.4), dpi=200)
fig.patch.set_alpha(0)
handles = []
for lr, col, lab in cases:
    ws_, _, js_ = run_gd(lr, N)
    k = np.arange(len(js_))
    h, = axes[0].plot(k, js_, color=col, lw=1.7, label=lab)
    handles.append(h)
    axes[1].plot(k, ws_, color=col, lw=1.7)
for ax in axes:
    style(ax)
    ax.set_xlabel("更新步数", color=FG, fontsize=9)
axes[0].set_ylabel("损失 J（对数轴）", color=FG, fontsize=9)
axes[0].set_yscale("log")
axes[0].axhline(37.27, color="#56d364", lw=1, ls=":", alpha=.9)
axes[1].set_ylabel("参数 w", color=FG, fontsize=9)
axes[1].set_ylim(-2, 12)
axes[1].axhline(3.57, color="#56d364", lw=1, ls=":", alpha=.9)
axes[1].text(37, 6.2, "最优 w ≈ 3.57", color="#56d364", fontsize=8)
fig.tight_layout(rect=(0, 0.12, 1, 1))
lg = fig.legend(handles, [c[2] for c in cases], loc="lower center", ncol=4,
                frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, 0.005))
for t in lg.get_texts(): t.set_color(FG)
fig.savefig(out/"lr-curves.png", transparent=True)
plt.close(fig)
print("lr curves done")
# ---------- 图 12：总结课 —— 直线逐步到位 ----------
def run_trace(lr, steps, w0=1.0, b0=0.0):
    out = [(0, w0, b0)]
    w, b = w0, b0
    for i in range(1, steps + 1):
        gw, gb = grad(w, b)
        w, b = w - lr * gw, b - lr * gb
        out.append((i, w, b))
    return out

trace = run_trace(4.5e-5, 20)
marks = [0, 1, 2, 3, 5, 20]
fig, axes = plt.subplots(2, 3, figsize=(9.2, 5.4), dpi=200, sharex=True, sharey=True)
fig.patch.set_alpha(0)
for ax, st in zip(axes.ravel(), marks):
    i, w0, b0 = trace[st]
    ax.scatter(area, price, s=22, color=ACC, alpha=.85, edgecolor="none", zorder=3)
    xs_ = np.array([45, 152])
    ax.plot(xs_, w0 * xs_ + b0, color=LINE, lw=2.0, zorder=4)
    style(ax)
    ax.set_title("第 %d 步　w=%.3f  b=%.2f" % (st, w0, b0), color=FG, fontsize=9, pad=5)
    ax.text(0.97, 0.06, "J = %.1f" % J(w0, b0), transform=ax.transAxes,
            ha="right", va="bottom", color="#56d364", fontsize=9)
    ax.set_xlim(45, 155); ax.set_ylim(140, 560)
for ax in axes[1]:
    ax.set_xlabel("面积（平方米）", color=MUTED, fontsize=8)
for ax in axes[:, 0]:
    ax.set_ylabel("房价（万元）", color=MUTED, fontsize=8)
fig.tight_layout()
fig.savefig(out/"summary-steps.png", transparent=True)
plt.close(fig)

# ---------- 图 13：总结课 —— 损失曲线与真实谷底 ----------
fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=200)
fig.patch.set_alpha(0)
N2 = 40
js_ = [J(w, b) for _, w, b in run_trace(4.5e-5, N2)]
ax.plot(np.arange(len(js_)), js_, color=ACC, lw=2.0, marker="o", ms=3)
ax.axhline(37.27, color="#3fb950", lw=1.2, ls=":")
ax.text(21, 37.27 * 1.25, "真实最低点 37.27", color="#3fb950", fontsize=9)
style(ax)
ax.set_yscale("log")
ax.set_xlabel("更新步数", color=FG, fontsize=10)
ax.set_ylabel("J（对数轴）", color=FG, fontsize=10)
for st in (1, 5, 20):
    ax.annotate("第 %d 步" % st, xy=(st, js_[st]), xytext=(st + 2.5, js_[st] * 3.2),
                color=MUTED, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=.8))
fig.tight_layout()
fig.savefig(out/"summary-loss.png", transparent=True)
plt.close(fig)
print("summary figures done")