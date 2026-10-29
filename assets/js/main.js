/* main.js — 全站唯一入口。
   每个初始化先查钩子元素是否存在，缺了就静默返回；所有监听尽量 passive。 */

import { initPalette } from "./palette.js";
import { initField } from "./field.js";
import { initReveal } from "./reveal.js";
import { initHeatmap } from "./heatmap.js";
import { initTelemetry } from "./telemetry.js";

const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)");

/* —— 1 · 移动端导航 —— */
function initNav() {
  const header = document.querySelector("[data-header]");
  const toggle = document.getElementById("navToggle");
  if (!header || !toggle) return;

  function setOpen(open) {
    header.setAttribute("data-open", open ? "true" : "false");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  toggle.addEventListener("click", function () {
    setOpen(header.getAttribute("data-open") !== "true");
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && header.getAttribute("data-open") === "true") setOpen(false);
  });

  document.addEventListener("click", function (event) {
    if (header.getAttribute("data-open") !== "true") return;
    const target = event.target;
    if (target && target.nodeType === 1 && header.contains(target)) return;
    setOpen(false);
  });

  const wide = window.matchMedia("(min-width: 900px)");
  function onChange() {
    if (wide.matches) setOpen(false);
  }
  if (typeof wide.addEventListener === "function") wide.addEventListener("change", onChange);
  else if (typeof wide.addListener === "function") wide.addListener(onChange);
}

/* —— 3 · 光标环 —— */
function initCursor() {
  const ring = document.querySelector("[data-cursor]");
  if (!ring) return;
  if (!window.matchMedia("(pointer: fine)").matches) return;
  if (REDUCED.matches) return;

  const SIZE = 26;
  const SIZE_HOVER = 44;
  const EASE = 0.18;
  let targetX = 0;
  let targetY = 0;
  let x = 0;
  let y = 0;
  let raf = 0;

  function tick() {
    x += (targetX - x) * EASE;
    y += (targetY - y) * EASE;
    ring.style.transform = "translate3d(" + x + "px," + y + "px,0) translate(-50%,-50%)";
    raf = window.requestAnimationFrame(tick);
  }

  function hide() {
    ring.style.opacity = "0";
    if (raf) window.cancelAnimationFrame(raf);
    raf = 0;
    ring.style.width = SIZE + "px";
    ring.style.height = SIZE + "px";
  }

  window.addEventListener("pointermove", function (event) {
    if (event.pointerType === "touch") return;
    targetX = event.clientX;
    targetY = event.clientY;
    if (!raf) {
      x = targetX;
      y = targetY;
      ring.style.opacity = "1";
      raf = window.requestAnimationFrame(tick);
    }
  }, { passive: true });

  window.addEventListener("pointerover", function (event) {
    const target = event.target;
    if (!target || target.nodeType !== 1) return;
    const hit = target.closest("a,button,[data-palette-open]");
    const size = hit ? SIZE_HOVER : SIZE;
    ring.style.width = size + "px";
    ring.style.height = size + "px";
  }, { passive: true });

  document.documentElement.addEventListener("mouseleave", hide, { passive: true });
  window.addEventListener("blur", hide, { passive: true });
}

/* —— 2b · 卡片指针聚光（钩子 data-glow） ——
   聚光本身在 CSS（.card::after 用 var(--spot)），这里只把指针换算成卡片内坐标写进
   --mx/--my；document 上一个 pointermove 委托全部卡片，写样式按帧合并。 */
