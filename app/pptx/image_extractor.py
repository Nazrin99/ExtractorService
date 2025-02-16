from pptx import Presentation
from PIL import Image
import pytesseract
import io

def extract_images_from_pptx_byte_stream(pptx_byte_stream):
    """
    Extracts images from each slide of a PowerPoint file (provided as a byte stream)
    and performs OCR on them. Returns a dictionary with slide numbers as keys
    and lists of OCR-extracted text as values.

    :param pptx_byte_stream: Byte stream of the PowerPoint (.pptx) file
    :return: A dictionary where keys are slide numbers (1-based)
             and values are lists of extracted text from the images on that slide
    """
    try:
        # Open the PowerPoint presentation from the byte stream
        presentation = Presentation(io.BytesIO(pptx_byte_stream))

        # Initialize the dictionary to store OCR results by slide number
        text_by_slide = {}

        # Iterate through all the slides in the presentation
        for slide_num, slide in enumerate(presentation.slides, start=1):
            ocr_results = []

            # Loop through all shapes on the slide
            for shape in slide.shapes:
                # Check if the shape contains a picture
                if shape.shape_type == 13:  # Shape type 13 corresponds to pictures
                    image = shape.image
                    image_bytes = image.blob  # Get the raw image bytes

                    # Extract text from the image byte stream using OCR
                    extracted_text = extract_text_from_image_byte_stream(image_bytes)
                    ocr_results.append(extracted_text)

            # Store the OCR results for the slide (empty list if no images)
            text_by_slide[slide_num] = ocr_results

        return text_by_slide

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
    try:
        # Convert the byte stream to a PIL Image
        image = Image.open(io.BytesIO(image_byte_stream))

        # Perform OCR on the image
        extracted_text = pytesseract.image_to_string(image)

        return extracted_text

    except Exception as e:
        return f"An error occurred while performing OCR: {e}"
