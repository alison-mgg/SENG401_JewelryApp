# from flask import Flask
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from database_connector import get_database
# from controllers.signup_controller import signup_bp
# #from gemini_config.settings import UPLOAD_FOLDER
# #from routes.image_routes import image_routes
# #from routes.description_routes import description_routes
# #^^These imports will be integrated once the ai connection branch is ready

# load_dotenv()

# app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"], supports_credentials=True)  # Enable CORS

# # MySQL Database configuration using environment variables
# app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
# app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
# app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
# app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')


# #For ai integration branch:
# #app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# # Register Blueprints
# #app.register_blueprint(image_routes)
# #app.register_blueprint(description_routes)

# app.register_blueprint(signup_bp)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend (React app hosted on Vercel)
# CORS(app, origins=["https://seng-401-jewelry-app.vercel.app/"], supports_credentials=True)
CORS(app, origins=["https://*.seng-401-jewelry-app.vercel.app"], supports_credentials=True)
# Vercel branch render-backend-deployment (change to main branch Vercel link after)

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

# Test route to confirm Render deployment
@app.route('/')
def home():
    return jsonify({"message": "Jewelry Dupe Finder backend running successfully!"})

# MARKER - test-db-connection and test-users routes are working from Render deployment
# with AWS RDS - vpc security group set to allow all traffic from 0.0.0.0 MySQL/Aurora
# Change this after testing done to make more secure

# Test route for DB connection
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
@app.route('/test-users')
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
    
# Signup route
@app.route('/signup', methods=['POST'])
def signup():
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

# Register Blueprints
from controllers.signup_controller import signup_bp
app.register_blueprint(signup_bp, url_prefix='/signup')

# Main entry point for the app
if __name__ == '__main__':
    app.run(debug=True)