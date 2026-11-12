/* main.js — 全站唯一入口。
   每个初始化先查钩子元素是否存在，缺了就静默返回；所有监听尽量 passive。 */

import { initPalette } from "./palette.js";
import { initField } from "./field.js";
import { initReveal } from "./reveal.js";
import { initHeatmap } from "./heatmap.js";
import { initTelemetry } from "./telemetry.js";

/* —— 0 · 动效开关：站内唯一真相 ——
   默认开：prefers-reduced-motion 只当建议，拿它硬杀动效会让用户以为站点坏了。
   选择写进 localStorage（只有 "off" 算关），状态落到 <html data-motion>，再派发 motionchange。 */
const MOTION_KEY = "motion:";

function storedMotion() {
  /* 只有明确存过 "off" 才算关；读不到（首次访问、隐私模式）一律按开。 */
  try {
    return window.localStorage.getItem(MOTION_KEY) !== "off";
  } catch (ignored) {
    return true;
  }
}

let motionOn = storedMotion();
document.documentElement.dataset.motion = motionOn ? "on" : "off";

export function isMotionOn() {
  return motionOn;
}

export function onMotionChange(fn) {
  document.addEventListener("motionchange", fn);
}

/* —— 0b · 指针状态：全站唯一一份 ——
   pointermove 只写这个对象；使用者挂 pointer.fn，每帧不再读事件。 */
const pointer = { x: 0, y: 0, seen: false, fn: null };
const motionApi = { isOn: isMotionOn, onChange: onMotionChange, pointer: pointer };

function watchPointer() {
  function emit() {
    if (pointer.fn) pointer.fn();
  }
  window.addEventListener("pointermove", function (event) {
    if (event.pointerType === "touch") return;
    pointer.x = event.clientX;
    pointer.y = event.clientY;
    pointer.seen = true;
    emit();
  }, { passive: true });
  /* 离开文档：先置空再通知，跟随者据此摘掉 .is-live。 */
  document.documentElement.addEventListener("mouseleave", function () {
    pointer.seen = false;
    emit();
  }, { passive: true });
}

function paintMotion() {
  const buttons = document.querySelectorAll("[data-motion-toggle]");
  for (let i = 0; i < buttons.length; i += 1) buttons[i].setAttribute("aria-pressed", motionOn ? "true" : "false");
}

function setMotion(on) {
  if (on === motionOn) return;
  motionOn = on;
  document.documentElement.dataset.motion = on ? "on" : "off";
  try {
    window.localStorage.setItem(MOTION_KEY, on ? "on" : "off");
  } catch (ignored) {
    /* 隐私模式写不进去：本次会话内照样生效 */
  }
  paintMotion();
  document.dispatchEvent(new CustomEvent("motionchange", { detail: { on: on } }));
}

function initMotionToggle() {
  /* HTML 里写死 aria-pressed="true"：关过站的访客进来要先对齐真实状态。 */
  paintMotion();
  const buttons = document.querySelectorAll("[data-motion-toggle]");
  for (let i = 0; i < buttons.length; i += 1) {
    buttons[i].addEventListener("click", function () {
      setMotion(!motionOn);
    });
  }
}

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

/* —— 2 · 指针跟随：光晕 + 光标环 ——
   一份插值、一个 rAF、每帧两次写；收敛即停（raf = 0），关闭时立刻隐藏。 */
