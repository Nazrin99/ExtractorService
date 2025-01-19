from app.pdf.image_extractor import extract_images_from_pdf_byte_stream_by_page
from app.pdf.text_extractor import extract_text_from_byte_stream_by_page
from app.pdf.link_extractor import extract_hyperlinks_from_byte_stream_by_page
from app.util.endpoint_data_util import convert_page_text_dict_to_json, convert_page_link_dict_to_json, convert_page_image_dict_to_json, construct_data_json
from app.util.util import decode_base64_to_bytes

def extract_information(file_type, data):
    """

    :param file_type: string which is a value from enumeration of file_format_enum.py
    :type data: base64 encoded string of the document's byte stream
    """

    document_byte_stream = decode_base64_to_bytes(data)

    page_image_dict = extract_images_from_pdf_byte_stream_by_page(document_byte_stream)
    page_text_dict = extract_text_from_byte_stream_by_page(document_byte_stream)

    data_json_object = construct_data_json(
        convert_page_image_dict_to_json(page_image_dict),
        convert_page_text_dict_to_json(page_text_dict)
    )

    # Create json object with the property file_type and data
    result = {
        "file_type": file_type,
        "data": data_json_object['data']
    }

    return result




