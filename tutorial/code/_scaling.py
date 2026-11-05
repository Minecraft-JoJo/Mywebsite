# -*- coding: utf-8 -*-
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
print("figures done")