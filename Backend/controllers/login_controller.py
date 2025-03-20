from flask import Blueprint, request, jsonify, make_response
from database_connector import get_database
import os

login_bp = Blueprint('login', __name__)

# Get the origin URL from environment variables
ORIGIN_URL = os.getenv('ORIGIN_URL')

# MARKER - Login route is working from Render deployment
@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        response = jsonify({"message": "Username and password are required!"})
        response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 400

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
                resp.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
                resp.headers.add('Access-Control-Allow-Credentials', 'true')
                return resp, 200
            else:
                response = jsonify({"message": "Invalid credentials"})
                response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 401
        else:
            response = jsonify({"message": "User not found"})
            response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 404

    except Exception as e:
        response = jsonify({"message": str(e)})
        response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 500

    finally:
        cursor.close()

@login_bp.route('/cookie', methods=['GET', 'POST'])
def getCookie():
    if request.method == 'POST':
        name = request.form.get('username')  # Use .get() to avoid errors if key is missing
        if not name:
            response = jsonify({"message": "Username is required"})
            response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 400
        
        resp = jsonify({"message": f"Cookie set for {username}"})  # Use jsonify instead of output
        resp.set_cookie('username', username, httponly=True, secure=(request.scheme == 'https'))
        resp.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
        resp.headers.add('Access-Control-Allow-Credentials', 'true')
        return resp
    elif request.method == 'GET':
        username = request.cookies.get('username')  # Retrieve the cookie value
        if username:
            resp = jsonify({"message": f"Cookie found for {username}", "username": username})
            resp.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
            resp.headers.add('Access-Control-Allow-Credentials', 'true')
            return resp, 200
        resp = jsonify({"message": "No cookie found"})
        resp.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
        resp.headers.add('Access-Control-Allow-Credentials', 'true')
        return resp, 404
