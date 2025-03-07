# flush some rubbish to wechat public account

## prequisites

## for mac only now

## python3

## gemini developer token

https://ai.google.dev/gemini-api/docs/sdks

## pinokio with fooocus-api

https://pinokio.computer/

https://github.com/rimsila/fooocus-API-pinokio

## a standalone chrome

https://developer.chrome.com/blog/chrome-for-testing/

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


```shell
python flush.py 提示词
```