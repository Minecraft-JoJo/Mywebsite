/* palette.js — ⌘K 检索面板。
   索引固定 23 条：NAV 5 + PROJECTS 6 + NOTES 12，
   与 index.html boot 日志里的 "palette: index loaded (23 records)" 对齐。 */

import { NAV, PROJECTS, NOTES } from "./data.js";

/* domain → notes.html 上的分组 id（.notes-group#dl / #backend / …）。 */
const DOMAIN_GROUP = {
  "Deep Learning": "dl",
  Backend: "backend",
  Systems: "systems",
  Desktop: "desktop",
  Language: "language",
  Frontend: "frontend"
};

/* 子路径前缀不硬编码：根页从 tokens.css 的 link 推出 "./"，notes/ 页推出 "../"，
   404 这种用绝对路径的页面推出 "/Mywebsite/"。 */
function resolveBase() {
  const link = document.querySelector('link[href$="tokens.css"]');
  if (!link) return "./";
  const href = link.getAttribute("href") || "";
  return href.replace("assets/css/tokens.css", "");
}

const BASE = resolveBase();

function stripDot(href) {
  return href.replace(/^\.\//, "");
}

function noteHref(note) {
  if (note.href.indexOf("./notes/") === 0) return BASE + stripDot(note.href);
  const group = DOMAIN_GROUP[note.domain] || "dl";
  return BASE + "notes.html#" + group;
}

function buildRecords() {
  const records = [];
  for (let i = 0; i < NAV.length; i += 1) {
    records.push({ label: NAV[i].label, hint: "PAGE", href: BASE + stripDot(NAV[i].href) });
  }
  for (let i = 0; i < PROJECTS.length; i += 1) {
    records.push({
      label: PROJECTS[i].title,
      hint: "PROJECT",
      href: BASE + "projects.html#" + PROJECTS[i].id
    });
  }
  for (let i = 0; i < NOTES.length; i += 1) {
    records.push({ label: NOTES[i].title, hint: "NOTE", href: noteHref(NOTES[i]) });
  }
  return records;
}

const RECORDS = buildRecords();

/* 子序列匹配：查询串的字符按顺序出现即可（不要求连续）。 */
function isSubsequence(query, text) {
  let at = 0;
  for (let i = 0; i < query.length; i += 1) {
    at = text.indexOf(query.charAt(i), at);
    if (at < 0) return false;
    at += 1;
  }
  return true;
}

/* 0 最好：label 连续子串 → label 子序列 → hint 命中；-1 表示不匹配。 */
function rank(record, query) {
  if (!query) return 0;
  const label = record.label.toLowerCase();
  if (label.indexOf(query) >= 0) return 0;
  if (isSubsequence(query, label)) return 1;
  const hint = record.hint.toLowerCase();
  if (hint.indexOf(query) >= 0) return 2;
  if (isSubsequence(query, hint)) return 2;
  return -1;
}

function isTypingTarget(node) {
  if (!node || node.nodeType !== 1) return false;
  const tag = node.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return true;
  return node.isContentEditable === true;
}

export function initPalette() {
  const dialog = document.getElementById("palette");
  const input = document.getElementById("paletteInput");
  const list = document.getElementById("paletteList");
  if (!dialog || !input || !list) return;

  let results = RECORDS;
  let active = 0;
  let opener = null;

  function render() {
    const frag = document.createDocumentFragment();
    for (let i = 0; i < results.length; i += 1) {
      const item = document.createElement("li");
      item.className = "palette__item";
      item.setAttribute("role", "option");
      item.setAttribute("aria-selected", i === active ? "true" : "false");
      item.dataset.href = results[i].href;
      const label = document.createElement("span");
      label.textContent = results[i].label;
      const hint = document.createElement("small");
      hint.textContent = results[i].hint;
      item.appendChild(label);
      item.appendChild(hint);
      frag.appendChild(item);
    }
    if (!results.length) {
      const empty = document.createElement("li");
      empty.className = "palette__empty";
      empty.textContent = "无匹配记录";
      frag.appendChild(empty);
    }
    list.replaceChildren(frag);
  }

  function filter() {
    const query = input.value.trim().toLowerCase();
    const picked = [];
    for (let i = 0; i < RECORDS.length; i += 1) {
      const score = rank(RECORDS[i], query);
      if (score >= 0) picked.push({ score: score, index: i });
    }
    picked.sort(function (a, b) { return a.score - b.score || a.index - b.index; });
    results = picked.map(function (row) { return RECORDS[row.index]; });
    active = 0;
    render();
  }

  function move(step) {
    if (!results.length) return;
    active = (active + step + results.length) % results.length;
    const items = list.children;
    for (let i = 0; i < items.length; i += 1) {
      if (items[i].classList.contains("palette__empty")) continue;
      items[i].setAttribute("aria-selected", i === active ? "true" : "false");
    }
    const current = items[active];
    if (current && typeof current.scrollIntoView === "function") {
      current.scrollIntoView({ block: "nearest" });
    }
  }

  function activate(index) {
    const record = results[index];
    if (!record) return;
    window.location.href = record.href;
  }

  function open(from) {
    if (dialog.open) return;
    opener = from && from.nodeType === 1 ? from : null;
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "");
    input.setAttribute("aria-expanded", "true");
    filter();
    input.focus();
    input.select();
  }

  function close() {
    input.setAttribute("aria-expanded", "false");
    if (typeof dialog.close === "function") {
      if (dialog.open) dialog.close();
    } else {
      dialog.removeAttribute("open");
    }
    if (opener && opener.isConnected) opener.focus();
  }

  const openers = document.querySelectorAll("[data-palette-open]");
  for (let i = 0; i < openers.length; i += 1) {
    openers[i].addEventListener("click", function () { open(openers[i]); });
  }

  input.addEventListener("input", filter);

  list.addEventListener("click", function (event) {
    const target = event.target;
    if (!target || target.nodeType !== 1) return;
    const item = target.closest(".palette__item");
    if (!item || !item.dataset.href) return;
    window.location.href = item.dataset.href;
  });

  dialog.addEventListener("keydown", function (event) {
    const key = event.key;
    if (key === "ArrowDown") {
      event.preventDefault();
      move(1);
    } else if (key === "ArrowUp") {
      event.preventDefault();
      move(-1);
    } else if (key === "Enter") {
      event.preventDefault();
      activate(active);
    } else if (key === "Escape") {
      event.preventDefault();
      close();
    }
  });

  /* 点击遮罩层（dialog 本体）关闭；点 .palette__panel 内部不关。 */
  dialog.addEventListener("click", function (event) {
    if (event.target === dialog) close();
  });

  dialog.addEventListener("cancel", function (event) {
    event.preventDefault();
    close();
  });
  dialog.addEventListener("close", function () {
    input.setAttribute("aria-expanded", "false");
  });

  document.addEventListener("keydown", function (event) {
    const key = event.key;
    if ((event.metaKey || event.ctrlKey) && (key === "k" || key === "K")) {
      event.preventDefault();
      open(null);
      return;
    }
    if (key === "/" && !isTypingTarget(event.target)) {
      event.preventDefault();
      open(null);
    }
  });

  render();
}
