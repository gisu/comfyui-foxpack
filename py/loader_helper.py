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
          "max": 5
        }),
        "vae_sdxl": (folder_paths.get_filename_list("vae"),),
        "vae_sd15": (folder_paths.get_filename_list("vae"),),
        "vae_sd3": (folder_paths.get_filename_list("vae"),),
        "vae_flux": (folder_paths.get_filename_list("vae"),),
        "vae_type_select": (["base","baked", "sdxl", "sd15", "sd3", "flux"],
          {
            "default": "base",
        })
      },
    }

  # version 1: baked, 2: sdxl, 3: sd15
  RETURN_TYPES = ("VAE",)
  RETURN_NAMES = ("vae",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Loader"

  def main(self, checkpoint_vae, vae_type, vae_sdxl, vae_sd15, vae_sd3, vae_flux, vae_type_select):
    vae_name = {
      1: vae_sdxl,
      2: vae_sd15,
      3: vae_sd3,
      4: vae_flux,
    }.get(vae_type, checkpoint_vae)

    if (vae_type_select != "base"):
      if (vae_type_select == "baked"):
        return (
          checkpoint_vae,
        )

      vae_path = folder_paths.get_full_path("vae", vae_name)
      sd = comfy.utils.load_torch_file(vae_path)
      vae = comfy.sd.VAE(sd=sd)

      return ( vae, )

    if (vae_type == 0):
      return ( checkpoint_vae, )

    vae_path = folder_paths.get_full_path("vae", vae_name)
    sd = comfy.utils.load_torch_file(vae_path)
    vae = comfy.sd.VAE(sd=sd)

    return (
      vae,
    )
