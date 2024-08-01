import folder_paths
import comfy.sd
import comfy.utils

class Universal_VAE_Loader:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "checkpoint_vae": ("VAE",),
        "vae_type": ("INT", {
          "default": 0,
          "forceInput": True,
          "min": 0,
          "max": 3
        }),
        "vae_sdxl": (folder_paths.get_filename_list("vae"),),
        "vae_sd15": (folder_paths.get_filename_list("vae"),),
      }
    }

  # version 1: baked, 2: sdxl, 3: sd15

  RETURN_TYPES = ("VAE",)
  RETURN_NAMES = ("vae",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Loader"

  def main(self, checkpoint_vae, vae_type, vae_sdxl, vae_sd15):
    vae_name = {
      0: checkpoint_vae,
      1: vae_sdxl,
      2: vae_sd15
    }.get(vae_type, checkpoint_vae)

    vae_path = folder_paths.get_full_path("vae", vae_name)
    sd = comfy.utils.load_torch_file(vae_path)
    vae = comfy.sd.VAE(sd=sd)

    return (
      vae,
    )