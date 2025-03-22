import requests
import json
from datetime import datetime
from gemini_config.settings import API_KEY, OUTPUT_JSON
from services.file_utils import save_to_json

# Define the possible jewelry questions for different types of jewelry
JEWELRY_QUESTIONS = {
    "watch": [
        "Choose the most accurate type of watch dial for this image: Analogue, Digital, Chronograph, or Hybrid?",
        "In one or two words, describe the watch's style.",
        "What is the material of the watch?",
        "What color is the background of the watch face?",
        "What is the width (thick or thin) of the band?",
        "What is the material of the band?",
        "Are there any gemstones or embellishments?",
        "If any, what is the visible brand logo?"
    ],
    "ring": [
        "What is the ring made of?",
        "Describe the ring's gemstone (if any) including color, cut, and size.",
        "Does the ring have any engravings or unique designs?",
        "What is the ring's general style? (e.g., wedding, casual, antique, modern)",
        "If any, what is the visible brand logo?"
    ],
    "necklace": [
        "What is the material of this necklace's chain?",
        "What type of chain does this necklace have?",
        "What type or style of necklace is this?",
        "What type of pendant does this necklace have, if any?",
        "Choose the most accurate possible necklace length for this image: Tight fit (collar/choker), Exact fit (princess), or Loose fit (matinee, opera, rope).",
        "If any, what is the visible brand logo?"
    ],
    "bracelet": [
        "What material is the bracelet made of?",
        "Does it have any charms or special attachments?",
        "Is the bracelet rigid (bangle) or flexible (chain, cord)?",
        "If any, what is the visible brand logo?"
    ],
    "earrings": [
        "What type of earrings are these? (studs, hoops, dangles, etc.)",
        "Describe any gemstones or decorations.",
        "What is the material of the earrings?",
        "If any, what is the visible brand logo?"
    ]
}

def ask_gemini(base64_image, question):
    """Send a single question to Gemini API along with the base64 image."""
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    # Build the request body with question and image data
    request_body = {
        "contents": [
            {
                "parts": [
                    {"text": question},  # The question text
                    {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},  # Base64-encoded image
                ]
            }
        ]
    }

    try:
        # Send the request to Gemini API
        response = requests.post(API_URL, json=request_body, headers={"Content-Type": "application/json"})
        response_data = response.json()  # Parse the JSON response

        # Handle invalid response data
        if not response_data or "candidates" not in response_data:
            print("Error: AI API returned invalid data", response_data)
            return None

        # Return the text response from the API
        return response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    except Exception as e:
        # Handle errors during the request
        print("Error making request to Gemini:", e)
        return None

def analyze_image(base64_image):
    """Analyze the image to detect jewelry type and ask follow-up questions."""
    # Ask Gemini to identify the type of jewelry
    jewelry_type_response = ask_gemini(base64_image, "What type of jewelry is this from the following list? Answer in one word: watch, ring, necklace, bracelet, or earrings?")
    
    if not jewelry_type_response:
        return {"error": "Failed to identify the jewelry type."}

    detected_type = jewelry_type_response.lower().strip()  # Extract and clean the detected type
    print(f"Detected jewelry type: {detected_type}")

    # Retrieve specific questions for the detected jewelry type
    questions = JEWELRY_QUESTIONS.get(detected_type, [])

    if not questions:
        return {
            "jewelry_type": detected_type,
            "description": "Jewelry type detected, but no specific questions are configured."
        }

    # Prepare to collect detailed answers
    detailed_description = []
    brand_name = ""

    # Ask Gemini the specific questions for the detected jewelry type
    for question in questions:
        answer = ask_gemini(base64_image, question)
        if answer:
            if "brand logo" in question.lower():  # Store the brand name if applicable
                brand_name = answer
            detailed_description.append(f"- {question}\n  {answer}")

    # Get product suggestions based on the detected jewelry type and brand name
    product_suggestions = get_product_suggestions(detected_type, brand_name)
    
    # Create a structured result with detailed descriptions and product suggestions
    result = {
        "jewelry_type": detected_type.capitalize(),  # Capitalize the jewelry type for neat output
        "description": "\n".join(detailed_description),  # Join the detailed descriptions into a single string
        "product_suggestions": product_suggestions,  # Include the product suggestions
        "timestamp": datetime.utcnow().isoformat(),  # Add the timestamp of the analysis
    }

    # Save the result to a JSON file
    save_to_json(result)
    return result

def get_product_suggestions(jewelry_type, brand_name):
    """Generate structured product suggestions based on the jewelry type and brand name."""
    if brand_name and brand_name.lower() != "unknown":
        # If a brand name is provided, use it in the search query
        search_query = f"{brand_name} {jewelry_type}"
    else:
        # If no brand name is provided, search for general options
        search_query = f"best {jewelry_type} for sale"
    
    # Return a list of example product suggestions (these would likely come from an actual product search)
    return [
        {"title": f"{search_query} - Option 1", "price": "$100-$200", "source": "Example Store"},
        {"title": f"{search_query} - Option 2", "price": "$200-$300", "source": "Example Store"},
    ]
