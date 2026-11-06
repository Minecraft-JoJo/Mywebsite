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
print("summary figures done")# -*- coding: utf-8 -*-
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
FG, MUTED, GRID, ACC = "#b8c2cc", "#8b949e", "#3f4650", "#58a6ff"

rng = np.random.default_rng(2024)
area = np.array([45,52,58,63,68,74,80,86,92,98,104,110,117,124,132,140,148,156,163,171], float)
price = np.round(3.2*area + 35 + rng.normal(0, 18, area.size), 1)
m = area.size

def analyse(name, x):
    H = np.array([[np.mean(x*x), np.mean(x)],[np.mean(x),1.0]])
    lam = np.linalg.eigvalsh(H)
    kappa = lam[-1]/lam[0]
    a_opt = 2.0/(lam[-1]+lam[0])
    rho = (lam[-1]-lam[0])/(lam[-1]+lam[0])
    steps = int(np.ceil(np.log(0.01)/np.log(rho))) if rho < 1 else 10**9
    return kappa, a_opt, steps

variants = [
  ("不缩放",          area),
  ("除以最大值",      area/area.max()),
  ("均值归一化",      (area-area.mean())/(area.max()-area.min())),
  ("标准化 Z-score",  (area-area.mean())/area.std()),
]
print("%-16s %12s %12s %12s" % ("方法","条件数","最优α","到1%的步数"))
info = {}
for name, x in variants:
    k,a,s = analyse(name,x); info[name]=(k,a,s)
    print("%-16s %12.0f %12.2e %12d" % (name,k,a,s))

# 实跑验证：不缩放跑 5000 步 vs 缩放后跑 50 步
def run(x, w0, alpha, steps):
    def J(w,b): return float(np.mean((w*x+b-price)**2)/2)
    def grad(w,b):
        r=w*x+b-price; return float(np.mean(r*x)), float(np.mean(r))
    A=np.c_[x,np.ones_like(x)]; sol,*_=np.linalg.lstsq(A,price,rcond=None)
    w,b=w0
    for _ in range(steps):
        gw,gb=grad(w,b); w,b=w-alpha*gw,b-alpha*gb
    return J(w,b), J(*sol)

k1,a1,s1 = info["不缩放"];      j_end, jmin = run(area, (1.0,0.0), a1, 5000)
print("\n不缩放  α=%.2e  5000 步后 J=%.2f   (最优 %.2f)" % (a1, j_end, jmin))
k2,a2,s2 = info["除以最大值"];   j_end2,_ = run(area/area.max(), (1.0/area.max(),0.0), a2, 200)
print("除以最大值 α=%.2e  200 步后 J=%.2f" % (a2, j_end2))

# ---- 图 ----
def style(ax):
    ax.set_facecolor("none"); ax.tick_params(colors=MUTED, labelsize=8)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_color(GRID)
    ax.grid(True, color=GRID, linewidth=0.5, alpha=0.6)

def figure(x, w0, alpha, fname, wlim, blim, steps=25):
    A=np.c_[x,np.ones_like(x)]; sol,*_=np.linalg.lstsq(A,price,rcond=None)
    def J(w,b): return float(np.mean((w*x+b-price)**2)/2)
    def grad(w,b):
        r=w*x+b-price; return float(np.mean(r*x)), float(np.mean(r))
    w,b=w0; path=[(w,b)]
    for _ in range(steps):
        gw,gb=grad(w,b); w,b=w-alpha*gw,b-alpha*gb; path.append((w,b))
    path=np.array(path)
    W,B=np.meshgrid(np.linspace(*wlim,300),np.linspace(*blim,300))
    Z=np.mean((W[...,None]*x+B[...,None]-price)**2,axis=-1)/2
    fig,ax=plt.subplots(figsize=(6.4,4.2),dpi=200); fig.patch.set_alpha(0)
    lv=np.logspace(np.log10(max(Z.min()*1.1,1e-2)),np.log10(np.percentile(Z,40)),12)
    ax.contourf(W,B,Z,levels=lv,cmap="inferno",alpha=.85,extend="both")
    ax.contour(W,B,Z,levels=lv,colors="#e6edf3",linewidths=.45,alpha=.3)
    ax.plot(path[:,0],path[:,1],color=ACC,lw=1.5,marker="o",ms=2.5)
    ax.plot([path[0,0]],[path[0,1]],"o",color="#f0f6fc",ms=7,mec="#0d1117",zorder=6)
    ax.plot([sol[0]],[sol[1]],"x",color="#3fb950",ms=11,mew=2.2,zorder=7)
    style(ax); ax.set_xlabel("w",color=FG,fontsize=10); ax.set_ylabel("b",color=FG,fontsize=10)
    ax.set_xlim(*wlim); ax.set_ylim(*blim)
    fig.tight_layout(); fig.savefig("img/"+fname,transparent=True); plt.close(fig)

Path("img").mkdir(exist_ok=True)
figure(area, (1.0,0.0), a1, "scaling-before.png", (0,7), (-40,110), 25)
figure(area/area.max(), (area.max(),0.0), a2*0.55, "scaling-after.png", (0,900), (-40,110), 25)
print("figures done")# -*- coding: utf-8 -*-
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
FG, MUTED, GRID, ACC = "#b8c2cc", "#8b949e", "#3f4650", "#58a6ff"

rng = np.random.default_rng(2024)
area = np.array([45,52,58,63,68,74,80,86,92,98,104,110,117,124,132,140,148,156,163,171], float)
price = np.round(3.2*area + 35 + rng.normal(0, 18, area.size), 1)

def style(ax):
    ax.set_facecolor("none"); ax.tick_params(colors=MUTED, labelsize=8)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_color(GRID)
    ax.grid(True, color=GRID, linewidth=0.5, alpha=0.6)

x = (area - area.mean())/area.std()
A = np.c_[x, np.ones_like(x)]
sol,*_ = np.linalg.lstsq(A, price, rcond=None)
def J(w,b): return float(np.mean((w*x+b-price)**2)/2)
def grad(w,b):
    r=w*x+b-price; return float(np.mean(r*x)), float(np.mean(r))
jmin = J(*sol)

# 一步验证
w,b = 37.78, 104.05
gw,gb = grad(w,b)
print("起点 J = %.2f" % J(w,b))
print("梯度 gw=%.2f gb=%.2f" % (gw,gb))
w1, b1 = w-1.0*gw, b-1.0*gb
print("alpha=1.0 一步后 w=%.3f b=%.3f J=%.4f (最优 %.4f)" % (w1,b1,J(w1,b1),jmin))

