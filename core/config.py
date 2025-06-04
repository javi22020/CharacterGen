import os

BFL_BASE_MODEL = "flux-pro-1.1-ultra"
BFL_EDIT_MODEL = "flux-kontext-pro"

# Replicate model identifiers. You can change these if Replicate updates the
# versions.
REPLICATE_BASE_MODEL = "blackforest-ai/flux-pro-1.1-ultra"
REPLICATE_EDIT_MODEL = "blackforest-ai/flux-kontext-pro"

# Default provider to use for generation. Can be overridden by setting the
# ``DEFAULT_PROVIDER`` environment variable to ``"REPLICATE"`` or ``"BFL"``.
DEFAULT_PROVIDER = os.environ.get("DEFAULT_PROVIDER", "BFL").upper()

# Output format for generated images
IMAGE_FORMAT = "png"