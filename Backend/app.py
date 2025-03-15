from flask import Flask
from flask_cors import CORS
#from gemini_config.settings import UPLOAD_FOLDER
#from routes.image_routes import image_routes
#from routes.description_routes import description_routes
#^^These imports willl be integrated once the ai connection branch is ready

app = Flask(__name__)
CORS(app)  # Enable CORS

#For ai integration branch:
#app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Register Blueprints
#app.register_blueprint(image_routes)
#app.register_blueprint(description_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)