# 画图
w0,b0,alpha,steps = 37.78, 104.05, 0.5, 20
w,b = w0,b0; path=[(w,b)]
for _ in range(steps):
    gw,gb=grad(w,b); w,b=w-alpha*gw,b-alpha*gb; path.append((w,b))
path=np.array(path)

W,B = np.meshgrid(np.linspace(-80,320,300), np.linspace(170,580,300))
Z = np.mean((W[...,None]*x+B[...,None]-price)**2, axis=-1)/2
fig,ax=plt.subplots(figsize=(6.4,4.4),dpi=200); fig.patch.set_alpha(0)
lv=np.logspace(np.log10(max(Z.min()*1.05,1e-2)), np.log10(np.percentile(Z,42)), 12)
ax.contourf(W,B,Z,levels=lv,cmap="inferno",alpha=.85,extend="both")
ax.contour(W,B,Z,levels=lv,colors="#e6edf3",linewidths=.45,alpha=.3)
ax.plot(path[:,0],path[:,1],color=ACC,lw=1.5,marker="o",ms=2.5)
ax.plot([w0],[b0],"o",color="#f0f6fc",ms=7,mec="#0d1117",zorder=6)
ax.plot([sol[0]],[sol[1]],"x",color="#3fb950",ms=11,mew=2.2,zorder=7)
style(ax); ax.set_xlabel("w",color=FG,fontsize=10); ax.set_ylabel("b",color=FG,fontsize=10)
ax.set_xlim(-80,320); ax.set_ylim(170,580)
fig.tight_layout(); fig.savefig("img/scaling-after.png",transparent=True); plt.close(fig)
print("after figure done; path end =", np.round(path[-1],2), "J=", round(J(*path[-1]),3))
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
FG, MUTED, GRID, BLUE, ORANGE, GREEN = "#b8c2cc", "#8b949e", "#3f4650", "#58a6ff", "#f0883e", "#3fb950"

# 原始 13 个样本
x0 = np.array([1.0, 1.5, 2.0, 2.2, 2.8, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.5, 7.0])
y0 = np.array([0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1], float)
# 追加 3 个远端样本（都良性）
xa = np.concatenate([x0, [12.0, 14.0, 16.0]])
ya = np.concatenate([y0, [1, 1, 1]])

def fit(x, y):
    A = np.c_[x, np.ones_like(x)]
    (w, b), *_ = np.linalg.lstsq(A, y, rcond=None)
    return w, b

w1, b1 = fit(x0, y0)
w2, b2 = fit(xa, ya)
bd1 = (0.5 - b1)/w1
bd2 = (0.5 - b2)/w2
print("原始: w=%.4f b=%.4f  0.5 的交叉点 x=%.3f" % (w1, b1, bd1))
print("加远端: w=%.4f b=%.4f  0.5 的交叉点 x=%.3f" % (w2, b2, bd2))
print("斜率变化: %.4f -> %.4f  (%.0f%%)" % (w1, w2, (w2-w1)/abs(w1)*100))
print("边界右移 %.2f cm，而数据只多了 3 个点" % (bd2-bd1))

def style(ax):
    ax.set_facecolor("none"); ax.tick_params(colors=MUTED, labelsize=8)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_color(GRID)
    ax.grid(True, color=GRID, linewidth=0.5, alpha=0.6)

fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.8), dpi=200, sharey=True)
fig.patch.set_alpha(0)
for ax, (x, y, w, b, bd, added) in zip(axes, [
        (x0, y0, w1, b1, bd1, False),
        (xa, ya, w2, b2, bd2, True)]):
    if added:
        ax.scatter(x0, y0, s=34, color=BLUE, alpha=.9, edgecolor="none", zorder=3, label="原始样本")
        ax.scatter([12,14,16], [1,1,1], s=46, color=ORANGE, marker="s", edgecolor="none", zorder=4, label="新增的 3 个")
    else:
        ax.scatter(x, y, s=34, color=BLUE, alpha=.9, edgecolor="none", zorder=3, label="样本")
    xs = np.linspace(0.5, 17, 200)
    ax.plot(xs, w*xs+b, color=GREEN, lw=1.8, zorder=5, label="线性拟合")
    ax.axhline(-0.25, color="#0d1117", lw=0)
    ax.axhline(0.5, color=MUTED, lw=1, ls="--", zorder=2)
    ax.axvline(bd, color=ORANGE, lw=1.2, ls=":", zorder=2)
    ax.annotate("", xy=(bd, 0.5), xytext=(bd, 0.5))
    ax.text(bd+0.15, 0.52, "边界 x=%.2f" % bd, color=ORANGE, fontsize=8, va="bottom")
    style(ax)
    ax.set_xlabel("肿瘤大小（cm）", color=FG, fontsize=9)
    ax.set_xlim(0, 17.5); ax.set_ylim(-0.45, 1.45)
    ax.set_yticks([0, 0.5, 1]); ax.set_yticklabels(["0 恶性", "0.5", "1 良性"])
    ax.set_title("原始数据" if not added else "加 3 个远端样本后", color=FG, fontsize=9.5, pad=6)
    lg = ax.legend(loc="lower right", frameon=False, fontsize=7)
    for t in lg.get_texts(): t.set_color(FG)
axes[0].set_ylabel("标签 y", color=FG, fontsize=9)
fig.tight_layout()
fig.savefig("img/logistic-intro.png", transparent=True)
plt.close(fig)
print("figure done")
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
FG, MUTED, GRID, BLUE, ORANGE, GREEN, PURPLE = "#b8c2cc", "#8b949e", "#3f4650", "#58a6ff", "#f0883e", "#3fb950", "#d2a8ff"
Path("img").mkdir(exist_ok=True)

def style(ax):
    ax.set_facecolor("none"); ax.tick_params(colors=MUTED, labelsize=8)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_color(GRID)
    ax.grid(True, color=GRID, linewidth=0.5, alpha=0.6)

def sig(z): return 1.0/(1.0+np.exp(-z))

