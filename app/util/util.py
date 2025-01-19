from io import BytesIO
import base64

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