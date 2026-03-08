# 🦞 Douyin Automation Skill

> Automate your Douyin (抖音) account operations with Selenium

## Quick Start

### 1. Setup

```bash
cd skills/douyin-automation

# Install dependencies (if not already installed)
pip3 install selenium webdriver-manager python-dotenv

# Create your config
cp .env.example .env
# Edit .env with your Douyin credentials
```

### 2. Run Example

```bash
python3 run_example.py
```

### 3. Use in Your Code

```python
from douyin_bot import DouyinBot

bot = DouyinBot(
    phone="13800138000",
    password="your_password"
)

# Login
bot.login()

# Post article
bot.post_article(
    title="My Article Title",
    content="Article content here..."
)

# Reply to comments
bot.reply_to_comments(
    post_url="https://www.douyin.com/video/...",
    replies={"好": "谢谢！", "喜欢": "❤️"}
)

# Close
bot.close()
```

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| Login | 🟡 Partial | Password & SMS support needed |
| Post Article | 🟡 Partial | Text + images |
| Get Comments | 🟡 Partial | Read comments from posts |
| Reply to Comments | 🟡 Partial | Auto-reply with templates |
| Human-like Delays | ✅ Done | Random delays between actions |
| Anti-detection | 🟡 Partial | Basic evasion implemented |

## Files

```
douyin-automation/
├── SKILL.md           # Skill documentation & learnings
├── README.md          # This file
├── douyin_bot.py      # Main automation class
├── config.py          # Configuration & settings
├── run_example.py     # Example usage script
├── .env.example       # Environment template
└── douyin_bot.log     # Logs (created on first run)
```

## Configuration

Edit `.env` or set environment variables:

```bash
export DOUYIN_PHONE=13800138000
export DOUYIN_PASSWORD=your_password
export DOUYIN_HEADLESS=false
```

## ⚠️ Important Warnings

1. **Terms of Service**: This may violate Douyin's ToS. Use at your own risk.
2. **Account Safety**: Add sufficient delays to avoid detection.
3. **Rate Limits**: Don't post/reply too frequently.
4. **Selectors**: Douyin changes their UI regularly - selectors may break.

## Troubleshooting

### Login fails
- Check credentials
- Douyin may require SMS verification
- Try manual login first to ensure account is valid

### Selectors not found
- Douyin updates their UI frequently
- Check `douyin_bot.log` for details
- May need to update selectors in `douyin_bot.py`

### CAPTCHA appears
- Add longer delays
- Reduce automation frequency
- May need manual intervention

## Learning Log

### 2026-03-07 (Day 1)
- ✅ Created skill structure
- ✅ Implemented basic DouyinBot class
- ✅ Login flow (partial - needs SMS support)
- ✅ Article posting (text + images)
- ✅ Comment reading
- ✅ Comment reply with templates
- ✅ Human-like delays
- ✅ Basic anti-detection measures
- ⏳ Need to test with real Douyin account
- ⏳ Need to update selectors based on actual UI

### 2026-03-08 (Day 2)
- ✅ Connected OpenClaw browser automation to creator portal
- ✅ Verified Day 0 title/content template is ready
- ✅ Completed login and published multiple Day0/Day1-style articles via creator backend
- ✅ Fixed workflow to explicitly select music before publishing
- ⚠️ Selenium startup unstable on this host (`Service Unavailable`)
- ✅ Added Selenium fallback logic and documented Playwright/browser-tool-first strategy
- ✅ Added auto-comment-reply v1 runbook (intent classification + delay/rate cap)
- 🔄 Next: implement stable comment-management parser + one-click auto reply executor

## Contributing

When you use this skill:
1. Update `SKILL.md` with lessons learned
2. Update selectors if they change
3. Add new features as needed
4. Log any issues in the learning section

---

🦞 Built with Selenium | Use responsibly
