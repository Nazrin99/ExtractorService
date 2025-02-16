import zipfile
import io
import xml.etree.ElementTree as ET
from docx import Document
from PIL import Image
import pytesseract
from app.util.util import reconstruct_image_from_byte_stream, delete_file


def extract_images_from_docx_byte_stream(docx_byte_stream):
    """
    Extracts images from a DOCX byte stream and returns them in a dictionary with paragraph numbers as keys.
    Each value is a list of image byte streams associated with that paragraph.

    :param docx_byte_stream: Byte stream of the DOCX file
    :return: A dictionary where the keys are paragraph numbers (1-based)
             and the values are lists of byte streams for the images on that paragraph.
    """
    try:
        # Load the DOCX byte stream
        docx_file = io.BytesIO(docx_byte_stream)

        # Open the DOCX file as a zip archive to access its contents
        with zipfile.ZipFile(docx_file) as docx_zip:
            # Extract document.xml and document.xml.rels
            document_xml = docx_zip.read("word/document.xml")
            rels_xml = docx_zip.read("word/_rels/document.xml.rels")

            # Parse the relationships XML to get image references
            rels_tree = ET.fromstring(rels_xml)
            rels = {rel.attrib['Id']: rel.attrib['Target'] for rel in rels_tree.findall(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}Relationship")}

            # Parse the document.xml content
            tree = ET.fromstring(document_xml)
            namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

            # Dictionary to store images by paragraph number
            images_by_paragraph = {}

            # Iterate through all paragraphs
            for para_idx, para in enumerate(tree.findall(".//w:p", namespace)):
                images_on_para = []

                # Look for runs in the paragraph
                for run in para.findall(".//w:r", namespace):
                    # Check if the run contains a graphic (image)
                    graphic = run.find(".//w:graphic", namespace)
                    if graphic is not None:
                        # Extract the image part's reference (Id from the relationship)
                        blip = graphic.find(".//a:blip",
                                            namespaces={'a': 'http://schemas.openxmlformats.org/drawing/ml/2006/main'})
                        if blip is not None and blip.attrib.get(
                                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"):
                            # Get the image file from the relationships
                            image_ref = blip.attrib[
                                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"]
                            image_file_path = rels.get(image_ref)

                            if image_file_path:
                                # Extract the image data from the DOCX zip file
                                image_data = docx_zip.read("word/" + image_file_path)
                                images_on_para.append(image_data)

                # If images are found in the paragraph, store them
                if images_on_para:
                    images_by_paragraph[para_idx + 1] = images_on_para

            return images_by_paragraph
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
    # Reconstruct the image from the byte stream to a temp file
    temp_file_path = reconstruct_image_from_byte_stream(image_byte_stream,
                                                        r"C:\Users\Nazrin\PycharmProjects\ExtractorService\temp")

    # Open the image using PIL
    image = Image.open(temp_file_path)

    # Perform OCR on the image
    extracted_text = pytesseract.image_to_string(image)

    # Delete the temporary image file
    delete_file(temp_file_path)

    return extracted_text
