import comfy.samplers
import folder_paths
import os
import re

def clamp(value, min_value, max_value):
  return max(min_value, min(value, max_value))

def numeric_range(value):
  if "-" in value:
    parts = value.split("-")
    return (float(parts[0]), float(parts[1]))
  return (float(value), float(value))

def clamp_in_list(value, lst):
  if value in list(lst):
    return value
  return lst[0]

def extract_setup(checkpoint_setups, cleanup_name, default_setup, delmiter = "/"):
  index = checkpoint_setups.find(cleanup_name)
  return_string = ""

  if index == -1:
    return default_setup

  substring = checkpoint_setups[index + len(cleanup_name):]

  if substring.startswith('='):
    substring = substring[1:]

    if substring.startswith('"'):
      end_quote = substring.find('"', 1)
      if end_quote != -1:
        return_string = substring[1:end_quote]
      else:
        return_string = default_setup
    else:
      space_index = substring.find(" ")
      if space_index != -1:
        return_string = substring[:space_index]
      else:
        return_string = substring
  else:
    return_string = default_setup

  settings = return_string.split(delmiter)

  return settings

class CheckpointSelector:
  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "checkpoint_name": (folder_paths.get_filename_list("checkpoints"),),
      }
    }

  RETURN_TYPES = (folder_paths.get_filename_list("checkpoints"), "STRING")
  RETURN_NAMES = ("ckpt_name", "name_str")
  CATEGORY = "Foxpack/Smart Sampler Setup"
  FUNCTION = "main"

  def main(self, checkpoint_name):
    cleanup_name = os.path.splitext(os.path.basename(checkpoint_name))[0]

    return (
      checkpoint_name,
      str(cleanup_name)
    )


class SetupSelector:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "checkpoint_name": ("STRING", {
              "forceInput": True,
              "multiline": False
            }),
            "checkpoint_setups": ("STRING", {
              "forceInput": True,
              "multiline": True
            }),
            "setup_prefix": ("STRING", {
              "default": "!",
              "multiline": False
            }),
            "delmiter": ("STRING", {
              "default": "/",
              "multiline": False
            }),
            "default_setup": ("STRING", {
              "default": "5/20/karras/dpmpp_2m",
              "multiline": False
            }),
            "default_meta": ("STRING", {
              "default": "0,-2,0",
              "multiline": False
            })
        }
    }

  RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING","STRING", "LIST", "STRING")
  RETURN_NAMES = ("set_cfg", "set_steps", "set_scheduler", "set_sampler", "setup_text", "setup", "meta")

  FUNCTION = "main"
  # OUTPUT_NODE = True

  CATEGORY = "Foxpack/Smart Sampler Setup"

  def main(self, checkpoint_name, checkpoint_setups, setup_prefix, delmiter, default_setup, default_meta):
    return_string = ""
    prefixed_name = str(setup_prefix) + str(checkpoint_name)

    index = checkpoint_setups.find(prefixed_name)

    if index != -1:
      if checkpoint_setups[index + len(prefixed_name)] == '=':
        if checkpoint_setups[index + len(prefixed_name) + 1] == '"':
          start_quote = index + len(prefixed_name) + 2
          end_quote = checkpoint_setups.find('"', start_quote + 1)
          if end_quote != -1:
            return_string = checkpoint_setups[start_quote:end_quote]
            print(return_string)
        else:
          space_index = checkpoint_setups.find(" ", index + len(prefixed_name))
          if space_index != -1:
            return_string = checkpoint_setups[index + len(prefixed_name):space_index]
          else:
            return_string = checkpoint_setups[index + len(prefixed_name):]
      else:
        return_string = prefixed_name[1:]

    if return_string == "":
      return_string = default_setup

    if return_string.startswith("="):
      return_string = return_string[1:]

    settings = return_string.split(delmiter)

    if (len(settings) < 5):
        # meta infos: version (0:sdxl, 1:sd15), clip, vae (0: baked, 1: sdxl load vae, 2: sd15 load vae)
        meta = default_meta
    else:
        meta = settings[4]

    setup = list(settings)
    setup_text = f"cfg: {settings[0]} | steps: {settings[1]} | scheduler: {settings[2]} | sampler: {settings[3]}"

    return (
      str(settings[0]),
      str(settings[1]),
      str(settings[2]),
      str(settings[3]),
      str(setup_text),
      list(setup),
      str(meta)
    )
