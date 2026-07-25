# 独立审查报告：AI协作阴性结果登记册

**审查者**：GPT-5.6-Sol (via Codex CLI)
**审查日期**：2026-07-25
**实现者**：DeepSeek-V4-Pro (via Claude Code CLI)
**项目版本**：v0.1.0-dev

> **审查基线**：以审查时磁盘中的项目文件为主，同时核对提示词内联快照。机械检查结果：4/4 条目在启用 JSON Schema Draft 2020-12 `FormatChecker` 后均通过 `entry.schema.json`；当前磁盘版 `registry.json` 的 `total_entries`、条目副本及全部 stats 与源条目一致。

---

## D1: Schema Compliance & Data Integrity
**评分**：3/5

### 发现

| # | 严重度 | 描述 | 修复建议 |
|---|--------|------|---------|
| 1 | MAJOR | `registry.json` 的 `$schema` 指向“单条目” `entry.schema.json`，因此聚合文件按其自声明 schema 校验会缺少 `id/title/domain/...` 等 11 个必填字段。聚合文件在语义上是自相矛盾的。 | 新建 `schema/registry.schema.json`，定义 metadata、entries、stats，并令 `entries.items` 引用 `entry.schema.json`；或在此之前移除错误的 `$schema`。 |
| 2 | MODERATE | 4 个现有条目虽全部通过，但 schema 的防护不足：根对象及嵌套对象未禁用额外字段；`reproducibility`/`links` 子字段没有 `required`；`lessons_learned` 描述为 1–5 条却没有 `minItems: 1`；数组没有 `uniqueItems`；也不约束 ID 年份与 `date` 年份一致。 | 明确开放/封闭策略；补齐嵌套 `required`、`minItems`、`uniqueItems`，并在脚本层检查 ID、目录名、文件名和年份的一致性。 |
| 3 | MODERATE | NRR-2026-001 的标题写“**两段式**分段”，但括号与方法均为 prep/exec/post **三段式**，这是人读版与机读版共同复制的语义错误。 | 将标题统一改为“三段式分段”，并增加从 JSON 生成/校验 Markdown 镜像字段的检查。 |
| 4 | MODERATE | `CLAUDE.md` 与现状漂移：初始来源仍把 NRR-2026-004 列作候选、BDC 仍列候选，而 `docs/existing-negative-results.md` 已明确收录前者并排除后者；其目录约定还称不存在 `_` 前缀目录，但 `_reviews/` 已存在。另外，CLAUDE 声称每条目 metadata 标注 `generation_model`，schema 与四个 JSON 均无此字段。 | 更新“初始条目来源”和目录树；决定 `_reviews/` 是否发布；在 schema 中正式加入生成/编辑 provenance，或删除无法兑现的约束。 |
| 5 | MODERATE | 审查提示词内联的 `registry.json` 快照把 `Qwen3.7-Max` 计为 1，但四条目及当前磁盘版应为 2（NRR-001、NRR-003）。这说明审查材料不是由权威源自动生成。 | 审查提示词应从已校验的磁盘文件自动嵌入，并记录文件哈希/commit；禁止手抄 stats。 |
| 6 | MINOR | Markdown 与 JSON 的六个指定镜像字段无实质矛盾，但有 5 处非完全一致：NRR-001 的效应量/样本量、NRR-002 的样本量、NRR-003 的样本量、NRR-004 的效应量分别省略或增加限定语。 | 把 JSON 设为唯一事实源，自动渲染基本信息与指标表；至少在 CI 中做规范化后比较。 |

---

## D2: Classification System Audit
**评分**：2/5

### 发现

