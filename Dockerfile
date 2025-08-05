# base image
FROM python:3.10-slim

# working directory
WORKDIR /app

# copy project files
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run the bot
CMD ["python3", "main.py"]
