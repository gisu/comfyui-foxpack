import ast
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

def variable_output_arr(separator, options, output_type, max_length: int = 2):
    if (type(options) == str):
      arr = [x.strip() for x in options.split(separator)]
    else:
      arr = options
    
    type_conversions = {
        "int": int,
        "float": float,
        "boolean": bool,
        "list": list,
    }

    if output_type in type_conversions:
        arr = [type_conversions[output_type](x) for x in arr]

    arr.extend([""] * (max_length - len(arr)))

    output = tuple(arr[:max_length])

    return output

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
    return (not value,)

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
        "options": (any_type, {
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
    return (
      variable_output_arr(seperator, options, output_type, 2)
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
        "options": (any_type, {
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
    return (
      variable_output_arr(seperator, options, output_type, 4)
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
        "options": (any_type, {
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
    return (
      variable_output_arr(seperator, options, output_type, 6)
    )

class Split_Entry_In_8Chunks:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "seperator": ("STRING", {
          "default": ",",
        }),
        "options": (any_type, {
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

  RETURN_TYPES = (any_type,any_type,any_type,any_type,any_type,any_type,any_type,any_type)
  RETURN_NAMES = ("value1","value2","value3","value4","value5","value6","value7","value8")
  OUTPUT_NODE = True

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, seperator, options, output_type):
    return (
      variable_output_arr(seperator, options, output_type, 8)
    )

class Change_Entry_From_List:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "index": ("INT", {
          "default": 0,
        }),
        "options": ("LIST", {
          "forceInput": True
        }),
        "change_value": (any_type, {
          "forceInput": True
        })
      }
    }

  RETURN_TYPES = ("LIST",)
  RETURN_NAMES = ("list",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, index, options, change_value):
    options[index] = change_value
    
    return (
      options,
    )

class Change_Entries_In_A_List:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "indexes": ("STRING", {
          "default": "",
        }),
        "options": ("LIST", {
          "forceInput": True
        }),
        "change_values": ("LIST", {
          "forceInput": True
        })
      }
    }

  RETURN_TYPES = ("LIST",)
  RETURN_NAMES = ("list",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, indexes, options, change_values):
    indexes = [int(x) for x in indexes.split(",")]
    for i, index in enumerate(indexes):
      options[index] = change_values[i]
      
    return (
      options,
    )

class Pick_Values_From_List:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "options": ("LIST", {
          "forceInput": True
        }),
        "indexes": ("STRING", {
          "default": "",
        })
      }
    }

  RETURN_TYPES = ("LIST",)
  RETURN_NAMES = ("options",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, indexes, options):
    indexes = [int(x) for x in indexes.split(",")]
    options = [options[x] for x in indexes]
    return (
      options,
    )

class Remove_Values_From_List:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "options": ("LIST", {
          "forceInput": True
        }),
        "indexes": ("STRING", {
          "default": "",
        })
      }
    }

  RETURN_TYPES = ("LIST",)
  RETURN_NAMES = ("options",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, indexes, options):
    indexes = [int(x) for x in indexes.split(",")]
    options = [options[x] for x in range(len(options)) if x not in indexes]
    
    return (
      options,
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
      if isinstance(value, (int, float)):
        value = int(value) if value.is_float() else value
        output = bool(False) if value == 0 else bool(True)
      elif type(value) == str:
        output = bool(False) if len(value) > 0 else bool(True)
      else:
        output = bool(value)
    elif output_type == "list":
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
      "required": {},
      "optional": {
        "list": ("LIST", {
          "forceInput": True
        }),
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
        "item7": (any_type, {
          "forceInput": True
        }),
        "item8": (any_type, {
          "forceInput": True
        }),
        "item9": (any_type, {
          "forceInput": True
        }),
        "item10": (any_type, {
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

class Override_Value_If_Unset:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "replace_value": ("STRING", {
          "default": "0",
          "forceInput": True,
        }),
        "replace_type": (["string", "int", "float", "boolean", "list"], {
          "default": "string",
          "forceInput": True,
        }),
      },
      "optional": {
        "value": (any_type, {
          "forceInput": True
        }),
      }
    }

  RETURN_TYPES = (any_type,)
  RETURN_NAMES = ("value",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, replaced_value, replace_type, value):
    if value: 
      return (value,)
    if replace_type == "string":
      return (replaced_value,)
    elif replace_type == "int":
      return (int(replaced_value),)
    elif replace_type == "float":
      return (float(replaced_value),)
    elif replace_type == "boolean":
      return (bool(replaced_value),)
    elif replace_type == "list":
      return ([replaced_value],)

class Pick_Value_From_Dict:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "dict": ("STRING", {
          "forceInput": True
        }),
        "key": ("STRING", {
          "default": "",
        }),
        "default_return": ("STRING", {
          "default": "",
        }),
        "return_type": (["string", "int", "float", "boolean", "list"],
        {
          "default": "string"
        }),
      }
    }

  RETURN_TYPES = (any_type,)
  RETURN_NAMES = ("value",)

  FUNCTION = "main"

  CATEGORY = "Foxpack/Logic"

  def main(self, dict, key, default_return, return_type):
    dict_str = "{" + dict + "}"
    dictionary = ast.literal_eval(dict_str)
    
    value = dictionary.get(key)
    if value is None:
      if return_type == "string":
        return (default_return,)
      elif return_type == "int":
        return (int(default_return),)
      elif return_type == "float":
        return (float(default_return),)
      elif return_type == "boolean":
        return (bool(default_return),)
      elif return_type == "list":
        return ([default_return],)
    return (value,)