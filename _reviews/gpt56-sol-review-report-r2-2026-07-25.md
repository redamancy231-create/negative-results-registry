# 独立审查报告 R2：AI 协作阴性结果登记册

**审查者**：GPT-5.6-Sol (via Codex CLI)  
**审查日期**：2026-07-25  
**项目版本**：v0.1.0（22 条目）

---

## D1: Number Drift

**评分**：2/5

| # | 严重度 | 描述 | 修复建议 |
|---|---|---|---|
| D1-1 | MAJOR | 三语 README 的当前条目数存在 18/22 冲突：概览均写 22，中文 badge 为 22，但英文和正体中文 badge 仍为 18；三份“核心信念”第 5 条及“为什么是我来做 / Why Me”也仍写 18。读者在第一屏无法判断哪个数字可信。 | 全局将当前规模统一为 22，并把条目数集中到单一可生成数据源；CI 从 `registry.json.metadata.total_entries` 校验三语 badge、核心段落和概览。 |
| D1-2 | MAJOR | 三语概览均写“22 entries，9 domains × 7 types”。磁盘上当前实际使用的是 **10 个 domain、4 个 category**；Schema 的完整分类容量则是 **12 个 domain、9 个 category**。“9 × 7”按两种口径均不成立。 | 明确文案口径：若描述已覆盖范围，写“10 个已使用领域 × 4 个已使用类型”；若描述分类体系，写“12 个领域 × 9 个类型”。建议两者同时列出并由 registry 自动计算。 |
| D1-3 | MINOR | 英文 README 另有“18 million AI-related repositories on GitHub”。它不是条目数，但与大量旧“18”混在一起且未给来源，增加数字检索和维护噪声。 | 给出可核验出处、统计日期和口径；若无法稳定维护，改为不依赖具体数量的定性表述。 |

**核验通过项**：

- `schema/entry.schema.json` 定义 12 个 domain、9 个 category；`methodology.md` 两组分类与 enum 完全一致。
- 磁盘 22 个 JSON 的实际统计为 10 个已使用 domain、4 个已使用 category；`registry.json` 的 `total_entries`、entries 数组长度、`stats.by_domain`、`stats.by_category` 均与实际一致。
- 三语 README 的条目表均为 22 行，且 ID、domain、category 与对应 JSON 全量一致。
- `CLAUDE.md` 未发现 BDC 或“3–5 个”残留；“项目启动时已收录 4 个条目”是可核验的历史陈述，不属于当前数字漂移。

## D2: Cross-Language Parity

**评分**：4.5/5

| # | 严重度 | 描述 | 修复建议 |
|---|---|---|---|
| D2-1 | MINOR | Footer 模型标注不完全同构：英文和正体中文同时标注生成模型与翻译模型，中文原稿仅标生成模型。中文不需要翻译模型本身合理，但提示词要求的三语元数据结构并未统一。 | 中文 footer 增加“翻译模型：不适用（原始语言）”，或在贡献规范中明确原始语言版本可省略翻译模型。 |

**核验通过项**：

- 三份 README 的 22 行条目表完全一致。
- 三份 README 的 5 条核心信念一一对应；其中共同残留的“18”属于内容正确性问题，已计入 D1，不重复计为翻译差异。
- 三份分类表均为相同的 12 domains + 9 categories，且均包含“为什么是我来做 / Why Me”小节。
- 英文 README 中仅语言切换 badge 保留“中文 / 正體中文”，属于有意界面文本；正体中文版本未发现简体中文残留。

## D3: Structural Drift

**评分**：2/5

| # | 严重度 | 描述 | 修复建议 |
|---|---|---|---|
| D3-1 | MAJOR | `templates/submission.md` 与 `submission-v2.md` 同时存在，但三语 README、三语 CONTRIBUTING 和 `CLAUDE.md` 的公共入口仍全部指向 v1。v2 新增的第三方分析证据、source commit/version、访问日期、纳入范围、复核步骤、事实/观察/推断区分及 MD/JSON 镜像要求，事实上不可发现，也不是当前权威流程。 | 确定唯一规范：优先把 v2 升为 `templates/submission.md` 或将所有入口改指 v2；归档旧版并在 CI 中检查禁止引用过期模板。 |
| D3-2 | MAJOR | 三语 README 的目录树彼此一致但显著落后磁盘，漏列 `.github/`、`en/`、`zh-Hant/`、`_reviews/`、`docs/index.html`、`.gitattributes`、`project_status.md`、`submission-v2.md` 和两个校验脚本。`CLAUDE.md` 更陈旧，仍把 README 描述为中英双语，并遗漏 CONTRIBUTING、Pages、CI 和新增语言目录。 | 从磁盘结构生成精简目录树，或只维护稳定的顶层结构；同步更新 `CLAUDE.md` 的项目结构、核心交付物和新条目流程。 |
| D3-3 | MODERATE | CONTRIBUTING 仍举例“最大 018 → 使用 019”，并称 `en/`、`zh-Hant/`“待创建”；同时让贡献者自行取“最大 ID + 1”，并发 PR 会产生 ID 冲突。 | 更新过时示例；由维护者/合并机器人在接受时分配 ID，或使用临时 slug/UUID，避免贡献者抢占连续编号。 |
| D3-4 | MODERATE | CI 的外链检查对 GitHub、arXiv 主动跳过，超时或 DNS 异常也记为 skipped；工作流中外链步骤仅 advisory。当前新条目的关键证据大多位于 GitHub，因此“链接检查通过”并不代表关键证据可访问。 | 区分 `verified / skipped-by-policy / transient-failure / broken`；对证据字段中的 GitHub 固定 commit/blob URL 至少做 HTTP 与路径存在性检查，并为关键一手证据设置阻断阈值。 |
| D3-5 | MODERATE | `validate_ci.py` 当前验证 Schema、条目数和 `stats.by_domain`，但不验证 `stats.by_category`、README 数字与表格、Markdown/JSON 语义镜像，也不检查 v2 第三方证据要求。 | 增加 registry 双向统计、三语表格生成/比对、模板版本检查和结构化镜像字段校验；将第三方条目的 commit、访问日期、证据定位设为条件必填。 |

