import requests
import json
from datetime import datetime
from gemini_config.settings import API_KEY, OUTPUT_JSON
from services.file_utils import save_to_json

def analyze_image(base64_image):
    """Send image to Gemini API for analysis and return the description."""
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    request_body = {
        "contents": [
            {
                "parts": [
                    {"text": "Describe this image in detail."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                ]
            }
        ]
    }

    try:
        response = requests.post(API_URL, json=request_body, headers={"Content-Type": "application/json"})
        response_data = response.json()
        
        if not response_data or "candidates" not in response_data:
            print("Error: AI API returned invalid data", response_data)
            return {"error": "Failed to get a valid AI-generated description."}

        # Extract description
        description = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No description provided.")

        result = {
            "description": description,
            "timestamp": datetime.utcnow().isoformat(),
        }

        save_to_json(result)
        return result

    except Exception as e:
        print("Error analyzing image:", e)
        return {"error": "Failed to analyze image."}