# ---------- 图1：S 曲线拟合肿瘤数据 ----------
x0 = np.array([1.0,1.5,2.0,2.2,2.8,3.0,3.5,4.0,4.5,5.0,5.5,6.5,7.0])
y0 = np.array([0,0,0,0,0,0,0,1,1,1,1,1,1], float)
m = x0.size
w, b, lr = 0.0, 0.0, 0.9
for _ in range(4000):
    p = sig(w*x0 + b)
    gw = np.mean((p - y0) * x0); gb = np.mean(p - y0)
    w -= lr*gw; b -= lr*gb
print("拟合结果 w=%.3f b=%.3f" % (w,b))
for xs in [3.0, 4.0, 5.0]:
    print("  大小 %.1f cm -> 预测 %.3f" % (xs, sig(w*xs+b)))

fig, ax = plt.subplots(figsize=(6.6, 3.6), dpi=200); fig.patch.set_alpha(0)
ax.scatter(x0, y0, s=42, color=BLUE, alpha=.9, edgecolor="none", zorder=3, label="样本")
xs = np.linspace(0, 8.4, 400)
ax.plot(xs, sig(w*xs+b), color=GREEN, lw=2.0, zorder=4, label="Sigmoid 拟合")
ax.axhline(0.5, color=MUTED, lw=1, ls="--", zorder=2)
xb = -b/w
ax.axvline(xb, color=ORANGE, lw=1.1, ls=":", zorder=2)
ax.text(xb+0.12, 0.05, "边界 x=%.2f" % xb, color=ORANGE, fontsize=8)
for xv in (4.5, 6.0):
    ax.plot([xv],[sig(w*xv+b)],"o",color=ORANGE,ms=6,zorder=6)
    ax.annotate("%.0f%%" % (100*sig(w*xv+b)), xy=(xv, sig(w*xv+b)), xytext=(xv+0.35, sig(w*xv+b)-0.16),
                color=ORANGE, fontsize=8)
style(ax); ax.set_xlabel("肿瘤大小（cm）", color=FG, fontsize=9)
ax.set_ylabel("预测概率", color=FG, fontsize=9)
ax.set_xlim(0, 8.4); ax.set_ylim(-0.05, 1.08)
lg = ax.legend(loc="lower right", frameon=False, fontsize=7.5)
for t in lg.get_texts(): t.set_color(FG)
fig.tight_layout(); fig.savefig("img/sigmoid-fit.png", transparent=True); plt.close(fig)

# ---------- 图2：Sigmoid 本身 ----------
fig, ax = plt.subplots(figsize=(6.6, 3.4), dpi=200); fig.patch.set_alpha(0)
z = np.linspace(-8, 8, 400)
ax.plot(z, sig(z), color=GREEN, lw=2.2, zorder=3)
ax.axhline(0.5, color=MUTED, lw=0.9, ls="--")
ax.axhline(1.0, color=GRID, lw=0.9, ls=":")
ax.axhline(0.0, color=GRID, lw=0.9, ls=":")
ax.axvline(0, color=GRID, lw=0.9, ls=":")
for zv in (-6, -3, 0, 3, 6):
    ax.plot([zv],[sig(zv)],"o",color=ORANGE,ms=6,zorder=5)
    ax.annotate("%.2f" % sig(zv), xy=(zv, sig(zv)), xytext=(zv, sig(zv)+ (0.13 if zv<4 else -0.18)),
                color=ORANGE, fontsize=8, ha="center")
style(ax); ax.set_xlabel("z", color=FG, fontsize=10); ax.set_ylabel("g(z)", color=FG, fontsize=10)
ax.set_xlim(-8, 8); ax.set_ylim(-0.08, 1.12)
ax.text(4.6, 0.06, "z 越大越接近 1\n但永远不等于 1", color=MUTED, fontsize=8, ha="center")
fig.tight_layout(); fig.savefig("img/sigmoid.png", transparent=True); plt.close(fig)

# ---------- 图3：常见激活函数 ----------
acts = [
    ("Sigmoid", lambda t: 1/(1+np.exp(-t)), GREEN),
    ("Tanh",    lambda t: np.tanh(t),        PURPLE),
    ("ReLU",    lambda t: np.maximum(0, t),  ORANGE),
    ("Leaky ReLU", lambda t: np.where(t>0, t, 0.1*t), BLUE),
]
fig, axes = plt.subplots(1, 4, figsize=(9.4, 2.6), dpi=200)
fig.patch.set_alpha(0)
for ax,(name,f,c) in zip(axes, acts):
    t = np.linspace(-4, 4, 400)
    ax.plot(t, f(t), color=c, lw=2.0)
    ax.axhline(0, color=GRID, lw=0.9); ax.axvline(0, color=GRID, lw=0.9)
    style(ax); ax.set_title(name, color=FG, fontsize=9, pad=5)
    ax.set_ylim(-1.3, 3.2); ax.set_xlim(-4,4)
    ax.set_xlabel("z", color=MUTED, fontsize=7.5)
fig.tight_layout(); fig.savefig("img/activations.png", transparent=True); plt.close(fig)
print("figs 1-3 done")
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
# ============================================================
# 以下为修正版（覆盖前面同名输出）
# ============================================================

# ---------- 修正：Sigmoid 拟合肿瘤（精确百分比） ----------
x0 = np.array([1.0,1.5,2.0,2.2,2.8,3.0,3.5,4.0,4.5,5.0,5.5,6.5,7.0])
y0 = np.array([0,0,0,0,0,0,0,1,1,1,1,1,1], float)
w, b, lr = 0.0, 0.0, 0.9
for _ in range(4000):
    p = sig(w*x0 + b); gw = np.mean((p-y0)*x0); gb = np.mean(p-y0)
    w -= lr*gw; b -= lr*gb
fig, ax = plt.subplots(figsize=(6.6, 3.6), dpi=200); fig.patch.set_alpha(0)
ax.scatter(x0, y0, s=42, color=BLUE, alpha=.9, edgecolor="none", zorder=3, label="样本")
xs = np.linspace(0, 8.4, 400)
ax.plot(xs, sig(w*xs+b), color=GREEN, lw=2.0, zorder=4, label="Sigmoid 拟合")
ax.axhline(0.5, color=MUTED, lw=1, ls="--", zorder=2)
xb = -b/w
ax.axvline(xb, color=ORANGE, lw=1.1, ls=":", zorder=2)
ax.text(xb-0.15, 0.62, "边界 x=%.2f" % xb, color=ORANGE, fontsize=8, ha="right")
for xv, txt, dy in [(4.0,"82.8%",0.10),(4.5,"99.0%",0.06),(6.0,">99.99%",-0.16)]:
    yv = sig(w*xv+b)
    ax.plot([xv],[yv],"o",color=ORANGE,ms=6,zorder=6)
    ax.annotate(txt, xy=(xv,yv), xytext=(xv+0.1, min(yv+dy,1.03)), color=ORANGE, fontsize=8)
