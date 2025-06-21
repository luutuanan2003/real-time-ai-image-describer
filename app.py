import os
import json
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI  # ✅ Correct import

# --- Load environment variables ---
load_dotenv()

# --- Configure logging ---
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# --- Determine if running in AWS ---
def running_in_aws():
    return (
        os.getenv("AWS_EXECUTION_ENV") or
        os.getenv("ECS_CONTAINER_METADATA_URI") or
        os.getenv("AWS_REGION")
    )

# --- Get OpenAI key from env or AWS Secrets Manager ---
def get_openai_key():
    if running_in_aws():
        import boto3
        client = boto3.client("secretsmanager", region_name="ap-southeast-2")
        response = client.get_secret_value(SecretId="real-time-ai/openai")
        secret = json.loads(response["SecretString"])
        logger.debug("[AWS] Retrieved OpenAI API key from Secrets Manager")
        return secret["OPENAI_API_KEY"]
    else:
        logger.debug("[LOCAL] Using OpenAI API key from environment")
        return os.getenv("OPENAI_API_KEY")

# --- Initialize OpenAI client (fixed line) ---
client = OpenAI(api_key=get_openai_key())

# --- Create Flask app ---
app = Flask(__name__, static_folder="static")
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/describe-image', methods=['POST'])
def describe_image():
    logger.debug("[DEBUG] Received request to /describe-image")
    
    try:
        data = request.get_json()
        logger.debug(f"[DEBUG] Request JSON: {data}")

        image_b64 = data.get("image_base64")
        logger.debug(f"[DEBUG] image_base64 exists? {bool(image_b64)}")

        if not image_b64:
            return jsonify({"error": "Missing image_base64 field"}), 400

        logger.debug("[DEBUG] Sending request to OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "What’s happening in this image?"},
                    {"type": "image_url", "image_url": {"url": image_b64}},
                ]}
            ],
            max_tokens=100
        )
        logger.debug(f"[DEBUG] OpenAI response: {response}")
        description = response.choices[0].message.content.strip()
        return jsonify({"description": description})

    except Exception as e:
        logger.exception("[ERROR] Exception occurred:")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
