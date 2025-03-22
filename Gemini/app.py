import os
import sys

# Get the absolute path of the backend directory
BaseDirectory = os.path.dirname(os.path.abspath(__file__))  # Directory where the current file (app.py) is located
ProjectRoot = os.path.dirname(BaseDirectory)  # Root directory of the project

# Modify system path to include the root project and Backend directories for module recognition
sys.path.insert(0, ProjectRoot)  # Ensures the root project directory is recognized
sys.path.insert(0, os.path.join(ProjectRoot, 'Backend'))  # Ensures Backend folder is recognized

# Import controller blueprints and database connection function
from Backend.controllers.signup_controller import signup_bp
from Backend.controllers.login_controller import login_bp
from Backend.controllers.chat_controller import save_chat_bp
from Backend.controllers.profile_controller import profile_bp
from Backend.database_connector import get_database

# Import necessary Flask modules and extensions
from flask import Flask, g  # Flask app creation and global request context handling
from flask_cors import CORS  # Handling Cross-Origin Resource Sharing (CORS) for frontend-backend communication
from dotenv import load_dotenv  # Load environment variables from a .env file for sensitive information
import mysql.connector  # MySQL connector to interact with the database

# Import settings and routes
from gemini_config.settings import UPLOAD_FOLDER  # Custom setting for upload folder path
from routes.image_routes import image_routes  # Routes for image-related functionality
from routes.description_routes import description_routes  # Routes for description-related functionality
from routes.similar_product_routes import similar_product_routes  # Routes for similar product functionality

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for the React frontend to communicate with Flask (on localhost:3000)
CORS(app, origins=["http://localhost:3000"], methods=["GET", "POST", "OPTIONS"], supports_credentials=True)  

# Configure upload folder and load environment variables
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER  # Set path for file uploads
load_dotenv()  # Load environment variables from the .env file
# Set up MySQL database connection using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# Configure session cookies for security and cross-origin handling
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JS from accessing session cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Allow cross-origin requests to access cookies

# Register blueprints for modularized routing
app.register_blueprint(image_routes)  # Register routes for image handling
app.register_blueprint(description_routes)  # Register routes for descriptions
app.register_blueprint(similar_product_routes)  # Register routes for similar products
app.register_blueprint(signup_bp)  # Register signup controller
app.register_blueprint(login_bp)  # Register login controller
app.register_blueprint(save_chat_bp)  # Register chat saving functionality
app.register_blueprint(profile_bp)  # Register profile management functionality

# Define a function to close the database connection after each request
@app.teardown_appcontext
def close_database(error):
    """Closes the database connection after each request"""
    database = getattr(g, 'database', None)  # Get the database connection from the global Flask object (g)
    if database is not None:
        database.close()  # Close the connection if it exists

# Run the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Start the app on all available network interfaces, port 5000
