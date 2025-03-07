import os
import sys
import re
import datetime
from dotenv import load_dotenv

from style import read_md, copy_content
from image import upload_html_images
from content import generate_content_by_llama, generate_cover_image, generate_content
from draft import draft
from pub import publish

ACCOUNT = "articles"


def log(*args, **kwargs):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} ", end="")
    print(*args, **kwargs)


if __name__ == "__main__":
    load_dotenv()

    base_dir = None
    if len(sys.argv) > 1:
        timestr = datetime.datetime.now().strftime("%Y-%m-%d.%H_%M_%S")
        log(f"现在时间：{timestr}")
        base_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            ACCOUNT,
            timestr,
        )
        os.makedirs(base_dir, exist_ok=True)
        if os.getenv("GEMINI_API_KEY"):
            log(f"使用 Gemini 生成内容：{"".join(sys.argv[1:])}")
            content, image_prompt = generate_content(
                prompt="".join(sys.argv[1:]), api_key=os.getenv("GEMINI_API_KEY")
            )
        else:
            log(f"使用 Llama 生成内容：{"".join(sys.argv[1:])}")
            content, image_prompt = generate_content_by_llama(
                prompt="".join(sys.argv[1:])
            )

        log("使用 Fooocus 生成图片")
        image_url = generate_cover_image(image_prompt, base_dir)

        # inject some text after the first line matches as a markdown h1
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            if re.match(r"^#[^#].*", line):
                lines.insert(idx + 1, "![cover](cover.png)")
                content = "\n".join(lines)
                break

        with open(os.path.join(base_dir, "index.md"), "w") as f:
            f.write(content)

        log("内容生成完毕")
    else:
        log("处理最后一篇文章")
        folders = [
            x
            for x in os.listdir(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), ACCOUNT)
            )
            if re.match(r"\d{4}-\d{2}-\d{2}\.\d{2}_\d{2}_\d{2}", x)
        ]
        if len(folders) == 0:
            raise ValueError("No matched folder found under articles")
        else:
            base_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                ACCOUNT,
                sorted(folders)[-1],
            )

    file_name = os.path.join(base_dir, "index.md")
    log("解析 markdown 文件")
    meta, html, title = read_md(file_name)
    log("上传图片到图床")
    html = upload_html_images(html, base_dir, os.getenv("SM_MS_TOKEN"))
    log("应用自定义样式")
    content = copy_content(html)
    log("发布文章为草稿")
    draft(title, meta["summary"])
    log("发布文章")
    publish(title)
    log("完成")
