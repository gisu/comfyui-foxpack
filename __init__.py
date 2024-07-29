from .py.smart_checkpoint_setup import SetupSelector, BaseSamplerSetup, OverrideSamplerSetup, CheckpointMetaExtractor
from .py.latent_helper import UniversalLatentHelper

NODE_CLASS_MAPPINGS = {
    "CheckpointMetaExtractor": CheckpointMetaExtractor,
    "BaseSamplerSetup": BaseSamplerSetup,
    "OverrideSamplerSetup": OverrideSamplerSetup,
    "SetupSelector": SetupSelector,
    "UniversalLatentHelper": UniversalLatentHelper
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CheckpointMetaExtractor": "SSS: Checkpoint Meta Extractor",
    "BaseSamplerSetup": "SSS: Base Sampler Setup",
    "OverrideSamplerSetup": "SSS: Override Sampler Setup",
    "SetupSelector": "SSS: Setup Selector",
    "UniversalLatentHelper": "Universal Latent Helper"
}

EXTENSION_NAME = "ComfUI-Foxpack"