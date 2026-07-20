"""Image processing utilities."""

import base64
import io
from typing import Optional, Tuple
from PIL import Image

from disaster_missing_persons.core.config import get_settings

settings = get_settings()


def compress_image(
    base64_string: str,
    max_size: Optional[Tuple[int, int]] = None,
    quality: Optional[int] = None,
) -> str:
    """Compress a base64-encoded image for bandwidth saving.

    Args:
        base64_string: Base64-encoded image string.
        max_size: Maximum dimensions (width, height).
        quality: JPEG quality (1-100).

    Returns:
        Compressed base64-encoded JPEG image.
    """
    try:
        max_size = max_size or (800, 800)
        quality = quality or settings.IMAGE_QUALITY

        # Strip data URI prefix if present
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        image_data = base64.b64decode(base64_string)
        img = Image.open(io.BytesIO(image_data))

        # Convert to RGB if necessary
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize if too large
        img.thumbnail(max_size, Image.LANCZOS)

        # Compress and convert back to base64
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        compressed = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/jpeg;base64,{compressed}"
    except Exception:
        # Return original if compression fails
        return base64_string


def generate_thumbnail(base64_string: str) -> str:
    """Generate a thumbnail from a base64-encoded image.

    Args:
        base64_string: Base64-encoded image string.

    Returns:
        Thumbnail base64-encoded JPEG image.
    """
    size = (settings.THUMBNAIL_WIDTH, settings.THUMBNAIL_HEIGHT)
    return compress_image(base64_string, max_size=size, quality=50)
