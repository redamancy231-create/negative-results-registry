# Kimi-K2.7-Code 变更审计报告

审查模型：Kimi-K2.7-Code · 日期：2026-07-26

## 发现汇总

- 🔴 严重：0 条
- 🟡 中等：1 条
- 🟢 轻微：4 条

## 逐维度发现

### 维度 1：Schema 迁移完整性

**🟢 轻微 | schema/entry.schema.json | 5 个第三方分析条目未填写可选字段 `source_project_url`**

抽查确认：NRR-2026-011、NRR-2026-016、NRR-2026-017、NRR-2026-019、NRR-2026-020 均为第三方分析条目（`source_authors != analyst`），但 `source_project_url` 为空。该字段在 Schema V2 中为可选，因此不构成合规性问题；然而第三方分析条目的可追溯性高度依赖源项目链接，建议后续补全论文或仓库 URL，以强化"证据可追溯"门槛。

其余检查通过：
- 22 个条目 JSON 全部包含 14 个必填字段，无缺失、无类型错误；
- 第一方条目 14 个，`source_authors == analyst == submitted_by`（均为 Acerolaorion），三角色一致；
- 第三方条目 8 个，`source_authors` 与 `analyst`/`submitted_by` 正确区分（如 NRR-2026-018 的 source_authors="Spencer Burleigh"、analyst="Acerolaorion"）；
- `jsonschema` 校验 22 个条目全部通过。

### 维度 2：.md/.json 双件一致性

**🟢 轻微 | 全部 22 条条目 | `source_project_url` 未在 `.md` 基本信息表中显式展示**

V2 新增的三个必填字段（`source_project`、`source_authors`、`analyst`）已在全部 22 条条目的 `.md` 基本信息表中出现，且取值与 JSON 一致。但 `source_project_url` 未在 `.md` 基本信息表中列出，仅在部分条目的相关链接或解读中以普通超链接形式出现。由于该字段是可选字段，本次审计将其列为轻微提示；若后续希望 `.md` 与 JSON 的字段映射更完整，可考虑在基本信息表中追加一行。

其余检查通过：
- NRR-2026-001 与 NRR-2026-018 抽查：`.md` 基本信息表中的"来源项目 / 来源作者 / 分析者"与 JSON 完全一致；
- 自动化扫描确认：所有 22 条目的 V2 字段值均可在对应 `.md` 中找到。

**🟢 轻微 | scripts/sync_md_v2.py（已删除） | 一次性回填脚本无法复核，但结果无遗漏**

`sync_md_v2.py` 已在仓库中删除，无法逐行审查其插入逻辑。不过实际结果验证表明 22 条条目的 `.md` 均已正确回填 V2 字段，未发现遗漏条目或字段错位。

### 维度 3：代码脚本逻辑

**🟡 中等 | scripts/check_external_links.py:27-28 | `classify_url()` 将所有非 HTTPError 异常统一标记为 `skipped`**

代码逻辑：
```python
except Exception as e:
    return ("skipped", type(e).__name__)
```

该写法把 DNS 解析失败、SSL 证书错误、连接超时、socket 异常等全部归为 `skipped`。在 CI 非阻塞策略下，这可以避免网络抖动导致误报；但代价是可能漏报真正的 broken 链接（例如域名拼写错误、证书严重错误、服务器已下线等）。建议至少将 `urllib.error.URLError` 中可识别的永久性错误（如 `ssl.SSLCertVerificationError`、`socket.gaierror`）单独分类为 `broken` 或在详情中给出更明确提示，而不是全部 `skipped`。

**🟢 轻微 | scripts/check_external_links.py:16,449 | 跨条目重复 URL 仅在首次出现的条目中计数**

脚本使用全局 `seen_urls` 去重，虽然全局计数 `global_counts` 准确，但按条目报告时，相同 URL 只在第一次遇到的条目中统计。例如多个条目引用同一仓库主页时，后续条目的 `verified/skipped/broken` 计数会少计该 URL。该行为不影响 CI 判定（只看是否有 broken），但会让"按条目分级报告"的条目级数字不完整。建议在未来版本将条目级统计与全局去重解耦，或在文档中说明条目计数仅统计本条目首次出现的 URL。

**🟢 轻微 | scripts/check_external_links.py | 本地 Windows 默认 GBK 控制台输出 emoji 时崩溃**

在 Windows 默认代码页（936/GBK）下直接运行 `python scripts/check_external_links.py` 会触发 `UnicodeEncodeError: 'gbk' codec can't encode character '\u2705'`。设置 `PYTHONIOENCODING=utf-8` 后可正常运行。此问题不影响 GitHub Actions（Ubuntu），但会降低本地 Windows 开发者的体验。建议在脚本开头设置 stdout 编码（如 `sys.stdout.reconfigure(encoding='utf-8')`）或避免在 print 中直接使用 emoji。