**补充核验**：`docs/index.html` 的 `DOMAIN_LABELS` 12 个 key 与 Schema 的 domain enum 完全一致；`CLAUDE.md` 对下划线前缀目录的说明与 `_reviews/` 的存在不冲突。

## D4: New Entry Quality

**评分**：1.5/5

| # | 严重度 | 描述 | 修复建议 |
|---|---|---|---|
| D4-1 | MAJOR | **NRR-2026-020 的中心方法错引一手框架 taxonomy。** 条目把 §9.6 写成“[S] 自述 → [E] 试行 → [I] 审查门禁 → [F] 证伪”，并据此设定 [E] 门槛；实际 §9.6 是 [S] Source-verified、[E] External-verified、[I] Inferred、[J] Expert judgment、[Sp] Speculative，根本没有 [F] 等级，[E] 也不是“试行级”。因此结论虽与源文档把相关资产标为 [Sp] 的现状相符，论证路径却建立在错误分类上。 | 按原框架五级重写方法与 expected result；把“源文档当前标注为 [Sp]”和“审查者认为证据应归为何级”分开。B1 的 2/4→4/4 应拆成 [S] 可核事实与 [I]/[Sp] 解释，不应发明 [E]/[F] 门槛。 |
| D4-2 | MAJOR | **NRR-2026-019 的 `fully-reproducible` 评级证据不足。** 条目没有固定 GitNexus 版本、索引快照、精确命令、手工调用清单、docx-pipeline commit 或直接证据文件 URL；链接只到仓库首页，notes 又称原始数据位于项目 memory 文件。第三方无法仅凭登记条目复现 3/81+ 与 0/17。 | 降级为 partially-reproducible，或补齐工具版本、两个仓库 commit、索引与查询命令、纳入/排除清单、逐条标注结果及固定 blob 链接。 |
| D4-3 | MAJOR | **NRR-2026-021 从 3 个目的性梯度样本外推“绝大多数开源项目”。** 自有项目群、有论文项目、纯代码项目并非随机或代表性样本；自有项目还受作者熟悉度与选择偏差影响。数据最多说明这三个案例中的提取率梯度，不能支持“适用对象极端狭窄”“开源生态满足率极低”等总体结论。 | 将结论限缩为案例研究；预注册更大、分层抽样的独立项目集，盲化分析者对项目归属，并报告置信区间、失败模式和反例。 |
| D4-4 | MAJOR | 四条 P2 第三方分析条目整体未落实 v2 的关键证据契约：普遍缺 source commit/version、访问日期、明确纳入范围、可定位的一手证据和可执行复核步骤，事实、观察与推断也未稳定分层。这使“第三方分析”更像维护者判断摘要，而非可独立审计的登记记录。 | 将 v2 设为唯一入口并对第三方条目强制字段化；为 019–022 逐条补录来源快照、证据表、核查命令和推断标签后重新审查 reproducibility。 |
| D4-5 | MODERATE | NRR-2026-019 的“3/81+”明确表示分母尚未穷尽，只能推出“至少检查 81 个调用、覆盖率至多约 3.7%”，不是精确捕获率。条目还在无对照数据时排除“GitNexus bug”，并声称 IMPORT/EXTENDS、跨模块关系更可靠。 | 使用上下界措辞，公开完整计数规则；把原因排除和其他边类型可靠性改为待验证假设，或补充同版本、同仓库的对照统计。 |
| D4-6 | MODERATE | NRR-2026-021 的证据卡可复算 37.5%=3/8、约 69%=5.5/8，因此 69% 不是算术错误；但条目未披露“部分可提取计 0.5”的规则，也把第一梯度的多个自有项目群概括成“3 个项目”之一，样本单位不一致。 | 在条目中明确 0/0.5/1 评分规则、逐组件分数和四舍五入口径；把 sample size 改为准确的项目/项目群层级，并单独报告每个项目。 |
| D4-7 | MODERATE | NRR-2026-022 的“源项目方法论文档=0”经本地 git 历史核查具有可支持性：上游快照 `5b9d40a` 根目录无 README、CLAUDE 或分析报告；相关文档由 fork 后续提交加入。但登记条目没有固定该 SHA/访问日期，没有定义“方法论文档”是否排除源码注释、commit message、IDE 配置或外部论文，也未给 fork/diff URL。 | 在条目中固定 upstream SHA 和 fork SHA，给 compare/blob 链接，列明搜索路径、文件类型与排除规则；将结论限定为“该快照内未发现符合所定义范围的独立方法论文档”。 |
| D4-8 | MODERATE | 抽查显示 Markdown 与 JSON 的大意一致，但不是严格语义镜像：019 的 JSON 保留更多调用链、机制推测与限制；021 的 Markdown lessons 省略中间 69%；022 两种格式都缺可直接复核的 fork 定位。 | 定义单一源格式并自动生成另一格式，或在 CI 中逐字段比对 hypothesis、method、results、lessons、limitations、links 与 reproducibility。 |