style(ax); ax.set_xlabel("肿瘤大小（cm）", color=FG, fontsize=9)
ax.set_ylabel("预测概率", color=FG, fontsize=9)
ax.set_xlim(0,8.4); ax.set_ylim(-0.05,1.12)
lg = ax.legend(loc="lower right", frameon=False, fontsize=7.5)
for t in lg.get_texts(): t.set_color(FG)
fig.tight_layout(); fig.savefig("img/sigmoid-fit.png", transparent=True); plt.close(fig)

# ---------- 修正：Sigmoid 本体（精确数值） ----------
fig, ax = plt.subplots(figsize=(6.6, 3.4), dpi=200); fig.patch.set_alpha(0)
z = np.linspace(-8, 8, 400)
ax.plot(z, sig(z), color=GREEN, lw=2.2, zorder=3)
ax.axhline(0.5, color=MUTED, lw=0.9, ls="--")
ax.axhline(1.0, color=GRID, lw=0.9, ls=":"); ax.axhline(0.0, color=GRID, lw=0.9, ls=":")
ax.axvline(0, color=GRID, lw=0.9, ls=":")
for zv, lab, dy in [(-6,"0.0025",0.14),(-3,"0.047",0.14),(0,"0.500",0.14),(3,"0.953",0.12),(6,"0.9975",-0.20)]:
    ax.plot([zv],[sig(zv)],"o",color=ORANGE,ms=6,zorder=5)
    ax.annotate(lab, xy=(zv,sig(zv)), xytext=(zv,sig(zv)+dy), color=ORANGE, fontsize=8, ha="center")
style(ax); ax.set_xlabel("z", color=FG, fontsize=10); ax.set_ylabel("g(z)", color=FG, fontsize=10)
ax.set_xlim(-8,8); ax.set_ylim(-0.10,1.15)
ax.text(4.9, 0.10, "z 再大也到不了 1\n只是无限逼近", color=MUTED, fontsize=8, ha="center")
fig.tight_layout(); fig.savefig("img/sigmoid.png", transparent=True); plt.close(fig)

# ---------- 重建：原始肿瘤散点 ----------
fig, ax = plt.subplots(figsize=(6.6, 3.4), dpi=200); fig.patch.set_alpha(0)
ax.scatter(x0, y0, s=40, color=BLUE, alpha=.9, edgecolor="none", zorder=3)
style(ax); ax.set_xlabel("肿瘤大小（cm）", color=FG, fontsize=10)
ax.set_ylabel("标签 y", color=FG, fontsize=10)
ax.set_xlim(0,8.2); ax.set_ylim(-0.35,1.35)
ax.set_yticks([0,1]); ax.set_yticklabels(["0 恶性","1 良性"])
ax.text(3.9, 0.5, "中间这片区域是空的\n肿瘤不可能「70% 良性」", ha="center", va="center", color=MUTED, fontsize=8.5)
fig.tight_layout(); fig.savefig("img/logistic-original.png", transparent=True); plt.close(fig)

# ---------- 重建：决策边界三联图 ----------
def _sig2(z): return 1.0/(1.0+np.exp(-z))
def _fit(F, y, lr=0.5, iters=8000):
    m, n = F.shape; mu, sd = F.mean(0), F.std(0); Fs = (F-mu)/sd
    A = np.c_[Fs, np.ones(m)]; th = np.zeros(n+1)
    for _ in range(iters):
        p = _sig2(A @ th); th -= lr * (A.T @ (p-y))/m
    return th, mu, sd
def _zval(x1, x2, th, mu, sd, poly):
    f = np.column_stack([x1.ravel(), x2.ravel()] + ([x1.ravel()**2, x2.ravel()**2] if poly else []))
    return (((f-mu)/sd) @ th[:-1] + th[-1]).reshape(x1.shape)
rng = np.random.default_rng(5); n = 40
XA = np.r_[rng.normal(1,1,n), rng.normal(-1,1,n)]; YA_ = np.r_[rng.normal(1,1,n), rng.normal(-1,1,n)]
yA = np.r_[np.ones(n), np.zeros(n)]
FA = np.column_stack([XA, YA_]); thA, muA, sdA = _fit(FA, yA)
n = 45
r_in = rng.uniform(0,1.2,n); t_in = rng.uniform(0,2*np.pi,n)
r_out = rng.uniform(2.6,3.6,n); t_out = rng.uniform(0,2*np.pi,n)
X1 = np.r_[r_in*np.cos(t_in), r_out*np.cos(t_out)]; X2 = np.r_[r_in*np.sin(t_in), r_out*np.sin(t_out)]
yC = np.r_[np.ones(n), np.zeros(n)]
FC = np.column_stack([X1,X2]); thB, muB, sdB = _fit(FC, yC)
FP = np.column_stack([X1,X2,X1**2,X2**2]); thC, muC, sdC = _fit(FP, yC)
gg = np.linspace(-4.2,4.2,400); G1, G2 = np.meshgrid(gg, gg)
fig, axes = plt.subplots(1,3, figsize=(9.6,3.2), dpi=200); fig.patch.set_alpha(0)
def _sc(ax,x1,x2,y):
    ax.scatter(x1[y==1],x2[y==1],s=22,color=BLUE,alpha=.85,edgecolor="none",zorder=3,label="y = 1")
    ax.scatter(x1[y==0],x2[y==0],s=22,color=ORANGE,alpha=.85,marker="s",edgecolor="none",zorder=3,label="y = 0")
specs = [(XA,YA_,yA,thA,muA,sdA,False,"线性边界（直线）"),
         (X1,X2,yC,thB,muB,sdB,False,"同样的直线，换一批数据"),
         (X1,X2,yC,thC,muC,sdC,True,"二次特征 → 圆形边界")]
for ax,(a1,a2,yy,th,mu,sd,po,ti) in zip(axes, specs):
    _sc(ax,a1,a2,yy)
    ax.contour(G1,G2,_zval(G1,G2,th,mu,sd,po),levels=[0],colors=GREEN,linewidths=2.0)
    ax.set_title(ti, color=FG, fontsize=9, pad=6)
    ax.set_xlim(-4.2,4.2); ax.set_ylim(-4.2,4.2); ax.set_aspect("equal"); style(ax)
    ax.set_xlabel("x1", color=MUTED, fontsize=8); ax.set_ylabel("x2", color=MUTED, fontsize=8)
