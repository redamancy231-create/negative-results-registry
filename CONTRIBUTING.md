# 贡献指南

> 欢迎提交你在 AI 协作中遇到的阴性/诚实结果。一本"别人踩过的坑"地图，需要别人的坑。

---

## 提交一条阴性结果

### 你需要的

- 一个 AI 协作实验——试了什么、预期什么、实际发生了什么
- 实际结果是阴性的（零结果、劣于基线、方法失败、工具不适用……见下方分类）
- 愿意以 CC BY 4.0 发布

### 你不需要的

- 学术论文格式
- 统计显著性（单案例诚实报告也欢迎）
- "大失败"——小到"换了个 prompt 反而更差"也可以

### 步骤

1. **Fork** 本仓库
2. 复制 `templates/submission.md` → 按模板填写
3. 创建 `entries/NRR-YYYY-NNN/` 目录（ID 用当前最大编号 +1，如现有最大为 NRR-2026-018，则用 NRR-2026-019）
4. 放入 `.md`（人读）+ `.json`（机读，按 `schema/entry.schema.json` 校验）
5. JSON 校验：
   ```bash
   pip install jsonschema
   python -c "import json, jsonschema; s=json.load(open('schema/entry.schema.json')); e=json.load(open('entries/NRR-2026-XXX/NRR-2026-XXX.json')); jsonschema.Draft202012Validator(s).validate(e); print('OK')"
   ```
6. 运行 `python scripts/generate_registry.py` 更新 `registry.json`
7. 提 **Pull Request**

---

## 什么可以提交？

| ✅ 欢迎 | ❌ 不适合 |
|---------|----------|
| Prompt 对照实验中无显著差异 | "我随便试了一下不行"（缺方法描述） |
| 方法论文献提取未达稳定门槛 | 不涉及 AI 协作的纯技术 bug |
| 某工具/模型在特定任务上失败 | 没有记录实验条件的印象式判断 |
| 策略回测中某因子无预测力 | 保密/未公开项目的结果 |
| Workflow 编排中某模式反效果 | 抄袭/造假/未获授权的内容 |

---

## 分类速查

### 按领域（12 类）

`prompt-engineering` · `code-review` · `methodology-extraction` · `workflow-orchestration` · `document-generation` · `multi-model-collaboration` · `quantitative-research` · `academic-writing` · `tool-building` · `skill-design` · `benchmarking` · `other`

### 按阴性结果类型（9 类）

| 类型 | 说明 |
|------|------|
| `null-result` | 实验组和对照组无显著差异 |
| `ceiling-effect` | 基线已很好，改进空间为零 |
| `worse-than-baseline` | 新方法比基线还差 |
| `failed-to-replicate` | 无法复现之前有效的发现 |
| `methodology-failure` | 实验设计/执行本身出问题 |
| `abandoned-dead-end` | 方向本身不可行 |
| `hypothesis-falsified` | 明确推翻了原有假设 |
| `tool-unfit-for-purpose` | 选的工具/模型不适合任务 |
| `other` | 不在以上分类 |

---

## 第三方分析

如果你提交的不是自己的实验，而是分析别人项目中记录的阴性结果：

- `submitted_by` 填你自己（分析者）
- 在 `reproducibility.notes` 中标注"第三方分析条目"和源项目
- 条件：目标项目本身**公开记录**了该阴性结果（不能从沉默中推断）

---

## 其他贡献方式

- **改进 Schema**：`schema/entry.schema.json` 的字段增删或约束调整 → Issue 讨论 → PR
- **改进分类体系**：`methodology.md` 中的领域/类型分类 → Issue 讨论
- **报告条目事实错误**：条目中的数字、引用等事实性错误 → Issue
- **翻译**：英文/正体中文翻译 → 见 `en/` 和 `zh-Hant/` 目录（待创建）

---

## 审查流程

提交 PR 后，维护者会检查：

1. JSON Schema 合规（`entry.schema.json` 校验通过）
2. 条目内容与模板一致性
3. 分类正确性（领域 + 类型）
4. ID 唯一性
5. `.md` 和 `.json` 双件齐全且内容一致

通过后合并，`registry.json` 随条目自动更新。

---

## 许可

- 条目内容版权归提交者所有，提交即同意以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 发布
- 提交即确认你有权授权该内容以 CC BY 4.0 发布
- 维护者保留拒绝不符合标准条目的权利

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
