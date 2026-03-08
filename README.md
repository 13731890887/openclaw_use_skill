# OpenClaw 抖音自动化 Skill（openclaw_use_skill）

## 人类请看（开发者操作）

### 1) 安装 skill（这一步由人来做，不是智能体）

先 clone 仓库，再把 skill 放到 OpenClaw 工作区：

```bash
git clone https://github.com/13731890887/openclaw_use_skill.git
cd openclaw_use_skill
mkdir -p ~/.openclaw/workspace/skills
cp -R skills/douyin-automation ~/.openclaw/workspace/skills/
```

### 2) 准备环境

- 登录抖音创作者后台：`https://creator.douyin.com`
- 允许必要的人工介入（验证码/风控）

### 3) 把下面这段话发给你的智能体

```text
请使用 skills/douyin-automation/SKILL.md 执行抖音图文发布。
严格顺序：标题→摘要→正文(>=100字)→AI配图→选音乐(悬停歌曲行后点“使用”)→确认“修改音乐”→发布→内容管理页核验。
若失败，记录原因并重试，不得跳过核验。
```

---

## 智能体请看（只负责执行，不负责安装）

你应当假设 skill 已由开发者安装完成。你需要做的是按 `skills/douyin-automation/SKILL.md` 执行流程：

1) 填标题、摘要  
2) 填正文（不少于100字）  
3) AI配图并确认封面  
4) 选择音乐：先悬停歌曲行，再点击右侧“使用”  
5) 确认主表单显示曲名，按钮变为“修改音乐”  
6) 点击发布  
7) 去内容管理页核验是否入库（已发布/审核中）

失败处理：记录失败原因、重试、回报结果。

---

## 建议

**建议交给智能体执行具体发布动作**，因为它更不容易漏掉关键步骤（尤其是音乐选择和发布后核验）。