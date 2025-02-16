import base64
import io
import os
import uuid
from io import BytesIO

from PIL import Image


def pdf_to_byte_stream(pdf_path):
    """
    Converts a PDF file to a byte stream.

    :param pdf_path: Path to the PDF file
    :return: Byte stream representing the PDF content
    """
    try:
        # Open the PDF file in binary read mode
        with open(pdf_path, "rb") as pdf_file:
            # Read the file content into a byte stream
            pdf_byte_stream = BytesIO(pdf_file.read())

        return pdf_byte_stream

    except Exception as e:
        return f"An error occurred: {e}"

def decode_base64_to_bytes(base64_string):
    """
    Decodes a Base64-encoded string back to a byte stream.

    Args:
        base64_string (str): The Base64-encoded string.

    Returns:
        bytes: The decoded byte stream.
    """
    return base64.b64decode(base64_string)

def reconstruct_image_from_byte_stream(byte_stream, output_directory):
    """
    Reconstructs an image from its byte stream, saves it to the specified directory,
    and returns the file path. The file name is generated dynamically, and the
    correct extension is determined from the byte stream metadata.

    Args:
        byte_stream (bytes): Byte stream of the image.
        output_directory (str): Directory to save the reconstructed image.

    Returns:
        str: The file path of the saved image.
    """
    # Create a BytesIO object from the byte stream
    image_stream = io.BytesIO(byte_stream)

    # Open the image using PIL
    image = Image.open(image_stream)

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Generate a unique file name with the correct extension
    file_name = f"{uuid.uuid4()}.{image.format.lower()}"  # Image.format gives the extension
    file_path = os.path.join(output_directory, file_name)

    # Save the image to the specified path
    image.save(file_path)

    print(f"Image successfully reconstructed and saved at {file_path}")
    return file_path

def delete_file(file_path):
    """
    Deletes the file at the specified file path.

    Args:
        file_path (str): The path to the file to be deleted.

    Returns:
        bool: True if the file was deleted successfully, False otherwise.
    """
    try:
        # Check if the file exists before attempting to delete
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")
            return True
        else:
            print(f"File '{file_path}' does not exist.")
            return False
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")
        return False