# CLAUDE.md — AI协作阴性结果登记册

> AI 助手项目指令 · 生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25

---

## 项目定位

**AI协作阴性结果登记册（Negative Results Registry for AI Collaboration）** 是一个结构化的、可检索的公开阴性结果数据库。核心信念：知道什么不work和知道什么work同等重要。

## 项目性质

这是一个**文档/知识类项目**，非软件项目。核心交付物：
- `registry.json` — 机器可读登记册（权威数据源，脚本自动生成）
- `entries/` — 22 条目，.md（人读）+ .json（机读）双件
- `methodology.md` — 分类体系与价值论述（三语）
- `templates/submission-v2.md` — 标准化提交模板
- `docs/index.html` — GitHub Pages 可浏览页面
- `.github/workflows/ci.yml` — CI 自动校验

## 关键约束

### 数据完整性
- 每个条目必须有 `.md`（人读）+ `.json`（机读，按 `schema/entry.schema.json` 校验）双件
- `registry.json` 是聚合索引，从各条目 `.json` 自动生成，不可手工维护
- 条目ID格式：`NRR-YYYY-NNN`（如 `NRR-2026-001`），按年递增

### 提交来源标注
- 每条目的 `submitted_by` 字段记录提交者
- 条目 .md 文件末尾标注 `生成模型`（底层 Markdown 不强制 schema 约束；JSON 中暂无对应字段，待 schema 演进）
- 提交者和维护者可以不是同一个人

### 许可
- 文档/数据：CC BY 4.0
- 条目内容版权归提交者所有，提交即同意以 CC BY 4.0 发布

## 目录约定

```
negative-results-registry/
├── README.md                    # 项目概览（三语：中文 / EN / zh-Hant）
├── CONTRIBUTING.md              # 贡献指南（三语）
├── CLAUDE.md                    # 本文件
├── LICENSE                      # CC BY 4.0
├── .gitignore · .gitattributes
├── methodology.md               # 分类体系 + 价值论述（三语）
├── registry.json                # 聚合索引（脚本生成，禁止手工维护）
│
├── .github/workflows/
│   └── ci.yml                   # CI：Schema 校验 + 链接检查
│
├── schema/
│   └── entry.schema.json        # JSON Schema (Draft 2020-12)
│
├── templates/
│   ├── submission-v2.md         # 提交模板（推荐使用）
│   └── submission.md            # 旧版模板（保留参考）
│
├── entries/                     # 22 条目（NRR-2026-001 ~ 022）
│   └── NRR-YYYY-NNN/            # 每条目独立目录
│       ├── NRR-YYYY-NNN.md      # 人读报告
│       └── NRR-YYYY-NNN.json    # 机读数据（权威源）
│
├── scripts/
│   ├── generate_registry.py     # entries/ → registry.json
│   ├── validate_ci.py           # Schema + 链接 + 一致性校验
│   ├── check_external_links.py  # 外部链接检查
│   └── update_readme.py         # registry.json → README 自动更新
│
├── docs/
│   ├── index.html               # GitHub Pages 可浏览页面
│   ├── fork-modification-directions.md
│   └── existing-negative-results.md
│
├── en/                          # English translation
├── zh-Hant/                     # 正體中文翻譯
└── _reviews/                    # 独立审查报告（R1 + R2, prompts/ 已 gitignored）
```

## 命名约定

- 条目目录：`entries/NRR-YYYY-NNN/`
- 条目文件：`NRR-YYYY-NNN.md` + `NRR-YYYY-NNN.json`
- `_` 前缀目录：`_reviews/` 存放审查材料（prompts + 独立审查报告），属 AI 工作中间产物
- 脚本：`scripts/` 下，Python 脚本用 `snake_case.py`

## 工作约定

### 添加新条目
1. 分配新 ID（查阅 `registry.json` 中已有最大 ID）
2. 复制 `templates/submission-v2.md` 填写内容
3. 创建 `entries/NRR-YYYY-NNN/` 目录
4. 编写 `.md` + `.json` 双件（JSON 按 Schema V2 校验：需含 `source_project`/`source_authors`/`analyst`）
5. 运行 `scripts/generate_registry.py` 更新 `registry.json`
6. 运行 `scripts/update_readme.py` 更新三语 README
7. 更新 `docs/existing-negative-results.md`（如条目源自自有项目）

### 收到外部提交（未来）
1. 验证 JSON Schema 合规
2. 检查条目内容与模板一致性
3. 分配 ID
4. 按上述流程加入

## 条目来源

项目启动时已收录 22 个条目（NRR-2026-001–022），来自 6 个自有公开项目 + 7 个外部来源（学术论文 + 开源项目）。完整列表见 `README.md` §条目概览，或运行 `scripts/generate_registry.py` 查看最新状态。

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
