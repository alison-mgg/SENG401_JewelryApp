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

save_chat_bp = Blueprint('save_chat', __name__)

@image_routes.route("/save-to-database", methods=["POST"])
def save_to_database():
    data = request.get_json()
    username = data.get("username")
    image_path = data.get("imagePath")
    description = data.get("description")

    if not username or not image_path or not description:
        return jsonify({"error": "Missing required data."}), 400

    upload_folder = os.path.join(os.getcwd(), "uploads")
    base_folder = os.path.dirname(os.getcwd())
    database_images_folder = os.path.join(base_folder, 'Database', 'images')
    print("Current Working Directory:", os.getcwd())
    print("Base Folder (two levels up):", base_folder)
    print("Upload Folder:", upload_folder)
    print("Database Images Folder:", database_images_folder)
    if not os.path.exists(database_images_folder):
        os.makedirs(database_images_folder)  # Create the folder if it doesn't exist

    source_path = os.path.join(upload_folder, image_path)
    destination_path = os.path.join(database_images_folder, image_path)
    print("source:", source_path)
    print("dest: ", destination_path)
    if not os.path.exists(source_path):
        return jsonify({"error": f"Source file does not exist: {source_path}"}), 400
    try:
        shutil.move(source_path, destination_path)
    except Exception as e:
        return jsonify({"error": f"Failed to move image: {str(e)}"}), 500
    
    try:
        conn = get_database()
        cursor = conn.cursor()

        sql = """
        INSERT INTO chats (username, img_path, links)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (username, destination_path, description))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({"error": f"Failed to save to database: {str(e)}"}), 500

    return jsonify({"message": "Successfully saved to database."})