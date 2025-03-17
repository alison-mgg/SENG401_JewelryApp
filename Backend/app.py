from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend deployment
CORS(app, resources={r"/*": {"origins": r"https://.*\.vercel\.app"}}, supports_credentials=True)


# MySQL Database configuration using environment variables
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

# Function to get database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    return connection

# Test route to confirm Heroku deployment
@app.route('/')
def home():
    return jsonify({"message": "Jewelry Dupe Finder backend running successfully!"})

# Route to test DB connection
@app.route('/test-db-connection')
def test_db_connection():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return jsonify({"database_status": "connected", "test_query_result": result})
    except Exception as e:
        return jsonify({"database_status": "error", "error": str(e)}), 500

# Test API endpoint
@app.route('/users')
def get_users():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users')
        
        # Fetch all the results
        users = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Register Blueprints
from controllers.signup_controller import signup_bp
app.register_blueprint(signup_bp, url_prefix='/signup')

# Signup route
@app.route('/api/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "https://seng-401-jewelry-app-git-development-alison-gartners-projects.vercel.app")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    connection = get_db_connection()
    cursor = connection.cursor()
    data = request.get_json()
    username = data['username']
    password = data['password']
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    try:
        cursor.execute(query, (username, password))
        connection.commit()
        return jsonify({"message": "User signed up successfully"}), 200
    except Error as e:
        print(f"The error '{e}' occurred")
        return jsonify({"message": "Error signing up"}), 500
    finally:
        cursor.close()
        connection.close()

# Main entry point for the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)