from django import template
from django.conf import settings
import os.path

register = template.Library()


@register.simple_tag
def safe_image_url(image_field):
    """
    Return the URL of the image or a default image URL if there's an error
    or if the image file doesn't exist.
    """
    default_image_url = f"{settings.MEDIA_URL}movie/images/default.jpg"
    try:
        # Check if image_field is valid and the actual file exists
        is_valid_field = image_field and hasattr(image_field, 'path')
        file_exists = False
        if is_valid_field:
            # Check path only if field and attribute are valid
            file_exists = os.path.exists(image_field.path)

        if file_exists:  # True implies is_valid_field was also true
            return image_field.url
        else:
            # Image field might be invalid or point to a non-existent file.
            return default_image_url
    except (ValueError, AttributeError):
        # Catch other potential errors with the image_field
        return default_image_url
