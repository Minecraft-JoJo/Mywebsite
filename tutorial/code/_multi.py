# -*- coding: utf-8 -*-
import numpy as np
rng = np.random.default_rng(11)
m = 20
area  = np.array([45,52,58,63,68,74,80,86,92,98,104,110,117,124,132,140,148,156,163,171], float)
floor = np.array([1,3,5,2,7,6,9,4,11,8,13,10,15,12,18,14,16,20,17,19], float)
age   = np.array([22,18,25,30,15,12,8,20,6,10,5,14,3,9,11,4,7,2,13,16], float)
price = np.round(2.6*area + 1.5*floor - 1.8*age + 60 + rng.normal(0, 10, m), 1)

X = np.c_[area, floor, age]
print("m =", m)
print("前 3 行:")
for i in range(3):
    print("  area=%3.0f floor=%2.0f age=%2.0f price=%6.1f" % (area[i], floor[i], age[i], price[i]))

def J(w, b):
    r = X @ w + b - price
    return float(np.mean(r**2) / 2)

def grad_loop(w, b):
    r = X @ w + b - price
    return np.array([np.mean(r * X[:, j]) for j in range(X.shape[1])]), float(np.mean(r))

# 矩阵形式：设计矩阵 A = [1, X]
A = np.c_[np.ones(m), X]          # m x 4，第一列是给 b 的常数 1
theta = np.array([0.0, 1.0, 0.5, -0.5])   # [b, w1, w2, w3]

def grad_matrix(theta):
    r = A @ theta - price
    return (1.0/m) * (A.T @ r)

g_loop, g_b = grad_loop(np.array([1.0, 0.5, -0.5]), 0.0)
g_mat = grad_matrix(theta)
print("\n起点 J = %.4f" % J(np.array([1.0,0.5,-0.5]), 0.0))
print("逐参偏导 dw =", np.round(g_loop, 3), " db = %.3f" % g_b)
print("矩阵形式   =", np.round(g_mat, 3), "  (顺序 [b,w1,w2,w3])")
print("两者一致:", np.allclose(np.r_[g_b, g_loop], g_mat))

# 梯度下降几步
alpha = 1e-5
w = np.array([1.0, 0.5, -0.5]); b = 0.0
print("\nstep |      w1    w2     w3       b         J")
for i in range(0, 6):
    print("%4d | %8.4f %6.2f %7.2f %7.4f %10.2f" % (i, w[0], w[1], w[2], b, J(w,b)))
    g, gb = grad_loop(w, b)
    w = w - alpha*g; b = b - alpha*gb

# 正规方程
sol, *_ = np.linalg.lstsq(A, price, rcond=None)
print("\n正规方程 theta =", np.round(sol, 4), " J = %.4f" % J(sol[1:], sol[0]))
