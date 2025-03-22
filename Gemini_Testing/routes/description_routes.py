import os
import json
from flask import Blueprint, jsonify
from gemini_config.settings import OUTPUT_JSON

description_routes = Blueprint("description_routes", __name__)

@description_routes.route("/description", methods=["GET"])
def get_description():
    """Fetch the latest AI-generated description."""
    
    # Check if the OUTPUT_JSON file exists
    if os.path.exists(OUTPUT_JSON):
        # If the file exists, open it and return its contents as a JSON response
        with open(OUTPUT_JSON, "r") as json_file:
            return jsonify(json.load(json_file))
    
    # If the file doesn't exist, return an error message
    return jsonify({"error": "No data available"})
