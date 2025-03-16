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

# import os

# DB_USERNAME = "admin"  # Your RDS username
# DB_PASSWORD = "yourpassword"  # Your RDS password
# DB_HOST = "jewelry-dupe-db.cp48gswg0leh.us-east-2.rds.amazonaws.com"
# DB_NAME = "jewelry_dupe_db"

# SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
# SQLALCHEMY_TRACK_MODIFICATIONS = False

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend (React app running on localhost:3000)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# MySQL Database configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

# Initialize SQLAlchemy (used for database ORM)
db = SQLAlchemy(app)

# Register Blueprints
from controllers.signup_controller import signup_bp
app.register_blueprint(signup_bp)

# For future AI integration, these lines will be useful:
# from routes.image_routes import image_routes
# from routes.description_routes import description_routes
# app.register_blueprint(image_routes)
# app.register_blueprint(description_routes)

# Main entry point for the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
