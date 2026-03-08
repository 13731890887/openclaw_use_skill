#!/usr/bin/env python3
"""
Example: Run Douyin Bot Operations

This script demonstrates how to use the DouyinBot class.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from douyin_bot import DouyinBot
from config import (
    DOUYIN_PHONE,
    DOUYIN_PASSWORD,
    DEFAULT_REPLIES,
    validate_config,
)


def main():
    """Main entry point."""
    print("🦞 Douyin Bot - Example Runner")
    print("=" * 50)
    
    # Validate configuration
    if not validate_config():
        print("\n⚠️  Please set your credentials in .env or environment variables")
        print("   Copy .env.example to .env and edit it")
        return
    
    # Create bot instance
    bot = DouyinBot(
        phone=DOUYIN_PHONE,
        password=DOUYIN_PASSWORD,
        headless=False,  # Set to True for background operation
    )
    
    try:
        # Step 1: Login
        print("\n🔐 Step 1: Logging in...")
        if not bot.login():
            print("❌ Login failed. Please check credentials.")
            return
        print("✅ Login successful!\n")
        
        # Step 2: Post an article (example from Day 0)
        print("📝 Step 2: Posting article...")
        title = "欢迎大家围观：我用小龙虾开始运营抖音--Day 1"
        content = """
大家好，我是新手内容创作者。

今天是我正式开启抖音运营的第一天，我决定做一个有点特别的账号——用小龙虾记录我的内容创作之旅。

为什么是小龙虾？
- 🦞 它够有辨识度，一眼就能记住
- 🦞 红色=喜庆=好运，图个吉利
- 🦞 剥虾的过程天然有"解压"属性
- 🦞 最重要的是——我爱吃

我的目标：
- 30 天内突破 1000 粉
- 找到属于自己的内容风格
- 把"吃小龙虾"这件事做出花样

如果你也感兴趣，欢迎关注我，一起看看这个小实验能走多远。

Day 1 完成。明天继续更新！
🦞 明天见！
"""
        
        # Uncomment to actually post:
        # if bot.post_article(title=title, content=content):
        #     print("✅ Article posted successfully!")
        # else:
        #     print("⚠️ Article post may have failed")
        
        print("📝 Article ready to post (uncomment code to enable)")
        print(f"   Title: {title}")
        print()
        
        # Step 3: Reply to comments (example)
        print("💬 Step 3: Reply to comments...")
        post_url = "https://www.douyin.com/video/YOUR_VIDEO_ID"  # Replace with actual URL
        
        # Uncomment to actually reply:
        # replies_sent = bot.reply_to_comments(
        #     post_url=post_url,
        #     replies=DEFAULT_REPLIES,
        #     max_replies=10,
        # )
        # print(f"✅ Sent {replies_sent} replies")
        
        print("💬 Reply system ready (uncomment code to enable)")
        print(f"   Default replies: {len(DEFAULT_REPLIES)} templates")
        print()
        
        print("=" * 50)
        print("✅ Example run complete!")
        print("\n📝 To enable actual operations, uncomment the code blocks above")
        print("⚠️  Remember: Use at your own risk - may violate Douyin ToS")
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        # Close browser
        print("\n👋 Closing browser...")
        bot.close()


if __name__ == "__main__":
    main()
