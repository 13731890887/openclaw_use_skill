# OpenClaw 抖音自动化 Skill（openclaw_use_skill）

## 人类请看

1. 先把 skill 放到你的 OpenClaw 工作区：

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -R skills/douyin-automation ~/.openclaw/workspace/skills/
```

2. 登录抖音创作者后台（`creator.douyin.com`）。
3. 把本仓库链接发给你的 OpenClaw。
4. 建议直接让智能体执行（更稳定，不易漏步骤）。

---

## 智能体请看

### 先安装 skill

1) 确认本地存在目录：`~/.openclaw/workspace/skills/douyin-automation`  
2) 若不存在，执行：

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -R skills/douyin-automation ~/.openclaw/workspace/skills/
```

3) 重新加载会话后，读取：`skills/douyin-automation/SKILL.md`

### 再执行发布

执行抖音图文发布时，必须按以下顺序：

1) 填标题、摘要  
2) 填正文（不少于100字）  
3) AI配图并确认封面  
4) 选择音乐：先悬停歌曲行，再点击右侧“使用”  
5) 确认主表单显示曲名，按钮变为“修改音乐”  
6) 点击发布  
7) 去内容管理页核验是否入库（已发布/审核中）

若失败：记录失败原因并重试，不得跳过核验。

---

## 建议

**建议交给智能体执行**，因为它更不容易漏掉关键步骤（尤其是音乐选择和发布后核验）。
