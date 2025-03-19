from flask import Blueprint, request, jsonify
from database_connector import get_database

login_bp = Blueprint('login', __name__)


@login_bp.route('/api/login', methods=['POST'])
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
                resp = jsonify({
                    "message": "Login successful!",
                    "user": {"id": user["id"], "username": user["username"], "email": user["email"]}
                })

                # Set secure flag based on request scheme (http or https)
                secure_flag = request.scheme == 'https'

                resp.set_cookie('username', username, httponly=True, secure=secure_flag)
                return resp, 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401
        else:
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        cursor.close()        

@login_bp.route('/api/cookie', methods=['GET', 'POST'])
def getCookie():
    if request.method == 'POST':
        name = request.form.get('username')  # Use .get() to avoid errors if key is missing
        if not name:
            return jsonify({"message": "Username is required"}), 400
        
        resp = jsonify({"message": f"Cookie set for {username}"})  # Use jsonify instead of output
        resp.set_cookie('username', username, httponly=True, secure=(request.scheme == 'https'))
        return resp
    elif request.method == 'GET':
        username = request.cookies.get('username')  # Retrieve the cookie value
        if username:
            return jsonify({"message": f"Cookie found for {username}", "username": username}), 200
        return jsonify({"message": "No cookie found"}), 404
