from flask import Blueprint, request, jsonify
from database_connector import get_database

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    database = get_database()
    cursor = database.cursor(dictionary=True)

    
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user['password']
            
            # Compare plain text passwords
            if password == stored_password:
                return jsonify({
                    "message": "Login successful!",
                    "user": {"id": user["id"], "username": user["username"], "email": user["email"]}
                }), 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401
        else:
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        cursor.close()        
            