function initFollow(motion) {
  const glow = document.querySelector("[data-pointer-glow]");
  const ring = document.querySelector("[data-cursor]");
  if (!glow && !ring) return;
  if (!window.matchMedia("(pointer: fine)").matches) return;

  const EASE = 0.12;
  const EPS = 0.1;
  const SIZE = 26;
  const SIZE_HOVER = 44;
  let x = 0;
  let y = 0;
  let live = false;
  let raf = 0;

  /* 环靠自己那句 translate(-50%,-50%) 居中；光晕由 CSS 负 margin 居中，这里不再减半宽高。 */
  function write() {
    const at = "translate3d(" + x.toFixed(2) + "px," + y.toFixed(2) + "px,0)";
    if (glow) glow.style.transform = at;
    if (ring) ring.style.transform = at + " translate(-50%,-50%)";
  }

  function tick() {
    const dx = pointer.x - x;
    const dy = pointer.y - y;
    x += dx * EASE;
    y += dy * EASE;
    const settled = dx > -EPS && dx < EPS && dy > -EPS && dy < EPS;
    if (settled) {
      x = pointer.x;
      y = pointer.y;
      raf = 0;
    }
    write();
    if (!settled) raf = window.requestAnimationFrame(tick);
  }

  function halt() {
    if (raf) window.cancelAnimationFrame(raf);
    raf = 0;
    live = false;
    if (glow) glow.classList.remove("is-live");
    if (ring) {
      ring.style.opacity = "0";
      ring.style.width = SIZE + "px";
      ring.style.height = SIZE + "px";
    }
  }

  /* 指针动了、动效开着、指针还在文档里——缺一个就收尾。 */
  function wake() {
    if (!motion.isOn() || !pointer.seen) {
      halt();
      return;
    }
    if (!live) {
      /* 首次真实 pointermove：先落到指针上，避免从 (0,0) 一路滑过去。 */
      live = true;
      x = pointer.x;
      y = pointer.y;
      write();
      if (glow) glow.classList.add("is-live");
      if (ring) ring.style.opacity = "1";
    }
    if (!raf) raf = window.requestAnimationFrame(tick);
  }

  pointer.fn = wake;

  window.addEventListener("pointerover", function (event) {
    const target = event.target;
    if (!ring || !target || target.nodeType !== 1) return;
    const size = target.closest("a,button,[data-palette-open]") ? SIZE_HOVER : SIZE;
    ring.style.width = size + "px";
    ring.style.height = size + "px";
  }, { passive: true });

  window.addEventListener("blur", halt, { passive: true });
  motion.onChange(wake);
}

/* —— 2b · 卡片指针聚光（钩子 data-glow） ——
   聚光本身在 CSS（.card::after 用 var(--spot)），这里只把指针换算成卡片内坐标写进
   --mx/--my；document 上一个 pointermove 委托全部卡片，写样式按帧合并。 */
function initGlow(motion) {
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
    if (event.pointerType === "touch" || !motion.isOn()) return;
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
function initParallax(motion) {
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
    if (event.pointerType === "touch" || !motion.isOn()) return;
    const w = window.innerWidth || 1;
    const h = window.innerHeight || 1;
    tx = (event.clientX / w - 0.5) * 2 * RANGE;
    ty = (event.clientY / h - 0.5) * 2 * RANGE;
    if (!raf) raf = window.requestAnimationFrame(tick);
  }, { passive: true });

  motion.onChange(function () {
    if (motion.isOn()) return;
    window.cancelAnimationFrame(raf);
    raf = 0;
    el.style.translate = "";
  });
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
function initBoot(motion) {
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

  if (skipped || !motion.isOn()) {
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

  /* 播出途中关掉动效：立刻全亮收尾，不留半截的启动序列。 */
  motion.onChange(function () {
    if (motion.isOn()) return;
    lightAll();
    finish();
  });
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

function initCounters(motion) {
  const nodes = document.querySelectorAll("[data-count]");
  if (!nodes.length) return;
  if (typeof window.IntersectionObserver !== "function") return;

  const items = [];
  for (let i = 0; i < nodes.length; i += 1) {
    const target = Number(nodes[i].getAttribute("data-count"));
    if (!Number.isFinite(target)) continue;
    items.push({ el: nodes[i], target: target, final: nodes[i].textContent });
  }
  if (!items.length) return;

  function run(item) {
    if (item.target <= 0 || !motion.isOn()) return;
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
      if (!motion.isOn()) {
        restore();
        return;
      }
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

  /* 惰性启动：HTML 里的文本本来就是最终值，关着就什么都不做；半途关掉由 frame() 自己收尾。 */
  let started = false;
  function arm() {
    if (started || !motion.isOn()) return;
    started = true;
    for (let i = 0; i < items.length; i += 1) io.observe(items[i].el);
  }

  motion.onChange(arm);
  arm();
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

function safe(run, arg) {
  try {
    run(arg);
  } catch (ignored) {
    /* 单个钩子失败不应拖垮其余钩子；页面无 JS 时也必须可读 */
  }
}

safe(watchPointer);
safe(initMotionToggle);
safe(initNav);
safe(initPalette);
safe(initFollow, motionApi);
safe(initGlow, motionApi);
safe(initParallax, motionApi);
safe(initProgress);
safe(initReveal, motionApi);
safe(initBoot, motionApi);
safe(initHud);
safe(initCounters, motionApi);
safe(initNotesFilter);
safe(initScrollSpy);
safe(initCopy);
safe(initNotFound);
safe(initField, motionApi);
safe(initHeatmap);
safe(initTelemetry);
