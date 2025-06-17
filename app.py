import os, base64, json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS  # ← ADD THIS
import openai

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)
CORS(app)  # ← ENABLE CORS FOR ALL ROUTES


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
        description = response.choices[0].message.content.strip()
        return jsonify({"description": description})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