**专项核验结论**：

- 019–022 的 `submitted_by` 均为 `Acerolaorion`，四条 `reproducibility.notes` 均明确含“第三方分析条目”。
- 四条 JSON 均通过现有 Schema 校验。
- NRR-2026-020 是 22 条中最弱条目：它不仅由 N=1 项目推断“固有信息密度天花板”并排除“分析深度不足”，还错误引用决定其结论等级的证据 taxonomy。NRR-2026-021 次之，主要问题是总体外推而非 69% 算术。

## D5: Adversarial Fresh-Eyes

**评分**：2.5/5

| # | 严重度 | 描述 | 修复建议 |
|---|---|---|---|
| D5-1 | MAJOR | “第三方分析条目”“社区登记册”等表述容易让新读者理解为已有独立社区贡献；实际上 22/22 的 `submitted_by` 都是 Acerolaorion。源项目作者、分析者、条目提交者与登记册维护者四种角色没有被清晰区分，来源多样性因此可能被误读为提交者独立性。 | 在首页展示“22 条记录 / 1 名提交者 / X 个源项目或项目群”，为 source author、analyst、submitter、reviewer 分设字段；达到预先定义的独立贡献门槛后再使用“社区登记册”。 |
| D5-2 | MODERATE | README 已坦诚这是维护者个人失败日志的原型，这是重要校准；但标题和前置定位仍使用“对抗文件抽屉问题”“公开/社区登记系统”等宏大表述，容易先形成超出 22 条单一提交者数据所能支持的印象。 | 将当前阶段称为“公开原型、案例库或维护者登记册”；公开社区化里程碑，如独立提交者数、独立复核率、治理与争议处理机制。 |
| D5-3 | MAJOR | 真正提交一条结果时仍缺稳定契约：ID 由谁分配、并发 PR 如何处理、v1/v2 哪个权威、Markdown 如何生成 JSON、最低证据与拒绝标准、审核时限、事实纠错、版本更新、撤回/争议、署名与隐私规则均不清楚。 | 在 CONTRIBUTING 建立一条端到端“首次提交路径”，提供示例 PR 和一键本地校验；写明 ID 分配、证据门槛、审核 SLA、纠错/撤回和第三方分析授权规则。 |
| D5-4 | MODERATE | “可检索”能力边界不清。当前已有 JSON 和 Pages 客户端过滤，适合结构化筛选；但没有清晰说明是否支持全文搜索、稳定查询 URL、API、导出或字段组合查询。 | 改称“机器可读、可按字段筛选”，并列出实际支持的查询能力；若保留“可检索”，提供搜索语法、永久链接和 API/导出说明。 |

**30 秒新读者判断**：可以大致理解为“用结构化 Markdown/JSON 记录 AI 协作中的失败、零结果与方法失效的公开原型”；但第一屏 18/22 冲突和“社区/第三方”角色混淆会立即削弱信任。

**最令人困惑之处**：同一维护者提交的外部项目分析被称为“第三方分析条目”。这里的“第三方”究竟相对于源项目、分析方法还是登记册维护者并不明确。

**实际提交前最需要补充的信息**：唯一模板与单一事实源、ID 分配策略、source commit/version/access date、纳入范围、一手证据定位、复核步骤、阴性结果边界、拒绝标准、审核时限、纠错/撤回/争议机制，以及外部贡献者署名与隐私政策。

---

## 终判

**判决**：MAJOR  
**理由**：项目已完成 22 条目、三语、Schema、registry、Pages 与 CI 的主体建设，但仍有影响可信度的实质问题：README 关键数字冲突，v2 证据规范未接入提交流程，新增条目存在证据分类错引、可复现性评级过强和由小样本外推生态结论。问题可修复且不阻断读取，故判为 MAJOR。

## 发现汇总

| CRITICAL | MAJOR | MODERATE | MINOR |
|---:|---:|---:|---:|
| 0 | 10 | 9 | 2 |