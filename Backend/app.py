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


# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend (React app hosted on Vercel)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)


app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')


# Register Blueprints
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)


# Main entry point for the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)