lg = axes[2].legend(loc="upper right", frameon=False, fontsize=7)
for t in lg.get_texts(): t.set_color(FG)
fig.tight_layout(); fig.savefig("img/decision-boundary.png", transparent=True); plt.close(fig)

print("ALL FIGURES DONE")

# ---------- 图：交叉熵 vs 平方误差 ----------
f = np.linspace(0.001, 0.999, 600)
ce1 = -np.log(f)          # y=1 时的交叉熵
ce0 = -np.log(1-f)        # y=0 时的交叉熵
se1 = (f-1)**2            # y=1 时的平方误差
se0 = f**2                # y=0 时的平方误差

fig, ax = plt.subplots(figsize=(6.8, 3.8), dpi=200); fig.patch.set_alpha(0)
ax.plot(f, ce1, color=GREEN, lw=2.0, label="交叉熵  y=1")
ax.plot(f, ce0, color=ORANGE, lw=2.0, label="交叉熵  y=0")
ax.plot(f, se1, color=GREEN, lw=1.4, ls="--", alpha=.65, label="平方误差  y=1")
ax.plot(f, se0, color=ORANGE, lw=1.4, ls="--", alpha=.65, label="平方误差  y=0")
style(ax)
ax.set_xlabel("模型的预测值 f(x)", color=FG, fontsize=9)
ax.set_ylabel("损失", color=FG, fontsize=9)
ax.set_xlim(0, 1); ax.set_ylim(0, 6)
ax.annotate("y=1 却预测 0.01\n损失 4.6", xy=(0.01, 4.6), xytext=(0.16, 5.0),
            color=GREEN, fontsize=8,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1))
ax.annotate("平方误差在这里只有 0.98", xy=(0.01, 0.98), xytext=(0.18, 0.35),
            color=MUTED, fontsize=8,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
lg = ax.legend(loc="upper center", frameon=False, fontsize=7.5, ncol=2)
for t in lg.get_texts(): t.set_color(FG)
fig.tight_layout(); fig.savefig("img/cross-entropy.png", transparent=True); plt.close(fig)

# ---------- 数值：用肿瘤数据算几个样本的损失 ----------
def _sig3(z): return 1.0/(1.0+np.exp(-z))
W, B = 5.987, -22.375
def _f(xv): return _sig3(W*xv + B)
print("=== 逐样本损失（w=5.987, b=-22.375）===")
for xv, yv, note in [(4.0, 1, "良性、判对了"), (2.0, 0, "恶性、判对了"),
                     (1.0, 1, "假设 1cm 的其实是良性（自信地判错）")]:
    pv = _f(xv)
    pv = min(max(pv, 1e-12), 1-1e-12)
    ce = -(yv*np.log(pv) + (1-yv)*np.log(1-pv))
    se = (pv-yv)**2
    print("  x=%.1f y=%d  f=%9.6f  交叉熵=%8.4f  平方误差=%8.4f  %s" % (xv,yv,pv,ce,se,note))
print("总交叉熵 J = %.4f" % np.mean([-(yy*np.log(min(max(_f(xx),1e-12),1-1e-12))) - (1-yy)*np.log(1-min(max(_f(xx),1e-12),1-1e-12))
      for xx, yy in zip(np.array([1.0,1.5,2.0,2.2,2.8,3.0,3.5,4.0,4.5,5.0,5.5,6.5,7.0]),
                          np.array([0,0,0,0,0,0,0,1,1,1,1,1,1], float))]))
print("ALL DONE")

# ---------- 图：MSE 在两种模型下的形状 ----------
_tx = np.array([1.0,1.5,2.0,2.2,2.8,3.0,3.5,4.0,4.5,5.0,5.5,6.5,7.0])
_ty = np.array([0,0,0,0,0,0,0,1,1,1,1,1,1], float)
_ws = np.linspace(0, 12, 600)

# 线性模型 + MSE：碗形
_J_lin = np.array([np.mean((w*_tx - _ty)**2)/2 for w in _ws])
fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=200); fig.patch.set_alpha(0)
ax.plot(_ws, _J_lin, color=BLUE, lw=2.2)
style(ax); ax.set_xlabel("w", color=FG, fontsize=10); ax.set_ylabel("J(w)", color=FG, fontsize=10)
ax.set_xlim(0, 12); ax.set_ylim(0, None)
imin = int(np.argmin(_J_lin))
ax.plot([_ws[imin]], [_J_lin[imin]], "o", color=GREEN, ms=7, zorder=5)
ax.annotate("一个最低点", xy=(_ws[imin], _J_lin[imin]), xytext=(_ws[imin]+1.5, _J_lin[imin]+1.2),
            color=GREEN, fontsize=8.5, arrowprops=dict(arrowstyle="->", color=GREEN, lw=1))
ax.text(0.5, _J_lin.max()*0.75, "线性模型 + 平方误差\n光滑的碗形", color=MUTED, fontsize=8.5)
fig.tight_layout(); fig.savefig("img/j-bowl.png", transparent=True); plt.close(fig)

# 逻辑回归 + MSE：坑坑洼洼
_J_log = np.array([np.mean((1/(1+np.exp(-w*_tx)) - _ty)**2)/2 for w in _ws])
fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=200); fig.patch.set_alpha(0)
ax.plot(_ws, _J_log, color=ORANGE, lw=2.2)
style(ax); ax.set_xlabel("w", color=FG, fontsize=10); ax.set_ylabel("J(w)", color=FG, fontsize=10)
ax.set_xlim(0, 12); ax.set_ylim(0, None)
from scipy.signal import argrelextrema
mins = argrelextrema(_J_log, np.less_equal, order=25)[0]
mins = [i for i in mins if 0 < i < len(_ws)-1][:4]
for i in mins:
    ax.plot([_ws[i]], [_J_log[i]], "o", color=MUTED, ms=6, zorder=5)
