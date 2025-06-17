import cv2
import time
import base64
import requests
from PIL import Image
import io

API_URL = "http://localhost:5000/describe-image"

def capture_and_describe():
    cap = cv2.VideoCapture(0)  # 0 = default webcam

    if not cap.isOpened():
        print("❌ Could not access the camera.")
        return

    print("📷 Camera started. Press Ctrl+C to stop.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to grab frame.")
                break

            # Resize for performance (optional)
            resized = cv2.resize(frame, (640, 480))

            # Convert to PIL Image and encode as JPEG
            img = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            b64 = base64.b64encode(buf.getvalue()).decode()
            image_data = f"data:image/jpeg;base64,{b64}"

            # Send to API
            try:
                res = requests.post(API_URL, json={"image_base64": image_data})
                if res.status_code == 200:
                    print("📝", res.json().get("description"))
                else:
                    print("⚠️ Error:", res.json())
            except Exception as e:
                print("❌ Request failed:", str(e))

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n👋 Stopping.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_describe()
