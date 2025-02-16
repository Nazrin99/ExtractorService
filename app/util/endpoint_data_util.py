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

    # Convert each propert in page_text_dict to string
    page_text_dict = {str(key): value for key, value in page_text_dict.items()}
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
        str(page): [str(byte_stream) for byte_stream in byte_list]
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

def simplify_data_json(json_object):
    """
    Combines the text from the "image" and "text" properties in the JSON object based on their keys.
    Creates a new JSON object with the combined text assigned to the "data" property.
    Includes the "file_type" property from the input JSON object in the output.

    Args:
        json_object (dict): Input JSON object with "image" and "text" properties.

    Returns:
        dict: A new JSON object with combined text under the "data" property and the "file_type".
    """
    combined_data = {}

    # Extract "image" and "text" properties from the input JSON object
    image_data = json_object.get("data", {}).get("image", {})
    text_data = json_object.get("data", {}).get("text", {})

    # Combine the text for matching keys
    for key in set(image_data.keys()).union(text_data.keys()):
        image_text = " ".join(image_data.get(key, []))  # Join image text if it's a list
        text_content = text_data.get(key, "")  # Get text content
        combined_data[key] = f"{image_text} {text_content}".strip()

    # Wrap the combined text in a "data" property and include "file_type"
    return {"data": combined_data}

def collapse_data_object(json_obj):
    """
    Combines all properties under the 'data' key of the JSON object into a single string
    and assigns the result back to the 'data' key.

    Args:
        json_obj (dict): JSON object containing a 'data' property with multiple keys.

    Returns:
        dict: Updated JSON object with combined 'data' string.
    """
    if 'data' in json_obj and isinstance(json_obj['data'], dict):
        combined_data = []

        for key, value in json_obj['data'].items():
            try:
                # Handle nested dictionaries or non-string values
                if isinstance(value, dict):
                    value = str(value)
                elif value is None:
                    value = ""  # Skip None values
                combined_data.append(str(value))
            except Exception as e:
                print(f"Error processing key {key}: {e}")

        # Combine all processed values into a single string
        json_obj['data'] = " ".join(combined_data)

        print(f"Processed {len(combined_data)} entries out of {len(json_obj['data'])}")

    return json_obj


