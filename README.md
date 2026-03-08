# OpenClaw 抖音自动化 Skill（openclaw_use_skill）

这个仓库用于分享可复用的 OpenClaw 技能，让其他开发者把同样的抖音自动化流程快速迁移到自己的智能体。

## 核心目标

让你的 OpenClaw 学会：

- 抖音创作者后台图文发布
- AI 配图 + 封面同步
- 配乐选择（悬停歌曲行 → 点击“使用”）
- 发布后在内容管理页做入库核验
- 评论区自动回复（v2：意图识别 + 安全护栏）

## Skill 位置

- 主技能目录：`skills/douyin-automation/`
- 对外分发套件（可选）：`openclaw-douyin-skill-kit/skills/douyin-automation/`

## 如何给你的 OpenClaw 安装

把仓库中的 skill 复制到你自己的 OpenClaw 工作区：

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -R skills/douyin-automation ~/.openclaw/workspace/skills/
```

然后重启/刷新 OpenClaw 会话。

## 给开发者的使用说明（可直接转发）

把这个仓库链接发给开发者，让他们对自己的 OpenClaw 说：

- “请使用 `douyin-automation` skill 执行抖音图文自动发布流程。”
- “发文前先选音乐，按悬停歌曲行后点击使用的规则执行。”
- “发布后去内容管理页核验是否入库。”

## 已验证关键规则

1. 正文建议 **≥100字**，否则可能出现“点击发布但未入库”。
2. 配乐必须按可见交互：**悬停歌曲行 → 点击右侧“使用”**。
3. 配乐成功判定：主表单出现曲名且按钮变为 **“修改音乐”**。
4. 发布成功判定：内容管理页能看到新作品（已发布/审核中）。

## 免责声明

请遵守抖音平台规则与当地法律，控制自动化频率，优先人工监督与低风险操作。