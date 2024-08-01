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