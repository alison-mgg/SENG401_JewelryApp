# Third-party imports
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Std library import
import os

# Local imports
import mysql.connector
from database_connector import get_database
from controllers.signup_controller import signup_bp
from controllers.login_controller import login_bp
#from gemini_config.settings import UPLOAD_FOLDER
#from routes.image_routes import image_routes
#from routes.description_routes import description_routes
#^^These imports will be integrated once the ai connection branch is ready

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend (React app hosted on Vercel)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# # MySQL Database configuration using environment variables
# MYSQL_HOST = os.getenv('MYSQL_HOST')
# MYSQL_USER = os.getenv('MYSQL_USER')
# MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
# MYSQL_DB = os.getenv('MYSQL_DB')
# MySQL Database configuration using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
# Function to get database connection
# def get_db_connection():
#     connection = mysql.connector.connect(
#         host=MYSQL_HOST,
#         user=MYSQL_USER,
#         password=MYSQL_PASSWORD,
#         database=MYSQL_DB
#     )
#     return connection

# Test database connection
# @app.route('/test_db_connection')
# def test_db_connection():
#     try:
#         db = get_db_connection()
#         cursor = db.cursor()
#         cursor.execute("SELECT 1")
        
#         # Ensure that the result is consumed
#         cursor.fetchall()  # Consume the result
        
#         cursor.close()
#         db.close()
#         return 'Database connection successful!'
#     except Exception as e:
#         return f'Database connection failed: {e}'

# Test API endpoint
# @app.route('/users')
# def get_users():
#     db = get_db_connection()
#     cursor = db.cursor(dictionary=True)
#     cursor.execute('SELECT * FROM users')
    
#     # Fetch all the results
#     users = cursor.fetchall()
    
#     cursor.close()
#     db.close()
    
#     return jsonify(users)

# Register Blueprints
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)

# Future integrations (commented out for now)
#app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER # For ai integration branch
#app.register_blueprint(image_routes)
#app.register_blueprint(description_routes)

# Main entry point for the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)