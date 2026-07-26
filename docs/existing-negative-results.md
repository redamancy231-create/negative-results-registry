# 自有阴性结果盘点

> 维护者自有项目中已识别的阴性/诚实结果。
> 此文件为内部工作文档——最终条目在 `entries/` 中独立维护。
> **最后更新**：2026-07-25（P0–P2 全部完成，NRR-2026-001–022 共 22 条目）
> 
> ⚠️ 此文件仅跟踪自有项目（非外部来源）。完整条目列表见 `README.md` §条目概览。

---

## 已收录（自有项目 15 条目：NRR-2026-001–010, 012–015, 019）

| ID | 来源 | 领域 | 分类 |
|----|------|------|------|
| [NRR-2026-001](../entries/NRR-2026-001/NRR-2026-001.md) | prompt-tdd-methodology | prompt-engineering | null-result |
| [NRR-2026-002](../entries/NRR-2026-002/NRR-2026-002.md) | prompt-tdd-methodology | prompt-engineering | null-result |
| [NRR-2026-003](../entries/NRR-2026-003/NRR-2026-003.md) | methodology-extraction-methodology | methodology-extraction | methodology-failure |
| [NRR-2026-004](../entries/NRR-2026-004/NRR-2026-004.md) | docx-pipeline | document-generation | methodology-failure |
| [NRR-2026-005](../entries/NRR-2026-005/NRR-2026-005.md) | etf-pattern-match-pybind11 | tool-building | ceiling-effect |
| [NRR-2026-006](../entries/NRR-2026-006/NRR-2026-006.md) | ma-case-study-pipeline | academic-writing | methodology-failure |
| [NRR-2026-007](../entries/NRR-2026-007/NRR-2026-007.md) | claude-skills | skill-design | methodology-failure |
| [NRR-2026-008](../entries/NRR-2026-008/NRR-2026-008.md) | docx-pipeline | code-review | methodology-failure |

---

## 候选（待评估是否纳入）

- ai-collaboration-framework 审查链（v1.3.2 rejected draft、v1.6 三件套同步失败等）
- 其他自有项目中已识别但未结构化的阴性结果

> 当前 22 条目已覆盖主要的自有项目和外部来源。后续扩展以外部提交为主。

---

## 排除（不纳入）

### BDC 项目（未公开，不符合纳入条件）

| # | 条目 | 分类 | 排除原因 |
|---|------|------|----------|
| 4 | LambdaRank 特征维度敏感性 | ceiling-effect | BDC 项目未公开，源数据和实验记录不可访问 |
| 5 | 静态特征未来信息泄漏 | methodology-failure | 同上 |
| 6 | Regime 检测滞后固有限制 | ceiling-effect | 同上 |

> 这三个阴性结果本身有纳入价值（方法论教训明确、可复现性好），但源项目未公开意味着外部读者无法验证原始数据。如果 BDC 项目未来公开或部分公开，可重新评估。

### 其他不纳入（非 AI 协作类 / 无实验结构 / 纯技术 bug）

- 笔记本冷启动问题（硬件问题）
- CloudDrive2 崩溃（软件 bug）
- Git Bash curl 中文编码（环境问题）
- git mv 破坏 .gitignore（已知 git 行为）

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
