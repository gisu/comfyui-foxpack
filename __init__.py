from .py.smart_checkpoint_setup import SetupSelector, BaseSamplerSetup, OverrideSamplerSetup, CheckpointMetaExtractor, CheckpointSelector
from .py.latent_helper import UniversalLatentHelper
from .py.logic_helper import Remap_Values, Negate_Boolean, Select_String_By_Index, Select_By_Index, Show_Type, Select_Line_By_Index, Split_Entry_In_2Chunks, Split_Entry_In_4Chunks, Split_Entry_In_6Chunks, Split_Entry_In_8Chunks, Convert_Into, Add_To_List, Change_Entry_From_List, Change_Entries_In_A_List, Pick_Values_From_List, Remove_Values_From_List, Override_Value_If_Unset
from .py.loader_helper import Universal_VAE_Loader
from .py.upscale_helper import Step_Denoise, Refine_Setup, Refine_Prompt



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
    "Show_Type": Show_Type,
    "Select_Line_By_Index": Select_Line_By_Index,
    "Split_Entry_In_2Chunks": Split_Entry_In_2Chunks,
    "Split_Entry_In_4Chunks": Split_Entry_In_4Chunks,
    "Split_Entry_In_6Chunks": Split_Entry_In_6Chunks,
    "Split_Entry_In_8Chunks": Split_Entry_In_8Chunks,
    "Universal_VAE_Loader": Universal_VAE_Loader,
    "Step_Denoise": Step_Denoise,
    "Refine_Setup": Refine_Setup,
    "Refine_Prompt": Refine_Prompt,
    "Convert_Into": Convert_Into,
    "Add_To_List": Add_To_List,
    "Change_Entry_From_List": Change_Entry_From_List,
    "Change_Entries_In_A_List": Change_Entries_In_A_List,
    "Pick_Values_From_List": Pick_Values_From_List,
    "Remove_Values_From_List": Remove_Values_From_List,
    "Override_Value_If_Unset": Override_Value_If_Unset,
    "CheckpointSelector": CheckpointSelector
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
    "Show_Type": "Show Type",
    "Select_Line_By_Index": "Select Line By Index",
    "Split_Entry_In_2Chunks": "Split Entry In 2 Chunks",
    "Split_Entry_In_4Chunks": "Split Entry In 4 Chunks",
    "Split_Entry_In_6Chunks": "Split Entry In 6 Chunks",
    "Split_Entry_In_8Chunks": "Split Entry In 8 Chunks",
    "Universal_VAE_Loader": "Universal VAE Loader",
    "Step_Denoise": "Step Denoise",
    "Refine_Setup": "Refine Setup",
    "Refine_Prompt": "Refine Prompt",
    "Convert_Into": "Convert Into",
    "Add_To_List": "Add To List",
    "Change_Entry_From_List": "Change Entry From List",
    "Change_Entries_In_A_List": "Change Entries In A List",
    "Pick_Values_From_List": "Pick Values From List",
    "Remove_Values_From_List": "Remove Values From List",
    "Override_Value_If_Unset": "Override Value If Unset",
    "CheckpointSelector": "Checkpoint Selector"
}

EXTENSION_NAME = "ComfUI-Foxpack"