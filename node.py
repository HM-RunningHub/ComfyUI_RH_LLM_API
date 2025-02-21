from openai import OpenAI
import time
from PIL import Image
import numpy as np
import base64
import os

def encode_image_b64(ref_image):
    i = 255. * ref_image.cpu().numpy()[0]
    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

    lsize = np.max(img.size)
    factor = 1
    while lsize / factor > 2048:
        factor *= 2
    img = img.resize((img.size[0] // factor, img.size[1] // factor))

    image_path = f'{time.time()}.webp'
    img.save(image_path, 'WEBP')

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # print(img_base64)
    os.remove(image_path)
    return base64_image

class RH_LLMAPI_Node():

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_baseurl": ("STRING", {"multiline": True}),
                "api_key": ("STRING", {"default": ""}),
                "model": ("STRING", {"default": ""}),
                "role": ("STRING", {"multiline": True, "default": "You are a helpful assistant"}),
                "prompt": ("STRING", {"multiline": True, "default": "Hello"}),
                "temperature": ("FLOAT", {"default": 0.6}),
                "seed": ("INT", {"default": 100}),
            },
            "optional": {
                "ref_image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("describe",)
    FUNCTION = "rh_run_llmapi"
    CATEGORY = "Runninghub"

    def rh_run_llmapi(self, api_baseurl, api_key, model, role, prompt, temperature, seed, ref_image=None):

        client = OpenAI(api_key=api_key, base_url=api_baseurl)
        if ref_image is None:
            messages = [
                {'role': 'system', 'content': f'{role}'},
                {'role': 'user', 'content': f'{prompt}'},
            ]
        else:
            base64_image = encode_image_b64(ref_image)
            messages = [
                {'role': 'system', 'content': f'{role}'},
                {'role': 'user', 
                 'content': [
                        {
                            "type": "text",
                            "text": f"{prompt}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                    ]},
            ]
        completion = client.chat.completions.create(model=model, messages=messages, temperature=temperature)
        if completion is not None and hasattr(completion, 'choices'):
            prompt = completion.choices[0].message.content
        else:
            prompt = 'Error'
        return (prompt,)