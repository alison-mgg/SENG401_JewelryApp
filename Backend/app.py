# Std library import
import os

# Third-party imports
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error, IntegrityError

# Local imports
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

# Get the origin URL from environment variables
ORIGIN_URL = os.getenv('ORIGIN_URL')

# Enable CORS for frontend (React app hosted on Vercel)
CORS(app, origins=[ORIGIN_URL], supports_credentials=True)

# # Vercel branch render-backend-deployment (change to main branch Vercel link after)
# CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# MySQL Database configuration using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# Function to get database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection

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

# Register Blueprints
app.register_blueprint(signup_bp, url_prefix='/signup')
app.register_blueprint(login_bp)

# Future integrations (commented out for now)
#app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER # For ai integration branch
#app.register_blueprint(image_routes)
#app.register_blueprint(description_routes)

# Main entry point for the app
if __name__ == '__main__':
    app.run(debug=True)
