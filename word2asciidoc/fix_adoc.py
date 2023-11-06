#!/usr/bin/env python3
import argparse
import pathlib
from word2asciidoc import read_emf_images, convert_emf_to_png, escape_double_angle_brackets, recolor_notes, \
    remove_text_by_patterns, use_block_tag_for_img_and_move_caption_ahead, escape_source_square_brackets, \
    add_anchors_to_bibliography, add_links_to_bibliography
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    handlers=[logging.FileHandler("my_log_file.log", mode='w', encoding='utf-8'),
                              logging.StreamHandler()])


def process_images(directory, content):
    logging.info("Convert the emf images in Asciidoc document to png")
    images_to_convert = read_emf_images(directory.name + "/media")
    for image_name, image_path in images_to_convert:
        try:
            logging.info(f"Convert the emf image: {image_name}")
            convert_emf_to_png(image_path, image_path.replace(".emf", ".png"))
            # 2.2 Replace all occurrences of emf to png in asciidoc file
            content = content.replace(image_name, image_name.replace(".emf", ".png"))
        except Exception:
            logging.error(f"Could not convert the emf image: {image_name}")
    return content


def process_content(content):
    logging.info("Removing certain patterns in asciidoc file")
    content = remove_text_by_patterns(content)

    logging.info("Escaping double angle brackets")
    content = escape_double_angle_brackets(content)

    logging.info("Styling note boxes")
    content = recolor_notes(content)

    logging.info("Adding anchors to bibliography")
    keys, content = add_anchors_to_bibliography(content)

    logging.info("Connecting in-document references to bibliography")
    content = add_links_to_bibliography(content, keys)

    logging.info("Fixing image captions")
    content = use_block_tag_for_img_and_move_caption_ahead(content)

    logging.info("Escaping square brackets")
    content = escape_source_square_brackets(content)

    return content


def write_output(output_file, content):
    logging.info(f"Writing fixed content to the output file: {output_file}")
    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(content)


def fix_asciidoc(input_file, output_file):
    directory = pathlib.Path(input_file).parent

    logging.info("Read the initial asciidoc file...")
    with open(input_file, 'r', encoding="utf-8") as file:
        content = file.read()

    content = process_images(directory, content)
    content = process_content(content)
    write_output(output_file, content)


def main() -> None:
    parser = argparse.ArgumentParser("Fixes issues in an AsciiDoc file generated from Word.")
    parser.add_argument("-i", "--adoc_input", required=True,
                        help="Path to the initial generated AsciiDoc file")
    parser.add_argument("-o", "--adoc_output", required=True,
                        help="Path to the output AsciiDoc file")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Overwrite existing files without asking")
    args = parser.parse_args()

    adoc_input = pathlib.Path(args.adoc_input)
    adoc_output = pathlib.Path(args.adoc_output)

    if not adoc_input.exists():
        raise FileNotFoundError(f"Adoc file does not exist: {adoc_input}")

    adoc_output.parent.mkdir(exist_ok=True, parents=True)

    if adoc_output.exists() and not args.force:
        raise FileExistsError(f"Output file already exists: {adoc_output}. Use --force to overwrite.")

    fix_asciidoc(adoc_input, adoc_output)


if __name__ == '__main__':
    main()
