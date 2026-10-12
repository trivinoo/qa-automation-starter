"""
Appium Mobile Automation Reference Script (Python).
This script shows the standard structure used by QA mobile automation engineers
to drive Android or iOS devices using the Appium WebDriver.
"""

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time

def create_android_driver():
    """
    Configures Desired Capabilities / Appium Options.
    In real projects, Appium Server runs on http://127.0.0.1:4723
    """
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android Emulator"
    options.app_package = "com.demo.qaapp"
    options.app_activity = ".MainActivity"
    # Or to test mobile web:
    # options.set_capability('browserName', 'Chrome')

    # Connect to local Appium 2.x server
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    return driver

def run_mobile_login_test():
    """
    Example test flow:
    1. Wait for elements
    2. Input credentials
    3. Tap button
    4. Assert welcome message
    """
    print("[Appium] Connecting to mobile device via Appium Server...")
    # driver = create_android_driver()

    print("[Appium Flow Step 1] Find element by Accessibility ID or Resource ID")
    # username_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "username_field")
    # username_field.send_keys("student@test.com")

    print("[Appium Flow Step 2] Find password element and enter secret")
    # password_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "password_field")
    # password_field.send_keys("Password123!")

    print("[Appium Flow Step 3] Locate and click Login Button")
    # login_btn = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='LOG IN']")
    # login_btn.click()

    print("[Appium Flow Step 4] Assert presence of welcome text on screen")
    # welcome_banner = driver.find_element(AppiumBy.ID, "com.demo.qaapp:id/welcome_text")
    # assert "QA Student" in welcome_banner.text

    print("[Appium] Mobile test flow concept demonstrated successfully.")

if __name__ == "__main__":
    run_mobile_login_test()
