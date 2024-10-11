from flask import Flask, request, jsonify
import base64
from PIL import Image
import io
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """Home route to welcome users and provide API information."""
    return "Welcome to the Image to Base64 API! Use the /convert endpoint to convert images."


@app.route('/convert', methods=['POST'])
def convert_image_to_base64():
    """Convert the uploaded image to a Base64 string."""
    try:
        # Check if a file is part of the request
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        # Get the image from the request
        image_file = request.files['image']

        # Open the image
        image = Image.open(image_file)

        # Convert the image to bytes
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        # Convert the image bytes to a Base64 string
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # Save the Base64 string to a text file
        with open('base64_image.txt', 'w') as f:
            f.write(img_base64)

        # Return the Base64 string as JSON response
        return jsonify({"base64_image": img_base64}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Run the app on the specified port
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
