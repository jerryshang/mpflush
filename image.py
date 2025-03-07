import os
import re
import csv
import hashlib
import requests

BASE_URL = "https://smms.app/api/v2"


def upload_html_images(html, article_dir, token):
    image_urls = re.findall(r"src=[\"']?([^\"']+)", html)

    for url in image_urls:
        if url.startswith("http"):
            continue
        image_path = url
        if not os.path.exists(os.path.join(article_dir, image_path)):
            continue

        remote_path = upload_image(image_path, article_dir, token)
        html = html.replace(url, remote_path)
    return html


def upload_image(image_path, article_dir, token):
    image_hash = hashlib.md5(
        open(os.path.join(article_dir, image_path), "rb").read()
    ).hexdigest()
    meta_path = os.path.join(article_dir, "image_meta.csv")
    if not os.path.exists(meta_path):
        with open(meta_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["hash", "local_path", "remote_path"])
    with open(meta_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == image_hash and row[2] != "":
                print("使用已有图床链接", row[2])
                return row[2]
    # upload image logic here

    # curl -X POST https://smms.app/api/v2/profile --header "Authorization: cvWulYsBFguOYbSjBuIQhvM3Clq1FCS7"
    # response = requests.post(
    #     BASE_URL + "/profile",
    #     headers={"Authorization": token},
    # )
    # print(response)
    # if response.status_code != 200:
    #     raise ValueError("check failed")

    response = requests.post(
        BASE_URL + "/upload",
        headers={"Authorization": token},
        files={"smfile": open(os.path.join(article_dir, image_path), "rb")},
    )

    if response.status_code != 200:
        raise ValueError("check failed")

    remote_path = response.json()["data"]["url"]
    print("图床图片链接", remote_path)

    with open(meta_path, "a") as f:
        writer = csv.writer(f)
        writer.writerow([image_hash, image_path, remote_path])
    return remote_path