| # | 严重度 | 描述 | 修复建议 |
|---|--------|------|---------|
| 1 | MAJOR | 12 个领域不是 MECE：`prompt-engineering` 与 `code-review`、`document-generation` 与 `academic-writing`、`workflow-orchestration` 与 `multi-model-collaboration`、`tool-building` 与 `skill-design` 明显重叠；`benchmarking` 又是可横切所有领域的活动。“other”只保证形式上的兜底，不等于穷尽良好。 | 改为分层/多标签：`task_domain`（代码、文档、研究等）+ `intervention`（prompt、tool、workflow、multi-model 等）+ `activity`（benchmark/evaluation）；或明确主领域优先级并允许 `secondary_domains`。 |
| 2 | MAJOR | 9 种类型混合了“观察结果”（null/worse）、“原因诊断”（ceiling/method/tool）与“处置”（abandoned），因此彼此重叠：零结果也可同时是天花板效应或假设被证伪。体系还缺少 `inconclusive-underpowered`、`interrupted/blocked`、`data-unavailable/data-quality`、`environment-or-version-drift`、`cost-or-safety-stop`。 | 拆成三轴：`outcome`、`cause`、`disposition`；至少先加入“不确定/低功效”和“外部中断/数据不可用”，避免把“未检出”登记成“无效”。 |
| 3 | MODERATE | NRR-2026-001 以 `prompt-engineering` 为主领域可以接受，因为干预是 prompt 结构；但任务本身是代码审查，单字段分类会丢失重要检索维度。`null-result` 也只有在等效界值或充分功效成立时才稳妥。 | 主领域保留，增加 `secondary_domains: [code-review]`；在统计结论修订前将 outcome 降级为 `inconclusive-underpowered` 或显式标记“估计接近零但区间宽”。 |
| 4 | MAJOR | NRR-2026-002 的 15-case Tier-0 Pilot 更像“低功效的 futility/no-go 决策”，不是已经证实的 `null-result`；也不应简单改成 `methodology-failure`，因为 Pilot 若有事前停止规则仍可设计正确。 | 新增 `pilot-futility`/`inconclusive-underpowered`，记录事前 go/no-go 阈值、观察计数和不确定区间；只有实验设计或执行失效时才用 `methodology-failure`。 |
| 5 | MODERATE | NRR-2026-003 归为 `methodology-extraction / methodology-failure` 是四条中最稳妥的；NRR-2026-004 的 `tool-unfit-for-purpose` 则过度归责于 mmdc。修复只需补齐工具链契约，说明工具并非“不适用”，更像 `integration-failure` 或管线假设失败。 | 保留 NRR-003；为 NRR-004 新增 `integration-failure`，或暂归 `methodology-failure` 并把“工具不适用”改为“默认互操作假设失败”。 |
| 6 | MODERATE | `models_used` 的 schema 描述允许模型或工具，但字段名、registry stats 名仍暗示只统计模型；前三条只列 LLM，第四条只列工具，语义与查询结果不一致。 | 推荐拆成 `llm_models_used` 与 `tools_used`；若保留混合数组，则统一改名 `systems_used`，并为每项增加 `type/version/provider`。 |

---

## D3: Factual Plausibility & Cross-Reference Integrity
**评分**：2/5

### 发现

