from diffusers import StableDiffusionPipeline
from diffusers import DPMSolverMultistepScheduler

from pathlib import Path
dir = str(Path.home())

from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker
from transformers import CLIPImageProcessor
safety_checker = StableDiffusionSafetyChecker.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5",subfolder='safety_checker')
from glob import glob
base_path = f"{dir}/.cache/huggingface/hub/models--stable-diffusion-v1-5--stable-diffusion-v1-5/snapshots/*"
snapshot_folder = glob(base_path)[0]
config_path = f"{snapshot_folder}/feature_extractor/preprocessor_config.json"
safety_feature_extractor = CLIPImageProcessor.from_json_file(config_path)

import torch

prompt = "bright colours, three sisters, eighteen year old, left one red hair, medium length bouncy curls, rosy cheeks, golden eyes, smiling, dresses in a feminine, pretty way; middle one long black hair, brown eyes, pale skin, dresses casually; right one short blue hair, purple eyes, blushing, dresses elegantly; school uniforms, pretty girls, anime style"
negative = "nsfw, nude, deformities, deformed features, deformed faces, mutations, mutated features, extra arms, extra limbs, extra fingers, mutated hands, poorly drawn hands, cloned face, duplicate, extra fingers, fused fingers, too many fingers, children, minors, more than three characters, multiple characters, words"

default_height = 512
default_width = 912
num_steps = 25
resolutions = [(640, 360), (854, 480), (1024, 576), (1280, 720), (1920, 1080)]

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
dtype = torch.float32
if device == "cuda":
    # torch.backends.cuda.matmul.allow_tf32 = True
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

def setValues(resolution, steps, deform):
    res = resolutions[resolution - 1]
    default_height = res[1]
    default_width = res[0]
    if device == "cuda" and deform:
        torch.backends.cuda.matmul.allow_tf32 = True
    num_steps = steps

def generate_scene(prompt, negative=negative, height=default_height, width=default_width, num_inference_steps=num_steps):
    print("generating...")
    results = pipeline(prompt=prompt, negative_prompt=negative, height=height, width=width, num_inference_steps=num_inference_steps)
    return results.images[0]


# import os
# cwd = os.getcwd()
# img = generate_scene(prompt)
# img.save(f'{cwd}/static/test.png')