function initGlow() {
  if (REDUCED.matches) return;
  if (!window.matchMedia("(pointer: fine)").matches) return;

  let card = null;
  let px = 0;
  let py = 0;
  let queued = false;

  function flush() {
    queued = false;
    if (!card) return;
    const rect = card.getBoundingClientRect();
    card.style.setProperty("--mx", (px - rect.left).toFixed(1) + "px");
    card.style.setProperty("--my", (py - rect.top).toFixed(1) + "px");
  }

  function pick(event) {
    const node = event.target;
    if (!node || node.nodeType !== 1) return null;
    return node.closest("[data-glow]");
  }

  document.addEventListener("pointermove", function (event) {
    if (event.pointerType === "touch") return;
    const el = pick(event);
    if (!el) return;
    card = el;
    px = event.clientX;
    py = event.clientY;
    if (queued) return;
    queued = true;
    window.requestAnimationFrame(flush);
  }, { passive: true });

  /* pointerleave 不冒泡，委托挂会冒泡的 pointerout：relatedTarget 仍在卡内就不算离开。 */
  document.addEventListener("pointerout", function (event) {
    const el = pick(event);
    if (!el) return;
    const to = event.relatedTarget;
    if (to && to.nodeType === 1 && el.contains(to)) return;
    el.style.removeProperty("--mx");
    el.style.removeProperty("--my");
    if (card === el) card = null;
  }, { passive: true });
}

/* —— 2c · 标题指针视差（data-parallax，缺省回落到 hero 的 h1） ——
   位移写在 translate 而非 transform：若之后有人给标题加 CSS transform，两者相乘而不是
   互相覆盖。±6px，rAF 插值，停稳后自停。 */
function initParallax() {
  if (REDUCED.matches) return;
  if (!window.matchMedia("(pointer: fine)").matches) return;
  if (!("translate" in document.documentElement.style)) return;
  const el = document.querySelector("[data-parallax]") || document.querySelector(".home-hero__title");
  if (!el) return;

  const RANGE = 6;
  const EASE = 0.14;
  const EPS = 0.05;
  let tx = 0;
  let ty = 0;
  let x = 0;
  let y = 0;
  let raf = 0;

  function tick() {
    x += (tx - x) * EASE;
    y += (ty - y) * EASE;
    const done = Math.abs(tx - x) < EPS && Math.abs(ty - y) < EPS;
    if (done) {
      x = tx;
      y = ty;
      raf = 0;
    }
    el.style.translate = x.toFixed(2) + "px " + y.toFixed(2) + "px";
    if (!done) raf = window.requestAnimationFrame(tick);
  }

  window.addEventListener("pointermove", function (event) {
    if (event.pointerType === "touch") return;
    const w = window.innerWidth || 1;
    const h = window.innerHeight || 1;
    tx = (event.clientX / w - 0.5) * 2 * RANGE;
    ty = (event.clientY / h - 0.5) * 2 * RANGE;
    if (!raf) raf = window.requestAnimationFrame(tick);
  }, { passive: true });
}

/* —— 4 · 阅读进度 —— */
function initProgress() {
  const bar = document.querySelector("[data-progress]");
  if (!bar) return;

  function update() {
    const doc = document.documentElement;
    const scrollable = doc.scrollHeight - window.innerHeight;
    const ratio = scrollable > 0 ? window.scrollY / scrollable : 0;
    const clamped = ratio < 0 ? 0 : ratio > 1 ? 1 : ratio;
    bar.style.transform = "scaleX(" + clamped.toFixed(4) + ")";
  }

  let queued = false;
  function schedule() {
    if (queued) return;
    queued = true;
    window.requestAnimationFrame(function () {
      queued = false;
      update();
    });
  }

  window.addEventListener("scroll", schedule, { passive: true });
  window.addEventListener("resize", schedule, { passive: true });
  update();
}

/* —— 6 · Boot 序列（仅首页） —— */
function initBoot() {
  const boot = document.querySelector("[data-boot]");
  if (!boot) return;
  const lines = boot.querySelectorAll(".boot__line");
  const skip = document.querySelector("[data-boot-skip]");
  if (!lines.length) return;

  const KEY = "boot-skipped";
  let skipped = false;
  try {
    skipped = window.sessionStorage.getItem(KEY) !== null;
  } catch (ignored) {
    skipped = false;
  }

  let timer = 0;
  let settle = 0;

  function lightAll() {
    for (let i = 0; i < lines.length; i += 1) lines[i].classList.add("is-on");
  }

  function finish() {
    window.clearTimeout(timer);
    window.clearTimeout(settle);
    boot.classList.remove("is-booting");
  }

  if (skipped || REDUCED.matches) {
    lightAll();
    return;
  }

  boot.classList.add("is-booting");
  let index = 0;
  function step() {
    if (index >= lines.length) {
      settle = window.setTimeout(finish, 320);
      return;
    }
    lines[index].classList.add("is-on");
    index += 1;
    timer = window.setTimeout(step, 90);
  }
  timer = window.setTimeout(step, 60);

  if (skip) {
    skip.addEventListener("click", function () {
      lightAll();
      finish();
      try {
        window.sessionStorage.setItem(KEY, "1");
      } catch (ignored) {
        /* 隐私模式下写不进去，跳过即可 */
      }
    });
  }
}

