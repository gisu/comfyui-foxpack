from .py.smart_checkpoint_setup import SetupSelector, BaseSamplerSetup, OverrideSamplerSetup, CheckpointMetaExtractor
from .py.latent_helper import UniversalLatentHelper
from .py.logic_helper import Remap_Values, Negate_Boolean, Select_String_By_Index, Select_By_Index, Show_Type

NODE_CLASS_MAPPINGS = {
    "CheckpointMetaExtractor": CheckpointMetaExtractor,
    "BaseSamplerSetup": BaseSamplerSetup,
    "OverrideSamplerSetup": OverrideSamplerSetup,
    "SetupSelector": SetupSelector,
    "UniversalLatentHelper": UniversalLatentHelper,
    "Remap_Values": Remap_Values,
    "Negate_Boolean": Negate_Boolean,
    "Select_String_By_Index": Select_String_By_Index,
    "Select_By_Index": Select_By_Index,
    "Show_Type": Show_Type
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CheckpointMetaExtractor": "SSS: Checkpoint Meta Extractor",
    "BaseSamplerSetup": "SSS: Base Sampler Setup",
    "OverrideSamplerSetup": "SSS: Override Sampler Setup",
    "SetupSelector": "SSS: Setup Selector",
    "UniversalLatentHelper": "Universal Latent Helper",
    "Remap_Values": "Remap Values",
    "Negate_Boolean": "Negate Boolean",
    "Select_String_By_Index": "Select string by index",
    "Select_By_Index": "Select by index",
    "Show_Type": "Show Type"
}

EXTENSION_NAME = "ComfUI-Foxpack"