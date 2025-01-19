import fitz  # PyMuPDF
from app.util.util import pdf_to_byte_stream

def extract_hyperlinks_from_byte_stream_by_page(pdf_byte_stream):
    """
    Extracts hyperlinks from a PDF byte stream and returns a dictionary with page numbers as keys.
    Each value is a list of tuples containing the link text and the real link (URL).

    :param pdf_byte_stream: Byte stream of the PDF file
    :return: A dictionary where keys are page numbers (1-based) and values are lists of (link text, link URL) tuples
    """
    try:
        # Open the PDF from the byte stream
        pdf_document = fitz.open(stream=pdf_byte_stream, filetype="pdf")

        # Dictionary to store hyperlinks by page
        hyperlinks_by_page = {}

        # Loop through each page in the PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)  # Load the page
            links = page.get_links()  # Get all links on the page

            # List to store (link text, real link) tuples for this page
            page_links = []

            # Process each link on the page
            for link in links:
                # Extract the real link (URL)
                uri = link.get("uri")
                if uri:  # Only process if a URI is found
                    # Try to get the link text if possible
                    rect = link.get("from")  # The rectangle containing the link text
                    if rect:
                        link_text = page.get_textbox(rect).strip()
                    else:
                        link_text = ""  # Fallback if no link text is available

                    # Add the (link text, real link) tuple to the page's list
                    page_links.append((link_text, uri))

            # Add the page's links to the dictionary (even if empty)
            hyperlinks_by_page[page_num + 1] = page_links

        # Close the PDF document
        pdf_document.close()

        return hyperlinks_by_page

    except Exception as e:
        return f"An error occurred: {e}"

def extract_hyperlinks_from_file_by_page(pdf_path):
    """
    Extracts hyperlinks from a PDF file and returns a dictionary with page numbers as keys.
    Each value is a list of tuples containing the link text and the real link (URL).

    :param pdf_path: Path to the PDF file
    :return: A dictionary where keys are page numbers (1-based) and values are lists of (link text, link URL) tuples
    """
    return extract_hyperlinks_from_byte_stream_by_page(pdf_to_byte_stream(pdf_path))

