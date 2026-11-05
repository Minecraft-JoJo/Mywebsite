# -*- coding: utf-8 -*-
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
