import pytesseract

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Update for your OS

# Example usage
print(f"Py Tesseract Version: {pytesseract.get_tesseract_version()}", )