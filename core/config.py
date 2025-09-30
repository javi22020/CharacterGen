import os

BFL_BASE_MODEL = "flux-pro-1.1-ultra"
BFL_EDIT_MODEL = "flux-kontext-pro"

# Replicate model identifiers. You can change these if Replicate updates the
# versions.
REPLICATE_BASE_MODEL = "blackforest-ai/flux-pro-1.1-ultra"
REPLICATE_EDIT_MODEL = "blackforest-ai/flux-kontext-pro"

# Google Gemini model identifiers for Nano Banana
# Note: Gemini is primarily for text generation, Imagen is for image generation
# This is a conceptual implementation - actual Google image generation would use Imagen API
GOOGLE_IMAGE_MODEL = "gemini-1.5-flash"  # Used for enhanced prompting
GOOGLE_EDIT_MODEL = "gemini-1.5-flash"   # Used for enhanced prompting

# Default provider to use for generation. Can be overridden by setting the
# ``DEFAULT_PROVIDER`` environment variable to ``"REPLICATE"``, ``"BFL"``, or ``"GOOGLE"``.
DEFAULT_PROVIDER = os.environ.get("DEFAULT_PROVIDER", "BFL").upper()

# Output format for generated images
IMAGE_FORMAT = "png"