# Dockerfile
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt update && apt install -y libgl1-mesa-glx gcc

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port Flask runs on
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
