from flask import Flask, request, jsonify
import base64
from app.logic import extract_information
from app.pdf.image_extractor import extract_images_from_pdf_byte_stream_by_page
from app.util.endpoint_data_util import convert_page_image_dict_to_json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/extract', methods=['POST'])
def extract():
    """
    Endpoint to validate and process JSON data sent via POST request.
    """
    try:
        # Parse the incoming JSON data
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate 'data' field
        if 'data' not in data:
            return jsonify({"error": "'data' field is missing"}), 400

        # Ensure 'data' is base64 encoded
        try:
            base64.b64decode(data['data'])
        except (base64.binascii.Error, ValueError):
            return jsonify({"error": "'data' field is not valid base64 encoded"}), 400

        # Validate 'file_type' field
        if 'file_type' not in data:
            return jsonify({"error": "'file_type' field is missing"}), 400

        if not isinstance(data['file_type'], str):
            return jsonify({"error": "'file_type' must be a string"}), 400

        # Ensure 'file_type' is one of the allowed types
        allowed_file_types = {"PDF", "PPTX", "DOCX", "TXT"}
        if data['file_type'].upper() not in allowed_file_types:
            return jsonify({
                "error": f"'file_type' must be one of {', '.join(allowed_file_types)}"
            }), 400

        # If all validations pass
        response_object = extract_information(str(data['file_type']), data['data'])

        return jsonify(response_object), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test', methods=['POST'])
def test():

    data = request.get_json()

    response = convert_page_image_dict_to_json(extract_images_from_pdf_byte_stream_by_page(data['data']))

    return jsonify({"message": response}), 200

if __name__ == '__main__':
    app.run(port=5001)

