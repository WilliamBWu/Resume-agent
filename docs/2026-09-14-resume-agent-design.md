# 简历 Agent 设计规格（方案 A）

**日期：** 2026-09-14  
**状态：** 已批准（2026-09-14）  
**范围：** Cursor 仓库内的「经历库 + 规则驱动 Agent」；交互形态与最终视觉版式后议。

---

## 1. 目标与非目标

### 1.1 目标

1. **动态更新经历：** 用户提供 Word、PDF、图片或项目相关文件，以及对话中的增量信息，合并进统一真相源。
2. **岗位适配：** 根据不同 JD，从真相源生成可丢弃、可再生的岗位版简历。
3. **多模态入库：** 支持 Word（.docx）、PDF、图片及常见项目说明类文件的抽取与归类。

### 1.2 非目标（本规格不覆盖）

- 具体聊天指令集、UI/预览方式、一键导出交互（后议）。
- 独立 Web 产品或后端服务。
- 自研简历领域 skill（优先复用现成 skills + 项目规则）。

---

## 2. 架构与仓库结构

### 2.1 总体形态

在 Cursor 仓库中维护个人经历库；Agent 依据 `.cursor/rules` 完成入库、合并与岗位适配。文档读写依赖已安装/可安装的现成 skills。

### 2.2 目录约定

```text
简历Agent/
├── inbox/                       # 原材料投放区
│   └── processed/YYYY-MM-DD/    # 已处理归档
├── data/
│   ├── master/                  # 真相源（Markdown）
│   │   ├── profile.md           # 基本信息、教育、技能总览
│   │   ├── experience.md        # 工作/实习经历
│   │   ├── projects.md          # 项目经历（或拆为 projects/<name>.md）
│   │   └── CHANGELOG.md         # 轻量变更摘要
│   └── versions/                # 岗位适配产物
│       └── <slug>/              # 如 bytedance-backend-2026/
├── templates/                   # 简历骨架（版式后议时再定）
├── docs/superpowers/specs/      # 本设计与后续规格
└── .cursor/rules/               # Agent 行为约定
```

### 2.3 真相源格式

- **主格式：Markdown。**
- 需要机器可解析的字段时，使用文件头 YAML（如 `role`、`period`、`tech`、`company`）。
- 不单独维护平行 JSON 库；若日后升级方案 C，再从 master 导出结构即可。

### 2.4 技能分工

| 环节 | Skill / 能力 | 说明 |
|------|----------------|------|
| Word 读/写 | `anthropics/skills@docx` | 抽取与（后议）导出 |
| PDF 读/写 | `anthropics/skills@pdf` | 含扫描件 OCR 路径 |
| 图片/难认扫描件 | Cursor 原生多模态；可选 `claude-office-skills@smart-ocr` | 中文扫描件兜底 |
| 岗位适配 | `composiohq/...@tailored-resume-generator` 或 `paramchoudhary/resumeskills@resume-tailor` | 二选一或按任务选用 |
| JD 分析（可选） | `paramchoudhary/resumeskills@job-description-analyzer` | 适配前分析 |
| ATS 检查（可选） | `paramchoudhary/resumeskills@resume-ats-optimizer` | 关键词与结构检查 |
| 多版本思路 | `paramchoudhary/resumeskills@resume-version-manager` + `data/versions/` | 落盘以本仓库为准 |
| 行为约束 | `.cursor/rules/` | 入库、合并、适配护栏；不写领域 skill |

---

## 3. 入库与动态更新

### 3.1 入库流程

1. **识别来源**
   - `.docx` → docx skill 抽文本
   - `.pdf` → pdf skill（扫描件走 OCR）
   - 图片 → Cursor 读图；效果差时可选 smart-ocr
   - 项目文件（README、设计说明、代码注释、截图说明等）→ 抽取「做了什么 / 技术栈 / 结果」，不整份粘贴进简历

2. **结构化归类**
   - 基本信息 / 教育 / 技能 → `profile.md`
   - 工作 / 实习 → `experience.md`
   - 项目 → `projects.md` 或 `projects/<name>.md`