/* —— 7 · HUD 分区读数（仅首页的 8 个区块） —— */
function initHud() {
  const out = document.querySelector("[data-hud-section]");
  if (!out) return;
  const order = ["overview", "boot", "capability", "metrics", "work", "probe", "knowledge", "contact"];
  const targets = [];
  for (let i = 0; i < order.length; i += 1) {
    const el = document.getElementById(order[i]);
    if (el) targets.push(el);
  }
  if (!targets.length) return;

  const seen = new Set();
  /* 视口中段那条窄带里出现的区块就是“当前区块”，避免大区块压低比例。 */
  const io = new IntersectionObserver(function (entries) {
    for (let i = 0; i < entries.length; i += 1) {
      const entry = entries[i];
      if (entry.isIntersecting) seen.add(entry.target.id);
      else seen.delete(entry.target.id);
    }
    for (let i = 0; i < order.length; i += 1) {
      if (seen.has(order[i])) {
        out.textContent = order[i].toUpperCase();
        return;
      }
    }
  }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });

  for (let i = 0; i < targets.length; i += 1) io.observe(targets[i]);
}

/* —— 12 · 指标数字滚动（CONTRACT §7 的 data-count） ——
   静态文本就是最终值：只在运行时覆盖，动画结束逐字符还原成初始化时抓到的那串字符。 */
function formatCount(value) {
  const whole = String(Math.round(value));
  let out = "";
  let digits = 0;
  for (let i = whole.length - 1; i >= 0; i -= 1) {
    out = whole.charAt(i) + out;
    digits += 1;
    if (digits % 3 === 0 && i > 0) out = "," + out;
  }
  return out;
}

function initCounters() {
  const nodes = document.querySelectorAll("[data-count]");
  if (!nodes.length) return;
  if (REDUCED.matches) return;
  if (typeof window.IntersectionObserver !== "function") return;

  const items = [];
  for (let i = 0; i < nodes.length; i += 1) {
    const target = Number(nodes[i].getAttribute("data-count"));
    if (!Number.isFinite(target)) continue;
    items.push({ el: nodes[i], target: target, final: nodes[i].textContent });
  }
  if (!items.length) return;

  function run(item) {
    if (item.target <= 0) return;
    if (document.visibilityState === "hidden") return;
    const target = item.target;
    const duration = 900;
    let begin = 0;
    let settled = false;

    function restore() {
      if (settled) return;
      settled = true;
      item.el.textContent = item.final;
    }

    function frame(now) {
      if (settled) return;
      if (!begin) begin = now;
      const elapsed = now - begin;
      if (elapsed < duration) {
        const eased = 1 - Math.pow(1 - elapsed / duration, 3);
        item.el.textContent = formatCount(target * eased);
        window.requestAnimationFrame(frame);
        return;
      }
      restore();
    }

    item.el.textContent = formatCount(0);
    window.requestAnimationFrame(frame);
    /* rAF 被节流（切到后台等）时兜底：静态值一定会回来 */
    window.setTimeout(restore, duration + 1500);
  }

  const io = new IntersectionObserver(function (entries, observer) {
    for (let i = 0; i < entries.length; i += 1) {
      if (!entries[i].isIntersecting) continue;
      observer.unobserve(entries[i].target);
      for (let j = 0; j < items.length; j += 1) {
        if (items[j].el === entries[i].target) {
          run(items[j]);
          break;
        }
      }
    }
  }, { threshold: 0.35 });

  for (let i = 0; i < items.length; i += 1) io.observe(items[i].el);
}

