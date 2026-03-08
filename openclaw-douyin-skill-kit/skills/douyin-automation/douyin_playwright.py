#!/usr/bin/env python3
"""
Douyin (抖音) Automation Bot using Playwright

More reliable than Selenium on macOS.
Automates: Login, Post Articles, Reply to Comments
"""

import os
import time
import random
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('douyin_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DouyinBot:
    """Douyin automation bot using Playwright."""
    
    DOUYIN_URL = "https://www.douyin.com"
    
    def __init__(self, headless=False):
        """
        Initialize the Douyin bot.
        
        Args:
            headless: Run browser in headless mode (default: False for manual login)
        """
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.logged_in = False
        
        logger.info("🦞 DouyinBot (Playwright) initialized")
    
    def setup_browser(self):
        """Set up Playwright browser."""
        self.playwright = sync_playwright().start()
        
        # Use Chromium with anti-detection
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
            ]
        )
        
        # Create context with user agent
        self.context = self.browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
        )
        
        # Add init script to hide automation
        self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """)
        
        self.page = self.context.new_page()
        logger.info("✅ Browser setup complete")
        
        return self.page
    
    def human_delay(self, min_sec=2, max_sec=5):
        """Add a human-like random delay."""
        delay = random.uniform(min_sec, max_sec)
        logger.debug(f"⏳ Waiting {delay:.2f}s")
        time.sleep(delay)
    
    def login(self):
        """
        Login to Douyin (manual verification supported).
        
        Returns:
            bool: True if login successful
        """
        if not self.page:
            self.setup_browser()
        
        try:
            logger.info("🔐 Navigating to Douyin...")
            # Use domcontentloaded for faster load, less strict than networkidle
            self.page.goto(self.DOUYIN_URL, wait_until='domcontentloaded', timeout=60000)
            self.human_delay(3, 5)
            
            print("\n" + "=" * 60)
            print("📱 请在浏览器中完成登录：")
            print("   1. 点击右上角登录按钮")
            print("   2. 选择登录方式（密码/短信验证码）")
            print("   3. 完成滑块/验证码（如有）")
            print("=" * 60)
            
            # Wait for user to complete login manually
            input("\n✅ 登录完成后按回车继续...")
            
            # Check if logged in
            if self._check_logged_in():
                self.logged_in = True
                logger.info("✅ Login successful!")
                return True
            else:
                logger.warning("⚠️ Login may not have completed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Login failed: {str(e)}")
            return False
    
    def _check_logged_in(self):
        """Check if user is logged in."""
        indicators = [
            "//img[contains(@class, 'avatar')]",
            "//div[contains(@class, 'user-info')]",
            "//span[contains(text(), '发布')]",
            "//button[contains(text(), '发布')]",
        ]
        
        for selector in indicators:
            try:
                element = self.page.query_selector(selector)
                if element and element.is_visible():
                    return True
            except:
                continue
        
        return False
    
    def post_article(self, title, content, images=None):
        """
        Post an article to Douyin.
        
        Args:
            title: Article title
            content: Article content
            images: List of image paths (optional)
        
        Returns:
            bool: True if post successful
        """
        if not self.logged_in:
            logger.error("❌ Not logged in")
            return False
        
        try:
            logger.info(f"📝 Posting article: {title[:30]}...")
            
            # Navigate to post page
            self.page.goto("https://creator.douyin.com/creator-micro/content/post/article?default-tab=5&enter_from=publish_page&media_type=article&type=new", wait_until='domcontentloaded', timeout=60000)
            self.human_delay(3, 5)
            
            # Fill title
            try:
                title_input = self.page.wait_for_selector(
                    "input[placeholder*='标题'], input[name='title']",
                    timeout=10000
                )
                if title_input:
                    title_input.fill(title)
                    logger.info("✅ Title entered")
                    self.human_delay(1, 2)
            except Exception as e:
                logger.warning(f"⚠️ Could not fill title: {e}")
            
            # Fill content
            try:
                content_input = self.page.wait_for_selector(
                    "textarea[placeholder*='内容'], textarea[name='content']",
                    timeout=10000
                )
                if content_input:
                    content_input.fill(content)
                    logger.info("✅ Content entered")
                    self.human_delay(1, 2)
            except Exception as e:
                logger.warning(f"⚠️ Could not fill content: {e}")
            
            # Upload images if provided
            if images:
                for image_path in images:
                    if self._upload_image(image_path):
                        logger.info(f"✅ Uploaded image: {image_path}")
            
            # Click publish
            print("\n" + "=" * 60)
            print("📝 文章已填写完成")
            print(f"   标题：{title}")
            print(f"   内容：{content[:50]}...")
            print("=" * 60)
            
            confirm = input("📤 确认发布？(y/n): ")
            if confirm.lower() == 'y':
                try:
                    publish_btn = self.page.wait_for_selector(
                        "button:has-text('发布'), button:has-text('发表')",
                        timeout=10000
                    )
                    if publish_btn:
                        publish_btn.click()
                        logger.info("📤 Publish button clicked")
                        self.human_delay(3, 5)
                        logger.info("✅ Article posted successfully!")
                        return True
                except Exception as e:
                    logger.warning(f"⚠️ Could not click publish: {e}")
                    print("⚠️  请手动点击发布按钮")
                    input("发布完成后按回车...")
                    return True
            else:
                print("❌ 取消发布")
                return False
                
        except Exception as e:
            logger.error(f"❌ Post failed: {str(e)}")
            return False
    
    def _upload_image(self, image_path):
        """Upload an image."""
        try:
            file_input = self.page.query_selector("input[type='file']")
            if file_input:
                file_input.set_input_files(os.path.abspath(image_path))
                self.human_delay(2, 4)
                time.sleep(3)
                return True
            return False
        except Exception as e:
            logger.error(f"Image upload failed: {str(e)}")
            return False
    
    def get_comments(self, post_url=None, max_comments=20):
        """
        Get comments from a post.
        
        Args:
            post_url: URL of the post
            max_comments: Maximum number of comments to retrieve
        
        Returns:
            list: List of comment dicts
        """
        if post_url:
            self.page.goto(post_url, wait_until='domcontentloaded', timeout=60000)
            self.human_delay(2, 4)
        
        comments = []
        
        try:
            # Scroll to comments
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.human_delay(2, 3)
            
            # Find comments
            comment_elements = self.page.query_selector_all(
                "div[class*='comment'], div[class*='CommentItem']"
            )
            
            for elem in comment_elements[:max_comments]:
                try:
                    comment_data = {
                        'author': elem.query_selector('.author-name').inner_text() if elem.query_selector('.author-name') else 'Unknown',
                        'text': elem.query_selector('.comment-text').inner_text() if elem.query_selector('.comment-text') else '',
                        'element': elem,
                    }
                    comments.append(comment_data)
                except:
                    continue
            
            logger.info(f"✅ Retrieved {len(comments)} comments")
            
        except Exception as e:
            logger.error(f"Failed to get comments: {str(e)}")
        
        return comments
    
    def reply_to_comments(self, post_url=None, replies=None, max_replies=10):
        """
        Reply to comments with keyword matching.
        
        Args:
            post_url: URL of the post
            replies: Dict mapping keywords to reply texts
            max_replies: Maximum replies to send
        
        Returns:
            int: Number of replies sent
        """
        if not replies:
            replies = {
                "好": "谢谢支持！🦞",
                "喜欢": "很高兴你喜欢！❤️",
                "哈哈": "😂😂😂",
            }
        
        comments = self.get_comments(post_url)
        replies_sent = 0
        
        for comment in comments:
            if replies_sent >= max_replies:
                break
            
            comment_text = comment.get('text', '').lower()
            
            for keyword, reply_text in replies.items():
                if keyword.lower() in comment_text:
                    try:
                        # Find reply button
                        reply_btn = comment['element'].query_selector(
                            "button:has-text('回复')"
                        )
                        if reply_btn:
                            reply_btn.click()
                            self.human_delay(1, 2)
                            
                            # Find reply input
                            reply_input = self.page.query_selector(
                                "textarea[placeholder*='回复']"
                            )
                            if reply_input:
                                reply_input.fill(reply_text)
                                self.human_delay(1, 2)
                                
                                # Click send
                                send_btn = self.page.query_selector(
                                    "button:has-text('发送')"
                                )
                                if send_btn:
                                    send_btn.click()
                                    replies_sent += 1
                                    logger.info(f"✅ Replied: {reply_text}")
                                    self.human_delay(3, 6)
                                    break
                    except Exception as e:
                        logger.debug(f"Could not reply: {e}")
        
        logger.info(f"✅ Sent {replies_sent} replies")
        return replies_sent
    
    def close(self):
        """Close the browser."""
        if self.browser:
            self.browser.close()
            logger.info("👋 Browser closed")
        if self.playwright:
            self.playwright.stop()


def main():
    """Main entry point for testing."""
    print("🦞 抖音自动化 - Playwright 版本")
    print("=" * 60)
    
    bot = DouyinBot(headless=False)
    
    try:
        # Login
        if bot.login():
            # Post article
            title = "欢迎大家围观：我用小龙虾开始运营抖音--Day 0"
            content = """
大家好，我是新手内容创作者。

今天是我正式开启抖音运营的第一天，我决定做一个有点特别的账号——用小龙虾记录我的内容创作之旅。

为什么是小龙虾？
- 🦞 它够有辨识度，一眼就能记住
- 🦞 红色=喜庆=好运，图个吉利
- 🦞 剥虾的过程天然有"解压"属性
- 🦞 最重要的是——我爱吃

Day 0 任务：
1. ✅ 注册账号，完善主页
2. ✅ 想好账号定位和名字
3. ✅ 准备第一批拍摄素材
4. ✅ 研究对标账号，学习爆款逻辑

我的目标：
- 30 天内突破 1000 粉
- 找到属于自己的内容风格
- 把"吃小龙虾"这件事做出花样

如果你也感兴趣，欢迎关注我，一起看看这个小实验能走多远。

Day 0 完成。明天正式开始内容发布。
🦞 明天见！
"""
            bot.post_article(title=title, content=content)
        
    except KeyboardInterrupt:
        print("\n⚠️  中断")
    finally:
        bot.close()
        print("✅ 完成")


if __name__ == "__main__":
    main()
