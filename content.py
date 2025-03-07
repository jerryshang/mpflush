import os
from google import genai
import requests
import json


def generate_content(prompt, api_key):
    try:
        client = genai.Client(api_key=api_key)
        # model = genai.GenerativeModel("gemini-1.5-flash")
        # model = genai.GenerativeModel("gemini-2.0-flash-exp")
        prompt = """
使用以下内容生成微信公众号文章，内容字数500-1000字左右，标题不超过20字，使用比较强烈语气的标题，摘要不多于120字：
{prompt}
返回数据中的 content 需要使用 markdown 格式。文章必须以h1开始。其它章节的要使用 h2 ，而不是用加重。同时根据文章内容生成不多于50单词的图像生成提示词，使用英文。除 image_prompt 需要使用英文外，其它内容都必须使用中文。
""".format(
            prompt=prompt
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": {
                    "required": [
                        "summary",
                        "content",
                        "image_prompt",
                    ],
                    "properties": {
                        "summary": {"type": "STRING"},
                        "content": {"type": "STRING"},
                        "image_prompt": {"type": "STRING"},
                    },
                    "type": "OBJECT",
                },
            },
        )
        resp = json.loads(response.text)
        return (
            """Summary:   {summary}
{content}""".format(
                summary=resp["summary"], content=resp["content"]
            ),
            resp["image_prompt"],
        )
    except Exception as e:
        print(f"Error generating text with Gemini: {e}")
        return None


def generate_cover_image(prompt, base_dir):
    json = """{
  "prompt": "__image_prompt__",
  "negative_prompt": "unrealistic, saturated, high contrast, big nose, painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label",
  "style_selections": [
    "Fooocus V2",
    "Fooocus Photograph",
    "Fooocus Negative"
  ],
  "performance_selection": "Speed",
  "aspect_ratios_selection": "892*384",
  "image_number": 1,
  "image_seed": -1,
  "sharpness": 2,
  "guidance_scale": 3,
  "base_model_name": "realisticStockPhoto_v20.safetensors",
  "refiner_model_name": "None",
  "refiner_switch": 0.5,
  "loras": [
    {
      "enabled": true,
      "model_name": "SDXL_FILM_PHOTOGRAPHY_STYLE_V1.safetensors",
      "weight": 0.25
    },
    {
      "enabled": true,
      "model_name": "None",
      "weight": 1
    },
    {
      "enabled": true,
      "model_name": "None",
      "weight": 1
    },
    {
      "enabled": true,
      "model_name": "None",
      "weight": 1
    },
    {
      "enabled": true,
      "model_name": "None",
      "weight": 1
    }
  ],
  "advanced_params": {
    "adaptive_cfg": 7,
    "adm_scaler_end": 0.3,
    "adm_scaler_negative": 0.8,
    "adm_scaler_positive": 1.5,
    "black_out_nsfw": false,
    "canny_high_threshold": 128,
    "canny_low_threshold": 64,
    "clip_skip": 2,
    "controlnet_softness": 0.25,
    "debugging_cn_preprocessor": false,
    "debugging_dino": false,
    "debugging_enhance_masks_checkbox": false,
    "debugging_inpaint_preprocessor": false,
    "dino_erode_or_dilate": 0,
    "disable_intermediate_results": false,
    "disable_preview": false,
    "disable_seed_increment": false,
    "freeu_b1": 1.01,
    "freeu_b2": 1.02,
    "freeu_enabled": false,
    "freeu_s1": 0.99,
    "freeu_s2": 0.95,
    "inpaint_advanced_masking_checkbox": true,
    "inpaint_disable_initial_latent": false,
    "inpaint_engine": "v2.6",
    "inpaint_erode_or_dilate": 0,
    "inpaint_respective_field": 1,
    "inpaint_strength": 1,
    "invert_mask_checkbox": false,
    "mixing_image_prompt_and_inpaint": false,
    "mixing_image_prompt_and_vary_upscale": false,
    "overwrite_height": -1,
    "overwrite_step": -1,
    "overwrite_switch": -1,
    "overwrite_upscale_strength": -1,
    "overwrite_vary_strength": -1,
    "overwrite_width": -1,
    "refiner_swap_method": "joint",
    "sampler_name": "dpmpp_2m_sde_gpu",
    "scheduler_name": "karras",
    "skipping_cn_preprocessor": false,
    "vae_name": "Default (model)"
  },
  "save_meta": true,
  "meta_scheme": "fooocus",
  "save_extension": "png",
  "save_name": "",
  "read_wildcards_in_order": false,
  "require_base64": false,
  "async_process": false,
  "webhook_url": ""
}"""
    json = json.replace("__image_prompt__", prompt).replace("\n", "")

    response = requests.post(
        "http://localhost:8888/v1/generation/text-to-image",
        data=json,
        headers={"Content-Type": "application/json", "Accept": "image/png"},
    )
    if response.status_code != 200:
        print(response)
        raise ValueError("Failed to generate image")
    with open(os.path.join(base_dir, "cover.png"), "wb") as f:
        f.write(response.content)


def generate_content_by_llama(prompt):
    json_str = """
{
  "model": "deepseek-r1:8b",
  "prompt": "__prompt__",
  "stream": false,
  "format":{
    "required": [
        "summary",
        "content",
        "image_prompt"
    ],
    "properties": {
        "summary": {"type": "string"},
        "content": {"type": "string"},
        "image_prompt": {"type": "string"}
    },
    "type": "object"
  }
}
    """.replace(
        "__prompt__",
        """
使用主题：“{prompt}”，生成一篇文章，字数800字左右。标题不超过20字，使用比较强烈语气。同时生成摘要，不多于100字。
返回数据中的 content 需要使用 markdown 格式：文章必须以h1开始。其它章节的要使用 h2。同时根据文章内容生成不多于10单词的文生图提示词。
""".format(
            prompt=prompt
        )
        .strip()
        .replace("\n", ""),
    )
    response = requests.post(
        "http://localhost:11434/api/generate",
        data=json_str,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    if response.status_code != 200:
        raise ValueError("Failed to generate content")
    resp = json.loads(json.loads(response.text)["response"])
    return (
        """Summary:   {summary}
{content}""".format(
            summary=resp["summary"], content=resp["content"]
        ),
        resp["image_prompt"],
    )
