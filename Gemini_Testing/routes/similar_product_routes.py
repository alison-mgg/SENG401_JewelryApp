from flask import Blueprint, request, jsonify
from services.gemini_request_links import get_similar_products  # Updated function

# Create a Blueprint for the routes
similar_product_routes = Blueprint("similar_product_routes", __name__)

@similar_product_routes.route("/similar-products", methods=["POST"])
def similar_products():
    try:
        # Get the description from the request body
        data = request.get_json()
        description = data.get("description")

        if not description:
            return jsonify({"error": "Description is required"}), 400

        # Fetch structured product data
        similar_products = get_similar_products(description)

        if similar_products:
            return jsonify({"similar_products": similar_products}), 200
        else:
            return jsonify({"error": "No similar products found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
