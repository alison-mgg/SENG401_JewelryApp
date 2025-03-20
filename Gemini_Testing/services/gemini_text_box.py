import requests
import json
from datetime import datetime
from gemini_config.settings import API_KEY, OUTPUT_JSON
from services.file_utils import save_to_json

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
        "What is the ring's general style? (e.g., wedding, casual, antique, modern)"
    ],
    "necklace": [
        "What is the material of this necklace's chain?",
        "What type of chain does this necklace have?",
        "What type or style of necklace is this?",
        "What type of pendant does this necklace have, if any?",
        "Choose the most accurate possible necklace length for this image: Tight fit: collar or choker style, Exact fit: princess style, or Loose fit: matinee, opera, or rope style."
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

def ask_gemini(input_data, question, is_text=False):
    """Send either image or text-based question to the Gemini API."""
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    if is_text:
        request_body = {
            "contents": [{"parts": [{"text": f"{question} {input_data}"}]}]
        }
    else:
        request_body = {
            "contents": [{
                "parts": [
                    {"text": question},
                    {"inline_data": {"mime_type": "image/jpeg", "data": input_data}},
                ]
            }]
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

def analyze_jewelry(input_data, is_text=False):
    """Identify jewelry type and ask follow-up questions based on either image or text input."""
    if is_text:
        jewelry_type_response = ask_gemini(input_data, "Based on the following description, what type of jewelry is this from the list: watch, ring, necklace, bracelet, or earrings?", is_text=True)
    else:
        jewelry_type_response = ask_gemini(input_data, "What type of jewelry is this from the list: watch, ring, necklace, bracelet, or earrings? Answer in one word.")

    if not jewelry_type_response:
        return {"error": "Failed to identify the jewelry type."}

    detected_type = jewelry_type_response.lower().strip()
    print(f"Detected jewelry type: {detected_type}")

    questions = JEWELRY_QUESTIONS.get(detected_type, [])

    if not questions:
        return {
            "jewelry_type": detected_type,
            "description": "Jewelry type detected, but no specific questions are configured."
        }

    detailed_description = []
    for question in questions:
        answer = ask_gemini(input_data, question, is_text=is_text)
        if answer:
            detailed_description.append(f"- {question}\n  {answer}")

    result = {
        "jewelry_type": detected_type.capitalize(),
        "description": "\n".join(detailed_description),
        "timestamp": datetime.utcnow().isoformat(),
    }

    save_to_json(result)
    return result
