from pptx import Presentation
from io import BytesIO

def extract_text_from_pptx_byte_stream(pptx_byte_stream):
    """
    Extracts text from each slide of a PowerPoint file provided as a byte stream
    and returns it in a dictionary with slide numbers as the keys.

    :param pptx_byte_stream: Byte stream of the PowerPoint file
    :return: A dictionary where the keys are slide numbers (1-based)
             and the values are the extracted text from the corresponding slides
    """
    try:
        # Load the PowerPoint file from the byte stream
        pptx_file = BytesIO(pptx_byte_stream)
        presentation = Presentation(pptx_file)

        # Initialize a dictionary to store text by slide number
        text_by_slide = {}

        # Loop through all slides in the presentation
        for slide_num, slide in enumerate(presentation.slides, start=1):
            slide_text = []

            # Extract text from all shapes on the slide
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        slide_text.append(paragraph.text)

            # Combine all text from the slide into a single string and store it
            text_by_slide[slide_num] = "\n".join(slide_text)

        return text_by_slide

    except Exception as e:
        return f"An error occurred: {e}"

def extract_text_from_pptx_file(pptx_path):
    pass
