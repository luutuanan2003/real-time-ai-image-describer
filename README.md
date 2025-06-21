# Real-Time AI Image Describer 🧠📷

This project is a Flask-based web application that uses OpenAI's GPT-4o model to describe images in real-time. It allows users to upload an image and receive a natural-language description of what's happening in that image — powered by modern AI.

## 🚀 Features

- Upload and send base64 images to the backend
- Uses OpenAI's GPT-4o with vision capabilities for image understanding
- Flask backend with CORS support
- Fully Dockerized and cloud-deployable
- AWS-ready integration (Secrets Manager support, scalable via containerization)
- Raspberry Pi integration with webcam support

## 🛠 Tech Stack

| Layer         | Tech Used                           |
|--------------|--------------------------------------|
| Frontend     | HTML/CSS/JS (Vanilla for now)        |
| Backend      | Python, Flask, Flask-CORS            |
| AI Model     | OpenAI GPT-4o (via OpenAI SDK v1.23) |
| Container    | Docker                               |
| Deployment   | AWS (Planned), GitHub                |
| Secrets Mgmt | AWS Secrets Manager (for prod)       |
| Local Env    | `.env` file (for dev only)           |
| Edge Device  | Raspberry Pi with camera module      |

## 🧩 Project Structure

```
real-time-ai-image-describer/
│
├── app.py              # Flask app
├── static/             # Frontend static files (index.html, JS, CSS)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker build definition
├── .env                # (Ignored) Local dev environment variables
├── raspberry_client.py # (Planned) Client script for Raspberry Pi
└── README.md           # This file
```

## ⚙️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key (from OpenAI) in a .env file
echo "OPENAI_API_KEY=sk-..." > .env

# Run the app
python app.py
```

## 🐳 Docker Usage

```bash
# Build image
docker build -t image-describer .

# Run container with .env
docker run --env-file .env -p 5050:5000 image-describer
```

Then visit: [http://localhost:5050](http://localhost:5050)

## ☁️ AWS Deployment (Coming Soon)

This app is ready to run on AWS ECS or EC2.

- OpenAI API key can be securely fetched from AWS Secrets Manager (`real-time-ai/openai`)
- Just change the environment setup and you're good to go.

## 🍓 Raspberry Pi Integration

The Raspberry Pi device will:

- Connect to a USB or Pi Camera
- Capture frames at regular intervals
- Encode the image to base64 and send to this Flask API
- Display the AI-generated description in real-time (e.g., on a small attached screen)

This allows the system to act as a real-time visual interpreter on the edge using affordable hardware.

## ✅ To-Do (Next Steps)

- [ ] Add frontend image upload UI
- [ ] Add webcam capture support
- [ ] Deploy to AWS ECS
- [ ] Setup CI/CD with GitHub Actions
- [ ] Write and deploy Raspberry Pi client