/* —— 8 · 知识库过滤（仅 notes.html） —— */
function initNotesFilter() {
  const input = document.getElementById("notesFilter");
  const count = document.getElementById("notesCount");
  if (!input) return;
  const rows = document.querySelectorAll("a.note-row[data-note-row]");
  if (!rows.length) return;

  function apply() {
    const query = input.value.trim().toLowerCase();
    let visible = 0;
    for (let i = 0; i < rows.length; i += 1) {
      const row = rows[i];
      const haystack = ((row.dataset.keywords || "") + " " + row.textContent).toLowerCase();
      const hit = !query || haystack.indexOf(query) >= 0;
      if (hit) {
        row.removeAttribute("hidden");
        visible += 1;
      } else {
        row.setAttribute("hidden", "");
      }
    }
    if (count) count.textContent = visible ? String(visible) : "无匹配";
  }

  input.addEventListener("input", apply, { passive: true });
  apply();
}

/* —— 9 · 文章目录滚动高亮 —— */
function initScrollSpy() {
  const nav = document.querySelector("nav[data-scrollspy]");
  if (!nav) return;
  const links = nav.querySelectorAll('a[href^="#"]');
  if (!links.length) return;

  const entries = [];
  for (let i = 0; i < links.length; i += 1) {
    const link = links[i];
    const raw = (link.getAttribute("href") || "").slice(1);
    if (!raw) continue;
    const target = document.getElementById(raw);
    if (target) entries.push({ link: link, target: target });
  }
  if (!entries.length) return;

  let current = null;
  function activate(link) {
    if (link === current) return;
    for (let i = 0; i < entries.length; i += 1) entries[i].link.classList.remove("is-active");
    if (link) link.classList.add("is-active");
    current = link;
  }

  const io = new IntersectionObserver(function (batch) {
    for (let i = 0; i < batch.length; i += 1) {
      if (!batch[i].isIntersecting) continue;
      for (let j = 0; j < entries.length; j += 1) {
        if (entries[j].target === batch[i].target) {
          activate(entries[j].link);
          break;
        }
      }
    }
  }, { rootMargin: "-12% 0px -70% 0px", threshold: 0 });

  for (let i = 0; i < entries.length; i += 1) io.observe(entries[i].target);
}

/* —— 10 · 代码复制 —— */
function legacyCopy(text) {
  try {
    const area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.top = "-1000px";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    const ok = document.execCommand("copy");
    document.body.removeChild(area);
    return ok;
  } catch (ignored) {
    return false;
  }
}

function copyText(text) {
  if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
    return navigator.clipboard.writeText(text).then(function () {
      return true;
    }, function () {
      return legacyCopy(text);
    });
  }
  return Promise.resolve(legacyCopy(text));
}

function initCopy() {
  const buttons = document.querySelectorAll("button[data-copy]");
  if (!buttons.length) return;

  function flash(button) {
    const original = button.dataset.copyLabel || button.textContent;
    button.dataset.copyLabel = original;
    button.textContent = "COPIED";
    window.setTimeout(function () {
      button.textContent = original;
    }, 1200);
  }

  for (let i = 0; i < buttons.length; i += 1) {
    const button = buttons[i];
    button.addEventListener("click", function () {
      const scope = button.closest(".art-code") || button.parentElement;
      const pre = scope ? scope.querySelector("pre") : null;
      if (!pre) return;
      copyText(pre.textContent || "").then(function (ok) {
        if (ok) flash(button);
      });
    });
  }
}

/* —— 11 · 404 路径回显 —— */
function initNotFound() {
  const node = document.getElementById("notFoundPath");
  if (!node) return;
  node.textContent = window.location.pathname + window.location.search;
}

function safe(run) {
  try {
    run();
  } catch (ignored) {
    /* 单个钩子失败不应拖垮其余钩子；页面无 JS 时也必须可读 */
  }
}

safe(initNav);
safe(initPalette);
safe(initCursor);
safe(initGlow);
safe(initParallax);
safe(initProgress);
safe(initReveal);
safe(initBoot);
safe(initHud);
safe(initCounters);
safe(initNotesFilter);
safe(initScrollSpy);
safe(initCopy);
safe(initNotFound);
safe(initField);
safe(initHeatmap);
safe(initTelemetry);
