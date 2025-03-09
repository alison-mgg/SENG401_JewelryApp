import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key for Gemini
API_KEY = os.getenv("GEMINI_API_KEY")

# Upload directory and output JSON file
UPLOAD_FOLDER = "uploads"
OUTPUT_JSON = "output.json"

# Allowed file types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
