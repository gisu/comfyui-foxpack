import re


class Big_Prompter:
  def __init__(self):
    pass

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "is_pony": (
          "BOOLEAN",
          {
            "default": False,
            "forceInput": True,
          },
        ),
        "char_collection": (
          "STRING",
          {"forceInput": True, "multiline": True, "default": ""},
        ),
        "positive_prompt": ("STRING", {"multiline": True, "default": ""}),
        "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
        "base_pos_prompt": (
          "STRING",
          {
            "multiline": True,
            "default": "cinematic, colorful background, concept art, 8k, dramatic lighting, high detail, highly detailed, hyper realistic, intricate, intricate sharp details, octane render, smooth, studio lighting, trending on artstation, best quality",
          },
        ),
        "base_neg_prompt": (
          "STRING",
          {
            "multiline": True,
            "default": "worst quality, low quality, text, censored, deformed, bad hand, blurry, (watermark),extra hands, extra dicks, extra fingers , deformed fingers",
          },
        ),
        "full_wildcard": ("STRING", {"default": "__a-pure-wc__"}),
        "technical_wildcard": ("STRING", {"default": "__a-technical-wc__"}),
        "artist_wildcard": ("STRING", {"default": "__a-artist-wc__"}),
        "use_pos_base": ("BOOLEAN", {"default": True}),
        "use_neg_base": ("BOOLEAN", {"default": True}),
        "use_full_wildcard": ("BOOLEAN", {"default": False}),
        "use_technical_wildcard": ("BOOLEAN", {"default": False}),
        "use_artist_wildcard": ("BOOLEAN", {"default": False}),
        "select_character": ("STRING", {"default": ""}),
        "rating": (
          ["explicit", "questionable", "save", "none"],
          {"default": "save"},
        ),
        "pony_quality": ([0, 1, 2, 3, 4], {"default": 4}),
      }
    }

  RETURN_TYPES = ("STRING", "STRING")
  RETURN_NAMES = ("pos_prompt", "neg_prompt")
  CATEGORY = "Foxpack/Prompter"
  FUNCTION = "main"

  def pony_quality_matrix(self, pony_quality):
    return {
      4: {
        "positive": "score_9,score_8_up,score_7_up,score_6_up,score_5_up,score_4_up",
        "negative": "score_4",
      },
      3: {
        "positive": "score_8_up,score_7_up,score_6_up,score_5_up,score_4_up",
        "negative": "score_4",
      },
      2: {
        "positive": "score_8,score_7_up,score_6_up",
        "negative": "score_6,score_5,score_4",
      },
      1: {"positive": "score_9", "negative": "score_4"},
      0: {"positive": "", "negative": ""},
    }.get(pony_quality, 4)

  def main(
    self,
    is_pony,
    char_collection,
    positive_prompt,
    negative_prompt,
    base_pos_prompt,
    base_neg_prompt,
    full_wildcard,
    technical_wildcard,
    artist_wildcard,
    select_character,
    rating,
    pony_quality,
    use_full_wildcard,
    use_technical_wildcard,
    use_artist_wildcard,
    use_pos_base,
    use_neg_base,
  ):
    pony_pos_quality = ""
    pony_neg_quality = ""

    if is_pony:
      pony_pos_quality, pony_neg_quality = self.pony_quality_matrix(
        pony_quality
      ).values()

    if use_full_wildcard:
      set_neg_base = base_neg_prompt if use_neg_base else ""

      pos_prompt = f"{pony_pos_quality},{full_wildcard}"
      neg_prompt = f"{pony_neg_quality},{base_neg_prompt}"

      pos_prompt = re.sub(r",+", ",", pos_prompt).strip(",")
      neg_prompt = re.sub(r",+", ",", neg_prompt).strip(",")

      return (pos_prompt, neg_prompt)

    set_rating = {
      "explicit": "rating_explicit",
      "questionable": "rating_questionable",
      "save": "rating_safe",
      "none": "",
    }.get(rating, "none")

    character_details = ""
    if select_character:
      pattern = rf'!{select_character}="([^"]+)"'
      match = re.search(pattern, char_collection)

      if match:
        character_details = f"{match.group(1)},BREAK"

    set_technical_wildcard = technical_wildcard if use_technical_wildcard else ""
    set_artist_wildcard = artist_wildcard if use_artist_wildcard else ""

    set_pos_base = base_pos_prompt if use_pos_base else ""
    set_neg_base = base_neg_prompt if use_neg_base else ""

    pos_prompt = f"{pony_pos_quality},{set_rating},{set_pos_base},{set_technical_wildcard},{character_details},{positive_prompt},{set_artist_wildcard}"

    neg_prompt = f"{pony_neg_quality},{set_neg_base},{negative_prompt}"

    pos_prompt = re.sub(r",+", ",", pos_prompt).strip(",")
    neg_prompt = re.sub(r",+", ",", neg_prompt).strip(",")

    return (pos_prompt, neg_prompt)
