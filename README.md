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


## 🧪 Raspberry Pi Setup & Deployment Guide

This project was successfully deployed and tested on a Raspberry Pi 5 with the following steps:

### ✅ 1. Flash Raspberry Pi OS Lite (64-bit)
- Use Raspberry Pi Imager
- Set:
  - Hostname: `pi-image-ai`
  - Enable SSH
  - Set username/password (e.g., `andyl`)
  - Wi-Fi SSID: `TuanAn168` (2.4GHz only)
  - Country: `VN` (to avoid 5GHz Wi-Fi issues)

### ✅ 2. Boot and Connect
- Insert SD card into Pi, power on
- Find Pi’s IP with: `nmap -sn 192.168.1.0/24`
- SSH in: `ssh andyl@192.168.1.123`

### ✅ 3. Set Up Python Environment
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv python3-opencv libatlas-base-dev libjpeg-dev git -y
git clone https://github.com/luutuanan2003/real-time-ai-image-describer.git
cd real-time-ai-image-describer
python3 -m venv venv
source venv/bin/activate
pip install --break-system-packages -r requirements.txt
pip install --break-system-packages Pillow
```

### ✅ 4. Set OpenAI API Key
```bash
echo "OPENAI_API_KEY=sk-..." > .env
```

### ✅ 5. Run Backend & Client
In one terminal:
```bash
cd ~/real-time-ai-image-describer
source venv/bin/activate
python app.py
```

In another terminal:
```bash
ssh andyl@192.168.1.123  # new session
cd ~/real-time-ai-image-describer
source venv/bin/activate
python realtime_camera.py
```

> This setup enables the Raspberry Pi 5 to act as a real-time AI-powered visual interpreter using a USB webcam.