| # | 严重度 | 描述 | 修复建议 |
|---|--------|------|---------|
| 1 | MAJOR | NRR-2026-001 把 `d≈0.03, n=24/臂` 叙述为零效应，但这只是点估计接近零。按独立双样本、双侧 α=0.05 粗略估算，n=24/臂检测事前目标 d=0.3 的功效约 17%；d=0.03 的近似 95% 区间约为 [-0.54, 0.60]。即使第二模型同规模复现，也不能替代等效性检验。 | 公布原始统计量、分配方式和每模型结果；做 TOST/等效性或报告置信区间，并预先定义最小实际重要效应。结论改为“未检出差异，数据与较宽效应范围均相容”。 |
| 2 | MAJOR | NRR-2026-002 未给两组准确率、错误计数、配对结构、区间或事前停止规则，却用“差异不显著”和“不值得 Tier 1”作结。15 cases 可支持低成本资源决策，但不能支持效果不存在；“提升 ≥10%”在 15 个案例上也只有约 1–2 个案例的粒度。 | 补齐 2×2/逐案例数据、Pilot 决策规则、成本函数和不确定区间；把“统计结论”与“资源配置决定”分开。 |
| 3 | MAJOR | NRR-2026-002 lessons 第 4 条由 A2+A3 泛化为“prompt 结构变异效应可能整体被高估”。两个任务、设计和样本不同，且两者均低功效；“两个未检出”不能合成为领域级零效应。 | 删除该泛化，或改为“形成待检验的元假设”；只有在预注册、多任务、足够功效的汇总研究后再作总体判断。 |
| 4 | MODERATE | NRR-2026-003 的 `≥3 源` 是复现计数门槛，不应仅因“2/22≈9%”就判定过严；3/22 也只有 13.6%，本身并不强。真正问题是源的独立性、模式定义、编码可靠性与候选生成过程。现有结果只能证明“5 个候选未过预设门”，不能证明“22 太少”或框架具有不可行性。 | 报告每个候选在 0/1/2 个源中的具体分布、源独立性和双人编码一致性；将“不可行性证明”降级为“本次管线未达门槛”。 |
| 5 | MAJOR | NRR-2026-004 的机制叙述存在可核查错误：官方 mermaid-cli 当前 CLI 源码没有 `--dpi` 参数；实际 docx-pipeline 的 `mermaid_renderer.py` 是按配置 DPI 计算像素宽度、调用 mmdc 的 width/scale 参数，再用 Pillow 注入 DPI。且 python-docx 1.2.0 对缺失 DPI 的 PNG 默认按 72 DPI 计算原生尺寸，不是条目声称的 Word 96 DPI，因此 `300/96≈3.125×` 不能作为该 python-docx 管线的已证实根因。 | 保存最小复现包（原始 PNG、pHYs、DOCX、`wp:extent`、截图）；记录 mmdc/python-docx/Word 精确版本与实际 argv；区分“实测倍率”和“理论解释”，在证据确认前撤回“任意版本”“300/96 根因”表述。 |
| 6 | MAJOR | 交叉引用尚不可发布：审查日 `negative-results-registry` GitHub 仓库及两个条目 URL 返回 404；即使仓库上线，`/entries/...` 也不是标准 GitHub 文件路径。三个条目 Markdown 的同仓库相对链接少了 `../`；NRR-004 两个外部相对链接不存在；其 JSON 还用同一个 docx-pipeline 根 URL 表示两个不同标签。 | 发布后使用 `/blob/main/entries/<ID>/<ID>.md` 或正确相对路径；修复 5 个断开的 Markdown 相对链接；把 NRR-004 的“DPI 参考”指向具体文件/commit；CI 增加内部链接和 HTTP 状态检查。 |

---

## D4: Structural Completeness
**评分**：2/5

### 发现

| # | 严重度 | 描述 | 修复建议 |
|---|--------|------|---------|
| 1 | MAJOR | `generate_registry.py` 定义了 `SCHEMA_PATH` 却完全不使用。隔离副本测试中加入一个只含 `id/domain/models_used` 的无效 JSON 后，脚本仍成功生成 5 条 registry，证明“聚合索引来自已校验条目”并未被工具强制执行。 | 在收集阶段用 Draft 2020-12 + format checker 校验；发现任一错误立即非零退出。同步检查 `.md + .json` 双件、目录/文件/ID 一致、ID 唯一、stats 重算一致。 |
| 2 | MAJOR | 对社区型登记册，缺少 `CONTRIBUTING.md`、可复制的校验命令、依赖声明、CI 和 PR 检查。模板只说“按 schema 校验”，没有告诉提交者使用何种工具或命令。 | 增加贡献指南、`requirements`/锁定依赖、`scripts/validate_registry.py`，并配置 CI 执行 schema、链接、重复 ID、Markdown 镜像和 registry 再生成差异检查。 |
| 3 | MAJOR | ID 由“查看当前最大 ID”人工分配，两个并发 PR 可得到同一编号；生成器也不拒绝重复 `id`，目录排序不能解决语义冲突。 | PR 初期允许临时 slug/UUID，由合并者分配顺序号；或用不可冲突 UUID。CI 必须验证全局 ID 唯一并检查年份序列。 |
| 4 | MODERATE | `_reviews/` 未进入 README/CLAUDE 目录约定，且 CLAUDE 明说无 `_` 前缀目录。`project_status.md` 被忽略且 README 不列出本身合理，但应明确它是本地维护文件，不能承担公开 roadmap 的职责。 | 把 `_reviews/` 定义为公开审计材料或加入忽略；另建公开 `ROADMAP.md`/Issues，保留 `project_status.md` 仅作本地执行记录。 |
| 5 | MODERATE | v0.1.0-dev 没有网页搜索尚可接受，`registry.json` 也能被程序过滤；但 README 宣称“按领域/类型/模型可检索”，却无查询示例、稳定 API、结构化 related-entry 字段或索引页面。 | 至少提供 jq/Python 查询示例和 `related_entry_ids`；后续再做静态搜索页。发布前把“可检索”限定为“可机器查询”，避免暗示已有界面。 |