if len(mins) >= 2:
    ax.annotate("好几个坑", xy=(_ws[mins[1]], _J_log[mins[1]]),
                xytext=(_ws[mins[1]]+1.4, _J_log[mins[1]]+0.22),
                color=MUTED, fontsize=8.5, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
ax.text(0.5, _J_log.max()*0.72, "逻辑回归 + 平方误差\n曲线坑坑洼洼", color=MUTED, fontsize=8.5)
fig.tight_layout(); fig.savefig("img/j-bumpy.png", transparent=True); plt.close(fig)
print("局部极小点数:", len(mins), "位置 w ≈", [round(float(_ws[i]),1) for i in mins])

# ---------- 图：-log(f) 与 -log(1-f) ----------
f = np.linspace(0.001, 0.999, 600)
fig, ax = plt.subplots(figsize=(6.6, 3.6), dpi=200); fig.patch.set_alpha(0)
ax.plot(f, -np.log(f), color=GREEN, lw=2.2, label="y = 1 时：-log(f)")
ax.plot(f, -np.log(1-f), color=ORANGE, lw=2.2, label="y = 0 时：-log(1-f)")
style(ax); ax.set_xlabel("模型预测的概率 f", color=FG, fontsize=9)
ax.set_ylabel("损失 L", color=FG, fontsize=9)
ax.set_xlim(0,1); ax.set_ylim(0,5)
ax.plot([0.9],[ -np.log(0.9)], "o", color=GREEN, ms=6, zorder=5)
ax.annotate("判对且自信 → 0.105", xy=(0.9,-np.log(0.9)), xytext=(0.55,1.6),
            color=GREEN, fontsize=8, arrowprops=dict(arrowstyle="->", color=GREEN, lw=1))
ax.plot([0.1],[ -np.log(0.1)], "o", color=GREEN, ms=6, zorder=5)
ax.annotate("判错且自信 → 2.30", xy=(0.1,-np.log(0.1)), xytext=(0.13,3.4),
            color=GREEN, fontsize=8, arrowprops=dict(arrowstyle="->", color=GREEN, lw=1))
lg = ax.legend(loc="upper center", frameon=False, fontsize=8)
for t in lg.get_texts(): t.set_color(FG)
fig.tight_layout(); fig.savefig("img/log-loss.png", transparent=True); plt.close(fig)
print("ALL DONE")

# ---------- 图：逻辑回归 + 平方误差的损失地形 ----------
_tx2 = np.array([1.,1.5,2,2.2,2.8,3,3.5,4,4.5,5,5.5,6.5,7])
_ty2 = np.array([0,0,0,0,0,0,0,1,1,1,1,1,1], float)
def _Js(w, b):
    return np.mean((1/(1+np.exp(-(w[...,None]*_tx2 + b[...,None]))) - _ty2)**2, axis=-1)/2
def _gs(w, b):
    p = 1/(1+np.exp(-(w*_tx2 + b))); r = p - _ty2; d = r*p*(1-p)
    return float(np.mean(d*_tx2)), float(np.mean(d))

Wg, Bg = np.meshgrid(np.linspace(-2, 10, 240), np.linspace(-50, 30, 240))
Zg = _Js(Wg, Bg)

fig, ax = plt.subplots(figsize=(6.6, 4.2), dpi=200); fig.patch.set_alpha(0)
lv = np.logspace(np.log10(0.011), np.log10(0.235), 11)
ax.contourf(Wg, Bg, np.log10(Zg), levels=np.log10(lv), cmap="inferno", alpha=.85, extend="both")
ax.contour(Wg, Bg, np.log10(Zg), levels=np.log10(lv), colors="#e6edf3", linewidths=.4, alpha=.3)
starts = [(0.0,-45.0,"#58a6ff"), (9.0,25.0,"#3fb950"), (5.0,-5.0,"#d2a8ff")]
for w0,b0,col in starts:
    w,bb = w0,b0; path=[(w,bb)]
    for _ in range(300):
        gw,gb = _gs(w,bb); w -= 0.5*gw; bb -= 0.5*gb
        path.append((w,bb))
    path=np.array(path)
    ax.plot(path[:,0], path[:,1], color=col, lw=1.6, alpha=.95)
    ax.plot([w0],[b0],"o",color=col,ms=6,mec="#0d1117",mew=1,zorder=6)
    ax.plot([path[-1,0]],[path[-1,1]],"*",color=col,ms=13,zorder=7)
style(ax)
ax.set_xlabel("w", color=FG, fontsize=10); ax.set_ylabel("b", color=FG, fontsize=10)
ax.set_xlim(-2,10); ax.set_ylim(-50,30)
ax.text(0.05, 0.93, "同一个损失，不同起点落到不同结局", transform=ax.transAxes,
        color=FG, fontsize=8.5)
fig.tight_layout(); fig.savefig("img/j-landscape.png", transparent=True); plt.close(fig)
print("landscape done")

# ---------- 图：凸 vs 非凸（示意图，参照官方幻灯片） ----------
def _draw_down_arrows(ax, t, J, idx, color):
    for i in idx:
        if i+1 >= len(t): continue
        ax.annotate("", xy=(t[i+1], J[i+1]), xytext=(t[i], J[i]),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3, mutation_scale=11))

fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.0), dpi=200)
fig.patch.set_alpha(0)

# 左：凸
t = np.linspace(0.1, 5.2, 400)
Jc = 0.32*(t-2.7)**2 + 0.30
ax = axes[0]
ax.plot(t, Jc, color=GREEN, lw=2.0)
idx = [40, 75, 110, 145]
_draw_down_arrows(ax, t, Jc, idx, ORANGE)
imin = int(np.argmin(Jc))
ax.plot([t[imin]], [Jc[imin]], "o", color=ORANGE, ms=9, mfc="none", mew=2.0, zorder=6)
style(ax); ax.set_title("线性回归 + 平方误差：凸", color=FG, fontsize=9.5, pad=8)
ax.set_xlabel("参数", color=MUTED, fontsize=8); ax.set_ylabel("J", color=MUTED, fontsize=8)
ax.set_xlim(0, 5.3); ax.set_ylim(0, 2.6); ax.set_xticks([]); ax.set_yticks([])
ax.text(0.5, 0.90, "只有一个坑，怎么走都到得了底", transform=ax.transAxes,
        ha="center", color=MUTED, fontsize=8)

# 右：非凸
Jn = 0.30*(t-2.7)**2 + 0.20*np.sin(3.4*t) + 0.62
ax = axes[1]
ax.plot(t, Jn, color=ORANGE, lw=2.0)
idx = [20, 55, 88]
_draw_down_arrows(ax, t, Jn, idx, GREEN)
loc = np.where((Jn[1:-1] < Jn[:-2]) & (Jn[1:-1] < Jn[2:]))[0] + 1
loc = [i for i in loc if 0.3 < t[i] < 5.0]
for i in loc:
    ax.plot([t[i]], [Jn[i]], "o", color=MUTED, ms=7, mfc="none", mew=1.6, zorder=6)
