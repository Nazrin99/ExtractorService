from app.pdf.image_extractor import extract_images_from_pdf_byte_stream_by_page
from app.pdf.text_extractor import extract_text_from_byte_stream_by_page
from app.docx.text_extractor import extract_text_from_byte_stream_by_paragraph
from app.docx.image_extractor import extract_text_from_image_byte_stream, extract_images_from_docx_byte_stream
from app.pptx.image_extractor import extract_images_from_pptx_byte_stream
from app.pptx.text_extractor import extract_text_from_pptx_byte_stream
from app.txt.text_extractor import extract_text_from_txt_byte_stream
from app.util.endpoint_data_util import convert_page_text_dict_to_json, convert_page_image_dict_to_json, construct_data_json, simplify_data_json, collapse_data_object
from app.util.util import decode_base64_to_bytes

def extract_information(file_type, data, return_representation=False, collapse_object=False):
    """

    :param return_representation:
    :param file_type: string which is a value from enumeration of file_format_enum.py
    :type data: base64 encoded string of the document's byte stream
    """

    document_byte_stream = decode_base64_to_bytes(data)

    if file_type == "PDF":
        page_image_dict = extract_images_from_pdf_byte_stream_by_page(document_byte_stream)
        page_text_dict = extract_text_from_byte_stream_by_page(document_byte_stream)
        data_json_object = construct_data_json(
            convert_page_image_dict_to_json(page_image_dict),
            convert_page_text_dict_to_json(page_text_dict)
        )
    elif file_type == "DOCX":
        page_text_dict = extract_text_from_byte_stream_by_paragraph(document_byte_stream)
        page_image_dict = extract_images_from_docx_byte_stream(document_byte_stream)
        data_json_object = construct_data_json(
            convert_page_text_dict_to_json(page_text_dict),
            convert_page_image_dict_to_json(page_image_dict)
        )
    elif file_type == "PPTX":
        page_text_dict = extract_text_from_pptx_byte_stream(document_byte_stream)
        page_image_dict = extract_images_from_pptx_byte_stream(document_byte_stream)
        data_json_object = construct_data_json(
            convert_page_text_dict_to_json(page_text_dict),
            convert_page_image_dict_to_json(page_image_dict)
        )
    elif file_type == "TXT":
        page_text_dict = extract_text_from_txt_byte_stream(document_byte_stream)
        data_json_object = construct_data_json(
            convert_page_text_dict_to_json(page_text_dict)
        )
    else:
        return f"Unsupported file type: {file_type}"

    if not return_representation:
        data_json_object = simplify_data_json(data_json_object)
        if collapse_object:
            data_json_object = collapse_data_object(data_json_object)

    # Create json object with the property file_type and data
    result = {
        "file_type": file_type,
        "data": data_json_object['data']
    }

    return result




