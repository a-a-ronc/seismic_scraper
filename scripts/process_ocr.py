import pytesseract
from pdf2image import convert_from_path
import os

def ocr_pdf(file_path, dpi=300):
    # Convert PDF to images
    images = convert_from_path(file_path, dpi=dpi)
    ocr_results = []
    for page_number, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        ocr_results.append({"page_number": page_number + 1, "text": text})
    return ocr_results

if __name__ == "__main__":
    input_pdf = "path/to/your/input.pdf"
    ocr_data = ocr_pdf(input_pdf)
    print(ocr_data)  # Or save it to a file for further processing
