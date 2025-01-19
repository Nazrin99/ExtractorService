import json
import base64

def convert_page_text_dict_to_json(page_text_dict):
    """
    Converts a dictionary of page numbers and strings into a JSON object
    with a single property 'text', where the properties are the page numbers
    and the values are the strings.

    Args:
        page_text_dict (dict): A dictionary where keys are page numbers (int or str)
                           and values are strings.

    Returns:
        dict: A dictionary representing the desired JSON structure.
    """
    # Wrap the input dictionary inside another dictionary under the 'text' property
    result = {"text": page_text_dict}

    return result


def convert_page_image_dict_to_json(page_image_dict):
    """
    Converts a dictionary with page numbers as keys and lists of byte streams
    as values into a JSON object with a single property 'image', where 'image'
    is an object mapping page numbers to lists of base64 encoded byte streams.

    Args:
        page_image_dict (dict): A dictionary where keys are page numbers (int or str)
                          and values are lists of byte streams.

    Returns:
        dict: A dictionary representing the desired JSON structure.
    """
    # Process the dictionary to base64 encode the byte streams
    encoded_dict = {
        str(page): [base64.b64encode(byte_stream).decode('utf-8') for byte_stream in byte_list]
        for page, byte_list in page_image_dict.items()
    }

    # Wrap the result in the desired JSON structure
    result = {
        "image": encoded_dict
    }

    return result


def convert_page_link_dict_to_json(page_link_dict):
    """
    Converts a dictionary with page numbers as keys and lists of tuples
    (link text, link) as values into a JSON object with a single property
    'link', where 'link' is an object mapping page numbers to lists of lists.

    Args:
        page_link_dict (dict): A dictionary where keys are page numbers (int or str)
                          and values are lists of tuples (str, str) representing
                          link text and link.

    Returns:
        dict: A dictionary representing the desired JSON structure.
    """
    # Convert the dictionary to the required format
    formatted_dict = {
        str(page): [[link_text, link] for link_text, link in link_list]
        for page, link_list in page_link_dict.items()
    }

    # Wrap the result in the desired JSON structure
    result = {
        "link": formatted_dict
    }

    return result


def construct_data_json(*json_objects):
    """
    Merges multiple JSON objects, each containing a single property, into a single JSON object
    with a property "data" containing the combined properties and values.
    Ensures no duplicate property names are present in the input objects.

    Args:
        *json_objects: Any number of JSON objects (dict), each with a single property.

    Returns:
        dict: A dictionary representing the merged object.

    Raises:
        ValueError: If duplicate property names are found in the input objects.
    """
    merged_data = {}
    seen_keys = set()

    for json_obj in json_objects:
        for key in json_obj:
            if key in seen_keys:
                raise ValueError(f"Duplicate property name detected: '{key}'")
            seen_keys.add(key)
            merged_data[key] = json_obj[key]

    # Wrap the merged data in a "data" property
    result = {
        "data": merged_data
    }

    return result