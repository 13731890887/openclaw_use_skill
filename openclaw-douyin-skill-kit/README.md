# OpenClaw Douyin Automation Skill Kit

This repo is a shareable package so other developers can teach their OpenClaw agent the same Douyin automation workflow.

## What is included

- `skills/douyin-automation/`
  - `SKILL.md` (workflow + guardrails + validated interaction pattern)
  - helper scripts (`douyin_bot.py`, `douyin_playwright.py`, `run_day0_ops.py`, etc.)

## How another developer installs it

### Option A (recommended): copy into OpenClaw workspace skills

1. Clone this repository.
2. Copy the skill folder into your OpenClaw workspace:

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -R skills/douyin-automation ~/.openclaw/workspace/skills/
```

3. Restart/reload your OpenClaw session.
4. Ask your agent naturally, e.g.:
   - “发布一篇抖音图文，先选音乐再发布”
   - “按 douyin-automation 的流程发文并核验是否入库”

### Option B: vendor as subfolder in your own repo

Keep `skills/douyin-automation` in your repo and sync it into `~/.openclaw/workspace/skills` during setup.

## Usage contract (important)

- Publish flow: title → summary → body → AI image → music → publish → manage-page verification.
- Music selection must use visible UI interaction: **hover row first, then click “使用”**.
- Success signal for music: main form shows selected song + button becomes **“修改音乐”**.
- Publishing guardrail: body should be **>= 100 Chinese characters** to avoid silent publish failure.

## Suggested share message for developers

"Give this GitHub link to your OpenClaw agent and ask it to follow the `skills/douyin-automation/SKILL.md` workflow for Douyin creator publishing."

## License

Use internally or adapt for your team.
