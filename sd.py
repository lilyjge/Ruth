from diffusers import StableDiffusionPipeline
from diffusers import DPMSolverMultistepScheduler

from pathlib import Path
dir = str(Path.home())

from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker
from transformers import CLIPImageProcessor
safety_checker = StableDiffusionSafetyChecker.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5",subfolder='safety_checker').half()
safety_feature_extractor = CLIPImageProcessor.from_json_file(f"{dir}/.cache/huggingface/hub/models--stable-diffusion-v1-5--stable-diffusion-v1-5/snapshots/451f4fe16113bff5a5d2269ed5ad43b0592e9a14/feature_extractor/preprocessor_config.json")

import torch

prompt = "bright colours, three sisters, eighteen year old, left one red hair, medium length bouncy curls, rosy cheeks, golden eyes, smiling, dresses in a feminine, pretty way; middle one long black hair, brown eyes, pale skin, dresses casually; right one short blue hair, purple eyes, blushing, dresses elegantly; school uniforms, pretty girls, anime style"
negative = "nsfw, nude, deformities, deformed features, mutations, mutated features, extra arms, extra limbs, extra fingers, mutated hands, poorly drawn hands, cloned face, duplicate, extra fingers, fused fingers, too many fingers, children, minors, more than three characters, words"

default_height = 512
default_width = 912

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
dtype = torch.float32
if device == "cuda":
    torch.backends.cuda.matmul.allow_tf32 = True
    dtype = torch.bfloat16
    default_height = 576
    default_width = 1024

pipeline = StableDiffusionPipeline.from_single_file(
    "https://huggingface.co/mdl-mirror/dark-sushi-mix/blob/main/darkSushiMixMix_darkerPruned.safetensors", 
    torch_dtype=dtype, 
    safety_checker=safety_checker,
    feature_extractor=safety_feature_extractor,
).to(device)
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)

def generate_scene(prompt, negative=negative, height=default_height, width=default_width, num_inference_steps=20):
    print("generating...")
    results = pipeline(prompt=prompt, negative_prompt=negative, height=height, width=width, num_inference_steps=num_inference_steps)
    return results.images[0]


# import os
# cwd = os.getcwd()
# img = generate_scene(prompt)
# img.save(f'{cwd}/static/test.png')