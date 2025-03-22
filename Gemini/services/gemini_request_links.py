import json
import requests
from gemini_config.settings import API_KEY  # Import the API key for authentication

# Load the output from output.json
def load_json(file_path):
    """Load JSON data from a specified file."""
    with open(file_path, 'r') as file:
        return json.load(file)  # Return the parsed JSON data

# Function to ask Gemini for similar products based on the description
def get_similar_products(description):
    """Fetch similar product suggestions based on the provided description."""
    
    # Define the API endpoint and include the API key for authentication
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    # Construct the query question to ask the Gemini model
    question = f"Given the following description: '{description}', please provide the brand name, model number, and a brief description of 5 similar products. Format your response as keywords that I can easily copy and paste into Google. Include approximate prices for each suggestion."
    
    # Create the request body with the query
    request_body = {
        "contents": [
            {
                "parts": [
                    {"text": question}  # The actual question is wrapped inside 'parts'
                ]
            }
        ]
    }

    try:
        # Send a POST request to the Gemini API with the question in JSON format
        response = requests.post(API_URL, json=request_body, headers={"Content-Type": "application/json"})
        response_data = response.json()  # Parse the JSON response

        # Check if the response is valid and contains the expected 'candidates' key
        if not response_data or "candidates" not in response_data:
            print("Error: Gemini API returned invalid data", response_data)
            return None

        # Extract and return the similar products from the API response
        similar_products = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return similar_products

    except Exception as e:
        # Catch any exceptions that occur during the request process and print an error message
        print("Error making request to Gemini:", e)
        return None
