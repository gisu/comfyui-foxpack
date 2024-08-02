import comfy.samplers
from nodes import CLIPTextEncode

class Step_Denoise:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "image_type": (["Free","Abstract", "Landscapes", "People"],
          {
            "default": "Landscapes",
          }),
        "free_rules": ("STRING", {
          "default": "0.7",
          "multiline": False,
        }),
        "abstract_rules": ("STRING", {
          "default": "0.60,0.55,0.45,0.40",
          "multiline": False,
        }),
        "landscape_rules": ("STRING", {
          "default": "0.50,0.45,0.40,0.35",
          "multiline": False,
        }),
        "people_rules": ("STRING", {
          "default": "0.35,0.30,0.25,0.20",
          "multiline": False,
        }),
      }
    }

  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("rules",)
  OUTPUT_NODE = True
  FUNCTION = "main"
  CATEGORY = "Foxpack/Upscale"

  def main(self, image_type, free_rules, abstract_rules, landscape_rules, people_rules):
    rules_dict = {
      "Free": free_rules,
      "Abstract": abstract_rules,
      "Landscapes": landscape_rules,
      "People": people_rules
    }
    
    rules = rules_dict.get(image_type, "").split(",")
    rules += [rules[-1]] * (4 - len(rules)) if len(rules) < 4 else []
    rules_str = ",".join(rules)

    return (
      str(rules_str),
    )

class Refine_Setup:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "used_cfg": ("FLOAT", {
          "forceInput": True,
        }),
        "used_steps": ("INT", {
          "forceInput": True,
        }),
        "used_scheduler": ("COMBO", {
          "multiline": False,
          "forceInput": True,
        }),
        "used_sampler": ("COMBO", {
          "multiline": False,
          "forceInput": True,
        }),
        "disable_override": ("BOOLEAN", {
          "default": True,
        }),
        "select_scheduler": (["internal"] + comfy.samplers.KSampler.SCHEDULERS, {
          "default": "internal",
        }),
        "select_sampler": (["internal"] + comfy.samplers.KSampler.SAMPLERS, {
          "default": "internal",
        }),
        "select_cfg": ("FLOAT", {
          "default": 0.0,
          "min": 0.0,
          "max": 16.0,
          "step": 0.1,
          "display": "number"
        }),
        "select_steps": ("INT", {
          "default": 0,
          "min": 0,
          "max": 100,
          "step": 1,
          "display": "number"
        }),
      }
    }

  RETURN_TYPES = ("FLOAT", "INT", comfy.samplers.KSampler.SAMPLERS, comfy.samplers.KSampler.SCHEDULERS)
  RETURN_NAMES = ("cfg", "steps", "sampler", "scheduler")

  FUNCTION = "main"
  CATEGORY = "Foxpack/Upscale"

  def main(self, used_scheduler, used_sampler, select_scheduler, select_sampler, select_cfg, select_steps, used_cfg, used_steps, disable_override):
    if disable_override:
      return (
        float(used_cfg),
        int(used_steps),
        used_sampler,
        used_scheduler,
      )
      
    return_sampler = used_sampler if select_sampler == "internal" else select_sampler
    return_scheduler = used_scheduler if select_scheduler == "internal" else select_scheduler
    return_cfg = used_cfg if select_cfg == 0.0 else select_cfg
    return_steps = used_steps if select_steps == 0 else select_steps
    
    return (
      float(return_cfg),
      int(return_steps),
      return_sampler,
      return_scheduler
    )

class Refine_Prompt: 
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "clip": ("CLIP",),
        "pos_prompt": ("CONDITIONING", {
          "forceInput": True,
        }),
        "neg_prompt": ("CONDITIONING", {
          "forceInput": True,
        }),
        "refine_prompt_pos": ("STRING", {
          "multiline": True,
          "default": ""
        }),
        "refine_prompt_neg": ("STRING", {
          "multiline": True,
          "default": ""
        }),
      }
    }

  RETURN_TYPES = ("CONDITIONING", "CONDITIONING")
  RETURN_NAMES = ("pos_prompt","neg_prompt")
  FUNCTION = "main"
  CATEGORY = "Foxpack/Upscale"

  def main(self, clip, pos_prompt, neg_prompt, refine_prompt_pos, refine_prompt_neg):
    additional_pos_cond = CLIPTextEncode().encode(clip, refine_prompt_pos)
    additional_neg_cond = CLIPTextEncode().encode(clip, refine_prompt_neg)

    combined_pos_cond = comfy.utils.combine_conditioning(pos_prompt, additional_pos_cond)
    combined_neg_cond = comfy.utils.combine_conditioning(neg_prompt, additional_neg_cond)
    
    return (
      combined_pos_cond,
      combined_neg_cond
    )