class CheckpointMetaExtractor:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "meta": ("STRING", {
          "forceInput": True,
          "multiline": False
        }),
      }
    }

  RETURN_TYPES = ("INT", "INT", "INT")
  RETURN_NAMES = ("version", "clip", "vae baked?")

  CATEGORY = "Foxpack/Smart Sampler Setup"

  FUNCTION = "metaFun"

  def metaFun(self, meta):
    meta = meta.split(",")
    version = meta[0]
    clip = int(meta[1])
    vae = meta[2]

    return (
      int(version),
      int(-abs(clip)),
      int(vae)
    )

class BaseSamplerSetup:
  def __init__(self):
    pass

  @classmethod

  def INPUT_TYPES(s):
    return {
      "required": {
        "setup": ("LIST", {
          "forceInput": True
        }),
        "cfg": ("FLOAT", {
          "default": 1.0,
          "min": 0.0,
          "max": 16.0,
          "step": 0.1,
          "display": "number"
        }),
        "steps": ("INT", {
          "default": 5,
          "min": 1,
          "max": 100,
          "step": 1,
          "display": "number"
        }),
        "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
        "sampler": (comfy.samplers.KSampler.SAMPLERS,),
      }
    }

  RETURN_TYPES = ("FLOAT", "INT", "STRING", "STRING", "STRING", "LIST")
  RETURN_NAMES = ("cfg", "steps", "scheduler", "sampler", "setup_text", "selected_setup")
  FUNCTION = "main"

  def main(self, setup, cfg, steps, scheduler, sampler):

    cfg_range = numeric_range(setup[0])
    clamp_cfg = clamp(cfg, cfg_range[0], cfg_range[1])

    steps_range = numeric_range(setup[1])
    clamp_steps = clamp(steps, steps_range[0], steps_range[1])

    clamp_scheduler = clamp_in_list(scheduler, setup[2].split(","))
    clamp_sampler = clamp_in_list(sampler, setup[3].split(","))

    selected_setup = [clamp_cfg, clamp_steps, clamp_scheduler, clamp_sampler]
    setup_text = f"cfg: {clamp_cfg} | steps: {clamp_steps} | scheduler: {clamp_scheduler} | sampler: {clamp_sampler}"

    return (
      float(clamp_cfg),
      int(clamp_steps),
      str(clamp_scheduler),
      str(clamp_sampler),
      str(setup_text),
      list(selected_setup)
    )

  CATEGORY = "Foxpack/Smart Sampler Setup"


class OverrideSamplerSetup:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "setup": ("LIST", {
                  "forceInput": True
                }),
                "override": ("BOOLEAN", {"default": False}),
                "cfg": ("FLOAT", {
                  "default": 1.0,
                  "min": 0.0,
                  "max": 16.0,
                  "step": 0.1,
                  "display": "number"
                }),
                "steps": ("INT", {
                  "default": 5,
                  "min": 1,
                  "max": 100,
                  "step": 1,
                  "display": "number"
                }),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
                "sampler": (comfy.samplers.KSampler.SAMPLERS,),
            },
        }

    RETURN_TYPES = ("FLOAT","INT", comfy.samplers.KSampler.SAMPLERS,
                  comfy.samplers.KSampler.SCHEDULERS, "STRING")
    RETURN_NAMES = ("cfg", "steps", "sampler", "scheduler", "setup_text")
    FUNCTION = "main"

    def main(self, override, setup, steps, cfg, sampler, scheduler):
      cfg_output = cfg if override else setup[0]
      steps_output = steps if override else setup[1]
      scheduler_output = scheduler if override else setup[2]
      sampler_output = sampler if override else setup[3]

      setup_text = f"cfg: {cfg_output} | steps: {steps_output} | scheduler: {scheduler_output} | sampler: {sampler_output}"

      return (
        float(cfg_output),
        int(steps_output),
        sampler_output,
        scheduler_output,
        str(setup_text)
      )

    CATEGORY = "Foxpack/Smart Sampler Setup"

