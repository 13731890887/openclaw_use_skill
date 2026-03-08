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

## Next Feature: Auto Comment Reply (v1)

1. Navigate to `https://creator.douyin.com/creator-micro/interaction/comment-management`.
2. Scan latest comments and skip already-replied items.
3. Classify comment intent:
   - 提问类：给步骤/建议
   - 支持类：感谢 + 轻引导关注
   - 质疑类：礼貌澄清，避免争执
4. Reply with short, human tone (8-40字), avoid repetitive templates.
5. Apply random delay (3-12s) between replies; cap per run (e.g., 20).
6. Log reply summary (count, failures, notable comments) back into this skill/README.

## Speed Optimization SOP (v2)

- 固定路径：直接从作品管理页进入“发布文章”页，减少首页跳转。
- 固定动作顺序（不回退）：标题 → 摘要 → 正文 → AI图 → 配乐 → 发布。
- 减少慢速输入：仅关键字段用 `type`，其余优先 `fill/evaluate`。
- 统一配乐策略：默认优先推荐榜第1首，避免反复搜索。
- 一次一篇，发布成功后立即开始下一篇，避免长时间停留导致状态漂移。
- 每篇发布前只做3项快检：标题有值 / 头图已生成 / 配乐已选中（先将鼠标悬停在目标歌曲行，待右侧“使用”按钮出现后再点击；不是仅点歌曲行。优先“我本将心向明月”等热曲，并确认弹窗关闭后仍保留曲名）。
- 失败重试策略：单步骤最多2次，仍失败就刷新当前页继续，不做长链回滚。
