#!/usr/bin/env python3
"""
Test script for Douyin login with manual verification support.
"""

import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_chromedriver():
    """Start ChromeDriver manually."""
    driver_path = "/Users/openclaw_writer/.wdm/drivers/chromedriver/mac64/145.0.7632.117/chromedriver-mac-arm64/chromedriver"
    process = subprocess.Popen([driver_path, "--port=9515", "--allowed-origins=*"])
    time.sleep(2)
    return process

def create_driver():
    """Create Chrome WebDriver with manual ChromeDriver."""
    options = Options()
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=options)
    return driver

def main():
    print("🦞 抖音登录测试")
    print("=" * 50)
    
    driver = None
    cd_process = None
    
    try:
        # Start ChromeDriver manually
        print("🚀 启动 ChromeDriver...")
        cd_process = start_chromedriver()
        
        # Create driver
        print("🌐 创建浏览器...")
        driver = create_driver()
        print("✅ 浏览器启动成功！")
        
        # Navigate to Douyin
        print("📍 访问抖音...")
        driver.get("https://www.douyin.com")
        
        print("\n" + "=" * 50)
        print("📱 请在浏览器中完成登录：")
        print("   1. 点击登录按钮")
        print("   2. 输入手机号/密码 或 短信验证")
        print("   3. 完成滑块/验证码（如有）")
        print("=" * 50)
        
        # Wait for user to complete login
        input("\n✅ 登录完成后按回车继续...")
        
        # Check login status
        print("\n🔍 检查登录状态...")
        try:
            # Look for user avatar or profile indicators
            indicators = [
                "//img[contains(@class, 'avatar')]",
                "//div[contains(@class, 'user-info')]",
                "//span[contains(text(), '发布')]",
                "//button[contains(text(), '发布')]",
            ]
            
            logged_in = False
            for selector in indicators:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    if elements and elements[0].is_displayed():
                        logged_in = True
                        print(f"✅ 检测到登录状态 (selector: {selector})")
                        break
                except:
                    continue
            
            if logged_in:
                print("\n🎉 登录成功！")
                
                # Try to post
                print("\n📝 准备发布文章...")
                
                # Look for publish button
                try:
                    publish_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '发布')]"))
                    )
                    print("✅ 找到发布按钮")
                    
                    # Navigate to create page
                    driver.get("https://www.douyin.com/create")
                    time.sleep(3)
                    
                    print("\n📄 文章发布页面已打开")
                    print("⚠️  请手动填写内容并发布（自动化可能被检测）")
                    
                except Exception as e:
                    print(f"⚠️  发布按钮未找到：{e}")
                
                input("\n按回车关闭浏览器...")
            else:
                print("⚠️  未检测到登录状态")
                input("按回车关闭浏览器...")
                
        except Exception as e:
            print(f"❌ 检查失败：{e}")
            input("按回车关闭浏览器...")
            
    except KeyboardInterrupt:
        print("\n⚠️  中断")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
    finally:
        if driver:
            print("\n👋 关闭浏览器...")
            driver.quit()
        if cd_process:
            cd_process.terminate()
        
        print("✅ 完成")

if __name__ == "__main__":
    main()
