/* data.js — 全站唯一内容索引。所有数字均可用 wc -l 复核。 */
export const SITE = {
  handle: "Minecraft-JoJo",
  title: "Minecraft-JoJo · Engineering Dossier",
  tagline: "机器学习 · 计算机视觉推理 · 生成模型微调 · 后端与桌面工程",
  repo: "https://github.com/Minecraft-JoJo",
  repoWeb: "https://github.com/Minecraft-JoJo/Mywebsite",
  ocrRepo: "https://github.com/Minecraft-JoJo/OCR_Manga_trans",
  base: "./"
};

export const NAV = [
  { label: "Index",       href: "./index.html",    match: "index" },
  { label: "Projects",    href: "./projects.html", match: "projects" },
  { label: "Knowledge",   href: "./notes.html",    match: "notes" },
  { label: "About",       href: "./about.html",    match: "about" },
  { label: "Contact",     href: "./contact.html",  match: "contact" }
];

export const METRICS = [
  { value: 52594, label: "行 Markdown 技术笔记", cmd: "find . -name '*.md' | xargs cat | wc -l" },
  { value: 83,    label: "篇独立文档",           cmd: "find . -name '*.md' | wc -l" },
  { value: 35245, label: "行 Python",            cmd: "find . -name '*.py' | xargs cat | wc -l" },
  { value: 309,   label: "帧姿态关键点标注",      cmd: "ls labels | wc -l" },
  { value: 6,     label: "完整工程档案",          cmd: "ls projects/*" },
  { value: 0,     label: "前端框架依赖 / KB",     cmd: "grep -r 'node_modules' assets || true" }
];

export const PROJECTS = [
  {
    id: "ocr-pipeline", n: "01",
    title: "漫画 OCR 翻译管线",
    tag: "Computer Vision · NLP · Render",
    lines: 969, modules: 9, repo: "https://github.com/Minecraft-JoJo/OCR_Manga_trans",
    summary: "RapidOCR 识别 → 版面分块重组 → 批量翻译 → 原图字块擦除与译文回填重绘。",
    stack: ["RapidOCR / PaddleOCR", "OpenCV", "HTTP 翻译 API", "Python 3.13", "ruff"],
    href: "./projects/ocr-pipeline.html"
  },
  {
    id: "train-framework", n: "02",
    title: "自建 PyTorch 训练框架",
    tag: "Framework · Training · Export",
    lines: 3012, modules: 29, repo: null,
    summary: "model / train / predata / cfg / logs 五层分离，含 ONNX 导出、TensorBoard、JWT 用户鉴权。",
    stack: ["PyTorch", "ONNX", "TensorBoard", "YAML 配置", "JWT"],
    href: "./projects/train-framework.html"
  },
  {
    id: "diffusion-lora", n: "03",
    title: "扩散模型 LoRA 微调",
    tag: "Generative · Fine-tuning · MLOps",
    lines: 91, modules: 1, repo: null,
    scale: "8,000 STEPS · DIM 64 / α 32 · BF16",
    summary: "kohya_ss 训练链本地化：配置模板生成、本地训练入口、每次训练留一份配置快照。",
    stack: ["kohya_ss", "Diffusers", "SDXL / LoRA", "uv", "WSL CUDA"],
    href: "./projects/diffusion-lora.html"
  },
  {
    id: "pose-pipeline", n: "04",
    title: "实时姿态估计推理管线",
    tag: "Real-time Inference · Overlay",
    lines: 5604, modules: 31, repo: null,
    summary: "YOLO pose → ONNX Runtime / TensorRT 缓存 → Win32 透明覆盖层 → PySide6 控制台与录制器。",
    stack: ["YOLO pose", "ONNX Runtime", "TensorRT", "Win32 API", "PySide6"],
    href: "./projects/pose-pipeline.html"
  },
  {
    id: "vision-classifier", n: "05",
    title: "图像分类实验台",
    tag: "CV · Transfer Learning",
    lines: 1495, modules: 8, repo: null,
    summary: "数据集加载、迁移学习训练、ONNX 导出与单图推理的完整闭环，作为分类任务的基准骨架。",
    stack: ["PyTorch", "torchvision", "ONNX", "argparse"],
    href: "./projects/vision-classifier.html"
  },
  {
    id: "service-layer", n: "06",
    title: "应用服务与数据层",
    tag: "Backend · Data · Auth",
    lines: 139, modules: 5, repo: null,
    scale: "139 LOC SERVICE · 7,994 LOC DOCS",
    summary: "FastAPI 服务模板、PostgreSQL + SQLAlchemy 数据层、JWT / passlib 鉴权链。",
    stack: ["FastAPI", "uvicorn", "PostgreSQL", "SQLAlchemy", "JWT", "Jinja2"],
    href: "./projects/service-layer.html"
  }
];

export const NOTES = [
  { title: "Attention（注意力机制）完全教程", lines: 2010, domain: "Deep Learning", href: "./notes/attention.html", featured: true },
  { title: "现代深度学习全景地图",             lines: 457,  domain: "Deep Learning", href: "./notes.html#dl", featured: true },
  { title: "Seq2Seq 网络介绍",                 lines: 1382, domain: "Deep Learning", href: "./notes.html#dl" },
  { title: "LSTM 网络介绍",                    lines: 647,  domain: "Deep Learning", href: "./notes.html#dl" },
  { title: "迁移学习",                         lines: 1021, domain: "Deep Learning", href: "./notes.html#dl" },
  { title: "FastAPI 教程",                     lines: 7994, domain: "Backend",       href: "./notes.html#backend" },
  { title: "PostgreSQL 教程",                  lines: 4449, domain: "Backend",       href: "./notes.html#backend" },
  { title: "数据库入门教程",                   lines: 3609, domain: "Backend",       href: "./notes.html#backend" },
  { title: "Linux 手册",                       lines: 6019, domain: "Systems",       href: "./notes.html#systems" },
  { title: "PySide6 学习手册",                 lines: 3148, domain: "Desktop",       href: "./notes.html#desktop" },
  { title: "Python 基础教程",                  lines: 3039, domain: "Language",      href: "./notes.html#language" },
  { title: "JavaScript 练习册",                lines: 3333, domain: "Frontend",      href: "./notes.html#frontend" }
];

export const SKILLS = [
  { domain: "Deep Learning 建模", level: "build",    detail: "从零实现 CNN / RNN / LSTM / Seq2Seq / Attention，含前向传播算例与训练脚本" },
  { domain: "计算机视觉推理",      level: "deploy",   detail: "YOLO pose 标注与训练、ONNX 导出、TensorRT 缓存、RapidOCR 版面还原" },
  { domain: "生成模型微调",        level: "build",    detail: "扩散模型 LoRA 训练链本地化、配置模板生成、训练运行记录" },
  { domain: "后端与数据层",        level: "deploy",   detail: "FastAPI 服务模板、PostgreSQL + SQLAlchemy、JWT / passlib 鉴权" },
  { domain: "桌面应用工程",        level: "build",    detail: "PySide6 全套控件族、资源打包、Windows 冻结分发" },
  { domain: "系统与工具链",        level: "operate",  detail: "Linux / Docker / conda / uv / git / ruff，WSL 与 Windows 双栈开发" }
];

export const STACK = [
  "Python", "PyTorch", "ONNX Runtime", "TensorRT", "OpenCV", "RapidOCR",
  "FastAPI", "PostgreSQL", "SQLAlchemy", "PySide6", "NumPy", "pandas",
  "scikit-learn", "kohya_ss", "Docker", "Linux", "WSL", "git", "uv", "ruff"
];
