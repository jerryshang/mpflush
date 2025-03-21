# flush some rubbish to wechat public account

## 思路

0. TODO 收集爆款文章主题词
1. 自己脑暴提示词
2. 调用 gemini API 生成文章内容和图片的提示词
3. 用本地部署的 fooocus 生成主题图
4. 上传图片到免费图床
5. 格式化 markdown 为临时网页
6. 用 selenium 打开浏览器并拷贝
7. 用 selenium 打开浏览器并完成草稿
8. 用 appnium 打开公众号助手发布

## prequisites

### for mac only now

### python3

### gemini developer token

https://ai.google.dev/gemini-api/docs/sdks

### pinokio with fooocus-api

https://pinokio.computer/

https://github.com/rimsila/fooocus-API-pinokio

### a standalone chrome

https://developer.chrome.com/blog/chrome-for-testing/

### appnium

```shell
npm install -g appium

appium driver install uiautomator2
```

## config

install python dependencies

```shell
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

create `.env` file

```
GEMINI_API_KEY=your_gemini_api_key
SM_MS_TOKEN=your_sm_ms_token
CHROME_PATH=chrome/mac_arm-134.0.6998.35/chrome-mac-arm64/Google Chrome for Testing.app

```

## run

keep a chrome open, and the wechat page open

```shell
open "./chrome/mac_arm-134.0.6998.35/chrome-mac-arm64/Google Chrome for Testing.app" --args --remote-debugging-port=9222 --user-data-dir=$(pwd)/.chrome --lang=zh-CN
```

connect your android phone, enable debug mode, and open 订阅号助手 .

keep appnium running,

```shell
export ANDROID_HOME=~/Library/Android/sdk && appium
```

then run

```shell
python flush.py 提示词
```


# uv


```shell
uv init
uv add diffusers
uv add torch
uv add transformers
uv add accelerate
uv add sentencepiece
uv pip install protobuf
# for lora
uv add peft
```

```shell
uv run imagegen.py
```