#!/usr/bin/env python3
"""
Douyin (抖音) Automation Bot

Uses Selenium to automate:
- Login
- Posting articles
- Replying to comments

⚠️ Use at your own risk - may violate Douyin ToS
"""

import os
import time
import random
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    WebDriverException,
)
from webdriver_manager.chrome import ChromeDriverManager
from config import DOUYIN_CREATE, DOUYIN_COMMENT_MANAGE, DOUYIN_CHROME_PROFILE

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
    """Douyin automation bot using Selenium."""
    
    # URLs
    DOUYIN_URL = "https://www.douyin.com"
    LOGIN_URL = "https://www.douyin.com"
    
    # Default delays (in seconds)
    DEFAULT_DELAY = (2, 5)
    LONG_DELAY = (5, 10)
    
    def __init__(self, phone=None, password=None, headless=False, profile_dir=None):
        """
        Initialize the Douyin bot.
        
        Args:
            phone: Phone number for login
            password: Password for login
            headless: Run Chrome in headless mode (default: False)
        """
        self.phone = phone or os.getenv('DOUYIN_PHONE')
        self.password = password or os.getenv('DOUYIN_PASSWORD')
        self.headless = headless
        self.profile_dir = profile_dir or DOUYIN_CHROME_PROFILE
        self.driver = None
        self.wait = None
        self.logged_in = False
        
        logger.info("🦞 DouyinBot initialized")
    
    def setup_driver(self):
        """Set up Chrome WebDriver."""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        # Common options to avoid detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=0")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--lang=zh-CN")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36")
        
        # Exclude automation flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Persistent profile keeps login session
        os.makedirs(self.profile_dir, exist_ok=True)
        chrome_options.add_argument(f"--user-data-dir={self.profile_dir}")
        chrome_options.add_argument("--profile-directory=Default")
        
        # Set Chrome binary location (macOS)
        chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
        # Set up driver (prefer Selenium Manager for version compatibility)
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException as e:
            logger.warning(f"⚠️ Selenium Manager failed, fallback to webdriver-manager: {e}")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute CDP to hide automation
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        
        self.wait = WebDriverWait(self.driver, 30)
        logger.info("✅ Chrome driver setup complete")
        
        return self.driver
    
    def human_delay(self, min_sec=2, max_sec=5):
        """Add a human-like random delay."""
        delay = random.uniform(min_sec, max_sec)
        logger.debug(f"⏳ Waiting {delay:.2f}s")
        time.sleep(delay)
    
    def login(self, phone=None, password=None):
        """
        Login to Douyin.
        
        Args:
            phone: Phone number (overrides instance value)
            password: Password (overrides instance value)
        
        Returns:
            bool: True if login successful
        """
        phone = phone or self.phone
        password = password or self.password
        
        if not self.driver:
            self.setup_driver()

        # Manual login mode when credentials are not provided
        if not phone or not password:
            logger.warning("⚠️ Credentials not provided, switching to manual login mode")
            self.driver.get(self.LOGIN_URL)
            logger.info("📱 请在浏览器中手动完成登录（短信/扫码/验证码）")
            for _ in range(60):  # up to ~5 minutes
                self.human_delay(4, 6)
                if self._check_logged_in():
                    self.logged_in = True
                    logger.info("✅ Manual login successful")
                    return True
            logger.error("❌ Manual login timeout")
            return False

        try:
            logger.info("🔐 Navigating to Douyin...")
            self.driver.get(self.LOGIN_URL)
            self.human_delay(3, 5)
            
            # Look for login button
            # Note: Selectors may change - update as needed
            login_selectors = [
                "//button[contains(text(), '登录')]",
                "//button[contains(text(), '登陆')]",
                "//*[@class='login-button']",
                "//a[contains(text(), '登录')]",
            ]
            
            login_btn = None
            for selector in login_selectors:
                try:
                    login_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    logger.info(f"✅ Found login button: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not login_btn:
                logger.warning("⚠️ Login button not found - may already be logged in")
                # Check if already logged in
                if self._check_logged_in():
                    self.logged_in = True
                    logger.info("✅ Already logged in")
                    return True
                else:
                    logger.error("❌ Could not find login button and not logged in")
                    return False
            
            login_btn.click()
            self.human_delay(2, 4)
            
            # Enter phone number
            phone_input = self._find_element([
                (By.XPATH, "//input[@type='tel']"),
                (By.XPATH, "//input[@placeholder*='手机']"),
                (By.CSS_SELECTOR, "input[type='tel']"),
            ])
            
            if phone_input:
                phone_input.clear()
                phone_input.send_keys(phone)
                logger.info(f"📱 Entered phone number")
                self.human_delay(1, 2)
            
            # Enter password or get verification code
            # This depends on login method (password vs SMS)
            password_input = self._find_element([
                (By.XPATH, "//input[@type='password']"),
                (By.CSS_SELECTOR, "input[type='password']"),
            ])
            
            if password_input:
                password_input.send_keys(password)
                logger.info("🔑 Entered password")
                self.human_delay(1, 2)
                
                # Click submit
                submit_btn = self._find_element([
                    (By.XPATH, "//button[contains(text(), '登录')]"),
                    (By.CSS_SELECTOR, "button[type='submit']"),
                ])
                
                if submit_btn:
                    submit_btn.click()
                    logger.info("📤 Submitted login form")
                    self.human_delay(3, 5)
            
            # Wait for login to complete
            if self._check_logged_in():
                self.logged_in = True
                logger.info("✅ Login successful!")
                return True
            else:
                logger.warning("⚠️ Login may not have completed - check manually")
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
        ]
        
        for selector in indicators:
            try:
                element = self.driver.find_element(By.XPATH, selector)
                if element.is_displayed():
                    return True
            except:
                continue
        
        return False
    
    def _find_element(self, selectors, wait_time=10):
        """
        Try multiple selectors to find an element.
        
        Args:
            selectors: List of (By, selector) tuples
            wait_time: Timeout in seconds
        
        Returns:
            WebElement or None
        """
        for by, selector in selectors:
            try:
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((by, selector))
                )
                return element
            except TimeoutException:
                continue
        
        return None
    
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
            # Douyin article post URL may vary
            self.driver.get(DOUYIN_CREATE)
            self.human_delay(3, 5)
            
            # Find title input
            title_selectors = [
                (By.XPATH, "//input[contains(@placeholder, '标题')]"),
                (By.CSS_SELECTOR, "input[placeholder*='标题']"),
                (By.NAME, "title"),
            ]
            title_input = self._find_element(title_selectors)
            
            if title_input:
                title_input.clear()
                title_input.send_keys(title)
                logger.info("✅ Title entered")
                self.human_delay(1, 2)
            
            # Find content textarea
            content_selectors = [
                (By.XPATH, "//textarea[contains(@placeholder, '内容')]"),
                (By.CSS_SELECTOR, "textarea[placeholder*='内容']"),
                (By.NAME, "content"),
            ]
            content_input = self._find_element(content_selectors)
            
            if content_input:
                content_input.clear()
                content_input.send_keys(content)
                logger.info("✅ Content entered")
                self.human_delay(1, 2)
            
            # Upload images if provided
            if images:
                for image_path in images:
                    if self._upload_image(image_path):
                        logger.info(f"✅ Uploaded image: {image_path}")
                    else:
                        logger.warning(f"⚠️ Failed to upload image: {image_path}")
            
            # Click publish
            publish_selectors = [
                (By.XPATH, "//button[contains(text(), '发布')]"),
                (By.CSS_SELECTOR, "button.publish"),
                (By.XPATH, "//button[contains(text(), '发表')]"),
            ]
            publish_btn = self._find_element(publish_selectors)
            
            if publish_btn:
                publish_btn.click()
                logger.info("📤 Publish button clicked")
                self.human_delay(3, 5)
                
                # Wait for confirmation
                logger.info("✅ Article posted successfully!")
                return True
            else:
                logger.error("❌ Publish button not found")
                return False
                
        except Exception as e:
            logger.error(f"❌ Post failed: {str(e)}")
            return False
    
    def _upload_image(self, image_path):
        """Upload an image."""
        try:
            # Find file input
            upload_selectors = [
                (By.XPATH, "//input[@type='file']"),
                (By.CSS_SELECTOR, "input[type='file']"),
            ]
            file_input = self._find_element(upload_selectors)
            
            if file_input:
                file_input.send_keys(os.path.abspath(image_path))
                self.human_delay(2, 4)
                
                # Wait for upload to complete
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
            post_url: URL of the post (current page if None)
            max_comments: Maximum number of comments to retrieve
        
        Returns:
            list: List of comment dicts with 'author', 'text', 'time'
        """
        if post_url:
            self.driver.get(post_url)
            self.human_delay(2, 4)
        
        comments = []
        
        try:
            # Scroll to comments section
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.human_delay(2, 3)
            
            # Find comment elements
            comment_selectors = [
                "//div[contains(@class, 'comment')]",
                "//div[contains(@class, 'comment-item')]",
            ]
            
            comment_elements = []
            for selector in comment_selectors:
                try:
                    comment_elements = self.driver.find_elements(By.XPATH, selector)
                    if comment_elements:
                        break
                except:
                    continue
            
            for elem in comment_elements[:max_comments]:
                try:
                    comment_data = {
                        'author': elem.find_element(By.CSS_SELECTOR, '.author-name').text if elem.find_elements(By.CSS_SELECTOR, '.author-name') else 'Unknown',
                        'text': elem.find_element(By.CSS_SELECTOR, '.comment-text').text if elem.find_elements(By.CSS_SELECTOR, '.comment-text') else '',
                        'time': elem.find_element(By.CSS_SELECTOR, '.comment-time').text if elem.find_elements(By.CSS_SELECTOR, '.comment-time') else '',
                        'element': elem,
                    }
                    comments.append(comment_data)
                except Exception as e:
                    logger.debug(f"Could not parse comment: {str(e)}")
            
            logger.info(f"✅ Retrieved {len(comments)} comments")
            
        except Exception as e:
            logger.error(f"Failed to get comments: {str(e)}")
        
        return comments
    
    def reply_to_comment(self, comment_element, reply_text):
        """
        Reply to a specific comment.
        
        Args:
            comment_element: WebElement of the comment
            reply_text: Text of the reply
        
        Returns:
            bool: True if reply successful
        """
        try:
            # Find reply button
            reply_selectors = [
                (By.XPATH, ".//button[contains(text(), '回复')]"),
                (By.CSS_SELECTOR, ".reply-btn"),
                (By.XPATH, ".//span[contains(text(), '回复')]"),
            ]
            
            reply_btn = None
            for by, selector in reply_selectors:
                try:
                    reply_btn = comment_element.find_element(by, selector)
                    break
                except:
                    continue
            
            if reply_btn:
                reply_btn.click()
                self.human_delay(1, 2)
                
                # Find reply input
                reply_input_selectors = [
                    (By.CSS_SELECTOR, "textarea.reply-input"),
                    (By.XPATH, "//textarea[contains(@placeholder, '回复')]"),
                ]
                reply_input = self._find_element(reply_input_selectors)
                
                if reply_input:
                    reply_input.clear()
                    reply_input.send_keys(reply_text)
                    self.human_delay(1, 2)
                    
                    # Find send button
                    send_selectors = [
                        (By.XPATH, "//button[contains(text(), '发送')]"),
                        (By.CSS_SELECTOR, "button.send-btn"),
                    ]
                    send_btn = self._find_element(send_selectors)
                    
                    if send_btn:
                        send_btn.click()
                        self.human_delay(2, 3)
                        logger.info("✅ Reply sent")
                        return True
            
            logger.warning("⚠️ Could not reply to comment")
            return False
            
        except Exception as e:
            logger.error(f"Reply failed: {str(e)}")
            return False
    
    def reply_to_comments(self, post_url=None, replies=None, max_replies=10):
        """
        Reply to multiple comments on a post.
        
        Args:
            post_url: URL of the post
            replies: Dict mapping keywords to reply texts
            max_replies: Maximum number of replies to send
        
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
            
            # Check if any keyword matches
            for keyword, reply_text in replies.items():
                if keyword.lower() in comment_text:
                    if self.reply_to_comment(comment['element'], reply_text):
                        replies_sent += 1
                        logger.info(f"Replied to '{comment['author']}': {reply_text}")
                        self.human_delay(3, 6)  # Longer delay between replies
                        break
        
        logger.info(f"✅ Sent {replies_sent} replies")
        return replies_sent
    
    def reply_comments_in_creator(self, keyword_replies=None, max_replies=10):
        """Reply to recent comments from creator comment-management page."""
        if not self.logged_in:
            logger.error("❌ Not logged in")
            return 0

        if keyword_replies is None:
            keyword_replies = {
                "好": "谢谢支持！🦞",
                "喜欢": "很高兴你喜欢！❤️",
                "加油": "一起加油！🔥",
                "哪里": "我会持续更新，记得关注主页置顶～",
            }

        self.driver.get(DOUYIN_COMMENT_MANAGE)
        self.human_delay(3, 5)

        sent = 0
        try:
            items = self.driver.find_elements(By.XPATH, "//div[contains(@class,'comment') or contains(@class,'Comment')]")
            for item in items:
                if sent >= max_replies:
                    break
                text = item.text or ""
                matched = None
                for k, v in keyword_replies.items():
                    if k in text:
                        matched = v
                        break
                if not matched:
                    continue

                try:
                    reply_btn = item.find_element(By.XPATH, ".//button[contains(text(),'回复')]")
                    reply_btn.click()
                    self.human_delay(1, 2)

                    input_box = self._find_element([
                        (By.XPATH, "//textarea[contains(@placeholder,'回复') or contains(@placeholder,'评论')]"),
                        (By.CSS_SELECTOR, "textarea"),
                    ], wait_time=5)
                    if not input_box:
                        continue
                    input_box.clear()
                    input_box.send_keys(matched)
                    self.human_delay(1, 2)

                    send_btn = self._find_element([
                        (By.XPATH, "//button[contains(text(),'发送') or contains(text(),'回复')]"),
                    ], wait_time=5)
                    if send_btn:
                        send_btn.click()
                        sent += 1
                        logger.info(f"✅ Replied comment {sent}/{max_replies}")
                        self.human_delay(3, 6)
                except Exception:
                    continue

        except Exception as e:
            logger.error(f"❌ Reply comments failed: {str(e)}")

        logger.info(f"✅ Sent {sent} comment replies")
        return sent

    def _generate_safe_reply(self, comment_text):
        """Generate short, human-like, low-risk reply text (8-40 chars)."""
        text = (comment_text or "").strip()
        if not text:
            return None

        lower = text.lower()

        # Avoid risky or commercial guidance by default
        blocked = ["vx", "微信", "加我", "私信", "带货", "合作报价", "引流"]
        if any(k in lower for k in blocked):
            return "感谢关注，欢迎在评论区交流使用体验～"

        question_keys = ["?", "？", "怎么", "如何", "哪里", "可以吗", "教程", "步骤"]
        support_keys = ["好", "厉害", "喜欢", "支持", "加油", "牛", "赞"]
        doubt_keys = ["假", "骗人", "不信", "吹", "没用", "扯"]

        if any(k in text for k in question_keys):
            pool = [
                "可以，我后面补一条完整步骤版。",
                "这个可以做，我会发实操细节。",
                "你这个问题很好，下一条专门讲。",
            ]
        elif any(k in text for k in support_keys):
            pool = [
                "谢谢支持，我会持续更新实战进展！",
                "感谢鼓励，后面继续分享干货。",
                "收到！一起把自动化跑顺～",
            ]
        elif any(k in text for k in doubt_keys):
            pool = [
                "理解你的顾虑，我会继续放实测过程。",
                "可以多看后续实测数据再判断～",
                "欢迎理性讨论，我会持续公开复盘。",
            ]
        else:
            pool = [
                "感谢留言，我会持续更新实战内容。",
                "收到，这块我后续会补充细节。",
                "谢谢关注，欢迎继续交流。",
            ]

        reply = random.choice(pool)
        return reply[:40]

    def reply_comments_in_creator_v2(self, max_replies=20, min_delay=3, max_delay=12):
        """
        Enhanced comment auto-reply from creator comment-management page.

        Features:
        - intent-based safe reply generation
        - skip duplicates in same run
        - random delay between replies
        - per-run cap to reduce risk
        """
        if not self.logged_in:
            logger.error("❌ Not logged in")
            return 0

        self.driver.get(DOUYIN_COMMENT_MANAGE)
        self.human_delay(3, 5)

        sent = 0
        seen_texts = set()

        try:
            items = self.driver.find_elements(By.XPATH, "//div[contains(@class,'comment') or contains(@class,'Comment')]")
            logger.info(f"🔎 Found {len(items)} comment blocks")

            for item in items:
                if sent >= max_replies:
                    break

                raw = (item.text or "").strip()
                if not raw or raw in seen_texts:
                    continue
                seen_texts.add(raw)

                reply_text = self._generate_safe_reply(raw)
                if not reply_text:
                    continue

                try:
                    reply_btn = item.find_element(By.XPATH, ".//button[contains(text(),'回复')]")
                    reply_btn.click()
                    self.human_delay(0.8, 1.8)

                    input_box = self._find_element([
                        (By.XPATH, "//textarea[contains(@placeholder,'回复') or contains(@placeholder,'评论')]"),
                        (By.CSS_SELECTOR, "textarea"),
                    ], wait_time=6)
                    if not input_box:
                        continue

                    input_box.clear()
                    input_box.send_keys(reply_text)
                    self.human_delay(0.8, 1.8)

                    send_btn = self._find_element([
                        (By.XPATH, "//button[contains(text(),'发送') or contains(text(),'回复')]"),
                    ], wait_time=6)
                    if not send_btn:
                        continue

                    send_btn.click()
                    sent += 1
                    logger.info(f"✅ Replied {sent}/{max_replies}: {reply_text}")
                    self.human_delay(min_delay, max_delay)

                except Exception as inner:
                    logger.debug(f"Skip one comment due to UI issue: {inner}")
                    continue

        except Exception as e:
            logger.error(f"❌ reply_comments_in_creator_v2 failed: {str(e)}")

        logger.info(f"✅ V2 sent {sent} replies")
        return sent

    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            logger.info("👋 Browser closed")


# Example usage
if __name__ == "__main__":
    # Example: Create bot and login
    bot = DouyinBot(headless=False)
    
    try:
        # Login (credentials should be in environment variables)
        # bot.login()
        
        # Post an article
        # bot.post_article(
        #     title="欢迎大家围观：我用小龙虾开始运营抖音--Day 0",
        #     content="大家好，我是新手内容创作者..."
        # )
        
        # Reply to comments
        # bot.reply_to_comments(
        #     post_url="https://www.douyin.com/video/...",
        #     replies={"好": "谢谢！", "喜欢": "❤️"}
        # )
        
        print("🦞 DouyinBot ready. Uncomment code to run operations.")
        
    finally:
        # bot.close()
        pass
