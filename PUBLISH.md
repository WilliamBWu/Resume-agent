# 发布到 GitHub

本目录 `opensource-kit/` 是**可公开**的独立模板，与上层私有经历库分离。请从本目录单独建仓库推送，**不要**把上层含真实简历的仓库直接设为 Public。

## 一次性发布

```bash
cd opensource-kit
git init
git add .
git status   # 确认没有真实姓名、手机、成绩单图片
git commit -m "Initial commit: open-source resume agent template"
```

在 GitHub 新建空仓库（例如 `resume-agent`），然后：

```bash
git branch -M main
git remote add origin https://github.com/<你的用户名>/resume-agent.git
git push -u origin main
```

或使用 GitHub CLI：

```bash
gh repo create resume-agent --public --source=. --remote=origin --push \
  --description "Cursor rules + master/versions workflow for tailored resumes"
```

## 发布前自检

- [ ] `git grep` 无真实姓名、手机、个人邮箱、学校证件照路径
- [ ] `data/master` 仅为演示人物或已清空待用户填写
- [ ] LICENSE / README 齐全
- [ ] `python scripts/validate_master.py` 通过

## 与私有库的关系

| 仓库 | 内容 |
|------|------|
| Public（本 kit） | rules、SCHEMA、演示数据、文档 |
| Private（上层目录） | 你的真实 master、versions、inbox、照片 |
