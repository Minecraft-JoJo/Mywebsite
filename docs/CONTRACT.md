# CONTRACT — 站点实现契约（唯一真相源）

> 本文件由主控编写。**任何执行者不得修改** `assets/css/tokens.css`、`assets/css/base.css`、
> `assets/js/data.js`、`docs/CONTRACT.md`，也不得修改他人拥有的文件。
> 若缺少某个令牌或组件，用现有的组合出来，不要在页面里另立变量。

---

## 1 · 硬约束（违反即返工）

1. **零构建**：直接手写 HTML/CSS/JS，无 npm 依赖、无打包器、无 CDN 外链（字体、图标、脚本一律本地或内联）。
2. **相对路径**：内部链接一律相对。**禁止任何以 `/` 开头的路径**（GitHub Pages project pages 会 404）。
   - 根级页面引用：`./assets/css/base.css`、`./notes.html`
   - `notes/` 下的页面引用：`../assets/css/base.css`、`../index.html`
3. **只用现有类**：页面级 CSS 只允许新增**本页专属**类（前缀用区块名，如 `.home-hero__*`），不得重定义 base.css 中的类。
4. **语义与可达性**：单一 `<main id="main">`；标题层级不跳级；所有交互控件用 `<button>`/`<a>`；装饰性 canvas/svg 加 `aria-hidden="true"`。
5. **数字必须真实**：只允许使用 `assets/js/data.js` 与下方表格里的数字，**不得编造**任何指标、年限、用户量、准确率。
6. **文案禁用词**（全站扫描，出现即改）：精通、熟练掌握、资深、顶尖、高手、大神、牛、极强、领先、天才、完美。
7. **不动**：不写 `.env` 内容、不展示本机/主机名路径、不出现任何密钥、不出现"辅助/自瞄/外挂"字样。
8. **字号下限**：正文字号不低于 13px，元数据/等宽标签不低于 12px，卡片标题不低于 19px。v1 出现的 10–11px 一律禁用。
9. **首页禁列数字**：首页不出现行数、文件数、帧数、模块数等规模指标（这些只允许出现在项目详情页与知识库）。首页只讲"能做什么"。

---

## 2 · 页面与文件ownership

| 页面 | 文件 | 拥有者 |
|---|---|---|
| 首页 | `index.html` `assets/css/home.css` | A1 |
| 项目索引 | `projects.html` `assets/css/projects.css` | A4 |
| 项目文章 01-03 | `projects/ocr-pipeline.html` `projects/train-framework.html` `projects/diffusion-lora.html` | A4 |
| 项目文章 04-06 | `projects/pose-pipeline.html` `projects/vision-classifier.html` `projects/service-layer.html` | A5 |
| 项目文章样式 | `assets/css/project-page.css` | 主控 |
| 知识库索引 | `notes.html` `assets/css/notes.css` | A3 |
| 文章页 | `notes/attention.html` `notes/ocr-pipeline.html` `assets/css/article.css` | A3 |
| 关于/联系/404 | `about.html` `contact.html` `404.html` `assets/css/pages.css` `robots.txt` `sitemap.xml` | B2 |
| 交互层 | `assets/js/main.js` `field.js` `palette.js` `reveal.js` `heatmap.js` `telemetry.js` | B1 |

---

## 3 · 页面骨架（逐页照抄，只替换标注处）

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title><!-- 页面标题 --> · Minecraft-JoJo</title>
  <meta name="description" content="<!-- 一句话，含关键技术词 -->">
  <meta name="theme-color" content="#07080A">
  <meta property="og:type" content="website">
  <meta property="og:title" content="<!-- 同 title -->">
  <meta property="og:description" content="<!-- 同 description -->">
  <meta property="og:image" content="./assets/svg/favicon.svg">
  <link rel="icon" href="./assets/svg/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="./assets/css/tokens.css">
  <link rel="stylesheet" href="./assets/css/base.css">
  <link rel="stylesheet" href="./assets/css/<!-- 本页 -->.css">
</head>
<body>
  <div class="grain" aria-hidden="true"></div>
  <div class="scanline" aria-hidden="true"></div>
  <a class="skip-link" href="#main">Skip to main content</a>
  <div class="cursor-ring" data-cursor aria-hidden="true"></div>
  <!-- HEADER 见 §4 -->
  <main id="main"> <!-- 页面内容 --> </main>
  <!-- FOOTER 见 §5 -->
  <div class="progress" data-progress aria-hidden="true"></div>
  <!-- PALETTE 见 §6 -->
  <script type="module" src="./assets/js/main.js"></script>
