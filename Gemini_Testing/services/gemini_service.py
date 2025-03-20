import requests
import json
from datetime import datetime
from gemini_config.settings import API_KEY, OUTPUT_JSON
from services.file_utils import save_to_json

#WORKING ON NECKLACE, WATCH, REST ARE UNTESTED
JEWELRY_QUESTIONS = {
    "watch": [
        "Choose the most accurate type of watch dial for this image: Analogue, Digital, Chronograph, or Hybrid?"
        "In one word to two words describe the watch's style."
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
        "What is the ring's general style? (e.g., wedding, casual, antique, modern)"
    ],
    "necklace": [
        "What is the material of this necklace's chain?"
        "What type of chain does this necklace have?"
        "What type or style of necklace is this"
        "What type of pendant does this necklace have, if any?"
        "Choose the most accurate possible necklace length for this image: Tight fit: collar or chocker style, Exact fit: princess style, or Loose fit: manitee, opera, or rope style."
    ],
    "bracelet": [
        "What material is the bracelet made of?",
        "Does it have any charms or special attachments?",
        "Is the bracelet rigid (bangle) or flexible (chain, cord)?"
    ],
    "earrings": [
        "What type of earrings are these? (studs, hoops, dangles, etc.)",
        "Describe any gemstones or decorations.",
        "What is the material of the earring?"
    ]
}

def ask_gemini(base64_image, question):
    """Send a single question to Gemini API."""
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    request_body = {
        "contents": [
            {
                "parts": [
                    {"text": question},
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
            return None

        return response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    except Exception as e:
        print("Error making request to Gemini:", e)
        return None


def analyze_image(base64_image):
    """Identify the type of jewelry, then get detailed answers with follow-up questions."""
    # Step 1: Identify the jewelry type
    jewelry_type_response = ask_gemini(base64_image, "What type of jewelry is this from the following list, answer in one word: watch, ring, necklace, bracelet, or earrings?")
    
    if not jewelry_type_response:
        return {"error": "Failed to identify the jewelry type."}

    # Extract the jewelry type
    detected_type = jewelry_type_response.lower().strip()
    print(f"Detected jewelry type: {detected_type}")

    # Step 2: Ask detailed questions based on the type
    questions = JEWELRY_QUESTIONS.get(detected_type, [])

    if not questions:
        other_type = ask_gemini(base64_image, "What do you see in this image, describe in one sentence and determine whether or not is a type of jewlery in the following format: This is an image of jewlery. or This is not an image of jewlery.")
        print(detected_type) #DEBUG line(troubleshooting)
        return {
            "jewelry_type": detected_type,
            "description": "Jewelry type detected, but no specific questions are configured."
        }


    detailed_description = []

    for question in questions:
        answer = ask_gemini(base64_image, question)
        if answer:
            detailed_description.append(f"- {question}\n  {answer}")

    # Format the result
    result = {
        "jewelry_type": detected_type.capitalize(),
        "description": "\n".join(detailed_description),
        "timestamp": datetime.utcnow().isoformat(),
    }

    # Save to output.json
    save_to_json(result)

    return result