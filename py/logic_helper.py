class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

class DynamicInputType(dict):
  def __init__(self, type):
    self.type = type

  def __getitem__(self, key):
    return (self.type, )

  def __contains__(self, key):
    return True

class TautologyStr(str):
  def __ne__(self, other):
    return False

class AlwaysEqualProxy(str):
  def __eq__(self, _):
    return True

  def __ne__(self, _):
    return False

class ByPassTypeTuple(tuple):
  def __getitem__(self, index):
    if index>0:
      index=0
    item = super().__getitem__(index)
    if isinstance(item, str):
      return TautologyStr(item)
    return item

def is_context_empty(ctx):
  return not ctx or all(v is None for v in ctx.values())

def is_none(value):
  if value is not None:
    if isinstance(value, dict) and 'model' in value and 'clip' in value:
      return is_context_empty(value)
  return value is None

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
    length = len(stringArray)
    index = index if index < length else length - 1
    selected_option = stringArray[index]
    
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
        "options": (any_type, {
          "forceInput": True
        }),
        "seperator": ("STRING", {
          "default": ",",
        }),
        "output_type": (["input","string", "int", "float", "boolean", "list"],
        {
          "default": "string"
        }),
      }
    }

  RETURN_TYPES = ByPassTypeTuple((AlwaysEqualProxy("*"),))
  OUTPUT_NODE = True

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, index, options, output_type, seperator):
    entry = None

    if isinstance(options, (str, list)):
      arr = options.split(seperator) if isinstance(options, str) else options
      entry = arr[min(index, len(arr) - 1)]
    else:
      entry = options

    conversion_map = {
      "string": str,
      "int": int,
      "float": float,
      "boolean": bool,
      "list": lambda x: [x]
    } 

    param = conversion_map.get(output_type, lambda x: x)(entry)
      
    return (
      param,
    )

class Split_Entry_In_2Chunks:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "seperator": ("STRING", {
          "default": ",",
        }),
        "options": ("STRING", {
          "forceInput": True
        })
      },
      "optional": {
        "output_type": (["string", "int", "float", "boolean", "list"],
        {
          "default": "string"
        }),
      }
    }

  RETURN_TYPES = (any_type,any_type)
  RETURN_NAMES = ("value1","value2")
  OUTPUT_NODE = True

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, seperator, options, output_type):
    arr = options.split(seperator)
    length = len(arr)
    arr = [x.strip() for x in arr]

    if output_type == "int":
      arr = [int(x) for x in arr]
    elif output_type == "float":
      arr = [float(x) for x in arr]
    elif output_type == "boolean":
      arr = [bool(x) for x in arr]
    elif output_type == "list":
      arr = [list(x) for x in arr]

    output = None
    if (length == 0):
      output = ("", "")
    elif (length == 1):
      output = (arr[0], "")
    else:
      output = (arr[0], arr[1])
      
    return (
      output
    )

class Split_Entry_In_4Chunks:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "seperator": ("STRING", {
          "default": ",",
        }),
        "options": ("STRING", {
          "forceInput": True
        })
      },
      "optional": {
        "output_type": (["string", "int", "float", "boolean", "list"],
        {
          "default": "string"
        }),
      }
    }

  RETURN_TYPES = (any_type,any_type,any_type,any_type)
  RETURN_NAMES = ("value1","value2","value3","value4")
  OUTPUT_NODE = True

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, seperator, options, output_type):
    arr = options.split(seperator)
    length = len(arr)
    arr = [x.strip() for x in arr]

    if output_type == "int":
      arr = [int(x) for x in arr]
    elif output_type == "float":
      arr = [float(x) for x in arr]
    elif output_type == "boolean":
      arr = [bool(x) for x in arr]
    elif output_type == "list":
      arr = [list(x) for x in arr]

    output = None
    if (length == 0):
      output = ("", "", "", "")
    elif (length == 1):
      output = (arr[0], "", "", "")
    elif (length == 2):
      output = (arr[0], arr[1], "", "")
    elif (length == 3):
      output = (arr[0], arr[1], arr[2], "")
    else:
      output = (arr[0], arr[1], arr[2], arr[3]) 
      
    return (
      output
    )