</body>
</html>
```

---

## 4 · HEADER（根级原文，`notes/` 页面把 href 换成 `../xxx.html`、logo 换 `../index.html`）

```html
<header class="site-header" data-header>
  <div class="wrap site-header__inner">
    <a class="brand" href="./index.html">
      <span class="brand__mark" aria-hidden="true">MJ</span>
      <span>Minecraft-JoJo</span>
      <span class="brand__sub mono xs">/ engineering dossier</span>
    </a>
    <nav class="site-nav" aria-label="主导航">
      <a class="nav-link" href="./index.html">Index</a>
      <a class="nav-link" href="./projects.html">Projects</a>
      <a class="nav-link" href="./notes.html">Knowledge</a>
      <a class="nav-link" href="./about.html">About</a>
      <a class="nav-link" href="./contact.html">Contact</a>
    </nav>
    <button class="btn header__cta" type="button" data-palette-open aria-haspopup="dialog">
      Search <span class="mono xs muted">⌘K</span>
    </button>
    <button class="nav-toggle" type="button" id="navToggle" aria-expanded="false" aria-controls="siteNav">Menu</button>
  </div>
</header>
```
> 当前页对应的 `nav-link` 加 `aria-current="page"`。

---

## 5 · FOOTER（根级原文）

```html
<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <p class="eyebrow">End of document</p>
        <p class="lede" style="margin-top:16px">这里的内容都可以被复核：文件、命令、出处，逐条给出。</p>
      </div>
      <div class="site-footer__links">
        <span class="mono xs muted">INDEX</span>
        <a href="./projects.html">Projects</a>
        <a href="./notes.html">Knowledge</a>
        <a href="./about.html">About</a>
        <a href="./contact.html">Contact</a>
      </div>
      <div class="site-footer__links">
        <span class="mono xs muted">REPO</span>
        <a href="https://github.com/Minecraft-JoJo" rel="noopener">GitHub / Minecraft-JoJo</a>
        <a href="https://github.com/Minecraft-JoJo/Mywebsite" rel="noopener">Source of this site</a>
      </div>
    </div>
    <div class="site-footer__meta" style="margin-top:48px">
      <div>BUILT <span data-metric="built">—</span> · RENDERED <span data-metric="load">—</span> · TRANSFER <span data-metric="bytes">—</span></div>
      <div>NO FRAMEWORKS · NO TRACKERS · NO WEBFONTS · 静态站点，由 GitHub Pages 托管</div>
    </div>
  </div>
</footer>
```

---

## 6 · PALETTE（`<dialog>`，根级原文；`notes/` 页面 href 前缀改为 `../`）

```html
<dialog class="palette" id="palette" aria-label="站内检索">
  <div class="palette__panel">
    <div class="palette__field">
      <span>⌘K</span>
      <input class="palette__input" id="paletteInput" type="search" placeholder="检索项目、文档、章节…" autocomplete="off" aria-controls="paletteList" aria-expanded="true" role="combobox" aria-autocomplete="list">
    </div>
    <ul class="palette__list" id="paletteList" role="listbox" aria-label="检索结果"></ul>
    <div class="palette__hint"><span>↑↓ 选择</span><span>↵ 打开</span><span>esc 关闭</span></div>
  </div>
</dialog>
```

---

## 7 · JS 钩子契约（HTML 只放钩子，行为由 B1 实现）

| 钩子 | 位置 | 语义 |
|---|---|---|
| `data-header` | header | 移动端开合；`#navToggle` 控制 `aria-expanded`→`data-open` |
| `data-palette-open` | 任意按钮 | 打开检索面板 |
| `#palette` `#paletteInput` `#paletteList` .palette__item | 见 §6 | 检索面板 |
| `data-cursor` | .cursor-ring | 自定义光标 |
| `data-progress` | .progress | 阅读进度条 |
| `data-reveal` | 任意块 | 进入视口时加 `.is-in`；错峰用 `style="--d:80ms"` |
| `data-count="52594"` | .metric__value 内 | 数字滚动 |
| `#fieldCanvas` `data-field` | 首页 hero | 背景场；`data-poster` 指向 SVG 兜底 |
| `#heatmapCanvas` `data-heat-temp` `data-heat-readout` | 首页探针 | 注意力热力图 + 温度滑杆 + 数值输出 |
| `data-marquee` | 跑马灯 track | 复制一份内容实现无缝循环 |
| `data-metric="load|bytes|built"` | footer | 真实性能读数 |
| `data-fps` | hero HUD | 实时帧率 |
| `data-copy` | pre 旁的按钮 | 复制代码 |
| `data-scrollspy` | 文章 TOC | 当前小节高亮 |

