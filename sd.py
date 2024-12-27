from diffusers import StableDiffusionPipeline
from diffusers import DPMSolverMultistepScheduler

import torch

prompt = "bright colours, three sisters, eighteen year old, left one red hair, bouncy curls, rosy cheeks, golden eyes, dresses in a feminine, pretty way; middle one long black hair, brown eyes, pale skin, dresses casually; right one short blue hair, purple eyes, dresses elegantly; school uniforms, pretty girls, anime style"
negative = "nsfw, nude, extra fingers, mutated hands, poorly drawn hands, cloned face, duplicate, extra fingers, fused fingers, too many fingers, children, minors"

device = "cuda" if torch.cuda.is_available() else "cpu"
pipeline = StableDiffusionPipeline.from_single_file(
    "https://huggingface.co/mdl-mirror/dark-sushi-mix/blob/main/darkSushiMixMix_darkerPruned.safetensors"
).to(device)
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)

def generate_scene(prompt, negative=negative, height=512, width=912, num_inference_steps=20):
    print("generating...")
    image = pipeline(prompt=prompt, negative_prompt=negative, height=height, width=width, num_inference_steps=num_inference_steps).images[0]
    return image