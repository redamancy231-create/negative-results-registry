# Fork 修改方向全景分析

> 如果你在考虑 fork 这个项目——先花 5 分钟读这份文档，30 秒定方向。
> v0.1 · 基于 v0.1.0（24 条目）分析 · 生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25

---

## 决策树（3 个问题，30 秒定位起点）

```
你想做什么？
├─ 只是加几条自己的阴性结果 → 不要 fork，提 PR
├─ 做一个不同领域的登记册 → §1 换领域复用
├─ 只记录自己不公开 → §2 个人错题本
├─ 用这个 Schema 做教学 → §3 教学/工作坊
├─ 改进登记册本身 → §4 扩展登记册
├─ 做学术元分析 → §5 学术元分析
└─ 先了解不该做什么 → §6 反模式
```

---

## §1 换领域复用

**适合**：你想做一个不同领域的阴性结果登记册（如"量化策略阴性结果""LLM 评估阴性结果""生物信息学阴性结果"）。

**修改清单**：

| 文件 | 修改 |
|------|------|
| `schema/entry.schema.json` | 改 `domain` enum——删除不相关的领域，添加新领域的代码 |
| `methodology.md` | 改分类体系表 + 示例说明 |
| `templates/submission-v2.md` | 改领域/类型下拉选项 |
| `docs/index.html` | 改 `DOMAIN_LABELS` 和 `CATEGORY_LABELS` 映射 |
| `README.md`（三语） | 改项目定位 + 分类表 |
| `entries/` | 删除已有条目，填入你的初始条目 |

**保留不变**：Schema 结构、CI、GitHub Pages、提交模板、双件机制（.md+.json）、registry.json 聚合逻辑。

**独立价值**：分类体系和初始条目是你的，基础设施是继承的。

**工作量**：~2-4 小时（主要是新领域条目的编写）。

---

## §2 个人错题本

**适合**：你只收自己的阴性结果，不期望社区贡献。想保持私密或只分享给少数人。

**修改清单**：

| 文件 | 修改 |
|------|------|
| `README.md` | 删除"提交一条阴性结果"和 CONTRIBUTING.md 链接——改为"这是我的个人 AI 实验错题本" |
| `CONTRIBUTING.md` | 删除或改为"不接受外部提交" |
| `.github/workflows/ci.yml` | 保留（校验仍有价值） |
| `entries/` | 删除已有条目，填自己的 |
| 仓库可见性 | 建议设为 **private** |

**独立价值**：24 条目的结构可以直接当模板——复制格式、改内容、用 CI 校验。

**工作量**：~1 小时。

---

## §3 教学/工作坊

**适合**：你是教师/培训者，想让学生提交 AI 实验的阴性结果作为课程作业或工作坊练习。

**修改清单**：

| 文件 | 修改 |
|------|------|
| `README.md` | 加"课程使用说明"——提交截止日期、评分标准、示例条目 |
| `templates/submission-v2.md` | 简化——去掉第三方分析专区，加"你学到了什么"的评分 rubric |
| `CONTRIBUTING.md` | 改为学生的提交指南——加分支命名规则、提交信息格式 |
| 仓库设置 | 每个学生一个分支或 fork → PR |

**为什么适合教学**：结构化的阴性反思比"写一篇心得体会"更容易评估——假设是否可证伪、方法是否可复现、教训是否可操作。

**工作量**：~2 小时配置 + 每个学期维护。

---

## §4 扩展登记册

**适合**：你想改进登记册本身——加 Schema 字段、改分类体系、增强 CI、加 API。

### 直接可开工的方向

| 方向 | 说明 | 修改文件 | 门槛 |
|------|------|---------|:--:|
| **Schema V2** | 添加 `preregistered`、`secondary_domains`、`analysis_plan` 等字段 | `schema/entry.schema.json` + 所有条目 | 低 |
| **多领域支持** | 允许条目标记多个 `domains`（数组）而非单选 | `schema/entry.schema.json` + `docs/index.html` 筛选逻辑 | 低 |
| **API 端点** | 提供 `registry.json` 的 REST API（GitHub Pages 不支持服务端，需用 GitHub API raw URL） | 新增 `docs/api.md` | 低 |
| **RSS/Atom Feed** | 从 `registry.json` 生成条目更新 feed | 新增 `scripts/generate_feed.py` | 中 |
| **条目间关系图** | 基于 `links` 数组渲染条目间引用关系 | 修改 `docs/index.html` | 中 |
| **分类体系重构** | 将 domain/category 从单轴改为多轴（task_domain × intervention × activity） | `schema/entry.schema.json` + 全部条目 + 三语 README | 高 |

