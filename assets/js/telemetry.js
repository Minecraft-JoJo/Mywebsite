/* telemetry.js — 页脚真实读数：load / bytes / built。
   任何一步取不到都写 “—”，不向任何输出通道抛东西。 */

const DASH = "—";
const MB = 1048576;
const KB = 1024;

function publish(name, value) {
  const nodes = document.querySelectorAll('[data-metric="' + name + '"]');
  for (let i = 0; i < nodes.length; i += 1) nodes[i].textContent = value;
}

function loadMillis() {
  const list = window.performance.getEntriesByType("navigation");
  const nav = list && list.length ? list[0] : null;
  if (!nav) return DASH;
  let ms = nav.duration;
  if (!(ms > 0)) ms = nav.responseEnd - nav.startTime;
  if (!Number.isFinite(ms) || ms <= 0) return DASH;
  return Math.round(ms) + " ms";
}

function transferSize() {
  const list = window.performance.getEntriesByType("resource");
  if (!list || !list.length) return DASH;
  let bytes = 0;
  for (let i = 0; i < list.length; i += 1) {
    const size = list[i].transferSize;
    if (Number.isFinite(size) && size > 0) bytes += size;
  }
  if (bytes <= 0) return DASH;
  if (bytes >= MB) return (bytes / MB).toFixed(1) + " MB";
  return (bytes / KB).toFixed(1) + " KB";
}

function builtDay() {
  const stamp = Date.parse(document.lastModified || "");
  if (!Number.isFinite(stamp)) return DASH;
  const date = new Date(stamp);
  const year = date.getFullYear();
  if (!(year > 1990 && year < 2200)) return DASH;
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return year + "-" + month + "-" + day;
}

export function initTelemetry() {
  if (!document.querySelector("[data-metric]")) return;

  function refresh() {
    try {
      publish("load", loadMillis());
    } catch (ignored) {
      publish("load", DASH);
    }
    try {
      publish("bytes", transferSize());
    } catch (ignored) {
      publish("bytes", DASH);
    }
    try {
      publish("built", builtDay());
    } catch (ignored) {
      publish("built", DASH);
    }
  }

  refresh();

  /* 模块在 load 之前就跑了：资源与导航计时还没结算，等 load 再量一次。 */
  if (document.readyState !== "complete") {
    window.addEventListener("load", function () {
      try {
        refresh();
      } catch (ignored) {
        publish("load", DASH);
        publish("bytes", DASH);
        publish("built", DASH);
      }
    }, { once: true, passive: true });
  }
}
