import json
import os
import logging
import re

# Configure logging to output messages with timestamp, log level, and message
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Define the path to the .json file (ensure it's writable)
BASE_DIR = os.getcwd()  # Get the current working directory
JSON_FILE_PATH = os.path.join(BASE_DIR, "similar_products.json")  # Path for saving the similar products JSON file

def format_similar_products(data):
    """
    Format and extract similar product information from the provided data.
    """
    try:
        # Log the received data type and the actual data for debugging
        logging.debug(f"Received Data Type: {type(data)}")
        logging.debug(f"Received Data: {json.dumps(data, indent=2)}")

        formatted_data = {"similar_products": []}  # Initialize the formatted data structure

        # Retrieve candidates from the input data
        candidates = data.get("candidates", [])
        if not candidates:
            return {"error": "No candidates found in response"}  # Return error if no candidates found

        # Extract content parts from the first candidate's response
        content = candidates[0].get("content", {}).get("parts", [])
        if not content or not isinstance(content[0], dict) or "text" not in content[0]:
            return {"error": "Missing or invalid text content in API response"}  # Return error if text content is invalid

        # Extract text containing product names and price ranges using regular expression
        text = content[0]["text"]
        product_pattern = re.compile(r"\*\*(.*?)\*\*.*?- (\$\d+-?\d*\+?)", re.S)  # Regex to capture product name and price
        matches = product_pattern.findall(text)  # Find all matching patterns

        # Populate the formatted data with extracted product information
        for match in matches:
            formatted_data["similar_products"].append({
                "name": match[0].strip(),  # Clean up product name by stripping extra spaces
                "price_range": match[1].strip(),  # Clean up price range
            })

        # DEBUGGING: Log the formatted data for verification
        logging.info(f"Formatted data: {json.dumps(formatted_data, indent=2)}")

        return formatted_data  # Return the formatted data containing product names and price ranges

    except Exception as e:
        # Log any exceptions that occur during the formatting process
        logging.error(f"Error in format_similar_products: {e}")
        return {"error": str(e)}  # Return the error message as part of the response
