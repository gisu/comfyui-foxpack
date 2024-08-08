import comfy.samplers
from nodes import CLIPTextEncode
import re
import numpy as np
import ast

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")
class Step_Denoise:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "image_type": (["Abstract", "Landscapes", "People","Free1","Free2","Free3"],
          {
            "default": "Landscapes",
          }
        ),
        "max_steps": ("INT", {
          "default": 4,
          "min": 1,
          "max": 10,
          "step": 1,
          "display": "number"
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
        "free_rules1": ("STRING", {
          "default": "0.7",
          "multiline": False,
        }),
        "free_rules2": ("STRING", {
          "default": "0.6-0.2",
          "multiline": False,
        }),
        "free_rules3": ("STRING", {
          "default": "0.33-0.25",
          "multiline": False,
        }),
      }
    }

  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("rules",)
  OUTPUT_NODE = True
  FUNCTION = "main"
  CATEGORY = "Foxpack/Upscale"

  def main(self, image_type, free_rules1, free_rules2, free_rules3, max_steps, abstract_rules, landscape_rules, people_rules):
    rules_dict = {
      "Free1": free_rules1,
      "Free2": free_rules2,
      "Free3": free_rules3,
      "Abstract": abstract_rules,
      "Landscapes": landscape_rules,
      "People": people_rules
    }

    rules = rules_dict.get(image_type, "").split(",")

    if len(rules) == 1 and "-" in rules[0]:
      start, end = map(float, rules[0].split("-"))
      rules = np.linspace(start, end, num=max_steps).tolist()
      rules = [str(round(x, 2)) for x in rules]

    rules += [rules[-1]] * (max_steps - len(rules)) if len(rules) < max_steps else []

    rules_str = ",".join(rules)

    return (
      rules_str,
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
        "used_scheduler": (any_type, {
          "forceInput": True,
        }),
        "used_sampler": (any_type, {
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
        })
      },
      "optional": {
        "refine_setup": ("STRING", {
          "default": ""
        })
      }
    }

  RETURN_TYPES = ("FLOAT", "INT", comfy.samplers.KSampler.SAMPLERS, comfy.samplers.KSampler.SCHEDULERS)
  RETURN_NAMES = ("cfg", "steps", "sampler", "scheduler")

  FUNCTION = "main"
  CATEGORY = "Foxpack/Upscale"

  def main(self, used_scheduler, used_sampler, select_scheduler, select_sampler, select_cfg, select_steps, used_cfg, used_steps, disable_override, refine_setup):

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

    if refine_setup and not re.search(r"\{.*\}", refine_setup):
      refine_setup = "{" + refine_setup + "}"

    dictionary = ast.literal_eval(refine_setup)

    print("refine_sampler dict", dictionary)

    if "sampler" in dictionary:
      return_sampler = dictionary["sampler"]
    if "scheduler" in dictionary:
      return_scheduler = dictionary["scheduler"]
    if "cfg" in dictionary:
      return_cfg = dictionary["cfg"]
    if "steps" in dictionary:
      return_steps = dictionary["steps"]


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

    combined_pos_cond = pos_prompt + additional_pos_cond[0]
    combined_neg_cond = neg_prompt + additional_neg_cond[0]


    return (
      combined_pos_cond,
      combined_neg_cond
    )
