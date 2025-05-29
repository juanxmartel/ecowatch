import os
from dotenv import load_dotenv

load_dotenv()

CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", 300)) 
REPORT_OUTPUT_DIR = os.getenv("REPORT_OUTPUT_DIR", "reports_output")