### 需要外部资源的方向

| 方向 | 说明 | 瓶颈 |
|------|------|------|
| **条目质量评分** | 类似 journal peer review——由独立评审者对条目打分 | 需要 ≥2 独立评审者 |
| **DOI 注册** | 给每个条目分配 DOI（如通过 Zenodo） | 需要 Zenodo/GitHub 集成 |

---

## §5 学术元分析

**适合**：你想用这个登记册的数据做跨条目统计分析——如"methodology-failure 在所有领域中占多大比例""哪些 models_used 组合最常出现在零结果中"。

**数据来源**：`registry.json` → `entries[]` → 每个条目的 `domain`、`category`、`models_used`、`effect_size`、`lessons_learned`。

**可做的分析**（当前 24 条目规模）：

| 分析 | 可行性 |
|------|:--:|
| 领域 × 类型交叉分布 | ✅ |
| 模型使用频次排名 | ✅ |
| 效应量模式聚类 | ⚠️ n=24 偏小 |
| 教训主题分类 | ✅ |
| 第一方 vs 第三方差异 | ⚠️ n=24 偏小，16 vs 8 |
| 跨条目模式识别（P1-P8 类） | ❌ n=24 不够（已知结论——methodology-extraction-methodology G5 审计） |

**局限**：24 条目全部来自同一作者——不能泛化到其他操作者。等条目数 ≥50 且包含 ≥3 独立提交者后方可做跨操作者分析。

---

## §6 反模式

以下基于本项目和 methodology-extraction-methodology 的实际踩坑经验：

| # | 反模式 | 详细 |
|---|--------|------|
| 1 | **不要 fork 只是为加几条条目**——提 PR。登记册的价值在网络效应 | Fork 越分散，`registry.json` 聚合越弱 |
| 2 | **不要只增加条目不更新 README 条目表**——README 表格和 registry.json 会漂移 | CI 不会自动检查 README 表格——需要手工同步 |
| 3 | **不要把"未检出差异"写成"证明无效"**——这是条目最常犯的统计错误 | 见 NRR-2026-001 的修复历程 |
| 4 | **不要删除失败的审查记录**——`_reviews/` 是项目的审计链 | 两轮 GPT-5.6-Sol 审查报告是项目质量的外部证据 |
| 5 | **不要改 Schema 后不更新 CI**——`validate_ci.py` 用的是 `entry.schema.json` | 改了 Schema 必须同步更新 CI 校验脚本 |
| 6 | **不要把第三方分析伪装成第一方报告**——`submitted_by` 必须如实填写 | 分析者和实验者不是同一个人时，reproducibility 评估的对象也不同 |
| 7 | **不要在 README 中声称"社区登记册"如果没有外部提交**——当前 24 条目全部来自维护者 | 见 v0.1.0 README "当前为维护者个人失败日志的结构化原型" |
| 8 | **不要改 `generate_registry.py` 后不重新生成 `registry.json`**——两者漂移会导致 CI 一致性检查失败 | `registry.json` 禁止手工维护，必须脚本生成 |
| 9 | **不要忽视 `.gitignore` 排除的文件**——`project_status.md` 和 `_reviews/prompts/` 故意不公开 | Fork 后检查你是否有需要排除的内部文件 |

---

## 方向排序（按实现门槛从低到高）

| 方向 | 门槛 | 独立价值 | 适合人群 |
|------|:--:|:--:|------|
| 个人错题本（private） | ★☆☆ | 高 | 任何用 AI 做项目的人 |
| 换领域复用 | ★★☆ | 高 | 有其他领域专业知识的 AI 协作者 |
| 教学/工作坊 | ★★☆ | 高 | 教师、培训者 |
| 加 Schema 字段 | ★★☆ | 中 | 想增强条目元数据的人 |
| 学术元分析 | ★★★ | 中 | 研究者 |
| 分类体系重构 | ★★★ | 低 | 方法论研究者 |
| RSS/Feed + API | ★★★ | 中 | 开发者 |

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
