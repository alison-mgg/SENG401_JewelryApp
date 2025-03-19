# from flask import Blueprint, request, jsonify
# from database_connector import get_database
# import os
# from werkzeug.utils import secure_filename
# from flask_cors import cross_origin
# import shutil

# save_chat_bp = Blueprint('save_chat', __name__)

# BASE_DIR = os.path.dirname(os.path.dirname(os.getcwd()))
# DATABASE_FOLDER = os.path.join(BASE_DIR, 'Database')
# UPLOADS_FOLDER = os.path.join(os.getcwd(), 'uploads')
# IMAGES_FOLDER = os.path.join(DATABASE_FOLDER, 'images')

# @save_chat_bp.route('/save-chat', methods=['POST'])
# def save_chat():
#     try:
#         data = request.get_json()

#         if not data:
#             return jsonify({"error": "Invalid data format"}), 400

#         username = data['username']
#         image_name = data['image_name']
#         response = data['response']

#         if not isinstance(image_name, str):
#             return jsonify({"error": "Invalid image name format"}), 400

#         image_path = os.path.join(UPLOADS_FOLDER, image_name)
#         new_image_path = os.path.join(IMAGES_FOLDER, image_name)

#         if not os.path.exists(image_path):
#             return jsonify({"error": "Image not found"}), 404

#         # Move image
#         shutil.move(image_path, new_image_path)

#         # Save to database
#         conn = get_database()
#         cursor = conn.cursor()

#         sql = """
#         INSERT INTO chats (username, img_path, response)
#         VALUES (%s, %s, %s)
#         """
#         cursor.execute(sql, (username, new_image_path, response))
#         conn.commit()
#         cursor.close()
#         conn.close()

#         return jsonify({"message": "Chat saved successfully"}), 200

#     except Exception as e:
#         return jsonify({"error": f"Server error: {str(e)}"}), 500
# # def save_chat():
# #     if 'image' not in request.files:
# #         return jsonify({"error": "No image uploaded"}), 400
    
# #     image = request.files['image']
# #     username = request.form.get('username')
# #     response = request.form.get('response')

# #     if not username or not response:
# #         return jsonify({"error": "Missing username or response"}), 400
    
# #     filename = secure_filename(image.filename)
# #     img_path = os.path.join(IMAGES_FOLDER, filename)
# #     try:
# #         image.save(img_path)
# #     except Exception as e:
# #         print(f"error: {str(e)}")
# #         return jsonify({"error": f"failed to save image: {str(e)}"}), 500

# #     try:
# #         conn = get_database()
# #         cursor = conn.cursor()
# #         cursor.execute("INSERT INTO saved_chats (username, img_path, response) VALUES (%s, %s, %s)",
# #                        (username, img_path, response))
# #         conn.commit()
# #         cursor.close()
# #         conn.close()
# #         return jsonify({"message": "Chat saved successfully!"}), 201
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500