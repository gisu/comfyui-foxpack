import torch
from nodes import EmptyLatentImage

class UniversalLatentHelper:
    def __init__(self):
      pass

    @classmethod
    def INPUT_TYPES(s):
        aspect_ratios = [
          "custom",
          "1:1",
          "3:2",
          "4:3",
          "5:8",
          "16:9",
          "1.85:1",
          "2:1",
          "2.39:1",
          "21:9",
          ]
      
        return {
            "required": {
                "version": ("STRING", {
                  "default": "xl",
                  "forceInput": True,
                }),
                "width": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "aspect_ratio": (aspect_ratios,),
                "format": (["landscape", "portrait"],),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
        
    RETURN_TYPES = ("INT", "INT", "INT", "LATENT")
    RETURN_NAMES = ("width", "height", "batch_size", "empty_latent")

    FUNCTION = "Latent_Size"

    CATEGORY = "Foxpack/Latent Helper"

    def Latent_Size(self, version, width, height, aspect_ratio, format, batch_size):
      ratios = {
        "custom": [[width, height],[width, height]],
        "1:1": [[512,512],[1024,1024]],
        "3:2": [[768,512],[1216,832]],
        "4:3": [[682,512],[1152,896]],
        "5:8": [[748,512],[1216,832]],
        "16:9": [[910,512],[1322,768]],
        "1.85:1": [[952,512],[1264,680]],
        "2:1": [[1024,512],[2048,1024]],
        "2.39:1": [[1224,512],[1587,664]],
        "21:9": [[1229,512],[1536,640]]
      }

      pick_ratio = ratios[aspect_ratio]
      pick_ration_for_version = pick_ratio[0] if version == "15" else pick_ratio[1]

      width, height = pick_ration_for_version[0], pick_ration_for_version[1]

      if (format == "portrait"):
          width, height = height, width

      height == height // 8
      width == width // 8

      print(f"Width: {width}, Height: {height}")

      latent = torch.zeros([batch_size, 4, height // 8, width // 8])
      
      return (
          int(width),
          int(height),
          int(batch_size),
          {"samples": latent},)