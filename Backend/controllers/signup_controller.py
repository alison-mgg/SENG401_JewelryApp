from flask import Blueprint, request, jsonify
from database_connector import get_database


signup_bp = Blueprint('signup', __name__)

# signup_bp = Blueprint('signup_bp', __name__)

# Route to test if the signup route is working
@signup_bp.route('/', methods=['GET'])
def signup_home():
    return jsonify({"message": "Signup route is working!"})

@signup_bp.route('signup', methods=['POST', 'OPTIONS']) #OPTIONS IS FOR DEBUG CODE
def signup():
    if request.method == 'OPTIONS': #DEBUG CODE
        return '', 200              #DEBUG CODE

    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "All fields are required!"}), 400

    # Create a cursor to execute queries
    database = get_database()
    cursor = database.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"message": "Email already in use"}), 400

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, password))
        database.commit()

        return jsonify({"message": "User created successfully!"}), 201

    except Exception as e:
        database.rollback()
        return jsonify({"message": str(e)}), 500

    finally:
        cursor.close()
