import os
from tqdm import tqdm
import re
import pdfplumber
import json
import openai
import logging
from config import INPUT_DIR, OUTPUT_DIR, LOG_DIR, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# Ensure directories exist (relying on config.py settings)
if not os.path.exists(INPUT_DIR):
    raise FileNotFoundError(f"Input directory does not exist: {INPUT_DIR}")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
logging.basicConfig(
    filename=f"{LOG_DIR}/processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Extract the text
def extract_text_from_pdf(file_path):
    data = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()
            data.append({"page_number": page_number + 1, "text": text})
    return data

# Parsing logic using regex to extract specific elements dynamically
def parse_configuration(page_text):
    try:
        # Match configuration name
        config_match = re.search(r"Configuration\s\d+:\s(\w+)", page_text)
        configuration_name = config_match.group(1) if config_match else None

        # Match number of levels
        levels_match = re.search(r"Levels:\s(\d+)", page_text)
        levels = int(levels_match.group(1)) if levels_match else None

        # Match load per level
        loads = re.findall(r"(\d+)\s*lbs", page_text)

        # Parse frame data
        frame_section = re.search(r"FRAME\s(.*?)\n\n", page_text, re.DOTALL)
        frame_data = frame_section.group(1).splitlines() if frame_section else []

        return {
            "configuration_name": configuration_name,
            "levels": levels,
            "loads": loads,
            "frame_data": frame_data
        }
    except Exception as e:
        logging.error(f"Error parsing configuration: {e}")
        return {
            "configuration_name": None,
            "levels": 0,
            "loads": [],
            "frame_data": []
        }

# Extract tables (e.g., Frame, Beam, Connector, Base Plate, etc.)
def extract_tables_from_page(page):
    tables = page.extract_table()
    return tables if tables else []

# Process the PDF
def process_pdf(file_path):
    extracted_data = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(tqdm(pdf.pages, desc="Processing PDF")):
            try:
                text = page.extract_text()
                tables = extract_tables_from_page(page)
                parsed_data = parse_configuration(text)
                parsed_data["page_number"] = page_number + 1
                parsed_data["tables"] = tables
                extracted_data.append(parsed_data)
            except Exception as e:
                logging.error(f"Error processing page {page_number + 1}: {e}")
    return extracted_data

# Save extracted data to JSON
def save_to_json(data, output_path):
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

# Main function
def main():
    for file_name in os.listdir(INPUT_DIR):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(INPUT_DIR, file_name)
            output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file_name)[0]}.json")
            logging.info(f"Processing file: {file_name}")
            try:
                extracted_data = process_pdf(file_path)
                save_to_json(extracted_data, output_path)
                logging.info(f"Successfully processed and saved: {output_path}")
            except Exception as e:
                logging.error(f"Failed to process {file_name}: {e}")

if __name__ == "__main__":
    main()
