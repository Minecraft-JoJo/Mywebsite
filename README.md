# Mywebsite · Engineering Dossier

个人技术档案站。零构建、零依赖、零外链的静态站点，直接由 GitHub Pages 托管。

- 线上地址：https://minecraft-jojo.github.io/Mywebsite/
- 源码仓库：https://github.com/Minecraft-JoJo/Mywebsite

---

## 1 · 这是什么

一份可复核的工程档案，不是简历。全站只写数字、文件、命令与取舍，不写形容词；
页面上出现的每一个数字都能用一条命令验证，命令就印在那个数字旁边。

| 页面 | 文件 |
|---|---|
| 首页 | `index.html` |
| 工程档案（6 份） | `projects.html` |
| 知识库索引 | `notes.html` |
| 深度文章 | `notes/attention.html` · `notes/ocr-pipeline.html` |
| 关于 / 联系 | `about.html` · `contact.html` |
| 404 | `404.html` |

## 2 · 硬约束（改代码前先读）

1. **零构建**：手写 HTML / CSS / ES module，无 npm、无打包器、无 CDN。
2. **相对路径**：除 `404.html` 外，全站禁止以 `/` 开头的 `href`/`src` —— 站点部署在子路径 `/Mywebsite/` 下。
3. **设计与组件只有一个来源**：`assets/css/tokens.css`（令牌）+ `assets/css/base.css`（共享组件）。页面级 CSS 只能加自己的前缀类。
4. **无 JS 必须完整可读**：入场动画不得把内容默认状态写成 `opacity:0`。
5. **数字必须实测**：口径见 `docs/CONTRACT.md §9`。文件数 `find … -name "*.py" | wc -l`，行数 `cat … | wc -l`。

## 3 · 本地预览（**必须用 HTTP 服务，不能双击打开**）

页面用原生 ES module，`file://` 下会被浏览器的模块 CORS 规则拦掉，检索面板与热力图都不会工作。

```bash
cd Mywebsite
python -m http.server 8080
# 打开 http://127.0.0.1:8080/
```

模拟线上子路径 `/Mywebsite/`：

```bash
cd ..                      # Mywebsite 的父目录
python -m http.server 8081
# 打开 http://127.0.0.1:8081/Mywebsite/
```

## 4 · 推流

```bash
cd Mywebsite
git add -A
git commit -m "site: engineering dossier"
git push origin main
```

然后在仓库 **Settings → Pages** 确认：

- Source: **Deploy from a branch**
- Branch: **main** / 目录 **/ (root)**

等 1–2 分钟。仓库根的 `.nojekyll` 会跳过 Jekyll 处理，保证 `assets/` 原样发布。

## 5 · 绑定自定义域名时唯一要改的地方

`404.html` 是全站唯一使用根级绝对路径 `/Mywebsite/` 的文件 —— 因为 GitHub Pages 会用它对任意层级的缺失路径作出响应，相对路径在深层 URL 下必然解析错误。

绑定域名后把该文件里的前缀换掉即可：

```bash
sed -i 's|/Mywebsite/|/|g' 404.html
```

其余页面全部相对路径，**不需要任何改动**。

## 6 · 目录

```
.
├── index.html · projects.html · notes.html · about.html · contact.html · 404.html
├── notes/
│   ├── attention.html          注意力机制精编（源：2,010 行笔记）
│   └── ocr-pipeline.html       OCR 管线工程复盘（源：9 文件 969 行）
├── assets/
│   ├── css/
│   │   ├── tokens.css          设计令牌（颜色 / 字号 / 间距 / 动效）
│   │   ├── base.css            重置 + 全部共享组件
│   │   └── home · projects · notes · article · pages.css
│   ├── js/
│   │   ├── data.js             内容索引（全站数字的唯一来源）
│   │   └── main · field · palette · reveal · heatmap · telemetry.js
│   └── svg/favicon.svg · hero-poster.svg
├── docs/CONTRACT.md            实现契约（页面骨架、钩子表、数字口径）
├── robots.txt · sitemap.xml · .nojekyll
└── README.md
```

## 7 · 复核抽查

```bash
grep -rnE '精通|熟练掌握|资深|顶尖|高手|大神|极强|领先|完美' *.html notes/*.html     # 应为空
grep -rn 'href="/\|src="/' *.html notes/*.html | grep -v 404.html                  # 应为空
grep -c '<loc>' sitemap.xml                                                        # 7
```

## 8 · 无障碍与性能约定

- 键盘可达：skip link、`⌘K` / `Ctrl+K` 检索面板（↑↓ 选择、↵ 打开、esc 关闭）、焦点样式完整。
- `prefers-reduced-motion: reduce` 下：背景场停止绘制、光标环关闭、boot 序列跳过、颗粒与扫描线隐藏。
- 无框架、无 Webfont、无追踪脚本；字体走系统栈，首屏零字体请求。
