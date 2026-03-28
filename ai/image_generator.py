import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def generate_image_for_post(news_title: str, image_path: str = "assets/post_image.png"):
    """
    Generate an image for the LinkedIn post with text overlay.

    Args:
        news_title: The title of the news article to display on the image
        image_path: Path where the image should be saved
    """
    # Create the assets directory if it doesn't exist
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)

    # Define image dimensions
    width, height = 1200, 630  # Standard LinkedIn post image size

    # Create a new image with a gradient background
    image = Image.new('RGB', (width, height), color=(64, 128, 200))  # Blue background

    # Draw gradient
    draw = ImageDraw.Draw(image)

    # Add a subtle gradient effect
    for i in range(height):
        r = int(64 + (i / height) * 32)
        g = int(128 + (i / height) * 32)
        b = int(200 + (i / height) * 32)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    # Add text overlay
    try:
        # Try to use a system font
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        # Fallback to default font if arial is not available
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Split title into multiple lines if too long
    max_line_width = 30
    words = news_title.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) <= max_line_width:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    # Calculate text position (centered)
    total_text_height = len(lines) * 60
    start_y = (height - total_text_height) // 2

    # Draw each line of text
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = start_y + i * 60

        # Add shadow effect
        draw.text((x+2, y+2), line, fill=(0, 0, 0), font=font_large)
        # Draw main text
        draw.text((x, y), line, fill=(255, 255, 255), font=font_large)

    # Add a subtle border
    draw.rectangle([10, 10, width-10, height-10], outline=(255, 255, 255), width=2)

    # Save the image
    image.save(image_path)
    print(f"Image saved to {image_path}")