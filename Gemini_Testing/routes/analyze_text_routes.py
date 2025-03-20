from flask import Blueprint, request, jsonify
from services.gemini_text_box import analyze_jewelry  # Import your function to get similar products


@app.route("/analyze_text", methods=["POST"])
def analyze_text():
    data = request.get_json()
    print("Received request:", data)  # Debugging line

    text_description = data.get("text", "")
    if not text_description:
        return jsonify({"error": "No text provided"}), 400

    result = analyze_jewelry(text_description, is_text=True)
    print("Response to send:", result)  # Debugging line

    return jsonify(result)