if len(loc) >= 2:
    ax.annotate("停在这", xy=(t[loc[0]], Jn[loc[0]]), xytext=(t[loc[0]]+0.1, Jn[loc[0]]+0.55),
                color=FG, fontsize=8, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
style(ax); ax.set_title("逻辑回归 + 平方误差：非凸", color=FG, fontsize=9.5, pad=8)
ax.set_xlabel("参数", color=MUTED, fontsize=8); ax.set_ylabel("J", color=MUTED, fontsize=8)
ax.set_xlim(0, 5.3); ax.set_ylim(0, 2.6); ax.set_xticks([]); ax.set_yticks([])
ax.text(0.5, 0.90, "好几个坑，可能停在浅的那个", transform=ax.transAxes,
        ha="center", color=MUTED, fontsize=8)
fig.tight_layout()
fig.savefig("img/convex-vs-nonconvex.png", transparent=True)
plt.close(fig)
print("convex figure done")

# ---------- 图：逻辑回归梯度下降的损失曲线 + 拟合结果 ----------
_gx = np.array([1.0,1.5,2,2.2,2.8,3,3.5,4,4.5,5,5.5,6.5,7])
_gy = np.array([0,0,0,0,0,0,0,1,1,1,1,1,1], float)
def _sg(z): return 1/(1+np.exp(-z))
def _J(w,b):
    f = np.clip(_sg(w*_gx+b), 1e-12, 1-1e-12)
    return float(-np.mean(_gy*np.log(f)+(1-_gy)*np.log(1-f)))
def _g(w,b):
    r = _sg(w*_gx+b)-_gy
    return float(np.mean(r*_gx)), float(np.mean(r))

_a = 0.5
_w, _b = 0.0, 0.0
_hist = [_J(_w,_b)]
for _ in range(2000):
    _gw, _gb = _g(_w,_b); _w -= _a*_gw; _b -= _a*_gb
    _hist.append(_J(_w,_b))
print("GD 最终: w=%.4f b=%.4f J=%.6f" % (_w,_b,_hist[-1]))
print("轨迹:", [(i, round(_hist[i],5)) for i in [0,1,5,10,50,100,500,2000] if i < len(_hist)])

fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=200); fig.patch.set_alpha(0)
ax.plot(range(len(_hist)), _hist, color=GREEN, lw=1.8)
style(ax)
ax.set_xlabel("迭代次数", color=FG, fontsize=9); ax.set_ylabel("J(w,b)", color=FG, fontsize=9)
ax.set_xlim(0, 2000); ax.set_ylim(0, 0.72)
ax.axhline(0.6931, color=MUTED, lw=0.9, ls=":")
ax.text(60, 0.706, "起点 0.6931 = ln2（瞎猜的成本）", color=MUTED, fontsize=7.5)
ax.annotate("第 2000 步：%.4f" % _hist[-1], xy=(2000,_hist[-1]), xytext=(1250,0.20),
            color=GREEN, fontsize=8, arrowprops=dict(arrowstyle="->", color=GREEN, lw=1))
fig.tight_layout(); fig.savefig("img/gd-logistic-loss.png", transparent=True); plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.2), dpi=200, sharey=True)
fig.patch.set_alpha(0)
_xs = np.linspace(0, 8.2, 300)
for ax, (ww,bb,title) in zip(axes, [(0.0,0.0,"训练前：w=0, b=0"), (_w,_b,"训练后：w=%.3f, b=%.2f" % (_w,_b))]):
    ax.scatter(_gx, _gy, s=30, color=BLUE, alpha=.9, edgecolor="none", zorder=3)
    ax.plot(_xs, _sg(ww*_xs+bb), color=GREEN, lw=2.0, zorder=4)
    ax.axhline(0.5, color=MUTED, lw=0.8, ls="--", zorder=1)
    style(ax); ax.set_title(title, color=FG, fontsize=9, pad=6)
    ax.set_xlabel("肿瘤大小（cm）", color=MUTED, fontsize=8)
    ax.set_xlim(0, 8.2); ax.set_ylim(-0.06, 1.10); ax.set_xticks([]); ax.set_yticks([0,0.5,1])
    ax.set_yticklabels(["0","0.5","1"])
axes[0].set_ylabel("预测概率", color=MUTED, fontsize=8)
axes[0].text(0.5, 0.42, "整条线贴在 0.5\n等于什么都没学到", transform=axes[0].transAxes,
             ha="center", color=MUTED, fontsize=8)
fig.tight_layout(); fig.savefig("img/gd-logistic-fit.png", transparent=True); plt.close(fig)
print("gd figures done")

# ---------- 图：习题数据（两特征） ----------
_rng4 = np.random.default_rng(31)
_x1 = np.round(_rng4.uniform(1.0, 8.0, 20), 1)
_x2 = np.round(_rng4.uniform(30, 70, 20), 1)
_zl = 1.1*_x1 - 0.055*_x2 - 2.6
_y4 = (_rng4.uniform(0,1,20) < 1/(1+np.exp(-_zl))).astype(float)
fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=200); fig.patch.set_alpha(0)
ax.scatter(_x1[_y4==1], _x2[_y4==1], s=42, color=BLUE, alpha=.9, edgecolor="none", label="y = 1 良性")
ax.scatter(_x1[_y4==0], _x2[_y4==0], s=42, color=ORANGE, alpha=.9, marker="s", edgecolor="none", label="y = 0 恶性")
style(ax)
ax.set_xlabel("肿瘤大小 x1（cm）", color=FG, fontsize=9)
ax.set_ylabel("患者年龄 x2", color=FG, fontsize=9)
ax.set_xlim(0.5, 8.5); ax.set_ylim(28, 74)
lg = ax.legend(loc="upper right", frameon=False, fontsize=7.5)
for t in lg.get_texts(): t.set_color(FG)
fig.tight_layout(); fig.savefig("img/exercise-tumors.png", transparent=True); plt.close(fig)
print("exercise figure done")

