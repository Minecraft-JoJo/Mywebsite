/* reveal.js — [data-reveal] 的入场。
   页面里没有任何 opacity:0 的 CSS 层：前置隐形只用 inline style，
   而且只加给首屏之外的元素，动画结束后再清掉，因此脚本失败时页面依然完整可读。
   prefers-reduced-motion: reduce 时整个模块空转。 */

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

export function initReveal() {
  const items = document.querySelectorAll(SELECTOR);
  if (!items.length) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const viewport = window.innerHeight || document.documentElement.clientHeight || 0;
  const limit = viewport * 0.92;
  const pending = [];

  /* 读尺寸集中一次，再集中写，避免读写交替引发重排。 */
  for (let i = 0; i < items.length; i += 1) {
    if (items[i].getBoundingClientRect().top < limit) continue;
    pending.push(items[i]);
  }
  for (let i = 0; i < pending.length; i += 1) {
    pending[i].style.opacity = "0";
    pending[i].style.transform = FROM;
  }
  if (!pending.length) return;

  const io = new IntersectionObserver(function (entries, observer) {
    for (let i = 0; i < entries.length; i += 1) {
      if (!entries[i].isIntersecting) continue;
      observer.unobserve(entries[i].target);
      play(entries[i].target);
    }
  }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });

  for (let i = 0; i < pending.length; i += 1) io.observe(pending[i]);
}
