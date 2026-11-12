/* field.js — Latent Field：首页 hero 的背景场。
   固定种子 + 预分配缓冲：循环里不新建对象；页面隐藏或 canvas 离开视口时 rAF 完全停下。
   兜底由 HTML 里那层内联 SVG 承担。v2：整帧 lighter 绘制，交点自然叠亮；注意力边
   3px 弱光 + 1px 亮线；1/5 节点套一张只生成一次的光斑贴图（逐帧仅 drawImage）。 */

const COUNT = 60;
const TAU = Math.PI * 2;
/* 贴图边长（CSS px，绘制时按节点半径缩放）；每 GLOW_EVERY 个节点挑一个套光斑。 */
const GLOW_SIZE = 96;
const GLOW_EVERY = 5;

function mulberry32(seed) {
  let a = seed >>> 0;
  return function random() {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* 光斑贴图只建一次：渐变对象是这类循环里最贵的分配，烤进离屏 canvas 后逐帧只剩 drawImage。 */
function makeGlow() {
  const pad = document.createElement("canvas");
  pad.width = GLOW_SIZE;
  pad.height = GLOW_SIZE;
  const glowCtx = pad.getContext("2d");
  if (!glowCtx) return pad;
  const half = GLOW_SIZE / 2;
  const grad = glowCtx.createRadialGradient(half, half, 0, half, half, half);
  grad.addColorStop(0, "rgba(99,214,203,0.16)");
  grad.addColorStop(0.55, "rgba(99,214,203,0.05)");
  grad.addColorStop(1, "rgba(99,214,203,0)");
  glowCtx.fillStyle = grad;
  glowCtx.fillRect(0, 0, GLOW_SIZE, GLOW_SIZE);
  return pad;
}

export function initField(motion) {
  const canvas = document.querySelector("#fieldCanvas[data-field]");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  const pointer = motion.pointer;

  const fpsEl = document.querySelector("[data-fps]");
  const glow = makeGlow();

  const nx = new Float32Array(COUNT);
  const ny = new Float32Array(COUNT);
  const sx = new Float32Array(COUNT);
  const sy = new Float32Array(COUNT);
  const depth = new Float32Array(COUNT);
  const radius = new Float32Array(COUNT);
  const glowR = new Float32Array(COUNT);
  /* 每帧算一次的屏幕坐标，四个绘制循环共用，避免同一串乘加重复四遍。 */
  const rx = new Float32Array(COUNT);
  const ry = new Float32Array(COUNT);
  const nearA = new Int32Array(COUNT);
  const nearB = new Int32Array(COUNT);
  /* 引力：240px 内连线提亮，增量 = min(1, 原 alpha×1.6) − 原 alpha（叠在批量描边上）。 */
  const GRAV = 240;
  const GRAV2 = GRAV * GRAV;
  const nearP = new Uint8Array(COUNT);
  const LINE_UP = "rgba(200,240,255,0.060)";
  const ATTN_UP = "rgba(99,214,203,0.180)";

  const random = mulberry32(0x9E3779B9);
  for (let i = 0; i < COUNT; i += 1) {
    nx[i] = random();
    ny[i] = random();
    sx[i] = (random() - 0.5) * 0.014;
    sy[i] = (random() - 0.5) * 0.014;
    depth[i] = 0.45 + random() * 1.15;
    radius[i] = 0.8 + random() * 0.8;
    /* 光斑半径 26–40px：未选中的为 0，绘制时跳过。 */
    glowR[i] = i % GLOW_EVERY === 0 ? 26 + random() * 14 : 0;
  }

  /* 邻居只在初始化时算一次：漂移速度极慢，拓扑变化肉眼不可见。 */
  for (let i = 0; i < COUNT; i += 1) {
    let best = -1;
    let bestD = Infinity;
    let second = -1;
    let secondD = Infinity;
    for (let j = 0; j < COUNT; j += 1) {
      if (i === j) continue;
      const ax = nx[i] - nx[j];
      const ay = ny[i] - ny[j];
      const d = ax * ax + ay * ay;
      if (d < bestD) {
        secondD = bestD;
        second = best;
        bestD = d;
        best = j;
      } else if (d < secondD) {
        secondD = d;
        second = j;
      }
    }
    nearA[i] = best < 0 ? i : best;
    nearB[i] = second < 0 ? i : second;
  }

  let cssW = 0;
  let cssH = 0;
  let raf = 0;
  let last = 0;
  let frames = 0;
  let fpsClock = 0;
  let onScreen = true;
  let visible = document.visibilityState !== "hidden";
  let targetX = 0;
  let targetY = 0;
  let easeX = 0;
  let easeY = 0;
  let gx = 0;
  let gy = 0;
  let vw = 1;
  let vh = 1;

  function resize() {
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    if (!w || !h) return;
    cssW = w;
    cssH = h;
    vw = window.innerWidth || 1;
    vh = window.innerHeight || 1;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function draw(dt) {
    if (!cssW || !cssH) return;
    /* 指针状态由 main.js 唯一持有：这里只读，不挂监听。 */
    const live = pointer.seen;
    if (live) {
      const rect = canvas.getBoundingClientRect();
      gx = pointer.x - rect.left;
      gy = pointer.y - rect.top;
      targetX = (pointer.x / vw - 0.5) * 2;
      targetY = (pointer.y / vh - 0.5) * 2;
    }
    easeX += (targetX - easeX) * 0.04;
    easeY += (targetY - easeY) * 0.04;
    const step = dt / 1000;

    for (let i = 0; i < COUNT; i += 1) {
      nx[i] += sx[i] * step;
      ny[i] += sy[i] * step;
      if (nx[i] < -0.05) nx[i] += 1.1;
      else if (nx[i] > 1.05) nx[i] -= 1.1;
      if (ny[i] < -0.05) ny[i] += 1.1;
      else if (ny[i] > 1.05) ny[i] -= 1.1;
      const bx = (nx[i] + easeX * 0.02 * depth[i]) * cssW;
      const by = (ny[i] + easeY * 0.02 * depth[i]) * cssH;
      rx[i] = bx;
      ry[i] = by;
      nearP[i] = 0;
      if (!live) continue;
      /* 朝指针偏移，位移按距离线性收到 6px 以内。 */
      const dx = gx - bx;
      const dy = gy - by;
      const d2 = dx * dx + dy * dy;
      if (d2 >= GRAV2) continue;
      const d = Math.sqrt(d2) || 1;
      const pull = 6 - (6 * d) / GRAV;
      rx[i] = bx + (dx / d) * pull;
      ry[i] = by + (dy / d) * pull;
      nearP[i] = 1;
    }

    ctx.clearRect(0, 0, cssW, cssH);

    /* 混合模式一帧只切两次：lighter 让交叉处累加变亮（"有光源"的来源），收尾必须复原。 */
    ctx.globalCompositeOperation = "lighter";

    ctx.beginPath();
    for (let i = 0; i < COUNT; i += 1) {
      const j = nearB[i];
      const x1 = rx[i];
      const y1 = ry[i];
      const x2 = rx[j];
      const y2 = ry[j];
      if ((x1 < 0 && x2 < 0) || (x1 > cssW && x2 > cssW)) continue;
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
    }
    ctx.strokeStyle = "rgba(200,240,255,0.10)";
    ctx.lineWidth = 1;
    ctx.stroke();

    /* 注意力边：同一条批量 path 描两遍 —— 先 3px 弱青做外发光，再 1px 亮青压中心。 */
    ctx.beginPath();
    for (let i = 0; i < COUNT; i += 1) {
      const j = nearA[i];
      const x1 = rx[i];
      const y1 = ry[i];
      const x2 = rx[j];
      const y2 = ry[j];
      if ((x1 < 0 && x2 < 0) || (x1 > cssW && x2 > cssW)) continue;
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
    }
    ctx.lineWidth = 3;
    ctx.strokeStyle = "rgba(99,214,203,0.06)";
    ctx.stroke();
    ctx.lineWidth = 1;
    ctx.strokeStyle = "rgba(99,214,203,0.30)";
    ctx.stroke();

    /* 引力提亮：只补指针附近的少量连线，逐条 stroke，不动整屏批量描边的开销。 */
    if (live) {
      ctx.lineWidth = 1;
      for (let i = 0; i < COUNT; i += 1) {
        for (let k = 0; k < 2; k += 1) {
          const j = k ? nearA[i] : nearB[i];
          if (!nearP[i] && !nearP[j]) continue;
          ctx.strokeStyle = k ? ATTN_UP : LINE_UP;
          ctx.beginPath();
          ctx.moveTo(rx[i], ry[i]);
          ctx.lineTo(rx[j], ry[j]);
          ctx.stroke();
        }
      }
    }

    ctx.beginPath();
    for (let i = 0; i < COUNT; i += 1) {
      const x = rx[i];
      const y = ry[i];
      const r = radius[i];
      if (x < -4 || y < -4 || x > cssW + 4 || y > cssH + 4) continue;
      ctx.moveTo(x + r, y);
      ctx.arc(x, y, r, 0, TAU);
    }
    ctx.fillStyle = "rgba(200,240,255,0.55)";
    ctx.fill();

    /* 光斑：贴图早就烤好，这里只按半径 drawImage，不新建渐变。 */
    for (let i = 0; i < COUNT; i += 1) {
      const gr = glowR[i];
      if (!gr) continue;
      const x = rx[i];
      const y = ry[i];
      if (x < -gr || y < -gr || x > cssW + gr || y > cssH + gr) continue;
      ctx.drawImage(glow, x - gr, y - gr, gr * 2, gr * 2);
    }

    ctx.globalCompositeOperation = "source-over";
  }

  function frame(now) {
    if (!last) last = now;
    const dt = Math.min(now - last, 64);
    last = now;
    draw(dt);
    if (fpsEl) {
      frames += 1;
      if (!fpsClock) fpsClock = now;
      const elapsed = now - fpsClock;
      if (elapsed >= 500) {
        fpsEl.textContent = String(Math.round((frames * 1000) / elapsed));
        frames = 0;
        fpsClock = now;
      }
    }
    raf = window.requestAnimationFrame(frame);
  }

  function start() {
    if (raf) return;
    last = 0;
    raf = window.requestAnimationFrame(frame);
  }

  function stop() {
    if (raf) window.cancelAnimationFrame(raf);
    raf = 0;
  }

  function sync() {
    if (motion.isOn() && visible && onScreen) start();
    else stop();
  }

  /* 惰性启动：sync() 自带开关判断且幂等（start/stop 都查 raf），关时清成透明，
     让 HTML 里那层内联 SVG 兜底透出来。 */
  function halt() {
    stop();
    if (cssW && cssH) ctx.clearRect(0, 0, cssW, cssH);
  }

  motion.onChange(function () {
    if (motion.isOn()) sync();
    else halt();
  });

  document.addEventListener("visibilitychange", function () {
    visible = document.visibilityState !== "hidden";
    sync();
  }, { passive: true });

  const io = new IntersectionObserver(function (entries) {
    for (let i = 0; i < entries.length; i += 1) onScreen = entries[i].isIntersecting;
    sync();
  }, { threshold: 0 });
  io.observe(canvas);

  let resizeTimer = 0;
  window.addEventListener("resize", function () {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(function () {
      resize();
      if (!raf && motion.isOn()) draw(16);
    }, 120);
  }, { passive: true });

  resize();
  sync();
}
