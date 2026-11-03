# Resume Agent（简历 Agent）

基于 [Cursor](https://cursor.com) 的**个人经历库 + 规则驱动 Agent**：把材料放进 `inbox/`，合并进 `data/master/`，再按 JD 生成可丢弃的岗位版到 `data/versions/`。

本仓库是**开源模板**（含虚构演示数据）。请勿把真实手机号、成绩单、证件照推到公开仓库。

## 特性

- **真相源 / 岗位版分离**：master 只增不因某次投递被污染；versions 可随时重生成
- **Cursor Rules**：入库、合并、岗位适配、一页撑满、教育选课、STAR 隐写等约定开箱即用
- **Skills 复用**：Word / PDF / 岗位裁剪等走现成 skills，不重复造轮子
- **可校验**：`scripts/validate_master.py` 检查 master 结构

## 快速开始

### 1. 用 Cursor 打开本仓库

### 2. 安装 Skills（本机一次）

```bash
npx skills add https://github.com/anthropics/skills --skill docx -y
npx skills add https://github.com/anthropics/skills --skill pdf -y
npx skills add https://github.com/ComposioHQ/awesome-claude-skills --skill tailored-resume-generator -y
```

可选：

```bash
npx skills add https://github.com/paramchoudhary/resumeskills --skill job-description-analyzer -y
npx skills add https://github.com/paramchoudhary/resumeskills --skill resume-ats-optimizer -y
npx skills add https://github.com/claude-office-skills/skills --skill smart-ocr -y
```

### 3. 换成你自己的材料

1. 删除或改写 `data/master/` 里的演示人物「张示例」
2. 把简历 Word/PDF、项目说明放进 `inbox/`
3. 在 Cursor 对话中说：`请入库并合并到 master`
4. 贴上 JD，说：`请生成岗位版到 data/versions 并导出 Word 与 PDF`

演示 JD 见 [`examples/sample-jd.md`](examples/sample-jd.md)；演示岗位版见 `data/versions/demo-ops-intern-2026/`。

### 4. 校验

```bash
pip install -r requirements-dev.txt
python -m pytest -v
python scripts/validate_master.py
```

## 目录

```text
├── inbox/                 # 原材料（默认 gitignore，勿提交隐私）
├── data/
│   ├── master/            # 真相源（演示数据可改成你的；公开 fork 请脱敏）
│   └── versions/          # 岗位版（可丢弃重生成）
├── examples/              # 示例 JD
├── .cursor/rules/         # Agent 行为规则
├── scripts/validate_master.py
└── docs/                  # 设计规格摘要
```

## 隐私与安全

- **不要**把真实 `profile`、成绩单、证件照、已投递简历推到 Public 仓库
- 建议：Public = 本模板；Private fork = 你的真实经历库
- 导出的 `.docx` / `.pdf` 默认被 `.gitignore` 忽略（除演示目录策略外，请按需调整）

## 规则要点（摘要）

默认岗位版顺序：**教育 → 实习 → 项目 → 校园 → 个人亮点与技能**。课程按 JD 从成绩表选列；&lt;90 不标分，≥90 可标可不标。项目用粗体简介贴 JD + 隐式 STAR 叙述。详见 `.cursor/rules/resume-tailor.mdc`。

## 第三方 Skills 许可

本项目规则引用的 skills 来自各自上游仓库，使用前请遵守其 License（如 Anthropic skills、Composio awesome-claude-skills 等）。

## License

MIT — 见 [LICENSE](LICENSE)。
