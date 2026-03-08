#!/usr/bin/env python3
"""One-shot operations for Day 0: publish first article + reply comments."""

from douyin_bot import DouyinBot
from config import DAY0_TITLE, DAY0_CONTENT, DOUYIN_PHONE, DOUYIN_PASSWORD


def main():
    bot = DouyinBot(phone=DOUYIN_PHONE, password=DOUYIN_PASSWORD, headless=False)
    try:
        print("🦞 启动 Day 0 运营流程")
        if not bot.login():
            print("❌ 登录失败，请先在弹出的浏览器手动完成登录后重试。")
            return

        print("📝 发布 Day 0 文章...")
        posted = bot.post_article(title=DAY0_TITLE, content=DAY0_CONTENT)
        print("✅ 发布成功" if posted else "⚠️ 发布可能失败，请人工确认")

        print("💬 回复最新评论...")
        count = bot.reply_comments_in_creator(max_replies=8)
        print(f"✅ 已回复 {count} 条评论")

    finally:
        bot.close()


if __name__ == "__main__":
    main()
