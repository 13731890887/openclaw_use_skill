# OpenClaw 抖音自动化 Skill（openclaw_use_skill）

## 全自动模式（完全信任智能体）

你可以让智能体自己完成：安装 skill → 学习规则 → 执行发布。

把下面这段直接发给智能体：

```text
你被完全授权：请自行安装并使用本仓库的 Douyin skill。
步骤：
1) 克隆仓库 https://github.com/13731890887/openclaw_use_skill.git
2) 将 skills/douyin-automation 复制到 ~/.openclaw/workspace/skills/
3) 读取 ~/.openclaw/workspace/skills/douyin-automation/SKILL.md
4) 按 skill 执行抖音图文发布流程并回报结果
硬性规则：
- 正文 >= 100字
- 音乐必须“悬停歌曲行后点击使用”
- 发布后必须到内容管理页核验是否入库（已发布/审核中）
失败时：记录原因并重试，不得跳过核验。
```

---

## 智能体执行标准

执行顺序固定：
1) 标题
2) 摘要
3) 正文（>=100字）
4) AI配图并确认封面
5) 选择音乐（悬停行 → 使用）
6) 确认“修改音乐”
7) 发布
8) 内容管理页核验

---

## 备注

本仓库默认按“智能体可自安装、自学习、自执行”设计。