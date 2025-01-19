import fitz
from app.util.util import pdf_to_byte_stream
from PIL import Image
import pytesseract
import io

def extract_images_from_pdf_by_page(pdf_path):
    """
    Extracts images from each page of a PDF (provided as a file path)
    and returns them in a dictionary with page numbers as keys.
    Each value is a list of byte streams for the images on that page.
    If no images are found on a page, an empty list is returned for that page.

    :param pdf_path: Path to the PDF file
    :return: A dictionary where the keys are page numbers (1-based)
             and the values are lists of byte streams for the images on that page
    """
    return extract_images_from_pdf_byte_stream_by_page(pdf_to_byte_stream(pdf_path))

def extract_images_from_pdf_byte_stream_by_page(pdf_byte_stream):
    """
    Extracts images from each page of a PDF (provided as a byte stream)
    and returns them in a dictionary with page numbers as keys.
    Each value is a list of byte streams for the images on that page.
    If no images are found on a page, an empty list is returned for that page.

    :param pdf_byte_stream: Byte stream of the PDF file
    :return: A dictionary where the keys are page numbers (1-based)
             and the values are lists of byte streams for the images on that page
    """
    try:
        # Open the PDF from the byte stream
        pdf_document = fitz.open(stream=pdf_byte_stream, filetype="pdf")

        # Initialize the dictionary to store images by page number
        images_by_page = {}

        # Iterate through all the pages in the PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)  # Load the page
            image_list = page.get_images(full=True)  # Get all images on the page

            # List to store byte streams for images on the current page
            images_on_page = []

            # Loop through the images on this page
            for img_index, img in enumerate(image_list):
                xref = img[0]  # The image reference (xref)
                base_image = pdf_document.extract_image(xref)  # Extract the image data
                image_bytes = base_image["image"]  # Get the image bytes

                # Append the byte stream for this image to the list
                images_on_page.append(image_bytes)

            # Add the page entry to the dictionary (empty list if no images)
            images_by_page[page_num + 1] = images_on_page

        # Close the PDF document
        pdf_document.close()

        return images_by_page

    except Exception as e:
        return f"An error occurred: {e}"

def extract_text_from_image_byte_stream(image_byte_stream):
    """
    Extracts text from an image byte stream using OCR.

    Args:
        image_byte_stream (bytes): Byte stream of the image.

    Returns:
        str: Extracted text from the image.
    """
    # Convert the byte stream to a PIL Image
    image = Image.open(io.BytesIO(image_byte_stream))

    # Perform OCR on the image
    extracted_text = pytesseract.image_to_string(image)
