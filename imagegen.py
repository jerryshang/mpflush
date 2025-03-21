import torch

from diffusers import FluxPipeline

# from diffusers import DiffusionPipeline

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell", revision="refs/pr/1", torch_dtype=torch.bfloat16
).to("mps")

# pipe = DiffusionPipeline.from_pretrained(
#     "SimianLuo/LCM_Dreamshaper_v7", torch_dtype=torch.float32
# ).to("mps")

pipe.load_lora_weights("strangerzonehf/Flux-Midjourney-Mix2-LoRA")


pipe.enable_attention_slicing()

prompt = "MJ v6, A cute anime style sloth character wearing black robes with blue hood holding milkshake, the background is orange and yellow with Japanese patterns, cute face with big eyes and smiling mouth, digital art by Kawaii Anime Style, Artstation contest winner, official fanart of the original characters. In full body portrait, cute anime sloths in robe drinking colorful drinks, detailed face features, bright colors, fantasy character design, official fan artwork. In the style of an ultra-detailed character portrait."


out = pipe(
    prompt=prompt,
    guidance_scale=0.0,
    height=512,
    width=512,
    num_inference_steps=4,
    max_sequence_length=64,
).images[0]


# out = pipe(
#     prompt=prompt,
#     num_inference_steps=40,
#     guidance_scale=8.0,
#     lcm_origin_steps=4,
#     output_type="pil",
# ).images[0]


out.save("image.png")
