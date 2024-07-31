class Universal_FreeU:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "model": ("MODEL",),
        "version": ("STRING", {
          "default": "xl",
          "forceInput": True,
        })
      }
    }

  RETURN_TYPES = ("MODEL",)
  