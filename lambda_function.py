import json, base64, os
import openai
from dotenv import load_dotenv

load_dotenv()  # Load .env file
openai.api_key = os.environ["OPENAI_API_KEY"]

print("API key loaded:", openai.api_key[:10], "...")  # Optional debug


def lambda_handler(event, context=None):
    try:
        body = json.loads(event['body'])
        image_base64 = body.get("image_base64", "")
        if not image_base64:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing image_base64 field"})
            }

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "What’s happening in this image?"},
                    {"type": "image_url", "image_url": {
                        "url": image_base64
                    }},
                ]}
            ],
            max_tokens=100
        )

        description = response.choices[0].message.content.strip()
        return {
            "statusCode": 200,
            "body": json.dumps({"description": description})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
