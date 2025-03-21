import json
import os
import logging
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Define the path to the .json file (ensure it's writable)
BASE_DIR = os.getcwd()  # Save in the current working directory
JSON_FILE_PATH = os.path.join(BASE_DIR, "similar_products.json")

def format_similar_products(data):
    try:
        logging.debug(f"Received Data Type: {type(data)}")
        logging.debug(f"Received Data: {json.dumps(data, indent=2)}")

        formatted_data = {"similar_products": []}

        candidates = data.get("candidates", [])
        if not candidates:
            return {"error": "No candidates found in response"}

        content = candidates[0].get("content", {}).get("parts", [])
        if not content or not isinstance(content[0], dict) or "text" not in content[0]:
            return {"error": "Missing or invalid text content in API response"}

        text = content[0]["text"]
        product_pattern = re.compile(r"\*\*(.*?)\*\*.*?- (\$\d+-?\d*\+?)", re.S)
        matches = product_pattern.findall(text)

        for match in matches:
            formatted_data["similar_products"].append({
                "name": match[0].strip(),
                "price_range": match[1].strip(),
            })

        # DEBUGGING: Print formatted data
        logging.info(f"Formatted data: {json.dumps(formatted_data, indent=2)}")

        return formatted_data

    except Exception as e:
        logging.error(f"Error in format_similar_products: {e}")
        return {"error": str(e)}