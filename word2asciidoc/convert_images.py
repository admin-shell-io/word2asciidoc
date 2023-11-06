import logging

from PIL import Image
import os
from wand.image import Image as wima


def convert_emf_to_png_with_wand(emf_file: str, png_file):
    with wima(filename=emf_file, resolution=500) as img:
        img.format = 'PNG'
        img.save(filename=png_file)


def convert_emf_to_png(emf_file, png_file):
    try:
        im = Image.open(emf_file)
        logging.info(f"Converting to PNG: {emf_file}")
        im.save(png_file, 'PNG')
    except OSError:
        convert_emf_to_png_with_wand(emf_file, png_file)


def read_emf_images(folder_path):
    image_files = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.emf'):
            image_files[file_name] = os.path.join(folder_path, file_name)
    return image_files
