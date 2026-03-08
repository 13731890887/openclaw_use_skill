---
name: douyin-automation
description: Use browser automation (Selenium/Playwright/OpenClaw browser) to operate a Douyin creator account with human-like delays, persistent Chrome profile login, article publishing, and comment replies. Trigger when asked to post Douyin content, maintain daily operations, or iteratively improve a reusable Douyin automation skill.
---

# Douyin Automation

## Runbook

1. Preferred: use OpenClaw `browser` tool on `https://creator.douyin.com` for reliable UI automation in-session.
2. Fallback: run `python3 run_day0_ops.py` (Selenium) or `python3 douyin_playwright.py` when local script execution is needed.
3. If login/captcha appears, complete it manually once (QR/SMS/slide), then continue automation.
4. Before publishing, prepare a background image pool (topic-matched, clean composition, portrait/cover-friendly).
5. Publish article first, then run comment-reply pass from creator comment-management.
6. After each run, append selector changes / failures / successful patterns into this skill.

## Files

- `douyin_bot.py`: Selenium bot (login, publish, reply)
- `config.py`: credentials/env, URLs, Day0 content, templates
- `run_day0_ops.py`: one-click Day 0 operation

## Environment

- Required: `DOUYIN_PHONE`, `DOUYIN_PASSWORD`
- Optional: `DOUYIN_CHROME_PROFILE` (persistent Chrome profile path)

## Lessons Learned

- Prefer creator backend URLs (`creator.douyin.com`) over frontend dynamic pages for stability.
- Keep a persistent Chrome profile to reduce repeated login/captcha friction.
- Use conservative operation frequency and randomized delays to lower risk.
- Expect selector drift; keep multiple fallback selectors per action.
- On this host (Chrome 145), Selenium may throw `WebDriverException: Service Unavailable`; keep Playwright/OpenClaw browser automation as primary fallback.
- For article publishing, `AI生成/AI换图` can auto-create head image and sync cover when local file upload is constrained.
- **Preflight checklist before publish**: 标题已填 → 摘要已填 → 正文已填 → 头图/封面可预览 → 配乐已选（页面显示曲名）→ 再点击发布。
- In this UI, `type` is more reliable than bulk `fill` for title/summary. Opening music modal may reset unsaved-looking fields, so verify again after closing modal.

## Comment Auto-Reply (v2)

1. Navigate to `https://creator.douyin.com/creator-micro/interaction/comment-management`.
2. Scan latest comments, skip empty/duplicate comments in the same run.
3. Classify comment intent and generate safe replies (8-40字):
   - 提问类：给后续步骤承诺，不编造外链
   - 支持类：感谢 + 持续更新承诺
   - 质疑类：礼貌澄清，避免争执升级
4. Use `reply_comments_in_creator_v2(max_replies=20, min_delay=3, max_delay=12)`.
5. Risk guardrails:
   - 不引导加私信/微信
   - 不发送营销导流话术
   - 命中敏感/安全关键词（密码、验证码、联系方式、密钥、越狱/绕过等）直接跳过不回复
   - 每轮最多回复20条，间隔随机
6. Log summary: replied count + skipped reasons + failed UI operations.

## Speed Optimization SOP (v2)

- 固定路径：直接从作品管理页进入"发布文章"页，减少首页跳转。
- 固定动作顺序（不回退）：标题 → 摘要 → 正文 → AI图 → 配乐 → 发布。
- 减少慢速输入：仅关键字段用 `type`，其余优先 `fill/evaluate`。
- 统一配乐策略：默认优先推荐榜第1首，避免反复搜索。
- 一次一篇，发布成功后立即开始下一篇，避免长时间停留导致状态漂移。
- 每篇发布前只做3项快检：标题有值 / 头图已生成 / 配乐已选中（先将鼠标悬停在目标歌曲行，待右侧"使用"按钮出现后再点击；不是仅点歌曲行。优先"我本将心向明月"等热曲，并确认弹窗关闭后仍保留曲名）。
- 失败重试策略：单步骤最多2次，仍失败就刷新当前页继续，不做长链回滚。

## Verified Workflow Steps (2026-03-08)

### Input Methods (实测有效)
- 标题/摘要：`type` + `slowly:true` 最稳定
- 正文：`evaluate` + `document.execCommand('insertText', false, text)`
- AI图片：点击"AI配图"后等待 5-6 秒，确认"AI换图"和"编辑封面"出现

### Publish Button Issue (待解决)
- 现象：点击"发布"按钮后，页面停留在编辑页，作品未提交
- 可能原因：按钮点击未触发提交 / 有隐藏校验未通过
- 临时方案：多次点击发布按钮，或使用 `evaluate` 直接触发按钮的 click 事件

### 成功判定标准
- 发布成功：页面跳转到"内容管理"或出现"发布成功"提示
- 作品管理页能看到新发布的文章

## Verified Music Selection Pattern (2026-03-08)

- ✅ 已实测成功：**悬停歌曲行 → 右侧出现"使用"按钮 → 点击"使用" → 关闭弹窗后显示曲名 + 按钮变"修改音乐"**。
- ✅ 判定标准：出现"修改音乐"即表示配乐绑定成功，可进入发布。
- ❌ 禁止旧方法：只点击歌曲行名称/封面，不算选中。
- ⚠️ 曲库限制：部分曲名（如"我本将心向明月"）可能不在当前可检索范围内，此时会自动退回推荐位/热门曲。成功选择任意曲后即视为配乐成功，不必强行指定。

### Verified Music Search Trigger经验（2026-03-08）

- 在"搜索音乐"框中，`evaluate` 直接赋值有时会被前端状态机清空，导致看似输入成功但未检索。
- 更稳做法：**逐字慢速输入（或等效的type slowly）**，每个字符都触发 input 事件。
- 触发检索优先级：
  1) 按 Enter；
  2) 若 Enter 不生效，点击搜索框外（blur）或点击搜索图标/按钮触发；
  3) 再等待结果刷新后再判断命中。
- 指定曲检索时，先用完整词：`我本将心向明月`；无结果再试短词：`将心向明月`。
- 命中后仍必须执行硬规则：悬停歌曲行，再点右侧"使用"，最后确认"修改音乐"。
