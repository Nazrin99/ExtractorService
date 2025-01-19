import fitz  # PyMuPDF
from app.util.util import pdf_to_byte_stream


def extract_text_from_byte_stream_by_page(pdf_byte_stream):
    """
    Extracts text from each page of a PDF using a byte stream (in-memory)
    and returns it in a dictionary with page number as the key.

    :param pdf_byte_stream: Byte stream of the PDF file
    :return: A dictionary where the keys are the page numbers (1-based)
             and the values are the extracted text from the corresponding pages
    """
    try:
        # Open the PDF from the byte stream
        pdf_document = fitz.open(stream=pdf_byte_stream, filetype="pdf")

        # Initialize a dictionary to store text by page number
        text_by_page = {}

        # Loop through all the pages
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)  # Get the page
            text = page.get_text()  # Extract text from the page

            # Store the extracted text in the dictionary with page number as key (1-based index)
            text_by_page[page_num + 1] = text

        # Close the PDF document
        pdf_document.close()

        return text_by_page

    except Exception as e:
        return f"An error occurred: {e}"

def extract_text_from_file_by_page(pdf_path):
    """
    Extracts text from each page of a PDF file using PyMuPDF and returns it in a dictionary
    with the page number as the key.

    :param pdf_path: Path to the PDF file
    :return: A dictionary where the keys are the page numbers (1-based)
             and the values are the extracted text from the corresponding pages
    """
    return extract_text_from_byte_stream_by_page(pdf_to_byte_stream(pdf_path))
