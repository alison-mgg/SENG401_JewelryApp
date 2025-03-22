import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from gemini_config.settings import UPLOAD_FOLDER
from datetime import datetime
import shutil
from services.file_utils import encode_image_to_base64, delete_file, allowed_file
from services.gemini_service import analyze_image
from Backend.database_connector import get_database

image_routes = Blueprint("image_routes", __name__)

@image_routes.route("/upload", methods=["POST"])
def upload_file():
    """Handle image upload and analysis."""
    
    # Check if the image is in the request
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded."}), 400

    file = request.files["image"]

    # Validate the file type and name
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type."}), 400

    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    renamed_filename = f"uploaded_{filename}"  # Rename the file for uniqueness
    image_path = os.path.join(UPLOAD_FOLDER, renamed_filename)
    file.save(image_path)

    print("File received:", image_path)

    # Convert image to base64 encoding for processing
    base64_image = encode_image_to_base64(image_path)
    if not base64_image:
        return jsonify({"error": "Failed to process image."}), 500

    # Analyze the image with the AI service
    result = analyze_image(base64_image)
    print("AI Response:", result)
    
    # Check if the AI analysis response is valid
    if not result or "description" not in result:
        return jsonify({"error": "Invalid response from AI analysis."}), 500

    # Return the result along with the renamed filename
    return jsonify({
        **result,
        "filename": renamed_filename,  # Include the renamed filename in the response
    })
