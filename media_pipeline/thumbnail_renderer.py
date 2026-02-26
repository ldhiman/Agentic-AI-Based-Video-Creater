from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import textwrap


WIDTH = 1080
HEIGHT = 1920


def render_thumbnail(
    image_path: str,
    overlay_text: str,
    output_path: str,
    font_path: str = "arial.ttf"
):
    """
    Create a YouTube Shorts thumbnail with bold overlay text.
    """

    # Load base image
    img = Image.open(image_path).convert("RGB")
    img = img.resize((WIDTH, HEIGHT))

    draw = ImageDraw.Draw(img)

    # Load font
    font_size = 140
    font = ImageFont.truetype(font_path, font_size)

    # Wrap text (max 3 lines)
    wrapped_text = "\n".join(textwrap.wrap(overlay_text.upper(), width=12))

    # Calculate text position
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, spacing=20)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = (WIDTH - text_width) / 2
    y = HEIGHT * 0.65  # lower third placement

    # Create text shadow layer
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.multiline_text(
        (x + 6, y + 6),
        wrapped_text,
        font=font,
        fill=(0, 0, 0, 200),
        spacing=20,
        align="center"
    )

    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img.convert("RGBA"), shadow)

    # Add stroke + main text
    draw = ImageDraw.Draw(img)

    draw.multiline_text(
        (x, y),
        wrapped_text,
        font=font,
        fill=(255, 255, 255),
        stroke_width=6,
        stroke_fill=(0, 0, 0),
        spacing=20,
        align="center"
    )

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(output_path, quality=95)

    print(f"✅ Thumbnail saved → {output_path}")