class Split_Entry_In_6Chunks:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "seperator": ("STRING", {
          "default": ",",
        }),
        "options": ("STRING", {
          "forceInput": True
        })
      },
      "optional": {
        "output_type": (["string", "int", "float", "boolean", "list"],
        {
          "default": "string"
        }),
      }
    }

  RETURN_TYPES = (any_type,any_type,any_type,any_type,any_type,any_type)
  RETURN_NAMES = ("value1","value2","value3","value4","value5","value6")
  OUTPUT_NODE = True

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, seperator, options, output_type):
    arr = options.split(seperator)
    length = len(arr)
    arr = [x.strip() for x in arr]

    if output_type == "int":
      arr = [int(x) for x in arr]
    elif output_type == "float":
      arr = [float(x) for x in arr]
    elif output_type == "boolean":
      arr = [bool(x) for x in arr]
    elif output_type == "list":
      arr = [list(x) for x in arr]

    output = None
    if (length == 0):
      output = ("", "", "", "", "", "")
    elif (length == 1):
      output = (arr[0], "", "", "", "", "")
    elif (length == 2):
      output = (arr[0], arr[1], "", "", "", "")
    elif (length == 3):
      output = (arr[0], arr[1], arr[2], "", "", "")
    elif (length == 4):
      output = (arr[0], arr[1], arr[2], arr[3], "", "") 
    elif (length == 5):
      output = (arr[0], arr[1], arr[2], arr[3], arr[4], "")
    else:
      output = (arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])
      
    return (
      output
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

class Select_Line_By_Index:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "options": ("STRING", {
          "default": "",
          "multiline": True,
        }),
      },
      "optional": {
        "index": ("INT", {
          "default": 0,
        }),
        "search_word": ("STRING", {
          "default": "",
        }),
      }
    }

  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("value",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, index, options, search_word):
    if search_word == "":
      stringArray = options.split("\n")
      length = len(stringArray)
      index = index if index < length else length - 1
      selected_option = stringArray[index]
    else:
      selected_option = ""
      stringArray = options.split("\n")
      for line in stringArray:
        if line.startswith(search_word):
          selected_option = line
          break

      selected_option = selected_option.replace(search_word, "").replace("=", "").replace('"', "").strip()
    
    
    return (
      str(selected_option),
    )


class Convert_Into:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "value": (any_type, {
          "forceInput": True
        }),
        "seperator": ("STRING", {
          "default": ",",
        }),
        "output_type": (["string", "int", "float", "boolean", "list"],
        {
          "default": "string"
        }),
      }
    }

  RETURN_TYPES = (any_type,)
  RETURN_NAMES = ("value",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, value, output_type, seperator):
    output = None

    if output_type == "string":
      if (type(value) == list):
        value = [str(x) for x in value]
        value = seperator.join(value)
      output = str(value)
    elif output_type == "int":
      output = int(value)
    elif output_type == "float":
      output = float(value)
    elif output_type == "boolean":
      output = bool(value)
    elif output_type == "list":
      # if value is value a string and is comma seperated
      if (type(value) == str):
        value = value.split(seperator)
        value = [int(x) if x.isdigit() else float(x) if x.replace(".", "", 1).isdigit() else x for x in value]
        output = value
      else:
        output = [value]

    return (
      output,
    )

class Add_To_List:
  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "list": ("LIST", {
          "forceInput": True
        }),
      },
      "optional": {
        "item1": (any_type, {
          "forceInput": True
        }),
        "item2": (any_type, {
          "forceInput": True
        }),
        "item3": (any_type, {
          "forceInput": True
        }),
        "item4": (any_type, {
          "forceInput": True
        }),
        "item5": (any_type, {
          "forceInput": True
        }),
        "item6": (any_type, {
          "forceInput": True
        }),
      }
    }

  RETURN_TYPES = ("LIST",)
  RETURN_NAMES = ("list",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, **kwargs):
    new_list = kwargs.get("list", [])
    new_list = [x for x in new_list if x is not None]
    
    for key, value in kwargs.items():
      if key.startswith('item') and value is not None:
        new_list.append(value)
    
    return (
      new_list,
    )
    