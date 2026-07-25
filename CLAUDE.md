# CLAUDE.md — AI协作阴性结果登记册

> AI 助手项目指令 · 生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25

---

## 项目定位

**AI协作阴性结果登记册（Negative Results Registry for AI Collaboration）** 是一个结构化的、可检索的公开阴性结果数据库。核心信念：知道什么不work和知道什么work同等重要。

## 项目性质

这是一个**文档/知识类项目**，非软件项目。核心交付物：
- `registry.json` — 机器可读登记册（权威数据源）
- `entries/` — 按条目ID组织的独立阴性结果报告（人读 .md + 机读 .json）
- `methodology.md` — 分类体系与价值论述
- `templates/submission.md` — 标准化提交模板

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
├── README.md                    # 项目概览（中英双语）
├── CLAUDE.md                    # 本文件
├── LICENSE                      # CC BY 4.0
├── .gitignore                   # 排除 project_status.md
├── methodology.md               # 为什么 + 分类体系
├── registry.json                # 聚合索引（从条目生成）
│
├── schema/
│   └── entry.schema.json        # JSON Schema (Draft 2020-12)
│
├── templates/
│   └── submission.md            # 提交模板（复制此模板填写）
│
├── entries/                     # 条目目录
│   ├── NRR-2026-001/
│   │   ├── NRR-2026-001.md
│   │   └── NRR-2026-001.json
│   └── ...
│
├── scripts/                     # 工具脚本
│   └── generate_registry.py     # 从 entries/ 生成 registry.json
│
├── _reviews/                    # 审查材料（prompts + 报告）
│   ├── prompts/
│   └── gpt56-sol-review-report-*.md
│
└── docs/                        # 补充文档
    └── existing-negative-results.md  # 自有阴性结果盘点
```

## 命名约定

- 条目目录：`entries/NRR-YYYY-NNN/`
- 条目文件：`NRR-YYYY-NNN.md` + `NRR-YYYY-NNN.json`
- `_` 前缀目录：`_reviews/` 存放审查材料（prompts + 独立审查报告），属 AI 工作中间产物
- 脚本：`scripts/` 下，Python 脚本用 `snake_case.py`

## 工作约定

### 添加新条目
1. 分配新 ID（查阅 `registry.json` 中已有最大 ID）
2. 复制 `templates/submission.md` 填写内容
3. 创建 `entries/NRR-YYYY-NNN/` 目录
4. 编写 `.md` + `.json` 双件
5. JSON 文件用 `schema/entry.schema.json` 校验
6. 运行 `scripts/generate_registry.py` 更新 `registry.json`
7. 更新 `docs/existing-negative-results.md`（如条目源自自有项目）

### 收到外部提交（未来）
1. 验证 JSON Schema 合规
2. 检查条目内容与模板一致性
3. 分配 ID
4. 按上述流程加入

## 初始条目来源

项目启动时已收录 4 个条目，全部来自维护者自有项目的历史阴性结果：

| ID | 来源项目 | 类型 | 概述 |
|----|---------|------|------|
| NRR-2026-001 | prompt-tdd-methodology | null-result | 三段式分段对审查质量无显著影响 |
| NRR-2026-002 | prompt-tdd-methodology | null-result | 声明式路由 vs NL 路由无差异 |
| NRR-2026-003 | methodology-extraction-methodology | methodology-failure | 22项目0模式达到≥3源稳定门槛 |
| NRR-2026-004 | docx-pipeline | methodology-failure | mmdc PNG 无 DPI 元数据→python-docx 默认 72 DPI 致图片拉伸 |

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
