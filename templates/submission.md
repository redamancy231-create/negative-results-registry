# 阴性结果提交模板

> 复制此模板，填写后放到 `entries/` 目录。文件名：`NRR-YYYY-NNN.md`（如 `NRR-2026-001.md`）。
> 同时请提供对应的 `NRR-YYYY-NNN.json` 机读版（按 `schema/entry.schema.json` 校验）。

---

## 基本信息

| 字段 | 内容 |
|------|------|
| **条目ID** | NRR-YYYY-NNN（提交时由维护者分配） |
| **标题** | 一句话描述这个阴性结果 |
| **领域** | prompt-engineering / code-review / methodology-extraction / workflow-orchestration / document-generation / multi-model-collaboration / quantitative-research / academic-writing / tool-building / skill-design / benchmarking / other |
| **分类** | null-result / ceiling-effect / worse-than-baseline / failed-to-replicate / methodology-failure / abandoned-dead-end / hypothesis-falsified / tool-unfit-for-purpose / other |
| **提交者** | 你的 GitHub 用户名或姓名 |
| **日期** | 实验结束日期（YYYY-MM-DD） |

---

## 实验概述

### 原始假设

> 你预期什么会有效？为什么会这样想？

_（填写）_

### 方法

> 简要描述：实验设计、样本量、使用的模型/工具、评估指标。

_（填写）_

### 预期结果

> 如果假设成立，你应该观察到什么？

_（填写）_

### 实际结果

> 实际发生了什么？尽量具体，有数据附数据。

_（填写）_

| 指标 | 数值 |
|------|------|
| 效应量 | （如有定量指标） |
| 样本量 | |
| 使用的模型 | |

---

## 解读与反思

### 为什么会失败？

> 你的分析：是假设本身错了、方法有问题、还是外部因素？

_（填写）_

### 学到了什么？（1-5条）

1. _（填写）_
2. _（填写）_
3. _（填写）_

---

## 可复现性

| 维度 | 评估 |
|------|------|
| **整体可复现性** | fully-reproducible / partially-reproducible / not-reproducible / not-assessed |
| **可用产物** | prompts / data / code / logs / analysis-script / raw-output / none |

> 备注：

_（填写）_

---

## 相关

### 后续是否成功？

> 后来换方法做成功了吗？如果有，链接/引用。

_（填写或"无"）_

### 相关链接

- _（链接到仓库/报告/相关条目）_

### 标签

> 自由标签，便于检索。例如：`prompt-tdd`, `GPT-5.5`, `DTW`, `审查衰减`

_（填写）_
