from flask import Blueprint, request, jsonify
from database_connector import get_database
import os
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
import shutil

save_chat_bp = Blueprint('save_chat', __name__)

@save_chat_bp.route('/save-to-database', methods=['POST'])
def save_to_database():
    data = request.get_json()
    username = data.get("username")
    image_path = data.get("imagePath")
    similar_products = data.get("similarProducts")  # Get similar products from the request

    print("Received data:", data)  # Log the received data

    if not username or not image_path or not similar_products:
        return jsonify({"error": "Missing required data."}), 400

    upload_folder = os.path.join(os.getcwd(), "uploads")
    base_folder = os.path.dirname(os.getcwd())
    database_images_folder = os.path.join(base_folder, 'Database', 'images')

    if not os.path.exists(database_images_folder):
        os.makedirs(database_images_folder)  # Create the folder if it doesn't exist

    source_path = os.path.join(upload_folder, image_path)
    destination_path = os.path.join(database_images_folder, image_path)

    print("Source Path:", source_path)
    print("Destination Path:", destination_path)

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
        INSERT INTO chats (username, img_path, response)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (username, destination_path, similar_products))  # Save similar products
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({"error": f"Failed to save to database: {str(e)}"}), 500

    return jsonify({"message": "Successfully saved to database."})