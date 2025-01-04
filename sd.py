from diffusers import StableDiffusionPipeline
from diffusers import DPMSolverMultistepScheduler

from pathlib import Path
dir = str(Path.home())

from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker
from transformers import CLIPImageProcessor
from glob import glob
base_path = f"{dir}/.cache/huggingface/hub/models--stable-diffusion-v1-5--stable-diffusion-v1-5/snapshots/*"
snapshot_folder = glob(base_path)[0]
config_path = f"{snapshot_folder}/feature_extractor/preprocessor_config.json"

import torch

prompt = "bright colours, three sisters, eighteen year old, left one red hair, medium length bouncy curls, rosy cheeks, golden eyes, smiling, dresses in a feminine, pretty way; middle one long black hair, brown eyes, pale skin, dresses casually; right one short blue hair, purple eyes, blushing, dresses elegantly; school uniforms, pretty girls, anime style"

class Art:
    def __init__(self):
        self.negative = "nsfw, nude, deformities, deformed features, deformed faces, mutations, mutated features, extra arms, extra limbs, extra fingers, extra hands, mutated hands, poorly drawn hands, cloned face, duplicate, extra fingers, fused fingers, too many fingers, children, minors, more than three characters, multiple characters, words"

        self.default_height = 512
        self.default_width = 912
        self.num_steps = 25
        self.resolutions = [(640, 360), (856, 480), (1024, 576), (1280, 720), (1920, 1080)]

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(self.device)
        self.dtype = torch.float32
        if self.device == "cuda":
            # torch.backends.cuda.matmul.allow_tf32 = True
            self.dtype = torch.bfloat16
            self.default_height = 576
            self.default_width = 1024

        self.pipeline = StableDiffusionPipeline.from_single_file(
            "https://huggingface.co/mdl-mirror/dark-sushi-mix/blob/main/darkSushiMixMix_darkerPruned.safetensors", 
            torch_dtype=self.dtype, 
            safety_checker=StableDiffusionSafetyChecker.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5",subfolder='safety_checker'),
            feature_extractor=CLIPImageProcessor.from_json_file(config_path),
        ).to(self.device)
        self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(self.pipeline.scheduler.config)

    def setValues(self, resolution, steps, deform):
        res = self.resolutions[resolution - 1]
        self.default_height = res[1]
        self.default_width = res[0]
        if self.device == "cuda":
            if deform:
                torch.backends.cuda.matmul.allow_tf32 = True
            else:
                torch.backends.cuda.matmul.allow_tf32 = False
        self.num_steps = steps
        print(torch.backends.cuda.matmul.allow_tf32)

    def generate_scene(self, prompt):
        print(prompt)
        print("generating...")
        results = self.pipeline(prompt=prompt, negative=self.negative, height=self.default_height, width=self.default_width, num_inference_steps=self.num_steps)
        return results.images[0]


# import os
# cwd = os.getcwd()
# img = generate_scene(prompt)
# img.save(f'{cwd}/static/test.png')