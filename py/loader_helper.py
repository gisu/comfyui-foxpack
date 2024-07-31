import folder_paths

class Universal_VAE_Loader:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "checkpoint_vae": ("VAE",),
        "version": ("INT", {
          "default": 0,
          "forceInput": True,
          "min": 0,
          "max": 2
        }),
        "vae_sdxl": (folder_paths.get_filename_list("vae"),),
        "vae_sd15": (folder_paths.get_filename_list("vae"),),
      }
    }

  # version 0: baked, 1: sdxl, 2: sd15

  RETURN_TYPES = ("VAE",)
  RETURN_NAMES = ("vae",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Loader"

  def main(self, checkpoint_vae, version, vae_sdxl, vae_sd15):
    if version == 0:
      return (
        checkpoint_vae,
      )
    elif version == 1:
      return (
        vae_sdxl,
      )
    elif version == 2:
      return (
        vae_sd15,
      )
    else:
      return (
        checkpoint_vae,
      )