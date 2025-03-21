import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from gemini_config.settings import UPLOAD_FOLDER
from datetime import datetime
import shutil
from services.file_utils import encode_image_to_base64, delete_file, allowed_file
from services.gemini_service import analyze_image
from database_connector import get_database

image_routes = Blueprint("image_routes", __name__)

@image_routes.route("/upload", methods=["POST"])
def upload_file():
    """Handle image upload and analysis."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded."}), 400

    file = request.files["image"]

    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type."}), 400

    filename = secure_filename(file.filename)
    renamed_filename = f"uploaded_{filename}"
    image_path = os.path.join(UPLOAD_FOLDER, renamed_filename)
    file.save(image_path)

    print("File received:", image_path)

    base64_image = encode_image_to_base64(image_path)
    if not base64_image:
        return jsonify({"error": "Failed to process image."}), 500

    result = analyze_image(base64_image)
    print("AI Response:", result)
    
    if not result or "description" not in result:
        return jsonify({"error": "Invalid response from AI analysis."}), 500

    # Return the renamed filename to the frontend
    return jsonify({
        **result,
        "filename": renamed_filename,  # Include the renamed filename in the response
    })
    # return jsonify(result)
