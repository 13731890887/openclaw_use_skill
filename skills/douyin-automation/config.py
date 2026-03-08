#!/usr/bin/env python3
"""
Configuration for Douyin Automation Bot

Store sensitive data in environment variables or edit carefully.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file if present

# =============================================================================
# Account Credentials
# =============================================================================
# ⚠️ IMPORTANT: Use environment variables in production!
# Set DOUYIN_PHONE and DOUYIN_PASSWORD in your .env file or shell

DOUYIN_PHONE = os.getenv('DOUYIN_PHONE', '')
DOUYIN_PASSWORD = os.getenv('DOUYIN_PASSWORD', '')
DOUYIN_CHROME_PROFILE = os.getenv('DOUYIN_CHROME_PROFILE', os.path.expanduser('~/.openclaw/douyin-chrome-profile'))

# =============================================================================
# Browser Settings
# =============================================================================
HEADLESS = False  # Set to True for background operation
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# =============================================================================
# Timing Settings (all in seconds)
# =============================================================================
# Delays to appear human-like
MIN_DELAY = 2
MAX_DELAY = 5
LONG_MIN_DELAY = 5
LONG_MAX_DELAY = 10

# Between actions
POST_DELAY = 3  # After posting
REPLY_DELAY = 5  # Between replies
SCROLL_DELAY = 2  # Between scrolls

# =============================================================================
# Rate Limits
# =============================================================================
# Stay under these to avoid detection
MAX_POSTS_PER_DAY = 5
MAX_REPLIES_PER_HOUR = 20
MAX_COMMENTS_TO_READ = 50

# =============================================================================
# Default Reply Templates
# =============================================================================
DEFAULT_REPLIES = {
    "好": "谢谢支持！🦞",
    "喜欢": "很高兴你喜欢！❤️",
    "哈哈": "😂😂😂",
    "棒": "继续努力！💪",
    "加油": "一起加油！🔥",
    "666": "🙏🙏🙏",
    "牛逼": "过奖了～",
    "怎么": "私信我详细说～",
    "哪里": "评论区置顶有链接～",
    "求": "已私信～",
}

# =============================================================================
# URLs
# =============================================================================
DOUYIN_BASE = "https://www.douyin.com"
DOUYIN_LOGIN = "https://www.douyin.com"
DOUYIN_CREATE = "https://creator.douyin.com/creator-micro/content/post/article?default-tab=5&enter_from=publish_page&media_type=article&type=new"
DOUYIN_COMMENT_MANAGE = "https://creator.douyin.com/creator-micro/interaction/comment-management"
DOUYIN_PROFILE = "https://www.douyin.com/user/self"

# =============================================================================
# Logging
# =============================================================================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "douyin_bot.log"

# =============================================================================
# Selectors (may need updates as Douyin changes their UI)
# =============================================================================
# These are common selectors - the bot will try multiple options
DAY0_TITLE = "欢迎大家围观：我用小龙虾开始运营抖音--Day 0"
DAY0_CONTENT = """大家好，我是新手内容创作者。\n\n今天是我正式开启抖音运营的第一天，我决定做一个有点特别的账号——用小龙虾记录我的内容创作之旅。\n\n为什么是小龙虾？\n- 🦞 它够有辨识度，一眼就能记住\n- 🦞 红色=喜庆=好运，图个吉利\n- 🦞 剥虾的过程天然有\"解压\"属性\n- 🦞 最重要的是——我爱吃\n\nDay 0 要做什么？\n1. ✅ 注册账号，完善主页\n2. ✅ 想好账号定位和名字\n3. ✅ 准备第一批拍摄素材\n4. ✅ 研究对标账号，学习爆款逻辑\n\n我的目标：\n- 30 天内突破 1000 粉\n- 找到属于自己的内容风格\n- 把\"吃小龙虾\"这件事做出花样\n\n如果你也感兴趣，欢迎关注我，一起看看这个小实验能走多远。\n\nDay 0 完成。明天正式开始内容发布。\n🦞 明天见！"""

SELECTORS = {
    "login_button": [
        "//button[contains(text(), '登录')]",
        "//button[contains(text(), '登陆')]",
        "//a[contains(text(), '登录')]",
    ],
    "phone_input": [
        "//input[@type='tel']",
        "//input[@placeholder*='手机']",
        "input[type='tel']",
    ],
    "password_input": [
        "//input[@type='password']",
        "input[type='password']",
    ],
    "publish_button": [
        "//button[contains(text(), '发布')]",
        "//button[contains(text(), '发表')]",
        "button.publish",
    ],
    "comment_section": [
        "//div[contains(@class, 'comment')]",
        "//div[contains(@class, 'comment-item')]",
    ],
    "reply_button": [
        "//button[contains(text(), '回复')]",
        ".reply-btn",
    ],
}

# =============================================================================
# Helper Functions
# =============================================================================

def validate_config():
    """Validate configuration and warn about missing values."""
    warnings = []
    
    if not DOUYIN_PHONE:
        warnings.append("⚠️ DOUYIN_PHONE not set")
    
    if not DOUYIN_PASSWORD:
        warnings.append("⚠️ DOUYIN_PASSWORD not set")
    
    for warning in warnings:
        print(warning)
    
    return len(warnings) == 0


if __name__ == "__main__":
    print("🦞 Douyin Bot Configuration")
    print("=" * 40)
    validate_config()
