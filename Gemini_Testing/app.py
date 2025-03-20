import os
import sys

# Get the absolute path of the backend directory
BaseDirectory = os.path.dirname(os.path.abspath(__file__))  # Directory of app.py
ProjectRoot = os.path.dirname(BaseDirectory)

sys.path.insert(0, ProjectRoot)  # Ensures the root project directory is recognized
sys.path.insert(0, os.path.join(ProjectRoot, 'Backend'))  # Ensures Backend is recognized

# Ensure Backend is in the Python module search path
#sys.path.append(os.path.abspath(BackendPath))
#sys.path.append(GeminiPath)

from Backend.controllers.signup_controller import signup_bp
from Backend.controllers.login_controller import login_bp
from Backend.controllers.chat_controller import save_chat_bp
from Backend.database_connector import get_database

from flask import Flask, g
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector


from gemini_config.settings import UPLOAD_FOLDER
from routes.image_routes import image_routes
from routes.description_routes import description_routes
from routes.similar_product_routes import similar_product_routes



app = Flask(__name__)

# Get the frontend origin URL from environment variables
ORIGIN_URL = os.getenv('ORIGIN_URL')

# Enable CORS for frontend (React app hosted on Vercel)
CORS(app, origins=[ORIGIN_URL], supports_credentials=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
load_dotenv()
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# for Cookies:
app.config['SESSION_COOKIE_SECURE'] = True  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JS access
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Allow cross-origin

# Test route to confirm Render deployment
@app.route('/', methods=['GET'])
def test_app():
    """Test route to verify the app is running and database connection works."""
    try:
        # Attempt to connect to the database
        db = get_database()
        cursor = db.cursor()
        cursor.execute("SELECT 1")  # Simple query to test the connection
        result = cursor.fetchone()
        cursor.close()
        db.close()

        # Return success response
        return jsonify({
            "status": "success",
            "message": "Gemini Testing app is running!",
            "database_status": "connected",
            "test_query_result": result
        }), 200
    except Exception as e:
        # Return error response if something goes wrong
        return jsonify({
            "status": "error",
            "message": "Gemini Testing app encountered an issue.",
            "error": str(e)
        }), 500
    
# Register Blueprints
app.register_blueprint(image_routes)
app.register_blueprint(description_routes)
app.register_blueprint(similar_product_routes)
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(save_chat_bp)


@app.teardown_appcontext
def close_database(error):
    """Closes the database connection after each request"""
    database = getattr(g, 'database', None)
    if database is not None:
        database.close()

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


