from enum import Enum


class WatchStatus(Enum):
    """
    Enumeration representing the status of a watch in the system.
    """

    # ACTIVE - Indicates that the watch is currently available and displayed
    # on the website or in the inventory. Active watches can be purchased 
    # or interacted with by users.
    ACTIVE = "ACTIVE"

    # INACTIVE - Indicates that the watch is currently unavailable or hidden 
    # from the website or inventory. This status is typically used for watches 
    # that are out of stock, discontinued, or temporarily removed from display.
    INACTIVE = "INACTIVE"

    
class WatchImageType(Enum):
    """
    Enumeration of image types to define the purpose and usage of watch images.
    """

    # PLACEHOLDER - Represents the primary image for a watch. 
    # This image is displayed in non-detailed contexts unless specific images 
    # are required. Commonly used in sections like image galleries and other 
    # general areas of the website. This type is a required field in the database.
    PLACEHOLDER = "PLACEHOLDER"

    # EXTERNAL - Represents additional images for a watch, primarily displayed 
    # on the watch detail page. While optional, it is recommended to include 
    # 2-3 EXTERNAL images for better user experience (UX).
    EXTERNAL = "EXTERNAL"

    # FEATURED - Represents a special image of the watch used in prominent 
    # displays, such as sections where a single watch is showcased as the main 
    # content.
    FEATURED = "FEATURED"
