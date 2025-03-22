import os
import base64
import json
from gemini_config.settings import OUTPUT_JSON  # Import the path for output JSON file from settings

def allowed_file(filename):
    """Check if the uploaded file is an allowed type (png, jpg, jpeg)."""
    # Checks if the file has a valid extension (png, jpg, jpeg) and returns True if allowed
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg"}

def encode_image_to_base64(image_path):
    """Convert an image file to a Base64 string."""
    try:
        # Open the image file in binary read mode and convert its content to base64
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")  # Return base64 encoded string of the image
    except Exception as e:
        print("Error reading image file:", e)  # Print error if there’s an issue reading the image file
        return None  # Return None if there is an error

def save_to_json(result):
    """Save result to output.json file."""
    try:
        # Open the output JSON file in write mode and dump the result as a formatted JSON object
        with open(OUTPUT_JSON, "w") as json_file:
            json.dump(result, json_file, indent=4)  # Save the result to the JSON file with an indent for readability
    except Exception as e:
        print("Error writing to JSON:", e)  # Print error if there’s an issue saving to the JSON file

def delete_file(file_path):
    """Delete the file after processing."""
    try:
        # Remove the file from the filesystem after processing
        os.remove(file_path)
        print("Deleted uploaded image:", file_path)  # Log the deletion of the file
    except Exception as e:
        print("Error deleting file:", e)  # Print error if there’s an issue deleting the file