> 缺 JS 时页面必须依然完整可读（无 JS 也能看到全部内容）。

---

## 8 · 文案规则（决定了全站气质）

- 结构：**事实 → 数字 → 取舍 → 一句结论**。形容词一律删除。
- 允许"看不懂"的术语，但每个术语旁**必须**给一个可验证锚点（文件名、行数、命令、指标）。
- 语气：冷静、具体、不解释自己多厉害；把难度写成工程过程，不写天赋。
- 示例（照此力度写）：
  - ✗ 「我精通 PyTorch」
  - ✓ 「自建训练框架 `model / train / predata / cfg / logs`，3,012 行，含 ONNX 导出与 TensorBoard 日志」
  - ✗ 「我有丰富的 CV 经验」
  - ✓ 「RapidOCR 识别 → 版面分块 → 批量翻译 → 回填重绘，9 模块 969 行；难点是译文回填时的字体宽度与换行重排」

---

## 9 · 已核准的真实数字（不得改动）

| 项 | 值 |
|---|---|
| Markdown 总量 | 52,594 行 / 83 篇 |
| Python 总量 | 35,245 行 |
| 单篇最大 | FastAPI 7,994 · Linux 6,019 · PostgreSQL 4,449 · 数据库入门 3,609 · JS 练习册 3,333 · PySide6 3,148 · Python 基础 3,039 |
| 深度模型笔记 | Attention 2,010 · Seq2Seq 1,382 · 迁移学习 1,021 · LSTM 647 · 全景地图 457 |
| 工程（行数 / Python 文件数） | OCR 969/9 · 训练框架 3,012/29 · 姿态管线 5,604/31 · 分类实验台 1,495/8 · LoRA 本地入口 91/1 · 服务层 139/5 |
| 口径定义 | 「文件数」= `find <dir> -name "*.py" -not -path "*__pycache__*" | wc -l`；「行数」= 同范围 `cat | wc -l`。禁止使用"模块数"等有歧义的说法 |
| 数据标注 | 309 帧 pose 关键点 |
| LoRA 训练实参 | max_train_steps 8,000 · epoch 4 · network_dim 64 · network_alpha 32 · learning_rate 1e-4 · AdamW8bit · bf16 · 640–1024 bucket（来源 `last_20261001-080553.json`） |
| 服务层代码 | `users/` 125 行（auth_db 52 / auth_utils 49 / creat_user 24）+ `live/main.py` 14 行；另 7,994 行 FastAPI 文档 |
| 外部链接 | `github.com/Minecraft-JoJo`、`.../Mywebsite`、`.../OCR_Manga_trans` |

---

## 10 · 自检（交付前必须自己跑，并把结果写进汇报）

```bash
grep -rn 'href="/' <你的文件> ; grep -rn "src="/" <你的文件>          # 必须为空
grep -rnE '精通|熟练掌握|资深|顶尖|高手|大神|极强|领先|完美' <你的文件>   # 必须为空
```

---

## 11 · 动效策略（v3 修订）

1. **动效默认开启**。不得用 `prefers-reduced-motion` 作为绘制/动画的硬门槛——所有者本人的机器就开着该系统开关，曾因此看到完全静止的页面。
2. 开关由站内按钮 `[data-motion-toggle]` 控制，状态写入 `<html data-motion="on|off">` 与 localStorage（键 `motion:`）。CSS 侧 `html[data-motion="off"]` 已统一停掉动画。
3. 满足 WCAG 2.2.2「可暂停」：用户能停，但不替用户停。

## 12 · 项目结构（v3 修订）

- `projects.html` 是**索引页**：6 张卡片，不放技术细节。
- 每个项目是**独立文章**：`projects/<id>.html`，使用 `assets/css/project-page.css` 的 `.pa-*` 类。
- 首页项目卡直接链到文章页（不再用锚点）。
