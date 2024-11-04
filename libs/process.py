import base64
import os
from PIL import Image

from pdf2image import convert_from_path
import os

def pdf_to_png(pdf_path: str, output_folder: str = "output_images"):
    """
    Convert pages of a PDF file to PNG images and save them to a specified folder.

    Args:
        pdf_path (str): The path to the PDF file to be converted.
        output_folder (str, optional): The directory where the PNG images will be saved.
            Defaults to "output_images".

    This function opens the specified PDF file, converts its pages to images, and saves 
    each page as a PNG file in the specified output folder.
    """
    # Convert each page in the PDF to an image
    images = convert_from_path(pdf_path)
    
    # Save each image in PNG format
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(image_path, "PNG")
    print(f"Converted {len(images)} pages to PNG images.")
    
def encode_image(image_path : str):
    """
    Encode an image file to base64.

    Args:
        image_path (str): The path to the image file to be encoded.

    Returns:
        str: The base64 encoded image data. If the file does not exist, returns None.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None

def crop_image(image_path : str, top : int = 0, bottom : int = 0, left : int = 0, right : str = 0):
    """
    Crop an image by removing specified amounts from the top, bottom, left, and right.

    Args:
        image_path (str): The path to the image file to be cropped.
        output_path (str): The path where the cropped image will be saved.
        top (int): The number of pixels to remove from the top.
        bottom (int): The number of pixels to remove from the bottom.
        left (int): The number of pixels to remove from the left.
        right (int): The number of pixels to remove from the right.
    """
    # Open the image file
    img = Image.open(image_path)

    # Calculate the crop boundaries
    width, height = img.size
    crop_box = (left, top, width - right, height - bottom)

    # Crop the image
    cropped_img = img.crop(crop_box)

    # Save the cropped image
    cropped_img.save(image_path)
    
def crop_images_in_folder(folder : str, top : int = 0, bottom : int = 0, left : int = 0, right : str = 0):
    """
    Crop all images in a specified folder by removing specified amounts from the top, bottom, left, and right.

    Args:
        folder (str): The folder containing the images to be cropped.
        top (int): The number of pixels to remove from the top.
        bottom (int): The number of pixels to remove from the bottom.
        left (int): The number of pixels to remove from the left.
        right (int): The number of pixels to remove from the right.
    """
    # Iterate through each image in the folder
    for filename in os.listdir(folder):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            # Get the image path
            image_path = os.path.join(folder, filename)

            # Crop the image
            crop_image(image_path, top, bottom, left, right)
