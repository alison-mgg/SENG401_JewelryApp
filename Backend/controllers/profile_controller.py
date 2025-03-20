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