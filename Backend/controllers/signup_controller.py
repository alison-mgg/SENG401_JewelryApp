from flask import Blueprint, request, jsonify, make_response
from database_connector import get_database
from mysql.connector import Error, IntegrityError
from werkzeug.security import generate_password_hash
import os

signup_bp = Blueprint('signup', __name__)

# Get the origin URL from environment variables
ORIGIN_URL = os.getenv('ORIGIN_URL')

@signup_bp.route('/', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        response = make_response('', 200)
        response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        response = jsonify({"message": "All fields are required!"})
        response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 400

    hashed_password = generate_password_hash(password)

    database = get_database()
    cursor = database.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            response = jsonify({"message": "Email already in use"})
            response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 400

        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        database.commit()

        response = jsonify({"message": "User created successfully!"})
        response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 201

    except IntegrityError as e:
        database.rollback()
        if e.errno == 1062:  # Duplicate entry error code
            response = jsonify({"message": "Email already in use"})
            response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 400
        else:
            response = jsonify({"message": f"Database Integrity Error: {str(e)}"})
            response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 500

    except Error as e:
        database.rollback()
        response = jsonify({"message": f"Database Error: {str(e)}"})
        response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 500

    except Exception as e:
        database.rollback()
        response = jsonify({"message": f"An unexpected error occurred: {str(e)}"})
        response.headers.add('Access-Control-Allow-Origin', ORIGIN_URL)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 500

    finally:
        cursor.close()
        database.close()