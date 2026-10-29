/* reveal.js — [data-reveal] 的入场。
   页面里没有任何 opacity:0 的 CSS 层：前置隐形只用 inline style，
   而且只加给首屏之外的元素，动画结束后再清掉，因此脚本失败时页面依然完整可读。
   动效关闭时整块直接可见，前置隐形一律不写。 */

const SELECTOR = "[data-reveal]";
const EASE = "cubic-bezier(.16,1,.3,1)";
const FROM = "translateY(14px)";

function settle(el) {
  el.style.opacity = "";
  el.style.transform = "";
}

function play(el) {
  let done = false;
  function finish() {
    if (done) return;
    done = true;
    settle(el);
  }
  if (typeof el.animate === "function") {
    const anim = el.animate(
      [{ opacity: 0, transform: FROM }, { opacity: 1, transform: "none" }],
      { duration: 420, easing: EASE, fill: "forwards" }
    );
    anim.addEventListener("finish", finish);
    anim.addEventListener("cancel", finish);
    window.setTimeout(finish, 1400);
    return;
  }
  finish();
}

export function initReveal(motion) {
  const items = document.querySelectorAll(SELECTOR);
  if (!items.length) return;

  const viewport = window.innerHeight || document.documentElement.clientHeight || 0;
  const limit = viewport * 0.92;
  const pending = [];
  const played = new Set();

  /* 读尺寸集中一次，再集中写，避免读写交替引发重排。 */
  for (let i = 0; i < items.length; i += 1) {
    if (items[i].getBoundingClientRect().top < limit) continue;
    pending.push(items[i]);
  }
  if (!pending.length) return;

  const io = new IntersectionObserver(function (entries, observer) {
    for (let i = 0; i < entries.length; i += 1) {
      if (!entries[i].isIntersecting) continue;
      observer.unobserve(entries[i].target);
      played.add(entries[i].target);
      play(entries[i].target);
    }
  }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });

  function hide() {
    for (let i = 0; i < pending.length; i += 1) {
      if (played.has(pending[i])) continue;
      pending[i].style.opacity = "0";
      pending[i].style.transform = FROM;
    }
  }

  /* 惰性启动：先关后开时按需挂观察；关掉时全部直接可见。 */
  let armed = false;
  function boot() {
    if (armed || !motion.isOn()) return;
    armed = true;
    hide();
    for (let i = 0; i < pending.length; i += 1) io.observe(pending[i]);
  }

  motion.onChange(function () {
    if (motion.isOn()) {
      boot();
      return;
    }
    armed = false;
    io.disconnect();
    for (let i = 0; i < pending.length; i += 1) settle(pending[i]);
  });

  boot();
}