# ---------- 图：偏差-方差打靶图 ----------
_rng9 = np.random.default_rng(11)
fig, axes = plt.subplots(1, 4, figsize=(9.6, 2.9), dpi=200)
fig.patch.set_alpha(0)
specs = [("低偏差 低方差", 0.0, 0.0, 0.16, "理想：又准又稳"),
         ("低偏差 高方差", 0.0, 0.0, 0.55, "抖，但平均在靶心"),
         ("高偏差 低方差", 0.42, 0.32, 0.16, "很稳，但偏了"),
         ("高偏差 高方差", 0.42, 0.32, 0.55, "又偏又抖")]
for ax, (title, cx, cy, spread, note) in zip(axes, specs):
    for r in (0.35, 0.65, 0.95):
        ax.add_patch(plt.Circle((0,0), r, fill=False, color=GRID, lw=1.0))
    ax.plot([-1.05,1.05],[0,0], color=GRID, lw=0.8)
    ax.plot([0,0],[-1.05,1.05], color=GRID, lw=0.8)
    px = cx + _rng9.normal(0, spread, 10)
    py = cy + _rng9.normal(0, spread, 10)
    ax.scatter(px, py, s=26, color=ORANGE, alpha=.85, edgecolor="none", zorder=4)
    ax.plot([cx],[cy], "x", color=BLUE, ms=11, mew=2.2, zorder=5)
    ax.set_xlim(-1.15,1.15); ax.set_ylim(-1.15,1.15); ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, color=FG, fontsize=9, pad=4)
    ax.text(0.5, -0.10, note, transform=ax.transAxes, ha="center", color=MUTED, fontsize=7.5)
fig.text(0.5, 0.012, "蓝叉 = 预测的平均位置；橙点 = 每次训练的落点", ha="center", color=MUTED, fontsize=8)
fig.tight_layout(rect=(0,0.04,1,1))
fig.savefig("img/bias-variance-darts.png", transparent=True); plt.close(fig)

# ---------- 图：训练/验证误差 vs 模型复杂度 ----------
_c = np.linspace(1, 12, 300)
_train = 0.85*np.exp(-0.45*_c) + 0.04
_val = 0.85*np.exp(-0.45*_c) + 0.05 + 0.0055*np.clip(_c-5.2,0,None)**2.1
fig, ax = plt.subplots(figsize=(6.6, 3.5), dpi=200); fig.patch.set_alpha(0)
ax.plot(_c, _train, color=BLUE, lw=2.0, label="训练误差")
ax.plot(_c, _val, color=ORANGE, lw=2.0, label="验证误差")
style(ax)
ax.set_xlabel("模型复杂度（比如多项式阶数）", color=FG, fontsize=9)
ax.set_ylabel("误差", color=FG, fontsize=9)
ax.set_xlim(1, 12); ax.set_ylim(0, 0.9); ax.set_xticks([])
_i = int(np.argmin(_val))
ax.axvline(_c[_i], color=GREEN, lw=1.0, ls=":")
ax.plot([_c[_i]], [_val[_i]], "o", color=GREEN, ms=7, zorder=6)
ax.text(1.2, 0.80, "欠拟合", color=MUTED, fontsize=8.5)
ax.text(9.6, 0.80, "过拟合", color=MUTED, fontsize=8.5)
ax.annotate("刚好", xy=(_c[_i], _val[_i]), xytext=(_c[_i]+0.3, _val[_i]+0.18),
            color=GREEN, fontsize=8.5, arrowprops=dict(arrowstyle="->", color=GREEN, lw=1))
lg = ax.legend(loc="center right", frameon=False, fontsize=8)
for t in lg.get_texts(): t.set_color(FG)
fig.tight_layout(); fig.savefig("img/complexity-curve.png", transparent=True); plt.close(fig)

# ---------- 图：学习曲线 ----------
_n = np.linspace(1, 100, 300)
fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.2), dpi=200)
fig.patch.set_alpha(0)
# 高偏差
tr_b = 0.10 + 0.25*np.exp(-_n/18)
va_b = 0.62 - 0.25*(1-np.exp(-_n/18))
for ax, (tr, va, ti, note) in zip(axes, [
        (tr_b, va_b, "高偏差（欠拟合）", "两条线很快贴住，一起停在很高的位置"),
        (0.04 + 0.03*np.exp(-_n/30), 0.16 + 0.60*np.exp(-_n/45), "高方差（过拟合）", "中间一直有条大缝，加数据能继续降")]):
    ax.plot(_n, tr, color=BLUE, lw=2.0, label="训练误差")
    ax.plot(_n, va, color=ORANGE, lw=2.0, label="验证误差")
    style(ax); ax.set_title(ti, color=FG, fontsize=9.5, pad=6)
    ax.set_xlabel("训练样本数 m", color=MUTED, fontsize=8); ax.set_ylabel("误差", color=MUTED, fontsize=8)
    ax.set_xlim(0,100); ax.set_ylim(0, 0.85); ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.5, 0.06, note, transform=ax.transAxes, ha="center", color=MUTED, fontsize=7.5)
lg = axes[0].legend(loc="center right", frameon=False, fontsize=7.5)
for t in lg.get_texts(): t.set_color(FG)
fig.tight_layout(); fig.savefig("img/learning-curves.png", transparent=True); plt.close(fig)
print("chapter5 figures done")

# ---------- 图：k 折交叉验证示意 ----------
kf = 5
fig, ax = plt.subplots(figsize=(8.2, 3.2), dpi=200); fig.patch.set_alpha(0)
for i in range(kf):
    yy = kf - i
    for j in range(kf):
        col = ORANGE if j == i else BLUE
        alpha = 0.85 if j == i else 0.30
        ax.add_patch(plt.Rectangle((j, yy-0.32), 0.94, 0.64, facecolor=col, alpha=alpha,
                                   edgecolor=GRID, lw=0.8))
    ax.text(-0.15, yy, "第 %d 折" % (i+1), ha="right", va="center", color=FG, fontsize=8.5)
    pass
ax.set_xlim(-1.4, 5.1); ax.set_ylim(0.1, 5.8)
ax.axis("off")
ax.text(2.5, 5.65, "橙色 = 这一折拿来当验证集　蓝色 = 训练集", ha="center", color=FG, fontsize=9)
ax.text(2.5, 0.30, "把 5 个验证分数平均 → 最终分数", ha="center", color=GREEN, fontsize=9)
fig.tight_layout(); fig.savefig("img/k-fold.png", transparent=True); plt.close(fig)
print("k-fold figure done")
