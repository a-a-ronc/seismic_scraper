import os
import json
from scripts.config import OUTPUT_DIR
from datetime import datetime

def consolidate_files():
    consolidated_data = {"files": []}

    for file_name in os.listdir(OUTPUT_DIR):
        if file_name.endswith(".json") and file_name != "consolidated_data.json":
            file_path = os.path.abspath(os.path.dirname(__file__))
            with open(file_path, "r") as infile:
                data = json.load(infile)
                consolidated_data["files"].append(data)

    # Save the consolidated file
    consolidated_path = os.path.join(
        OUTPUT_DIR, f"consolidated_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    with open(consolidated_path, "w") as outfile:
        json.dump(consolidated_data, outfile, indent=4)

    print(f"Consolidated data saved to {consolidated_path}")

if __name__ == "__main__":
    consolidate_files()
    if not os.path.exists(OUTPUT_DIR):
        raise FileNotFoundError(f"Output directory {OUTPUT_DIR} does not exist.")
