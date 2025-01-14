from enum import Enum


class BrandImageTypes(Enum):
    """
    Enumeration of brand image types to define their usage and dimensions.
    """
    LIGHT_IMAGE = "LIGHT_IMAGE"  # Medium-sized image (700-1000 width) for light-themed contexts.
    DARK_IMAGE = "DARK_IMAGE"    # Medium-sized image (700-1000 width) for dark-themed contexts.
    PLACEHOLDER = "PLACEHOLDER"  # Full HD image for large displays like hero sections.