3. **原料归档**  
   处理完成后移至 `inbox/processed/YYYY-MM-DD/`，保持 `inbox/` 与 `data/master/` 职责清晰。

### 3.2 合并与冲突策略

| 情况 | 处理 |
|------|------|
| 同一段经历（公司/项目名 + 时间重叠） | 以用户**最新提供**的材料为准；替换或更新表述，并在 CHANGELOG 记一句 |
| 补充细节（指标、技术点、职责） | 合并进同一条目，不另开重复条 |
| 不确定是否同一条 | 标 `待确认`，先问用户再写入 |
| 未出现过的业绩/职位/公司 | **禁止编造** |

### 3.3 更新入口

| 入口 | 行为 |
|------|------|
| 材料入库 | 投放 Word/项目文件 → 抽取 → 合并 master |
| 对话增量 | 用户口述补充 → 只改对应条目 |

两入口均写回同一真相源。**岗位版不得当作真相源直接修改。**

### 3.4 变更可追溯

- 每次合并在 `data/master/CHANGELOG.md` 增加一行：日期、来源（文件名或对话摘要）、改动条目。
- 细粒度 diff 依赖 git。

---

## 4. 岗位适配与产物边界

### 4.1 层级边界

| 层级 | 路径 | 角色 |
|------|------|------|
| 真相源 | `data/master/` | 只反映真实经历；仅入库与对话增量可改 |
| 岗位版 | `data/versions/<slug>/` | 裁剪、重排、措辞适配；可丢弃后重生成 |
| 模板 | `templates/` | 版式骨架；适配逻辑不绑定单一导出格式 |

**硬规则：** 岗位适配禁止回写 master。发现缺口时输出缺口清单并询问用户，不编造补齐。

### 4.2 适配流水线

1. 输入：JD 文本或摘要 +（可选）侧重点  
2. 分析：抽取关键词、必备/加分项、职责重心  
3. 改写：从 master 选条、调序、调整强调与关键词密度  
4. 落盘：`data/versions/<slug>/`（至少一份 Markdown；DOCX/PDF 导出后议）  
5. 可选：ATS 检查；维护 versions 清单便于对照

### 4.3 改写护栏

- 只重组与重写，不虚构；事实须在 master 有依据。
- 按岗裁剪：弱相关可缩短或下沉。
- 同一事实可在岗位版换表述；master 保持中性完整表述。
- JD 要求但 master 缺失的内容 → 显式「缺口清单」。

---

## 5. 错误处理与质量约定

- 无法解析的文件：保留在 inbox，记录失败原因，不部分写入可疑内容。
- 合并歧义：停下来问用户，不静默猜测。
- 适配缺信息：列缺口，不生成虚假条目。
- 导出格式失败（后议实现时）：保留 Markdown 岗位版作为底稿。

---

## 6. 测试要点（实现阶段）

- 用一份样例 `.docx` 走通：inbox → master 对应段落有内容、CHANGELOG 有记录、原料已归档。
- 对同一项目投递「补充材料」：应合并而非重复两条。
- 故意冲突的两份表述：以较新材料为准，并有 CHANGELOG。
- 给定 JD 生成 versions：master 未被改写；岗位版可指出缺口。
- 图片/扫描件至少一条路径可抽出可读文本（原生或 OCR）。

---

## 7. 已决议与待后议

### 已决议

- 采用方案 A（资料库 + Cursor Agent）。
- 真相源为 Markdown（可选 YAML frontmatter）。
- 用户原材料以 Word 与项目文件为主；其余格式按上表处理。
- 不自写简历领域 skill；用现成 skills + `.cursor/rules`。
- 默认岗位适配 skill：`composiohq/awesome-claude-skills@tailored-resume-generator`。

### 待后议

- 具体交互流程与指令命名。
- 简历视觉版式与 templates 内容。
- 默认导出格式（仅 MD / 同时 DOCX·PDF）及命名规范细节。

---

## 8. 后续步骤

用户审阅并批准本规格后：

1. 使用 writing-plans 输出实现计划。  
2. 搭建目录与规则、安装约定 skills、跑通入库与适配最小闭环。
