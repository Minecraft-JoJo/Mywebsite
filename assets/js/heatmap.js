/* heatmap.js — 注意力探针。
   Q / K 的唯一真相源是页面上的 .home-probe__mat；解析不到 128 个整数就静默用下面这份常量
   （与 index.html 中那段 8×8 完全一致）。τ 由滑杆给出，行软归一化。 */

const D = 8;
const SCALE = Math.sqrt(D);
const CELLS = D * D;

const FALLBACK_Q = [
  1, 0, 1, -1, 0, 1, 0, -1,
  0, 1, -1, 1, 0, 0, 1, 0,
  1, -1, 0, 0, 1, 1, -1, 0,
  -1, 0, 1, 1, 0, -1, 0, 1,
  0, 1, 0, -1, 1, 0, 1, -1,
  1, 1, -1, 0, 0, 1, 0, 0,
  0, -1, 1, 1, -1, 0, 0, 1,
  -1, 1, 0, 0, 1, -1, 1, 0
];

const FALLBACK_K = [
  0, 1, 1, -1, 0, 0, 1, -1,
  1, 0, -1, 0, 1, 1, 0, 0,
  -1, 1, 0, 1, 0, -1, 1, 0,
  0, 0, 1, 1, -1, 0, 0, 1,
  1, -1, 0, 0, 1, 0, -1, 1,
  0, 1, 0, -1, 1, 1, 0, 0,
  1, 0, 1, 0, 0, -1, 1, -1,
  -1, 0, 0, 1, 0, 1, -1, 1
];

function readMatrices() {
  const node = document.querySelector(".home-probe__mat");
  if (!node) return null;
  const text = node.textContent || "";
  if (text.indexOf("Q =") < 0) return null;
  const nums = text.match(/-?\d+/g);
  if (!nums || nums.length !== CELLS * 2) return null;
  const q = new Float64Array(CELLS);
  const k = new Float64Array(CELLS);
  for (let i = 0; i < CELLS; i += 1) {
    const a = Number(nums[i]);
    const b = Number(nums[i + CELLS]);
    if (!Number.isFinite(a) || !Number.isFinite(b)) return null;
    q[i] = a;
    k[i] = b;
  }
  return { q: q, k: k };
}

function tokenColor(styles, name, fallback) {
  let raw = "";
  try {
    raw = (styles.getPropertyValue(name) || "").trim();
  } catch (ignored) {
    raw = "";
  }
  return /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(raw) ? raw : fallback;
}

function hexToRgb(hex) {
  let body = hex.replace("#", "");
  if (body.length === 3) {
    body = body.charAt(0) + body.charAt(0) + body.charAt(1) + body.charAt(1) + body.charAt(2) + body.charAt(2);
  }
  const value = parseInt(body, 16);
  return [(value >> 16) & 255, (value >> 8) & 255, value & 255];
}

function mix(from, to, t) {
  return [
    Math.round(from[0] + (to[0] - from[0]) * t),
    Math.round(from[1] + (to[1] - from[1]) * t),
    Math.round(from[2] + (to[2] - from[2]) * t)
  ];
}

/* W = softmax(QKᵀ / √8 / τ)，逐行做数值稳定 softmax（先减行最大值）。 */
function weights(q, k, tau) {
  const w = new Float64Array(CELLS);
  for (let r = 0; r < D; r += 1) {
    let max = -Infinity;
    for (let c = 0; c < D; c += 1) {
      let dot = 0;
      for (let t = 0; t < D; t += 1) dot += q[r * D + t] * k[c * D + t];
      const score = dot / SCALE / tau;
      w[r * D + c] = score;
      if (score > max) max = score;
    }
    let total = 0;
    for (let c = 0; c < D; c += 1) {
      const e = Math.exp(w[r * D + c] - max);
      w[r * D + c] = e;
      total += e;
    }
    for (let c = 0; c < D; c += 1) w[r * D + c] = w[r * D + c] / total;
  }
  return w;
}

export function initHeatmap() {
  const canvas = document.getElementById("heatmapCanvas");
  const slider = document.querySelector("#heatTemp[data-heat-temp]");
  if (!canvas || !slider) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const readout = document.querySelector("[data-heat-readout]");
  const parsed = readMatrices();
  const q = parsed ? parsed.q : Float64Array.from(FALLBACK_Q);
  const k = parsed ? parsed.k : Float64Array.from(FALLBACK_K);

  const rootStyles = getComputedStyle(document.documentElement);
  const low = hexToRgb(tokenColor(rootStyles, "--void-3", "#12151A"));
  const mid = hexToRgb(tokenColor(rootStyles, "--cyan", "#57E3D2"));
  const high = hexToRgb(tokenColor(rootStyles, "--amber", "#F2B441"));
  const labelColor = tokenColor(rootStyles, "--muted", "#8B9199");
  const faintColor = tokenColor(rootStyles, "--muted-2", "#5E656E");

  const W = 480;
  const H = 320;
  const padL = 20;
  const padT = 26;
  const padR = 6;
  const padB = 10;
  const gridW = W - padL - padR;
  const gridH = H - padT - padB;
  const cellW = gridW / D;
  const cellH = gridH / D;
  let current = 1;

  function paint(tau) {
    current = tau;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const bw = Math.round(W * dpr);
    const bh = Math.round(H * dpr);
    if (canvas.width !== bw) canvas.width = bw;
    if (canvas.height !== bh) canvas.height = bh;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = "#07080A";
    ctx.fillRect(0, 0, W, H);

    const w = weights(q, k, tau);
    let min = Infinity;
    let max = -Infinity;
    for (let i = 0; i < CELLS; i += 1) {
      if (w[i] < min) min = w[i];
      if (w[i] > max) max = w[i];
    }
    const span = max - min || 1;

    for (let r = 0; r < D; r += 1) {
      for (let c = 0; c < D; c += 1) {
        const t = (w[r * D + c] - min) / span;
        const rgb = t < 0.5 ? mix(low, mid, t * 2) : mix(mid, high, (t - 0.5) * 2);
        const alpha = (0.28 + 0.72 * t).toFixed(3);
        ctx.fillStyle = "rgba(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + "," + alpha + ")";
        ctx.fillRect(padL + c * cellW + 0.5, padT + r * cellH + 0.5, cellW - 1, cellH - 1);
      }
    }

    ctx.font = "9px ui-monospace, Menlo, Consolas, monospace";
    ctx.textBaseline = "middle";
    ctx.fillStyle = labelColor;
    ctx.textAlign = "center";
    for (let c = 0; c < D; c += 1) {
      ctx.fillText(String(c + 1), padL + c * cellW + cellW / 2, padT - 7);
    }
    ctx.textAlign = "right";
    for (let r = 0; r < D; r += 1) {
      ctx.fillText(String(r + 1), padL - 7, padT + r * cellH + cellH / 2);
    }
    ctx.fillStyle = faintColor;
    ctx.textAlign = "right";
    ctx.fillText("softmax(QKᵀ/√8/τ)", W - padR, padT - 16);
  }

  function setReadout(tau) {
    if (readout) readout.textContent = "τ = " + tau.toFixed(2);
  }

  const initial = Number(slider.value);
  const start = Number.isFinite(initial) && initial > 0 ? initial : 1;
  paint(start);
  setReadout(start);

  slider.addEventListener("input", function () {
    const raw = Number(slider.value);
    const tau = Number.isFinite(raw) && raw > 0 ? raw : 1;
    paint(tau);
    setReadout(tau);
  }, { passive: true });

  window.addEventListener("resize", function () {
    if (!canvas.isConnected) return;
    paint(current);
  }, { passive: true });
}
