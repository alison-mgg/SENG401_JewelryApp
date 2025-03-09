#May need to rename this or move this when we make a proper app.py-
#-for all of backend
from flask import Flask
from flask_cors import CORS
from gemini_config.settings import UPLOAD_FOLDER
from routes.image_routes import image_routes
from routes.description_routes import description_routes

app = Flask(__name__)
CORS(app)  # Enable CORS

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Register Blueprints
app.register_blueprint(image_routes)
app.register_blueprint(description_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
