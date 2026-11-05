"""第 1 章示例：训练，就是让一个数字变小。

任务：猜出 y = 2x + 1 这条线（数据有噪声）。
你现在不需要看懂梯度下降的公式，只需要盯着 loss 这个数字往下走。
"""

import numpy as np

# ---------- 1. 造一批数据 ----------
rng = np.random.default_rng(42)

x = rng.uniform(-1, 1, size=(100, 1))          # 100 个样本，每个 1 个特征
y = 2.0 * x + 1.0 + rng.normal(0, 0.1, (100, 1))  # 真值 + 噪声

# ---------- 2. 随便猜一个初始参数 ----------
w = 0.0   # 我们想让 w 变成 2
b = 0.0   # 我们想让 b 变成 1

lr = 0.5  # 学习率：每次往前走多大一步
history = []

# ---------- 3. 反复调整 ----------
for epoch in range(201):
    y_pred = x * w + b                 # 前向：用当前参数做预测
    loss = np.mean((y_pred - y) ** 2)  # 损失：预测错了多少（均方误差）
    history.append(loss)

    dw = 2 * np.mean((y_pred - y) * x)  # 损失对 w 的导数
    db = 2 * np.mean(y_pred - y)        # 损失对 b 的导数

    w -= lr * dw                        # 沿着导数反方向走一小步
    b -= lr * db

    if epoch in (0, 1, 2, 5, 10, 20, 50, 100, 200):
        print(f"epoch {epoch:3d}   loss={loss:8.4f}   w={w:7.4f}   b={b:7.4f}")

print()
print(f"最终 w = {w:.4f}   （真值 2.0）")
print(f"最终 b = {b:.4f}   （真值 1.0）")
print(f"loss 从 {history[0]:.4f} 降到 {history[-1]:.6f}")