其余检查通过：
- `is_own_project()` 判定条件 `source_authors == analyst == submitted_by` 与 Schema V2 三角色语义一致；在所有 22 条目上正确区分 14 个第一方与 8 个第三方条目；
- `classify_url()` 对 github.com/arxiv.org 限速跳过、HTTP 403/429 跳过、其他 4xx/5xx 标记为 broken 的逻辑正确；urllib 默认会跟随 301/302 redirect，返回最终状态码，行为合理；
- `generate_summary()` 按 `source_project` 去重，README 显示的"7 个自有公开项目 + 7 个外部来源"与脚本计算结果一致；
- `update_readme.py --check` 与 `validate_ci.py --skip-external-links` 均通过。

### 维度 4：三语文档一致性

**🟢 轻微 | templates/submission-v2.md:12 | 提交模板步骤 3 与 CONTRIBUTING.md / 三语 README 的 ID 分配措辞不一致**

- `CONTRIBUTING.md`（中文/英文/正體中文）步骤 3 与三语 README "5 分钟流程"步骤 3 均明确：使用临时标识命名（如 `temp-method-failure`），正式 ID 由维护者在合并 PR 时分配；
- `templates/submission-v2.md` 步骤 3 原文："创建 `entries/NRR-YYYY-NNN/` 目录（ID 用当前最大编号 +1，分配后告知维护者）"。

虽然两者最终都指向"维护者分配正式 ID"，但 `submission-v2.md` 的措辞暗示贡献者可以先自行选择 `NRR-YYYY-NNN` 形式的编号，与"临时标识"说法存在轻微冲突，可能导致贡献者困惑。建议将 `submission-v2.md` 步骤 3 统一为与 CONTRIBUTING.md 一致的临时标识表述。

其余检查通过：
- 中文 CONTRIBUTING.md 的证据门槛定义清晰可操作（假设可证伪 / 方法可复核 / 证据可追溯）；
- 三语 CONTRIBUTING.md 的 ID 分配措辞一致（临时标识 → 维护者分配）；
- 三语 README 的"5 分钟流程"步骤 3 统一为"临时标识命名；正式 ID 由维护者分配"；
- 不存在 `submission.md` 与 `submission-v2.md` 的功能性混用：`submission.md` 作为旧版模板保留参考，`submission-v2.md` 为当前推荐模板，目录结构说明中已明确标注。

### 维度 5：残留引用

**🟢 轻微 | project_status.md:46 | `entry_sources.json` 在历史记录中被提及**

`project_status.md` 的"已完成"列表中写有"废弃 entry_sources.json，update_readme.py 直接从条目读 source_project"。这是变更历史记录，不是功能性引用；未在 CI、脚本、模板或 README 中发现对该文件的功能性读取/写入调用。

其余检查通过：
- 未在 `scripts/`、`templates/`、`entries/`、`README.md`、三语 README、`CONTRIBUTING.md` 等核心文件中发现 `entry_sources.json` 的功能性引用；
- 旧 Schema（11 必填字段）的引用仅出现在 `_reviews/` 历史审查报告中，核心代码与文档均使用 14 必填字段的 V2 描述。

## 验证记录

- `python scripts/validate_ci.py --skip-external-links`：CI PASSED（22 条目 schema 有效、内部链接无 broken、registry.json 计数一致）。
- `python scripts/update_readme.py --check`：All READMEs in sync with registry.json。
- `python scripts/check_external_links.py`（设置 `PYTHONIOENCODING=utf-8` 后）：Total 0 verified, 33 skipped, 0 broken；22/22 entries clean。
- `jsonschema` 校验 22 条目：0 错误。

## 总体评估

- 变更窗口质量：**通过**
- 是否建议追加修复：**是（轻微）**

本次 v0.2.0 Schema V2 升级整体合规：22 条目回填完整、.md/.json 双件一致、三语 CONTRIBUTING/README 的 ID 分配与证据门槛措辞统一、已废弃的 `entry_sources.json` 无功能性残留引用、`update_readme.py` 的 `is_own_project()` 逻辑与三角色语义一致。未发现严重或中等合规问题。

建议的追加修复均为轻微级别，按优先级排序：
1. 统一 `templates/submission-v2.md` 步骤 3 为"临时标识"表述，与 CONTRIBUTING.md / README 保持一致；
2. 为 5 个缺少 `source_project_url` 的第三方分析条目补全源论文/仓库链接；
3. 优化 `check_external_links.py` 的异常分类，将可识别的永久性网络错误（DNS/SSL 等）从 blanket `skipped` 中分离；
4. 解耦 `check_external_links.py` 的条目级 URL 计数与全局去重，或补充说明；
5. 增强 `check_external_links.py` 的 stdout 编码兼容性，避免 Windows 默认控制台崩溃。
