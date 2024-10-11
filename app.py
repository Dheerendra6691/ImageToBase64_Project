from flask import Flask, request, jsonify
import base64
from PIL import Image
import io
import os
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Image to Base64 API! Use the /convert endpoint to convert images."

@app.route('/convert', methods=['POST'])
def convert_image_to_base64():
    try:
        # Check if a file is part of the request
        if 'image' not in request.files:
            logging.error("No image provided in the request.")
            return jsonify({"error": "No image provided"}), 400

        # Get the image from the request
        image_file = request.files['image']

        # Check if the uploaded file is an image
        if not image_file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            logging.error("Invalid file type provided: %s", image_file.filename)
            return jsonify({"error": "Invalid file type. Please upload an image file."}), 400

        image = Image.open(image_file)

        # Convert the image to bytes
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        # Convert the image bytes to a Base64 string
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # Return the Base64 string as JSON response
        return jsonify({"base64_image": img_base64}), 200

    except Exception as e:
        logging.exception("An error occurred while processing the image.")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
