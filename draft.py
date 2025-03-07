import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def draft(title, summary):
    options = Options()
    options.binary_location = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "chrome/mac_arm-134.0.6998.35/chrome-mac-arm64/Google Chrome for Testing.app",
    )
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if driver.current_url.startswith("https://mp.weixin.qq.com/cgi-bin/home"):
            break

    home_link = driver.find_element(By.LINK_TEXT, "首页")
    home_link.click()

    create_link = driver.find_element(By.CLASS_NAME, "new-creation__menu-item")
    create_link.click()

    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if driver.current_url.startswith("https://mp.weixin.qq.com/cgi-bin/appmsg"):
            break

    title_input = driver.find_element(By.ID, "title")
    title_input.send_keys(Keys.COMMAND, "a")
    title_input.send_keys(title)

    author_input = driver.find_element(By.ID, "author")
    author_input.send_keys("小梁教授")

    iframe = driver.find_element(By.ID, "ueditor_0")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(iframe))
    if iframe.tag_name == "iframe":

        driver.switch_to.frame(iframe)

        content_input = driver.find_element(By.CLASS_NAME, "rich_media_content")
        content_input.send_keys(Keys.COMMAND, "a")
        content_input.send_keys(Keys.COMMAND, "v")

        driver.switch_to.default_content()
    else:
        content_input = driver.find_element(
            By.XPATH,
            "//div[@contenteditable='true' and parent::*[contains(@class, 'rich_media_content')]]",
        )
        content_input.click()
        content_input.send_keys(Keys.COMMAND, "a")
        content_input.send_keys(Keys.COMMAND, "v")

    time.sleep(3)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    summary_input = driver.find_element(By.ID, "js_description")
    summary_input.send_keys(summary)
    time.sleep(3)

    # div_origin = driver.find_element(By.XPATH, "//div[text()='原创']")
    hover_image = driver.find_element(By.ID, "js_cover_area")
    # ActionChains(driver).scroll_to_element(div_origin).scroll_by_amount(0, 100)

    ActionChains(driver).move_to_element(hover_image).perform()
    menu_choose = driver.find_element(By.LINK_TEXT, "从正文选择")
    menu_choose.click()
    time.sleep(1)

    image_items = driver.find_elements(By.CLASS_NAME, "appmsg_content_img_item")
    image_item = image_items[0]
    image_item.click()
    time.sleep(2)

    menu_next = driver.find_element(By.XPATH, "//*[text()='下一步']")
    ActionChains(driver).move_to_element(menu_next).click().perform()
    time.sleep(2)

    button_confirm = driver.find_element(By.XPATH, "//button[text()='确认']")
    ActionChains(driver).move_to_element(button_confirm).click().perform()
    time.sleep(3)

    # save it!
    submit_button_wrapper = driver.find_element(By.ID, "js_submit")
    submit_button = submit_button_wrapper.find_element(By.TAG_NAME, "button")
    submit_button.click()

    time.sleep(10)

    # parent = driver.window_handles[0]
    # child = driver.window_handles[1]
    # driver.switch_to.window(child)
    driver.close()

    # driver.switch_to.window(parent)
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if driver.current_url.startswith("https://mp.weixin.qq.com/cgi-bin/home"):
            break

    home_link = driver.find_element(By.LINK_TEXT, "首页")
    home_link.click()
    try:
        draft_menu = driver.find_element(By.XPATH, "//span[contains(text(), '草稿箱')]")
        draft_menu.click()
    except Exception:
        content_management_menu = driver.find_element(
            By.XPATH, "//span[contains(text(), '内容管理')]"
        )
        content_management_menu.click()
        draft_menu = driver.find_element(By.XPATH, "//span[contains(text(), '草稿箱')]")
        draft_menu.click()
