class Big_Prompter:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "prompt": ("STRING", {
          "forceInput": True
        }),
        "options": ("STRING", {
          "forceInput": True
        }),
      }
    }