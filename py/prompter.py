class Big_Prompter:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "base_setup": ("STRING", {
          })
        "prompt": ("STRING", {
          "forceInput": True
        }),
        "options": ("STRING", {
          "forceInput": True
        }),
      }
    }