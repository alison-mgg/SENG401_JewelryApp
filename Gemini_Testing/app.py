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

# Explicitly define allowed origins (for local development, it's common to allow localhost:3000)
CORS(app, origins=["http://localhost:3000"], methods=["GET", "POST", "OPTIONS"], supports_credentials=True)  # Allow React frontend to communicate with Flask

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
load_dotenv()
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')



# Register Blueprints
app.register_blueprint(image_routes)
app.register_blueprint(description_routes)
app.register_blueprint(similar_product_routes)
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(save_chat_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


