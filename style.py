import os
import time
import re
import markdown
import markdown.extensions.meta
import css_inline

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def get_h1_headers(markdown_string):
    md = markdown.Markdown(extensions=["markdown.extensions.toc"])
    md.convert(markdown_string)
    toc = md.toc_tokens
    h1_headers = [header["name"] for header in toc if header["level"] == 1]
    return h1_headers


def read_md(file_name):
    with open(file_name, "r") as f:
        markdown_text = f.read()

        title = get_h1_headers(markdown_text)[0] or ""

        lines = markdown_text.splitlines()

        for idx, line in enumerate(lines):
            if re.match(r"^#[^#].*", line):
                lines.pop(idx)
                break

        markdown_text = "\n".join(lines)

        md = markdown.Markdown(extensions=["meta"])
        html = md.convert(markdown_text)
        return md.Meta, html, title


def copy_content(html):
    options = Options()
    options.binary_location = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "chrome/mac_arm-134.0.6998.35/chrome-mac-arm64/Google Chrome for Testing.app",
    )

    cwd = os.path.abspath(os.getcwd())
    css = open(os.path.join(cwd, "style.css"), "r").read()

    html = """<html>
<head>
    <style>{css}</style>
</head>
<body>
    {html}
</body>
</html>""".format(
        html=html, css=css
    )

    html = css_inline.inline(html)

    with open("tmp.html", "w") as f:
        f.write(html)

    try:
        driver = webdriver.Chrome(options=options)
        driver.get("file://" + os.path.join(cwd, "tmp.html"))

        time.sleep(3)

        root_element = driver.find_element(By.TAG_NAME, "body")
        root_element.send_keys(Keys.COMMAND, "a")
        root_element.send_keys(Keys.COMMAND, "c")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pass
        # driver.quit()  # Close the browser
