# Std library import
import os

# Third-party imports
from flask import Flask, jsonify, g, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error, IntegrityError

# Local imports
from controllers.signup_controller import signup_bp
from controllers.login_controller import login_bp
from controllers.chat_controller import save_chat_bp

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get the origin URL from environment variables
ORIGIN_URL = os.getenv('ORIGIN_URL')

# Enable CORS for frontend (React app hosted on Vercel)
CORS(app, origins=[ORIGIN_URL], supports_credentials=True)

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

# for Cookies:
app.config['SESSION_COOKIE_SECURE'] = True  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JS access - CHANGED TO TRUE
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Allow cross-origin

# Test route to confirm Render deployment
@app.route('/')
def home():
    return jsonify({"message": "Jewelry Dupe Finder backend running successfully!"})

# Test route for DB connection
@app.route('/test-db-connection', methods=['GET'])
def test_db_connection():
    try:
        # Attempt to connect to the database
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT 1")  # Simple query to test the connection
        result = cursor.fetchone()
        cursor.close()
        db.close()

        # Return success response
        return jsonify({
            "database_status": "connected",
            "test_query_result": result
        }), 200
    except Exception as e:
        # Log the error for debugging
        print(f"Database connection error: {str(e)}")
        return jsonify({
            "database_status": "error",
            "error": str(e)
        }), 500

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
app.register_blueprint(signup_bp, url_prefix='/signup')
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(save_chat_bp, url_prefix='/chat')

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
