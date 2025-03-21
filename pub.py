import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


def create_android_driver():
    capabilities = dict(
        platformName="Android",
        automationName="uiautomator2",
        deviceName="Android",
        appPackage="com.tencent.mp",
        appActivity="com.tencent.mp.feature.launcher.ui.LauncherActivity",
        language="zh",
        locale="CN",
        uiautomator2ServerInstallTimeout=60000,
        noReset=True,
    )

    appium_server_url = "http://localhost:4723"
    driver = webdriver.Remote(
        appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities)
    )
    return driver


def publish(title):
    driver = create_android_driver()
    time.sleep(5)
    el = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="发表"]')
    el.click()
    el = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="草稿"]')
    el.click()
    time.sleep(3)
    el = driver.find_element(
        by=AppiumBy.XPATH, value=f'//*[contains(@text, "{title}")]'
    )
    el.click()

    time.sleep(3)
    el = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="下一步"]')
    el.click()

    time.sleep(3)
    el = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="发表"]')
    el.click()

    time.sleep(3)
    el = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="发表"]')
    el.click()
