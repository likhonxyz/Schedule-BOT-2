# Official Python runtime base image
FROM python:3.10-slim

# কাজের ডিরেক্টরি সেট করা
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy পুরো কোডবেস
COPY . .

# ENV variables যেগুলো রানটাইমে fly.toml থেকে আসবে
ENV SESSION_STRING=""
ENV API_ID=""
ENV API_HASH=""
ENV ADMIN_ID=""
ENV GROUPS=""

# কমান্ড যা container শুরু হলে রান করবে
CMD ["python3", "main.py"]