class Complete_Setup:
  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "checkpoint_setups": ("STRING", {
          "forceInput": True,
          "multiline": True
        }),
        "checkpoint_name": (folder_paths.get_filename_list("checkpoints"),),
        "cfg": ("FLOAT", {
          "default": 5.0,
          "min": 0.0,
          "max": 16.0,
          "step": 0.1,
          "display": "number"
        }),
        "steps": ("INT", {
          "default": 20,
          "min": 1,
          "max": 100,
          "step": 1,
          "display": "number"
        }),
        "scheduler": (comfy.samplers.KSampler.SCHEDULERS, {
          "default": "karras"
        }),
        "sampler": (comfy.samplers.KSampler.SAMPLERS, {
          "default": "dpmpp_2m"
        }),
        "override": ("BOOLEAN", {"default": False}),
        "cfg_override": ("FLOAT", {
          "default": 5.0,
          "min": 0.0,
          "max": 16.0,
          "step": 0.1,
          "display": "number"
        }),
        "steps_override": ("INT", {
          "default": 20,
          "min": 1,
          "max": 100,
          "step": 1,
          "display": "number"
        }),
        "scheduler_override": (comfy.samplers.KSampler.SCHEDULERS, {
          "default": "karras"
        }),
        "sampler_override": (comfy.samplers.KSampler.SAMPLERS, {
          "default": "dpmpp_2m"
        }),
      },
      "optional": {
        "optional_setups": ("STRING", {
          "default": "",
          "multiline": True
        })
      }
    }

  RETURN_TYPES = (folder_paths.get_filename_list("checkpoints"),"STRING", "STRING", "INT", "INT", "INT", "FLOAT","INT", comfy.samplers.KSampler.SAMPLERS, comfy.samplers.KSampler.SCHEDULERS, "LIST", "STRING", "STRING")
  RETURN_NAMES = ("ckpt_name", "recommended_setup_str", "used_setup_str", "version", "clip", "vae_variant", "cfg", "steps", "sampler", "scheduler", "meta_list", "opt_setup_dict", "comb_sampler_settings")

  FUNCTION = "main"
  CATEGORY = "Foxpack/Smart Sampler Setup"

  def main(self, checkpoint_setups, checkpoint_name, cfg, steps, scheduler, sampler, override, cfg_override, steps_override, scheduler_override, sampler_override, optional_setups):
    cleanup_name = os.path.splitext(os.path.basename(checkpoint_name))[0]
    settings = ""
    selected_optional_setup = "{}"
    used_default_setup = False
    
    if (cleanup_name):
      pattern = rf'!{cleanup_name}:(.+)'
      pattern_optional = rf'!{cleanup_name}:(.+)'
  
      match = re.search(pattern, checkpoint_setups)
      match_optional = re.search(pattern_optional, optional_setups)
      
      if match:
        settings = match.group(1).split("/")
      else:
        pattern = rf'!DEFAULT:(.+)'
        match = re.search(pattern, checkpoint_setups)
        used_default_setup = True
        if match:
          settings = match.group(1).split("/")
        else:
          settings = ["5", "20", "karras", "dpmpp_2m", "0", "-2", "0"]

      if match_optional:
        selected_optional_setup = match_optional.group(1)

    # version 0 = sdxl, 1 = sd15, 2 = flux
    version = 0
    clip = -2
    vae_variant = 0

    version = settings[4]
    clip = int(settings[5])
    vae_variant = settings[6]

    vae_string = "baked" if vae_variant == 0 else "external"
    versionname = {
      "0": "sdxl",
      "1": "sd15",
      "2": "flux"
      }.get(version, "sdxl")

    used_default_setup_str = " (used default setup)" if used_default_setup else ""
    recommended_setup_str = f"Checkpoint ({versionname}): {cleanup_name}{used_default_setup_str}\ncfg: {settings[0]}, steps: {settings[1]}, scheduler: {settings[2]}, sampler: {settings[3]}\nvae: {vae_string}, clip: {clip}, version: {version}"
    
    cfg_range = numeric_range(settings[0])
    clamp_cfg = clamp(cfg, cfg_range[0], cfg_range[1])
    steps_range = numeric_range(settings[1])
    clamp_steps = clamp(steps, steps_range[0], steps_range[1])
    clamp_scheduler = clamp_in_list(scheduler, settings[2].split(","))
    clamp_sampler = clamp_in_list(sampler, settings[3].split(","))

    cfg_output = cfg_override if override else clamp_cfg
    steps_output = steps_override if override else clamp_steps
    scheduler_output = scheduler_override if override else clamp_scheduler
    sampler_output = sampler_override if override else clamp_sampler

    is_override = " (overridden settings)" if override else ""

    used_setup_str = f"Checkpoint ({versionname}): {cleanup_name}{is_override}\ncfg: {cfg_output}, steps: {int(steps_output)}, scheduler: {scheduler_output}, sampler: {sampler_output}"

    
    filename = f"%date_%seed_%counter_{versionname}"

    sampler_settings = f"{cfg_output},{int(steps_output)},{sampler_output},{scheduler_output}"

    meta_list = [
      checkpoint_name,
      filename,
      float(cfg_output),
      int(steps_output),
      sampler_output,
      scheduler_output
    ]

    return (
      checkpoint_name,
      recommended_setup_str,
      used_setup_str,
      int(version),
      int(-abs(clip)),
      int(vae_variant),
      float(cfg_output),
      int(steps_output),
      sampler_output,
      scheduler_output,
      meta_list,
      selected_optional_setup,
      sampler_settings
    )
