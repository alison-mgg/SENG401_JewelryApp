from flask import Flask
from flask_cors import CORS
from gemini_config.settings import UPLOAD_FOLDER
from routes.image_routes import image_routes
from routes.description_routes import description_routes
from routes.similar_product_routes import similar_product_routes

app = Flask(__name__)

# Explicitly define allowed origins (for local development, it's common to allow localhost:3000)
CORS(app, origins=["http://localhost:3000"], methods=["GET", "POST", "OPTIONS"])  # Allow React frontend to communicate with Flask

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Register Blueprints
app.register_blueprint(image_routes)
app.register_blueprint(description_routes)
app.register_blueprint(similar_product_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


