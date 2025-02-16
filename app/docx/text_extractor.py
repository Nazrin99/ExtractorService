from docx import Document
import io


def extract_text_from_byte_stream_by_paragraph(docx_byte_stream):
    """
    Extracts text from each paragraph of a .docx file using a byte stream (in-memory)
    and returns it in a dictionary with paragraph numbers as the key.

    :param docx_byte_stream: Raw byte stream of the .docx file
    :return: A dictionary where the keys are the paragraph numbers (1-based index)
             and the values are the extracted text from the corresponding paragraphs.
    """
    try:
        # Load the .docx file from the byte stream
        docx_document = Document(io.BytesIO(docx_byte_stream))

        # Initialize a dictionary to store text by paragraph number
        text_by_paragraph = {}

        # Loop through all paragraphs in the document
        for paragraph_num, paragraph in enumerate(docx_document.paragraphs, start=1):
            text_by_paragraph[paragraph_num] = paragraph.text

        # sort the keys of the dictionary
        text_by_paragraph = dict(sorted(text_by_paragraph.items(), key=lambda item: int(item[0])))

        return text_by_paragraph

    except Exception as e:
        return f"An error occurred: {e}"


def extract_text_from_file_by_paragraph(docx_path):
    """
    Extracts text from each paragraph of a .docx file and returns it in a dictionary
    with the paragraph number as the key.

    :param docx_path: Path to the .docx file
    :return: A dictionary where the keys are the paragraph numbers (1-based index)
             and the values are the extracted text from the corresponding paragraphs.
    """
    try:
        # Read the file as a raw byte stream
        with open(docx_path, "rb") as file:
            docx_byte_stream = file.read()

        return extract_text_from_byte_stream_by_paragraph(docx_byte_stream)

    except Exception as e:
        return f"An error occurred: {e}"
