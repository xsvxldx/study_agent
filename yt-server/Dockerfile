FROM python:3.10-slim

# Install ffmpeg and system deps
RUN apt-get update && apt-get install -y ffmpeg curl && apt-get clean

# Create working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
RUN mkdir /app/downloads

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
