import boto3
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os

# AWS Secrets Manager
def get_openai_key():
    client = boto3.client("secretsmanager", region_name="ap-southeast-2")
    response = client.get_secret_value(SecretId="real-time-ai/openai")
    secret = json.loads(response["SecretString"])
    return secret["OPENAI_API_KEY"]

openai.api_key = get_openai_key()

# Serve static/index.html
app = Flask(__name__, static_folder="static")
CORS(app)


@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/describe-image', methods=['POST'])
def describe_image():
    data = request.get_json()
    image_b64 = data.get("image_base64")

    if not image_b64:
        return jsonify({"error": "Missing image_base64 field"}), 400

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "What’s happening in this image?"},
                    {"type": "image_url", "image_url": {"url": image_b64}},
                ]}
            ],
            max_tokens=100
        )
        description = response.choices[0].message.get("content", "").strip()
        return jsonify({"description": description})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
