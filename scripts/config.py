import os

# Define the base directory
BASE_DIR = r"C:\Users\AaronCendejas\World Class Integration\Engineering 2 - Documents\Software\Python Programs\seismic_scraper"

# Define subdirectories
INPUT_DIR = f"{BASE_DIR}\\data\\input"
OUTPUT_DIR = f"{BASE_DIR}\\data\\output"
LOG_DIR = f"{BASE_DIR}\\data\\logs"

# Ensure directories exist
for dir_path in [INPUT_DIR, OUTPUT_DIR, LOG_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

print(f"Base Directory: {BASE_DIR}")
print(f"Input Directory: {INPUT_DIR}")
print(f"Output Directory: {OUTPUT_DIR}")
print(f"Log Directory: {LOG_DIR}")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OpenAI API key not found. Set it as an environment variable.")