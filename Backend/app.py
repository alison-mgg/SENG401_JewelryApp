from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from database_connector import get_database
#from gemini_config.settings import UPLOAD_FOLDER
#from routes.image_routes import image_routes
#from routes.description_routes import description_routes
#^^These imports will be integrated once the ai connection branch is ready

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS

# MySQL Database configuration using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')


#For ai integration branch:
#app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Register Blueprints
#app.register_blueprint(image_routes)
#app.register_blueprint(description_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)