from django import template
from django.conf import settings
import os.path

register = template.Library()

@register.simple_tag
def safe_image_url(image_field):
    """
    Return the URL of the image or a default image URL if there's an error.
    """
    try:
        return image_field.url
    except (ValueError, AttributeError):
        # Return a default image URL if there's an issue with the image field
        return f"{settings.MEDIA_URL}movie/images/default.jpg" 