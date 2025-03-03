import os
import base64
import json
from gemini_config.settings import OUTPUT_JSON

def allowed_file(filename):
    """Check if the uploaded file is an allowed type."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg"}

def encode_image_to_base64(image_path):
    """Convert an image file to a Base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print("Error reading image file:", e)
        return None

def save_to_json(result):
    """Save result to output.json."""
    try:
        with open(OUTPUT_JSON, "w") as json_file:
            json.dump(result, json_file, indent=4)
    except Exception as e:
        print("Error writing to JSON:", e)

def delete_file(file_path):
    """Delete the file after processing."""
    try:
        os.remove(file_path)
        print("Deleted uploaded image:", file_path)
    except Exception as e:
        print("Error deleting file:", e)
