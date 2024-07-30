class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

class Remap_Values:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "search_string": ("STRING", {
          "forceInput": True,
          "default": "",
          "multiline": False,
        }),
        "map": ("STRING", {
          "default": "",
          "multiline": False,
        }),
      }
    }

  RETURN_TYPES = ("STRING", "STRING")
  RETURN_NAMES = ("output", "show_help")

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, search_string, map):
    if map == "":
      return search_string
    map = map.split(",")
    map = {k: v for k, v in [x.split(":") for x in map]}
    entry = map.get(search_string)
    print("entry:", entry)

    show_help = "show me some help"
    
    return (
      str(entry),
      show_help
    )

class Negate_Boolean:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "value": ("BOOLEAN", {
          "forceInput": True
        }),
      }
    }

  RETURN_TYPES = ("BOOLEAN",)
  RETURN_NAMES = ("value",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, value):
    return not value

class Select_String_By_Index:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "index": ("INT", {
          "default": 0,
        }),
        "options": ("STRING", {
          "forceInput": True
        }),
      }
    }

  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("value",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"
  
  def main(self, index, options):
    stringArray = options.split(",")
    selected_option = stringArray[index]
    
    print("selectedoption:", selected_option)
    
    return (
      str(selected_option),
    )

class Select_By_Index:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "index": ("INT", {
          "default": 0,
        }),
        "options": ("STRING", {
          "forceInput": True
        }),
      }
    }

  RETURN_TYPES = (any_type,)
  RETURN_NAMES = ("value")

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, index, options):
    return (
      str(options[index]),
    )

class Show_Type:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "value": (any_type, {
          "forceInput": True
        }),
      }
    }

  RETURN_TYPES = ()
  RETURN_NAMES = ()

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, value):
    print("Show_Type", value, type(value))
    return ()