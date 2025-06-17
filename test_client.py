from PIL import Image
import io, base64, json
from lambda_function import lambda_handler

# Convert and encode image correctly
img = Image.open("test.png").convert("RGB")
buf = io.BytesIO()
img.save(buf, format="JPEG")
b64 = base64.b64encode(buf.getvalue()).decode()
event = {"body": json.dumps({"image_base64": f"data:image/jpeg;base64,{b64}"})}

res = lambda_handler(event)
print("Status:", res["statusCode"])
print("Response:", json.loads(res["body"]))
