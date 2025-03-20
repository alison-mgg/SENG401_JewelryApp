#  COMMENTED OUT BC I SEPARATED THE RESPONSIBILITIES INTO 
# DIFFERENT FILES. ONCE THOSE ARE FINALIZED, DELETE THIS.



#  import os
# import json
# import base64
# import requests
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from werkzeug.utils import secure_filename
# from datetime import datetime
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# API_KEY = os.getenv("GEMINI_API_KEY")

# # Flask setup
# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend communication

# # Configurations
# UPLOAD_FOLDER = "uploads"
# OUTPUT_JSON = "output.json"
# IMAGE_PATH = "TestImage.jpg"

# # Ensure upload directory exists
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# # Helper function to check allowed file extensions
# def allowed_file(filename):
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# # Convert image to Base64
# def encode_image_to_base64(image_path):
#     try:
#         with open(image_path, "rb") as image_file:
#             return base64.b64encode(image_file.read()).decode("utf-8")
#     except Exception as e:
#         print("Error reading image file:", e)
#         return None

# # Call Gemini API to analyze the image
# def analyze_image(base64_image):
#     API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

#     request_body = {
#         "contents": [
#             {
#                 "parts": [
#                     {"text": "Describe this image in detail."},
#                     {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
#                 ]
#             }
#         ]
#     }

#     try:
#         response = requests.post(API_URL, json=request_body, headers={"Content-Type": "application/json"})
#         response_data = response.json()
        
#         if not response_data or "candidates" not in response_data:
#             print("Error: AI API returned invalid data", response_data)
#             return {"error": "Failed to get a valid AI-generated description."}

#         # Extract the description
#         description = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No description provided.")

#         result = {
#             "description": description,
#             "timestamp": datetime.utcnow().isoformat(),
#         }

#         # Save to output.json
#         with open(OUTPUT_JSON, "w") as json_file:
#             json.dump(result, json_file, indent=4)

#         print("Returning result:", result)
#         return result

#     except Exception as e:
#         print("Error analyzing image:", e)
#         return {"error": "Failed to analyze image."}

# # Endpoint for image upload & analysis
# @app.route("/upload", methods=["POST"])
# def upload_file():
#     if "image" not in request.files:
#         return jsonify({"error": "No image uploaded."}), 400

#     file = request.files["image"]

#     if file.filename == "" or not allowed_file(file.filename):
#         return jsonify({"error": "Invalid file type."}), 400

#     filename = secure_filename(file.filename)
#     image_path = os.path.join(app.config["UPLOAD_FOLDER"], f"uploaded_{int(datetime.utcnow().timestamp())}_{filename}")
#     file.save(image_path)

#     print("File received:", image_path)

#     base64_image = encode_image_to_base64(image_path)
#     if not base64_image:
#         return jsonify({"error": "Failed to process image."}), 500

#     result = analyze_image(base64_image)
    
#     if not result or "description" not in result:
#         return jsonify({"error": "Invalid response from AI analysis."}), 500

#     # Cleanup: Delete the uploaded image after processing
#     os.remove(image_path)
#     print("Deleted uploaded image:", image_path)

#     return jsonify(result)

# # Endpoint to get the latest description
# @app.route("/description", methods=["GET"])
# def get_description():
#     if os.path.exists(OUTPUT_JSON):
#         with open(OUTPUT_JSON, "r") as json_file:
#             return jsonify(json.load(json_file))
#     return jsonify({"error": "No data available"})

# # Start the Flask server
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
