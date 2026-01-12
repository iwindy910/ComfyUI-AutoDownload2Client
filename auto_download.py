import torch
import numpy as np
from PIL import Image
import io
import base64
import datetime
from server import PromptServer

class AutoDownloadNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI2Client"})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "transmit_to_client"
    OUTPUT_NODE = True
    CATEGORY = "custom_nodes/Image"

    def transmit_to_client(self, image, filename_prefix):
        ui_images = []
        now = datetime.datetime.now()
        timestamp = now.strftime("%y_%m%d_%H%M_%S")
        
        for index, img_tensor in enumerate(image):
            i = 255. * img_tensor.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_bytes = buffer.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            PromptServer.instance.send_sync("auto_download_direct", {
                "data": img_base64,
                "filename": f"{filename_prefix}_{timestamp}.png"
            })
            
        return {"ui": {"images": []}}

NODE_CLASS_MAPPINGS = {"AutoDownloadNode": AutoDownloadNode}
NODE_DISPLAY_NAME_MAPPINGS = {"AutoDownloadNode": "AutoDownload2Client"}
