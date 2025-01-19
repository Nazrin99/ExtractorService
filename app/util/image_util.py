from PIL import Image
from io import BytesIO
import os

def get_image_format_from_byte_stream(image_byte_stream):
    """
    Determines the image format (PNG, JPG, GIF, BMP) from the provided byte stream.

    :param image_byte_stream: Byte stream of the image
    :return: A string indicating the image format (e.g., 'png', 'jpeg', 'gif', 'bmp')
    """
    try:
        # Open the image from the byte stream using PIL (Pillow)
        img = Image.open(BytesIO(image_byte_stream))

        # Get the image format in its original form (e.g., 'png', 'jpeg', 'gif', 'bmp')
        img_format = img.format.lower()

        # Return the image format
        return img_format

    except Exception as e:
        return f"Error: {e}"


def save_images_from_byte_streams(output_directory, images_dict):
    """
    Saves images from a dictionary of byte streams to an output directory.

    :param output_directory: The directory to save the image files.
    :param images_dict: A dictionary where keys are integers (e.g., page numbers)
                        and values are lists of byte streams (each representing an image).
    """
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    for key, byte_streams in images_dict.items():
        for index, byte_stream in enumerate(byte_streams):
            try:
                # Get the file extension from the byte stream
                file_extension = get_image_format_from_byte_stream(byte_stream)

                if not file_extension:
                    print(f"Could not determine the file format for key {key}, index {index + 1}")
                    continue

                # Create a file name using the key, index, and file extension
                file_name = f"{key}_{index + 1}.{file_extension}"
                file_path = os.path.join(output_directory, file_name)

                # Open the byte stream as an image
                image = Image.open(BytesIO(byte_stream))

                # Save the image with the determined format
                image.save(file_path, format=image.format)

                # Print the name of the successfully created file
                print(f"Successfully created: {file_name}")

            except Exception as e:
                print(f"Failed to create file for key {key}, index {index + 1}: {e}")