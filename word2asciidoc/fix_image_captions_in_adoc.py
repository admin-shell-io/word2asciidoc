import re


# Define the callback function
def replacement(match):
    # Use block figure tag
    figure_tag: str = match[1]
    figure_tag = figure_tag.replace("image:", "image::")

    # remove "Figure+num" as it will be automatically done in AsciiDoc
    caption: str = match[2]
    caption = re.sub(r'^Figure \d*:?', '', caption)

    # Move the caption to the beginning of the figure tag
    modified_figure_tag = f'.{caption.strip()}\n{figure_tag}\n'

    return modified_figure_tag


def use_block_tag_for_img_and_move_caption_ahead(content):
    # Define the regular expression pattern to match figure tags with specific captions
    pattern = r'(image:\S+\[.*?\])\s+?\n?\n?(Figure.*?\n)'

    # Replace the original figure tags with the modified ones
    new_content = re.sub(pattern, replacement, content)
    return new_content
