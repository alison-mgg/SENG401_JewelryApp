# Std library import
import os

# Third-party imports
from flask import Flask, jsonify, g, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv
from Gemini_Testing.routes import similar_product_routes
import mysql.connector
from mysql.connector import Error, IntegrityError

# Local imports
from database_connector import get_database
from controllers.signup_controller import signup_bp
from controllers.login_controller import login_bp
from controllers.chat_controller import save_chat_bp

from database_connector import get_database

from Gemini_Testing.gemini_config.settings import UPLOAD_FOLDER
from Gemini_Testing.routes.image_routes import image_routes
from Gemini_Testing.routes.description_routes import description_routes
# ^^These imports will be integrated once the ai connection branch is ready

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get the origin URL from environment variables
ORIGIN_URL = os.getenv('ORIGIN_URL')

# Enable CORS for frontend (React app hosted on Vercel)
CORS(app, origins=[ORIGIN_URL], supports_credentials=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# for Cookies:
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = False  # Prevent JS access - CHANGED TO TRUE
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Allow cross-origin

# Test route to confirm Render deployment
@app.route('/')
def home():
    return jsonify({"message": "Jewelry Dupe Finder backend running successfully!"})

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

# Test API endpoint for users
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
        
        return jsonify({"message": "Successfully connected to the users table", "users": users})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test API endpoint for chats
@app.route('/test-chats')
def get_chats():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM chats')
        
        # Fetch all the results
        chats = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return jsonify({"message": "Successfully connected to the chats table", "chats": chats})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Register Blueprints
app.register_blueprint(image_routes)
app.register_blueprint(description_routes)
app.register_blueprint(similar_product_routes)
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(save_chat_bp)

# Teardown function to close the database connection after each request
@app.teardown_appcontext
def close_database(error):
    """Closes the database connection after each request"""
    database = getattr(g, 'database', None)
    if database is not None:
        database.close()

# Main entry point for the app
if __name__ == '__main__':
    app.run(debug=True)



# THIS IS FROM GEMINI TESTING APP.PY

# import os
# import sys

# # Get the absolute path of the backend directory
# BaseDirectory = os.path.dirname(os.path.abspath(__file__))  # Directory of app.py
# ProjectRoot = os.path.dirname(BaseDirectory)

# sys.path.insert(0, ProjectRoot)  # Ensures the root project directory is recognized
# sys.path.insert(0, os.path.join(ProjectRoot, 'Backend'))  # Ensures Backend is recognized

# # Ensure Backend is in the Python module search path
# #sys.path.append(os.path.abspath(BackendPath))
# #sys.path.append(GeminiPath)

# from Backend.controllers.signup_controller import signup_bp
# from Backend.controllers.login_controller import login_bp
# from Backend.controllers.chat_controller import save_chat_bp
# from Backend.database_connector import get_database

# from flask import Flask, g
# from flask_cors import CORS
# from dotenv import load_dotenv
# import mysql.connector


# from gemini_config.settings import UPLOAD_FOLDER
# from routes.image_routes import image_routes
# from routes.description_routes import description_routes
# from routes.similar_product_routes import similar_product_routes



# app = Flask(__name__)

# # Explicitly define allowed origins (for local development, it's common to allow localhost:3000)
# CORS(app, origins=["http://localhost:3000"], methods=["GET", "POST", "OPTIONS"], supports_credentials=True)  # Allow React frontend to communicate with Flask

# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# load_dotenv()
# app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
# app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
# app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
# app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# # for Cookies:
# app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
# app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JS access
# app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Allow cross-origin

# # Register Blueprints
# app.register_blueprint(image_routes)
# app.register_blueprint(description_routes)
# app.register_blueprint(similar_product_routes)
# app.register_blueprint(signup_bp)
# app.register_blueprint(login_bp)
# app.register_blueprint(save_chat_bp)


# @app.teardown_appcontext
# def close_database(error):
#     """Closes the database connection after each request"""
#     database = getattr(g, 'database', None)
#     if database is not None:
#         database.close()

        
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)