---

## D5: Adversarial Challenge
**评分**：2/5

### 发现

| # | 严重度 | 描述 | 修复建议 |
|---|--------|------|---------|
| 1 | MAJOR | 只有 4 条、同一提交者、同一生态的结果，尚不能证明项目已经“对抗文件抽屉问题”；它目前更像维护者个人失败日志的结构化原型。若没有外部征集、纳入规则和长期保存机制，确有成为“新抽屉”的风险。 | 将措辞降级为“旨在/尝试对抗”；公布纳入/排除流程、治理与维护承诺；至少引入若干独立提交者和不同任务域后再作社区级声称。 |
| 2 | MAJOR | 多个“失败条件”是事后解释而非事前死亡判据：NRR-001 的“任务类型决定效应量上限”、NRR-003 的“n=22 太小/门槛太严”都没有在条目中给出预注册证据。它们可作为假说，但不能冒充实验已经验证的因果解释。 | schema 增加 `preregistered`, `decision_rule`, `analysis_plan`, `alternative_explanations`, `evidence_for_interpretation`；明确区分 observation、inference、speculation。 |
| 3 | MAJOR | NRR-001/002 的 `fully-reproducible` 夸大：复现依赖可变的托管模型别名、服务端实现、CLI、评审模型和可能未固定的温度/种子。可重跑代码不等于可复现同一结果。 | 改为 `partially-reproducible`，除非归档精确模型快照；记录 provider model ID、日期、参数、commit、环境锁文件、原始输出和评审协议，并区分 repeatable/reproducible/replicable。 |
| 4 | MODERATE | `submitted_by` 对当前单作者原型可作为显示署名，但不足以保证 CC BY 4.0 的完整 provenance：没有“权利持有人/希望显示的署名/来源作品/修改说明/AI 辅助范围/许可确认”。“版权归提交者所有”也可能忽略共同作者或上游材料。 | 增加贡献者许可声明及 provenance 字段；要求提交者确认有权授权，分别记录人类作者、操作者、AI 辅助和来源项目，保留修改历史。 |
| 5 | MAJOR | **最弱条目是 NRR-2026-004。** 它的实验没有出现 LLM，`models_used` 只有 mmdc、python-docx、Word，与 README 明确排除“不涉及 AI 协作的纯技术 bug”相冲突；分类过度归责工具，DPI 根因又存在事实疑点，且“所有文档/任意版本”是无证据的全称断言。 | 在发布前移出登记册，或补充明确的 AI 协作研究问题、版本化最小复现与实测证据，并把类别改为 integration/methodology failure；删除全称断言。 |

---

## 终判

**判决**：MAJOR
**理由**：四个条目在当前磁盘上均通过 entry schema，聚合计数也正确；但 registry 自声明了错误 schema，生成流程不执行校验，分类轴非 MECE，两个统计结论明显过度，NRR-004 的 DPI 机制与项目范围均存在实质疑点，且多处链接失效。项目适合作为内部原型，完成统计降级、事实复核、验证/贡献流程和链接修复前不宜公开发布。

---

## 发现汇总

| 严重度 | 数量 |
|--------|------|
| CRITICAL | 0 |
| MAJOR | 16 |
| MODERATE | 11 |
| MINOR | 1 |