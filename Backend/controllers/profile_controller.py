from flask import Blueprint, request, jsonify
from database_connector import get_database
import os
from werkzeug.utils import secure_filename
from flask_cors import cross_origin

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/user/<username>', methods=['GET'])
def get_user(username):
    database = get_database()
    cursor = database.cursor(dictionary=True)

    try:
        cursor.execute("SELECT username, email FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# profile_controller.py

@profile_bp.route('/api/user/<username>/images', methods=['GET'])
def get_user_images(username):
    database = get_database()
    cursor = database.cursor(dictionary=True)

    try:
        cursor.execute("SELECT img_path, response FROM chats WHERE username = %s", (username,))
        chats = cursor.fetchall()

        if chats:
            chats_with_urls = [
                {
                    "img_path": f"/static/{chat['img_path']}",
                    "response": chat["response"]
                }
                for chat in chats
            ]
            return jsonify(chats_with_urls), 200
        else:
            return jsonify({"error": "No images found for this user"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()