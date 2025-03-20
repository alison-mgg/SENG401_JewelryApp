import json
import requests
from gemini_config.settings import API_KEY

# Load the output from output.json
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to ask Gemini for similar products based on the description
def get_similar_products(description):
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    # Query asking for similar products
    question = f"Given the following description: '{description}', please provide the brand name, model number, and a brief description of 5 similar products. Format your response as keywords that I can easily copy and paste into Google. Include approximate prices for each suggestion."
    
    request_body = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }

    try:
        response = requests.post(API_URL, json=request_body, headers={"Content-Type": "application/json"})
        response_data = response.json()

        if not response_data or "candidates" not in response_data:
            print("Error: Gemini API returned invalid data", response_data)
            return None

        # Extract the response from Gemini (should be links)
        similar_products = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return similar_products

    except Exception as e:
        print("Error making request to Gemini:", e)
        return None

