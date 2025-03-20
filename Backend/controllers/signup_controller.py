from flask import Blueprint, request, jsonify
from database_connector import get_database
from mysql.connector import Error, IntegrityError
from werkzeug.security import generate_password_hash

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "All fields are required!"}), 400

    hashed_password = generate_password_hash(password)

    database = get_database()
    cursor = database.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"message": "Email already in use"}), 400

        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        database.commit()

        return jsonify({"message": "User created successfully!"}), 201

    except IntegrityError as e:
        database.rollback()
        if e.errno == 1062:  # Duplicate entry error code
            return jsonify({"message": "Email already in use"}), 400
        else:
            return jsonify({"message": f"Database Integrity Error: {str(e)}"}), 500

    except Error as e:
        database.rollback()
        return jsonify({"message": f"Database Error: {str(e)}"}), 500

    except Exception as e:
        database.rollback()
        return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        database.close()