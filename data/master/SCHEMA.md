# Master 条目约定

## 文档级 frontmatter

每个 `profile.md` / `experience.md` / `projects.md` 文件顶部：

```yaml
schema_version: 1
updated: YYYY-MM-DD
```

## 条目块格式

在 `experience.md` / `projects.md` 中，每条经历是一个 `##` 标题，标题后紧跟一个 `yaml` 围栏作为元数据，再跟 bullet 正文。

### 工作/实习（experience）

```markdown
## 示例公司 · 后端实习生

```yaml
id: exp-example-corp-2024
type: internship   # work | internship
title: 后端实习生
company: 示例公司
period: 2024-06 ~ 2024-09
tech: [Go, MySQL]
status: active     # active | pending_confirm
```

- 职责或成果 1（须有材料依据）
- 职责或成果 2
```

### 项目（projects）

```markdown
## 简历解析工具

```yaml
id: proj-resume-parser
type: project
name: 简历解析工具
title: 个人项目
period: 2025-01 ~ 2025-03
tech: [Python, FastAPI]
status: active
```

- 做了什么
- 结果/指标（无依据则不写数字）
```

## id 规则

- 小写 kebab-case
- 经历：`exp-<company-slug>-<yyyy>`
- 项目：`proj-<name-slug>`
- 同一实体更新时 **保持 id 不变**

## 教育课程与成绩（profile）

在对应学历条目下维护可选课程库，供岗位版按 JD 选列：

```markdown
### 课程与成绩

| 课程 | 成绩 | 备注 |
|------|------|------|
| Python 程序设计 | 92 | |
| 财务管理 | 88 | |
```

- 岗位版「教育背景」：荣誉一行、课程一行；按 JD 从本表灵活选课（勿写死固定课单）
- **<90 不标分**；**≥90 可标可不标**（按 JD/版面）；无成绩材料不编造分数

## 禁止

- 无材料依据的量化指标
- 把岗位版措辞回写进 master
- 静默合并不确定是否同一实体的条目（应设 `status: pending_confirm` 并询问用户）
